from src.app import db


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String())

    def __init__(self, name):
        self.video_name = name

    def __repr__(self):
        return f"Video_{self.id} - {self.video_name}"
