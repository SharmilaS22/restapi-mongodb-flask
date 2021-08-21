from flask import Flask, request
import pymongo
from bson.objectid import ObjectId
from decouple import config

app = Flask(__name__)

db_url = config('MONGO_URI')

client = pymongo.MongoClient(db_url)
db = client['userDB']
collection = db['users']

@app.get('/')
def root_route():
    return "Hello World!"


''' -----------  /user  ----------- '''
@app.route('/user', methods = ['GET'])
def getAllUsers():

    users = collection.find({})

    user_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        user_list.append(user)
    
    return {
        "msg"   : "Success",
        "users" : user_list
    }

@app.route('/user', methods = ['POST'])
def addANewUser():

    user_data = request.get_json()

    collection.insert_one(user_data)

    return {
        "msg" : "Successfully added!"
    }

@app.route('/user', methods = ['DELETE'])
def deleteAllUsers():

    collection.delete_many({})

    return {
        "msg" : "Deleted Successfully!"
    }


''' -----------  /user/:userid  ----------- '''

@app.route('/user/<userid>', methods = ['GET'])
def getUser(userid:int):

    user = collection.find_one({"_id" : ObjectId(userid)})

    if (user is None):
        return {
            'msg' : "No user with the given id exists"
        }
    
    user['_id'] = str(user['_id'])

    return {
        "msg"  : "Success",
        "user" : user
    }

@app.route('/user/<userid>', methods = ['DELETE'])
def deleteUser(userid:int):

    collection.delete_one({"_id": ObjectId(userid)})

    return {
        "msg" : "Deleted Successfully!"
    }

@app.route('/user/<userid>', methods = [ 'PATCH', 'PUT' ])
def updateUser(userid:int):

    modified_count = collection.update_one(
        {"_id": ObjectId(userid)},
        { "$set": request.get_json()}
    ).modified_count

    if (modified_count == 0):
        return {
            "msg" : "No user exists with the given id"
        }
    
    return {
        "msg" : "Updated Successfully"
    }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)