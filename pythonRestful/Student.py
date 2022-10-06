from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = 'student'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    address = db.Column(db.String(100))
    birthday = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, address, birthday, phone):
        self.name = name
        self.address = address
        self.birthday = birthday
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.name

