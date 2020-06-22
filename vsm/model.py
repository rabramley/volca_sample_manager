import os
from flask import current_app
from werkzeug.utils import secure_filename
from datetime import datetime
from vsm.database import db


class Sample(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(500), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    @property
    def filepath(self):
        return os.path.join(
            current_app.config["FILE_UPLOAD_DIRECTORY"],
            secure_filename(
                "{}_{}".format(self.id, self.filename)
            ),
        )


class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True, unique=True)
    filename = db.Column(db.String(500), nullable=False)
    created_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)

    @property
    def filepath(self):
        return os.path.join(
            current_app.config["FILE_UPLOAD_DIRECTORY"],
            secure_filename(
                "{}_{}".format(self.id, self.filename)
            ),
        )
