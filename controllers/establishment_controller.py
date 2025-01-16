from flask import json, jsonify, make_response, request
from sqlalchemy import text
from models.database import db, Establishment, Coordinates


def index():
    filter = request.args.get("filter", False)
    result = []
    try:
        establishments = db.session.query(Establishment).all()
        for e in establishments:
            result.append({
                "id": e.id,
                "code": e.code,
                "block": e.block,
                "address": e.address,
                "type": e.type,
                "no_of_resident": len(e.resident),
                "coordinates": [{"x": c.x, "y": c.y} for c in e.coordinates]
            })
        return result
    except Exception as e:
        print(str(e))
    return make_response(jsonify(result), 200)


def store_coordinates():
    if request.method == 'POST':
        try:
            data = request.get_json()
            coordinates = data["coordinates"]
            establishment_id = data["establishment_id"]
            establishment = db.session.query(
                Establishment).filter_by(id=establishment_id).first()
            if establishment is None:
                return make_response(
                    jsonify({'message': 'Invalid Establishment'}), 400)
            data = []
            if (establishment.coordinates is not None):
                db.session.execute(text("DELETE FROM coordinates WHERE establishment_id = :establishment_id"),
                                   {"establishment_id": establishment_id})
                db.session.commit()
            for coor in coordinates:
                coords = Coordinates()
                coords.establishment_id = establishment.id
                coords.x = coor["x"]
                coords.y = coor["y"]
                data.append(coords)
            db.session.add_all(data)
            db.session.commit()
            return make_response(
                jsonify({'status': 'success', 'message': 'Coordinates Stored!'}), 201)
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return make_response(jsonify({'status': 'error', 'message': e}), 500)
