import base64
import datetime
import time
from flask import json, jsonify, make_response, request
from sqlalchemy import text
from models.database import Coordinates, EstablishmentImage, db, Establishment, Resident


def index():
    filter = request.args.get("filter", False)
    result = []
    try:
        sql = f"""
            SELECT
                a.id as resident_id,
                a.*,
                b.*
            FROM
                resident a
            INNER JOIN
                establishment b
            ON
                b.id = a.establishment_id"""

        if filter:
            sql += f""" WHERE (a.first_name LIKE '%{filter}%' OR a.last_name LIKE '%{filter}%')"""
        residents = db.session.execute(text(sql)).all()

        for resident in residents:
            coordinates = db.session.query(Coordinates).filter_by(
                establishment_id=resident.establishment_id).all()
            establishment_image = db.session.query(EstablishmentImage).filter_by(
                establishment_id=resident.establishment_id).first()
            with open("image_attachments/" + establishment_image.filename, "rb") as image_file:
                base64_string = base64.b64encode(image_file.read())
                encoded_string = base64_string.decode('ascii')
            result.append({
                "id": resident.resident_id,
                "establishment_id": resident.establishment_id,
                "first_name": resident.first_name,
                "middle_name": resident.middle_name,
                "last_name": resident.last_name,
                "occupation": resident.occupation,
                "present_address": resident.present_address,
                "age": resident.age,
                "sex": resident.sex,
                "nationality": resident.nationality,
                "civil_status": resident.civil_status,
                "birth_date": resident.birth_date.strftime("%d-%m-%Y"),
                "contact_no": resident.contact_no,
                "emergency_address": resident.emergency_address,
                "emergency_name": resident.emergency_name,
                "emergency_contact_no": resident.emergency_contact_no,
                "code": resident.code,
                "block": resident.block,
                "address": resident.address,
                "type": resident.type,
                "coordinates": [{"x": c.x, "y": c.y} for c in coordinates],
                "image": encoded_string
            })
    except Exception as e:
        print(str(e))
    return make_response(jsonify(result), 200)


def show(id):
    try:
        establishment = db.session.query(
            Establishment).filter_by(id=id).first()

        if establishment is None:
            return make_response(
                jsonify({'message': 'Invalid Establishment ID'}), 400)
        residents = []
        for resident in establishment.resident:
            print()
            residents.append({
                "id": resident.id,
                "first_name": resident.first_name,
                "middle_name": resident.middle_name,
                "last_name": resident.last_name,
                "occupation": resident.occupation,
                "present_address": resident.present_address,
                "age": resident.age,
                "gender": resident.sex,
                "nationality": resident.nationality,
                "civil_status": resident.civil_status,
                "birth_date": resident.birth_date.strftime("%d-%m-%Y"),
                "contact_no": resident.contact_no,
                "emergency_address": resident.emergency_address,
                "emergency_name": resident.emergency_name,
                "emergency_contact_no": resident.emergency_contact_no
            })

        establishment_image = db.session.query(
            EstablishmentImage).filter_by(establishment_id=id).first()
        with open("image_attachments/" + establishment_image.filename, "rb") as image_file:
            base64_string = base64.b64encode(image_file.read())
            encoded_string = base64_string.decode('ascii')
        result = {
            "id": establishment.id,
            "code": establishment.code,
            "block": establishment.block,
            "address": establishment.address,
            "type": establishment.type,
            "residents": residents,
            "image": encoded_string
        }
        return make_response(jsonify(result), 200)
    except Exception as e:
        print(str(e))
        db.session.rollback()
        return make_response(jsonify({'status': 'error', 'message': e}), 500)


def create():
    if request.method == 'POST':
        try:
            data = request.get_json()
            establishment = Establishment()
            establishment.code = data['code']
            establishment.block = data['block']
            establishment.address = data['address']
            establishment.type = data['type']
            residents = []
            rows = data['residents']
            
            for row in rows:
                birth_date = datetime.datetime.strptime(row['birth_date'], "%d-%m-%Y").date()
                resident = Resident()
                resident.first_name = row['first_name']
                resident.middle_name = row['middle_name']
                resident.last_name = row['last_name'],
                resident.occupation = row['occupation']
                resident.present_address = row['present_address']
                resident.age = row['age']
                resident.sex = row['gender'],
                resident.nationality = row['nationality']
                resident.civil_status = row['civil_status']
                resident.birth_date = birth_date
                resident.contact_no = row['contact_no']
                resident.emergency_name = row['emergency_name']
                resident.emergency_adress = row['emergency_address']
                resident.emergency_contact_no = row['emergency_contact_no']
                residents.append(resident)
            establishment.resident = residents
            filesnames = []
            for i in data['images']:
                image = EstablishmentImage()
                image.filename = i['name']
                filesnames.append(image)
                convert_and_save(i['base64'], i['name'])
            establishment.establishment_image = filesnames

            db.session.add(establishment)
            db.session.commit()
            return make_response(
                jsonify({'status': 'success', 'message': 'Resident Added!'}), 201)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return make_response(jsonify({'status': 'error', 'message': e}), 500)


def update(id):
    if request.method == 'PUT':
        try:
            data = request.get_json()
            establishment = db.session.query(
                Establishment).filter_by(id=id).first()
            if establishment is None:
                return make_response(
                    jsonify({'message': 'Invalid Establishment ID'}), 400)
            establishment.code = data['code']
            establishment.block = data['block']
            establishment.address = data['address']
            establishment.type = data['type']
            residents = []
            rows = data['residents']    
            for row in rows:
                birth_date = datetime.datetime.strptime(row['birth_date'], "%d-%m-%Y").date()
                resident = Resident()
                resident.first_name = row['first_name']
                resident.middle_name = row['middle_name']
                resident.last_name = row['last_name'],
                resident.occupation = row['occupation']
                resident.present_address = row['present_address']
                resident.age = row['age']
                resident.sex = row['gender'],
                resident.nationality = row['nationality']
                resident.civil_status = row['civil_status']
                resident.birth_date = birth_date
                resident.contact_no = row['contact_no']
                resident.emergency_name = row['emergency_name']
                resident.emergency_address = row['emergency_address']
                resident.emergency_contact_no = row['emergency_contact_no']
                residents.append(resident)
            establishment.resident = residents
            filesnames = []
            for i in data['images']:
                image = EstablishmentImage()
                image.filename = i['name']
                filesnames.append(image)
                convert_and_save(i['base64'], i['name'])
            if len(filesnames) > 0:
                establishment.establishment_image = filesnames
            db.session.commit()
            return make_response(
                jsonify({'status': 'success', 'message': 'Information Updated!'}), 200)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return make_response(jsonify({'status': 'success', 'message': e}), 500)


def convert_and_save(b64_string, name):
    with open("image_attachments/" + name, "wb") as fh:
        fh.write(base64.b64decode(b64_string))
