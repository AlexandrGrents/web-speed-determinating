from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

db = SQLAlchemy()

@dataclass
class RunnedProcess(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    frameCount: int = db.Column(db.Integer)
    currentFrame: int = db.Column(db.Integer)

    def to_dict(self):
        return dict(id = self.id, frameCount = self.frameCount, currentFrame = self.currentFrame)

@dataclass
class EndedProcess(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    mp4: str = db.Column(db.String(50), default=None)
    webm: str = db.Column(db.String(50), default=None)
    json: str = db.Column(db.String(50), default=None)

    def to_dict(self):
        return dict(id = self.id, mp4 = self.mp4, webm = self.webm, json = self.json)


class StartedProcess(db.Model):
    id:int = db.Column(db.Integer, primary_key=True)
    priority:int = db.Column(db.Integer, default=None)

    def to_dict(self):
        return dict(id = self.id, priority = self.priority)


def get_process(process_id):
    process = EndedProcess.query.get(process_id)
    status = 'end'
    if not process:
        status = 'run'
        process = RunnedProcess.query.get(process_id)
    if not process:
        status = 'start'
        process = StartedProcess.query.get(process_id)
    process_dict = process.to_dict()
    process_dict.update({'status': status})

    return process_dict

def set_process(process_id, status, app, **kwargs):
    with app.app_context():
        if status == 'start':
            process = StartedProcess(id=process_id, priority=1)
            db.session.add(process)
            db.session.commit()



        if status == 'run':
            process = StartedProcess.query.get(process_id)
            if process:
                db.session.delete(process)

            process = RunnedProcess.query.get(process_id)
            if not process:
                process = RunnedProcess(id=process_id, frameCount=kwargs.get('frameCount'), currentFrame=kwargs.get('currentFrame'))
                db.session.add(process)
                db.session.commit()
            else:
                process.frameCount = kwargs.get('frameCount', process.frameCount)
                process.currentFrame = kwargs.get('currentFrame', process.currentFrame)
                db.session.add(process)
                db.session.commit()

        if status == 'end':
            process = RunnedProcess.query.get(process_id)
            if process:
                db.session.delete(process)

            process = EndedProcess.query.get(process_id)
            if not process:
                process = EndedProcess(id=process_id)
                db.session.commit()

            process.mp4 = kwargs.get('mp4', process.mp4)
            process.webm = kwargs.get('webm', process.webm)
            process.json = kwargs.get('json', process.json)

            db.session.add(process)
            db.session.commit()
        process_dict = process.to_dict()
        process_dict.update({'status': status})
        return process_dict

