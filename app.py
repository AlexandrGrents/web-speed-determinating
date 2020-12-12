import os

from flask import Flask, render_template, jsonify, request, url_for

from determining_vehicle_speed.sort.sort import Sort, KalmanBoxTracker
#from detector import create_detector


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'

#detector = create_detector()

last_id = 0
videos = {'kompol-11s': os.path.join(os.getcwd(), 'static', 'input.mp4')}
detect_processes = {1:{'status': 'run', 'frameCount':220, 'currentFrame':100}, 2:{'status': 'end', 'webmFileName':'20201213003800.webm', 'mp4FileName': '20201213003800.mp4', 'jsonFileName': '20201213003800.json'}}

if os.environ.get('CROSS_ORIGIN'):
	from flask_cors import CORS
	CORS(app)


@app.route('/detect', methods = ['POST'])
def video_detect():
	video = request.form.get('video')
	if video == 'custom':
		video_file = request.files['video-file']
		path_to_video = os.path.join(os.getcwd(), 'tmp', video_file.filename)
		video_file.save(path_to_video)
	else:
		path_to_video = videos.get(video)
	if path_to_video is None:
		return '', 400
	global last_id
	last_id += 1
	info_about_bbox = request.form.get('bbox')
	detect_processes[last_id] = {'status': 'run'}

	return jsonify({"id":last_id})


@app.route('/result/<int:detect_id>')
def check_result(detect_id):
	result = detect_processes.get(detect_id)
	if result is None:
		return '', 404
	return jsonify(result)


if __name__=="__main__":
	app.run()