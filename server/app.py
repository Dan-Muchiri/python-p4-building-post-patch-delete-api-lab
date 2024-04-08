#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
    return make_response(  bakeries,   200  )

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()

    if bakery == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            bakery_dict = bakery.to_dict()

            response = make_response(
                bakery_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(bakery, attr, request.form.get(attr))

            db.session.add(bakery)
            db.session.commit()

            bakery_dict = bakery.to_dict()

            response = make_response(
                bakery_dict,
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(bakery)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Bakery deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

@app.route('/baked_goods', methods=['GET', 'POST'])
def reviews():

    if request.method == 'GET':
        bgs = []
        for bg in BakedGood.query.all():
            bg_dict = bg.to_dict()
            bgs.append(bg_dict)

        response = make_response(
            bgs,
            200
        )

        return response

    elif request.method == 'POST':
        new_bg = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            created_at=request.form.get("created_at"),
            updated_at=request.form.get("updated_at"),
            bakery_id=request.form.get("bakery_id"),
        )

        db.session.add(new_bg)
        db.session.commit()

        bg_dict = new_bg.to_dict()

        response = make_response(
            bg_dict,
            201
        )

        return response
    
@app.route('/baked_goods/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def baked_goods_by_id(id):
    bg = BakedGood.query.filter_by(id=id).first()

    if bg == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response

    else:
        if request.method == 'GET':
            bg_dict = bg.to_dict()

            response = make_response(
                bg_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(bg, attr, request.form.get(attr))

            db.session.add(bg)
            db.session.commit()

            bg_dict = bg.to_dict()

            response = make_response(
                bg_dict,
                200
            )

            return response

        elif request.method == 'DELETE':
            db.session.delete(bg)
            db.session.commit()

            response_body = {
                "delete_successful": True,
                "message": "Baked Good deleted."
            }

            response = make_response(
                response_body,
                200
            )

            return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)