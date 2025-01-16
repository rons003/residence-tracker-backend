from flask import json, jsonify, make_response, request
from sqlalchemy import text
from models.database import db, Establishment


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
                "no_of_resident": len(e.resident)
            })
        return result
    except Exception as e:
        print(str(e))
    return make_response(jsonify(result), 200)