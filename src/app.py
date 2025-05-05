"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"success": True,
                     "family": members}
    return jsonify(response_body), 200

#to add new member of the family:
@app.route('/members', methods=['POST'])
def new_member():
    data = request.json
    print(data) #added to check in the terminal if members have been added successfully on Postman
    new = jackson_family.new_member(data)
    response_body = {"success": True,
                     "new_member": new}
    return jsonify(response_body), 201

#to delete a member of the family by id:
@app.route('/members/<int:id>', methods=['DELETE'])
def handle_delete(id):
    result = jackson_family.delete_member(id)
    if result:
        return jsonify({"message": f"Member with id {id} deleted"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404



#to get a member of the family by id:
@app.route('/members/<int:id>', methods=['GET'])
def handle_get(id):
    result = jackson_family.get_member(id)
    if result:
        return jsonify({"message": f"Member with id {id} : {result}"}), 200
    else:
        return jsonify({"error": "Member not found"}), 404



# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
