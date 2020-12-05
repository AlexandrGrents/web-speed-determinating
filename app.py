import os

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_bs4 import Bootstrap
from werkzeug.utils import secure_filename

from determining_vehicle_speed.detect import detect_on_video
from determining_vehicle_speed.sort.sort import Sort
from detector import create_detector
from forms import VideoForm

app = Flask(__name__)
sio = SocketIO(app, async_mode = 'eventlet')

bootstrap = Bootstrap(app)
detector = create_detector()

app.config['SECRET_KEY'] = '1234'


@app.route('/')
def index():
	return 'hello world'

@app.route('/video', methods = ['GET', 'POST'])
def video():
	video_form = VideoForm()
	if video_form.validate_on_submit():
		f = video_form.input_file.data

		filename = secure_filename(f.filename)
		if not filename:
			return "bad request", 400
		tracker = Sort(max_age = 50)

		input_file_path = os.path.join(os.getcwd(), 'files', filename)
		output_file_path = os.path.join(os.getcwd(), 'files', 'output.mp4')
		coef_file_path = os.path.join(os.getcwd(), 'determining_vehicle_speed', 'coef.json')
		mask_file_path = os.path.join(os.getcwd(), 'determining_vehicle_speed', 'mask.png')

		f.save(input_file_path)
		detections = detect_on_video(input_file_path, output_file_path, detector, tracker, coef_file=coef_file_path, mask_file = mask_file_path, to_mp4 = True)
		print(detections[1]['detections'][6])
		print(type(detections[1]['detections'][6]['bbox']))
		print(type(detections[1]['detections'][6]['bbox'][0]))
		print(type(detections[1]['detections'][6]['speed']))
		return jsonify(detections), 200

	return render_template('video.html', video_form = video_form)