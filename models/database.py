from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Establishment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    block = db.Column(db.Integer)
    address = db.Column(db.String(200))
    type = db.Column(db.String(100))
    resident = db.relationship(
        'Resident', backref='resident', lazy=True)
    establishment_image = db.relationship(
        'EstablishmentImage', backref='establishment_image', lazy=True)


class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishment.id'),
                                 nullable=False)
    first_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    occupation = db.Column(db.String(100))
    present_address = db.Column(db.String(100))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(5))
    nationality = db.Column(db.String(25))
    civil_status = db.Column(db.String(25))
    birth_date = db.Column(db.DateTime())
    contact_no = db.Column(db.String(15))
    emergency_name = db.Column(db.String(100))
    emergency_adress = db.Column(db.String(100))
    emergency_contact_no = db.Column(db.String(15))


class EstablishmentImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishment.id'),
                                 nullable=False)
    filename = db.Column(db.String(100))


class Coordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    establishment_id = db.Column(db.Integer, db.ForeignKey('establishment.id'),
                                 nullable=False)
    x = db.Column(db.Float(), nullable=False)
    y = db.Column(db.Float(), nullable=False)