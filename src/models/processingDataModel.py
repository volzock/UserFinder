from src.app import db
from src.models.videoModel import VideoModel


class ProcessingDatarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_id = db.Column(db.Integer, db.ForeignKey('videoModel.id'), nullable=False)
    username = db.relationship('VideoModel', backref=db.backref('processingDatarModel', lazy=True))
    photo = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.id} - {self.name}"
