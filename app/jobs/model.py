# jobs/model/jobModel.py

from app.config.connect import db

class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=True)
    url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime(), nullable=True)
    

    def __init__(self, title,company,location,salary,url,created_at):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.url = url
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "salary": self.salary,
            "url": self.url,
            "created_at": self.created_at
        }
