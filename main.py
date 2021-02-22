from flask import Flask, request, jsonify, json
from flask_restful import Api, Resource
from datetime import datetime 
from flask_cors import CORS
from flask_pymongo import PyMongo
from marshmallow import Schema, fields, ValidationError
from bson.json_util import dumps
from json import loads


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://dbThumbtack:db4405787@cluster0.sgm44.mongodb.net/Thumbtacks?retryWrites=true&w=majority"
mongo = PyMongo(app)

class TankSchema(Schema):
    location = fields.String(required=True)
    lat = fields.Float(required=True)
    long = fields.Float(required=True)
    percentage_full = fields.Integer(required=True)

CORS(app) 
api = Api(app)

@app.route("/")
def welcome():   
    return "Welcome to My third LAB"

profile = {
    "sucess": True,
    "data": {
        "last_updated": "2/7/2021, 4:42:51 PM",
        "username": "Thumbtack",
        "role": "Engineer in Training",
        "color": "blue"
    }
}

@app.route("/profile", methods=["GET", "POST", "PATCH"])
def get_profile():
    if request.method == "GET":
        return jsonify(profile)

    if request.method == "POST":
        Profile_DB["data"]["last_updated"] = (dte.strftime("%c"))
        Profile_DB["data"]["username"] = (request.json["username"])
        Profile_DB["data"]["role"] = (request.json["role"])
        Profile_DB["data"]["color"] = (request.json["color"])
       
        return jsonify(Profile_DB)

    else:
        return jsonify(Profile_DB)

@app.route("/data", methods=["GET", "POST"])
def tank_data():
    if request.method == "POST":
        try:
            newTank = TankSchema().load(request.json)
            tank_id = mongo.db.tanks.insert_one(newTank).inserted_id
            tank = mongo.db.tanks.find_one(tank_id)
            
            return loads(dumps(tank))
        except ValidationError as e:
            return e.messages, 400   

    elif request.method == "GET":
            tank = mongo.db.tanks.find()
            return jsonify(loads(dumps(tank)))  

@app.route("/data/<ObjectId:id>", methods=["PATCH", "DELETE"])
def update(id):
    if request.method == "PATCH":
            mongo.db.tanks.update_one({"_id": id}, {"$set": request.json})
            tank = mongo.db.tanks.find_one(id) 
            return loads(dumps(tank))

    elif request.method == "DELETE":
           result = mongo.db.tanks.delete_one({"_id": id})
           
    if result.deleted_count == 1:
            return {
                "success": True
            }
    else:
            return {
                "success": False
            }, 400


if __name__ == '__main__':
      app.run(
     debug=True,
     port=3000,
     host="0.0.0.0"
  )
