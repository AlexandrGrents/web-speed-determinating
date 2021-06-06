import os
import cv2
import json

from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.data.datasets import register_coco_instances

from determining_vehicle_speed.detect import detect_on_frame, drow_on_frame
from determining_vehicle_speed.utils.masker import Masker
from determining_vehicle_speed.speedometer import Speedometer
from models import get_process, set_process


CLASS_NAMES = ['car', 'minibus', 'trolleybus', 'tram', 'truck', 'bus', 'middle_bus', 'ambulance', 'fire_truck', 'middle_truck', 'tractor', 'uncategorized', 'van', 'person']


def create_detector():
	register_coco_instances("my_dataset", {'thing_classes': CLASS_NAMES}, "", "")
	dataset_metadata = MetadataCatalog.get("my_dataset")

	print(os.getcwd())
	cfg = get_cfg()
	cfg.merge_from_file(model_zoo.get_config_file("LVISv0.5-InstanceSegmentation/mask_rcnn_R_50_FPN_1x.yaml")) # получение используемой модели 
	cfg.MODEL.WEIGHTS = "model_final.pth" # путь к найденным лучшим весам модели
	cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # установить порог распознавания объекта в 50% (объекты, распознанные с меньшей вероятностью не будут учитываться)
	cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(CLASS_NAMES) # число классов для распознавания

	return DefaultPredictor(cfg)


def async_detect_on_video(time_code, video_path, detector, tracker, app, out_file_settings, out_format_settings):
	print('time code:', time_code)
	print('pwd: ', os.getcwd())
	mask_file = os.path.join(os.getcwd(), 'determining_vehicle_speed', 'mask.png')
	coef_file = os.path.join(os.getcwd(), 'determining_vehicle_speed', 'coef.json')

	need_video = out_format_settings == 'output-video' or out_format_settings == 'output-all'
	need_json = out_format_settings == 'output-json' or out_format_settings == 'output-all'



	# Создаём считыватель исходного видео
	istream = cv2.VideoCapture(video_path)

	# Получаем данные о исходном видео
	w = int(istream.get(cv2.CAP_PROP_FRAME_WIDTH))
	h = int(istream.get(cv2.CAP_PROP_FRAME_HEIGHT))
	fps = int(istream.get(cv2.CAP_PROP_FPS))
	frame_count = int(istream.get(cv2.CAP_PROP_FRAME_COUNT))

	# Создаём писателя для результирующего видео
	if need_video:
		mp4_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], str(time_code) + '.mp4')
		webm_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], str(time_code) + '.webm')

		fourcc_mp4 = cv2.VideoWriter_fourcc(*'XVID')
		fourcc_webm = cv2.VideoWriter_fourcc(*'VP80')
		writer_mp4 = cv2.VideoWriter(mp4_path, fourcc_mp4, fps, (w, h), True)
		writer_webm = cv2.VideoWriter(webm_path, fourcc_webm, fps, (w, h), True)

	# Создаём экземпляр класса Masker для выделения проезжей части на каждом кадре
	masker = Masker(mask_file, size=(w, h))
	speedometer = Speedometer(coef_file, fps=fps, size=(w, h))
	detections_on_video = []

	set_process(time_code, status='run', app=app, currentFrame=0, frameCount=frame_count)

	# Обрабатываем видео покадрово
	for frame_id in range(frame_count):
		# Считываем кадр, создаём кадр для видео с результатом
		ret, frame = istream.read()
		if not ret:
			break

		# Выделяем проезжую часть
		masked_frame = masker.apply(frame)

		# Распознаём объекты на кадре
		detections = detect_on_frame(masked_frame, detector, tracker, speedometer, out_file_settings)

		# Добавляем кадр с разметкой к результирующему видео
		if need_video:
			out_frame = drow_on_frame(frame, detections, CLASS_NAMES)
			writer_mp4.write(out_frame)
			writer_webm.write(out_frame)

		detections.pop('for_draw', None)

		detections['frame_id'] = frame_id
		detections_on_video.append(detections)
		set_process(time_code, status='run', app=app, currentFrame=frame_id)

	# Сохраняем видео с результатом
	if need_video:
		writer_mp4.release()
		writer_webm.release()

	if need_json:
		json_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], str(time_code) + '.json')
		with open(json_path, 'w') as f:
			json.dump(detections_on_video, f)

	print('end process: ', time_code)

	process_settings = dict(status='end', app=app)
	if need_video:
		process_settings['webm'] = str(time_code) + '.webm'
		process_settings['mp4'] = str(time_code) + '.mp4'

	if need_json:
		process_settings['json'] = str(time_code) + '.json'

	set_process(time_code, **process_settings)

	return detections_on_video


if __name__ == "__main__":
	detector = create_detector()
