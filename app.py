import os
from datetime import datetime
from threading import Thread

from flask import Flask, render_template, jsonify, request, url_for, send_from_directory
from flask_migrate import Migrate


#from flask_webpack import Webpack

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
#webpack = Webpack(app)

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


videos = {'kompol-11s': os.path.join(os.getcwd(), 'static', 'input.mp4')}
detect_processes = {1:{'status': 'run', 'frameCount':220, 'currentFrame':100}, 2:{'status': 'end', 'webmFileName':'20201213003800.webm', 'mp4FileName': '20201213003800.mp4', 'jsonFileName': '20201213003800.json'}}


@app.route('/detect', methods = ['POST'])
def video_detect():
	global detect_processes
	video = request.form.get('video')
	time_code = get_time_code()
	if video == 'custom':
		video_file = request.files['video-file']
		file_format = os.path.splitext(video_file.filename)[1]
		video_path = os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER'], time_code + file_format)
		video_file.save(video_path)
	else:
		video_file = videos.get(video)
	if video_file is None:
		return '', 400



	detect_processes[time_code] = {'status': 'start'}
	tracker = Sort(max_age=60)
	KalmanBoxTracker.count = 0

	process = set_process(time_code, status='start', app = app)

	Thread(target=async_detect_on_video, args=(time_code, video_file, detector, tracker, app)).start()

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
