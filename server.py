import requests as rq
from flask import Flask, request, jsonify

app = Flask(__name__)

# constants
PORT = 8000
HOST = "0.0.0.0"
URL = "https://api.scansan.com/v1/area_codes/search"
QUERY = "?area_name=Brixton"
ADDRESS = URL + QUERY
AUTH_TOKEN = "370b0b6f-3f09-4807-b7fe-270a4e5ba2c2"

#

# get request
r = rq.get(ADDRESS, headers={"X-Auth-Token": AUTH_TOKEN})
print(r.content)


if __name__ == "main":
    app.run(host=HOST, port=PORT, debug=True)