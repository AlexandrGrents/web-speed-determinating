from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.data.datasets import register_coco_instances

CLASS_NAMES = ['car', 'minibus', 'trolleybus', 'tram', 'truck', 'bus', 'middle_bus', 'ambulance', 'fire_truck', 'middle_truck', 'tractor', 'uncategorized', 'van', 'person']


def create_detector():
	register_coco_instances("my_dataset", {'thing_classes': CLASS_NAMES}, "", "")
	dataset_metadata = MetadataCatalog.get("my_dataset")

	cfg = get_cfg()
	cfg.merge_from_file(model_zoo.get_config_file("LVISv0.5-InstanceSegmentation/mask_rcnn_R_50_FPN_1x.yaml")) # получение используемой модели 
	cfg.MODEL.WEIGHTS = "model_final.pth" # путь к найденным лучшим весам модели
	cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5   # установить порог распознавания объекта в 50% (объекты, распознанные с меньшей вероятностью не будут учитываться)
	cfg.MODEL.ROI_HEADS.NUM_CLASSES = len(CLASS_NAMES) # число классов для распознавания

	return DefaultPredictor(cfg) 