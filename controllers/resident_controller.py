from flask import json, jsonify, make_response, request
from sqlalchemy import text
from models.database import db, Establishment, Resident


def index():
    result = []
    try:
        sql = """
            SELECT
                a.*,
                b.*
            FROM
                resident a
            INNER JOIN
                establishment b
            ON
                b.id = a.establishment_id"""
        residents = db.session.execute(text(sql)).all()

        for resident in residents:
            result.append({
                "id": resident.id,
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
                "birth_date": resident.birth_date,
                "contact_no": resident.contact_no,
                "emergency_name": resident.emergency_name,
                "emergency_contact_no": resident.emergency_contact_no,
                "code": resident.code,
                "block": resident.block,
                "address": resident.address,
                "type": resident.type
            })
    except Exception as e:
        print(str(e))
    return make_response(jsonify(result), 200)


def show(id):
    try:
        sql = """
            SELECT
                a.*,
                b.*
            FROM
                resident a
            INNER JOIN
                establishment b
            ON
                b.id = a.establishment_id
            WHERE
                a.id = :id"""
        resident = db.session.execute(text(sql), {"id": id}).first()
        if resident is None:
            return make_response(
                jsonify({'message': 'Invalid Resident ID'}), 400)
        result = {
            "id": resident.id,
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
            "birth_date": resident.birth_date,
            "contact_no": resident.contact_no,
            "emergency_name": resident.emergency_name,
            "emergency_contact_no": resident.emergency_contact_no,
            "code": resident.code,
            "block": resident.block,
            "address": resident.address,
            "type": resident.type
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
                resident = Resident()
                resident.first_name = row['first_name']
                resident.middle_name = row['middle_name']
                resident.last_name = row['last_name'],
                resident.occupation = row['occupation']
                resident.present_address = row['present_address']
                resident.age = row['age']
                resident.sex = row['sex'],
                resident.nationality = row['nationality']
                resident.civil_status = row['civil_status']
                resident.birth_date = row['birth_date']
                resident.contact_no = row['contact_no']
                resident.emergency_name = row['emergency_name']
                resident.emergency_adress = row['emergency_address']
                resident.emergency_contact_no = row['emergency_contact_no']
                residents.append(resident)
            establishment.resident = residents

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
                resident = Resident()
                resident.first_name = row['first_name']
                resident.middle_name = row['middle_name']
                resident.last_name = row['last_name'],
                resident.occupation = row['occupation']
                resident.present_address = row['present_address']
                resident.age = row['age']
                resident.sex = row['sex'],
                resident.nationality = row['nationality']
                resident.civil_status = row['civil_status']
                resident.birth_date = row['birth_date']
                resident.contact_no = row['contact_no']
                resident.emergency_name = row['emergency_name']
                resident.emergency_adress = row['emergency_address']
                resident.emergency_contact_no = row['emergency_contact_no']
                residents.append(resident)
            establishment.resident = residents

            db.session.commit()
            return make_response(
                jsonify({'status': 'success', 'message': 'Information Updated!'}), 200)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return make_response(jsonify({'status': 'success', 'message': e}), 500)
