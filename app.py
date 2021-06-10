import os
from datetime import datetime
from threading import Thread
import json

from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
from flask_migrate import Migrate

from determining_vehicle_speed.sort.sort import Sort, KalmanBoxTracker
from detector import create_detector, async_detect_on_video
from models import db, get_process, set_process
import matplotlib 
matplotlib.rcParams['backend'] = 'TkAgg' 
matplotlib.use('TKAgg')


def get_time_code():
	now = datetime.now()
	return int(now.strftime("%Y%m%d%H%M%S"))


app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.getcwd(), 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_NATIVE_UNICODE'] = True
app.config['UPLOAD_FOLDER'] = 'files'

db.init_app(app)
migrate = Migrate(app, db)
if os.environ.get('CROSS_ORIGIN'):
	from flask_cors import CORS
	CORS(app)


detector = create_detector()


videos = {
	'kompol-11s': os.path.join(os.getcwd(), 'static', 'input.mp4'),
	'kompol-11s-10fps': os.path.join(os.getcwd(), 'static', 'input10fps.mp4'),
	'kompol-2min-5fps': os.path.join(os.getcwd(), 'static', 'new_input5fps.mp4'),
}
detect_processes = {1:{'status': 'run', 'frameCount':220, 'currentFrame':100}, 2:{'status': 'end', 'webmFileName':'20201213003800.webm', 'mp4FileName': '20201213003800.mp4', 'jsonFileName': '20201213003800.json'}}


@app.route('/detect', methods = ['POST'])
def video_detect():
	global detect_processes
	video = request.form.get('video')
	time_code = get_time_code()
	if video == 'custom':
		video_file = request.files['video-file']
		file_format = os.path.splitext(video_file.filename)[1]
		video_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], str(time_code) + file_format)
		video_file.save(video_path)
	else:
		video_path = videos.get(video)
	if video_path is None:
		return '', 400

	out_file_settings = request.form.get('out_file_settings')
	if not (out_file_settings is None):
		out_file_settings = json.loads(out_file_settings)
	out_format_settings = request.form.get('out_format_settings')

	detect_processes[time_code] = {'status': 'start'}
	tracker = Sort(max_age=60)
	KalmanBoxTracker.count = 0

	process = set_process(time_code, status='start', app=app)

	Thread(target=async_detect_on_video, args=(time_code, video_path, detector, tracker, app, out_file_settings, out_format_settings)).start()

	return jsonify(process)

@app.route('/')
def index():
	return render_template('interface.html')

@app.route('/result/<int:detect_id>')
def check_result(detect_id):
	result = get_process(detect_id)
	if result is None:
		return '', 404
	return jsonify(result)

@app.route('/file/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__=="__main__":
	app.run()
