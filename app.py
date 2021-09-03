from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS
import yaml

app = Flask(Shopping Cart Apllication)
config = yaml.load(open('database.yaml'))
client = MongoClient(config['uri'])
# db = client.lin_flask
db = client['lin_flask']
CORS(app)

@app.route('/data', methods=['POST'])
def data():
    
    # POST a data to database
    if request.method == 'POST':
        body = request.json
        name = body['product name']
        price = body['price']

        # db.users.insert_one({
        db['cart'].insert_one({
            "Product name": name,
            "price": price
        })
        return jsonify({
            'status': 'Data is posted to MongoDB!',
            'product name': name,
            'price': price
        })

@app.route('/data/<string:id>', methods=['DELETE', 'PUT'])
def onedata(id):

    # GET a specific data by id
    if request.method == 'GET':
        data = db['cart'].find_one({'_id': ObjectId(id)})
        id = data['_id']
        name = data['product name']
        price = data['price']
        dataDict = {
            'id': str(id),
            'product name': name,
            'price': price
        }
        print(dataDict)
        return jsonify(dataDict)
        
    # DELETE a data
    if request.method == 'DELETE':
        db['cart'].delete_many({'_id': ObjectId(id)})
        print('\n # Deletion successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is deleted!'})

    # UPDATE a data by id
    if request.method == 'PUT':
        body = request.json
        name = body['product name']
        price = body['price']

        db['cart'].update_one(
            {'_id': ObjectId(id)},
            {
                "$set": {
                    "product name":name,
                    "price":price
                }
            }
        )

        print('\n # Update successful # \n')
        return jsonify({'status': 'Data id: ' + id + ' is updated!'})

if __name__ == '__main__':
    app.debug = True
    app.run()