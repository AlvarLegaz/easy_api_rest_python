import http.client
from flask import Flask
from flask import request
import os
from dotenv import load_dotenv
from app import util
from app.UsersJsonFileManager import UsersJsonFileManager


load_dotenv()
file_name = os.getenv('USERS_FILE')

db_Json_File = UsersJsonFileManager(file_name)

api_application = Flask(__name__)
HEADERS = {"Content-Type": "text/plain", "Access-Control-Allow-Origin": "*"}


@api_application.route("/")
def hello():
    return ("Hello from users api", http.client.OK, HEADERS)


@api_application.route("/test_hello_user/<name>/<int:verify_code>")
def hello_user(name, verify_code):
    hello_str = 'Hello user:'+name + " with verify_code:" + str(verify_code)
    return (hello_str, http.client.OK, HEADERS)


@api_application.route("/users", methods=['GET'])
def get_users_list():
    entries = db_Json_File.list_entries()
    return (entries, http.client.OK, HEADERS)


@api_application.route("/users", methods=['POST'])
def set_user():
    try:
        entry = request.get_json()
        entry = db_Json_File.create_entry(entry)
        return (entry, http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)


@api_application.route("/users/<id>", methods=['GET'])
def get_user_by_id(id):
    try:
        entry_read = db_Json_File.read_entry(int(id))
        return (entry_read, http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)


@api_application.route("/users/<id>", methods=['PUT'])
def update_user_by_id(id):
    try:
        entry = request.get_json()
        entry_updated = db_Json_File.update_entry(int(id), entry)
        return (entry_updated, http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)


@api_application.route("/users/<id>", methods=['DELETE'])
def delete_user_by_id(id):
    try:
        entry_deleted = db_Json_File.delete_entry(int(id))
        return (entry_deleted, http.client.OK, HEADERS)
    except TypeError as e:
        return (str(e), http.client.BAD_REQUEST, HEADERS)
