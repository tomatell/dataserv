import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import datetime
from dataserv.Farmer import Farmer, db
from flask import Flask, make_response


# Initialize the Flask application
app = Flask(__name__)


# Helper functions
def secs_to_mins(seconds):
    if seconds < 60:
        return "{0} second(s)".format(int(seconds))
    elif seconds < 3600:
        return "{0} minute(s)".format(int(seconds/60))
    else:
        return "{0} hour(s)".format(int(seconds/3600))


# Routes
@app.route('/')
def index():
    return "Hello World."


@app.route('/api/register/<btc_addr>', methods=["GET"])
def register(btc_addr):
    # create Farmer object to represent user
    user = Farmer(btc_addr)

    # error template
    error_msg = "Registration Failed: {0}"

    # attempt to register the farmer/farming address
    try:
        user.register()
        return make_response("User registered.", 200)
    except ValueError:
            msg = "Invalid BTC Address."
            return make_response(error_msg.format(msg), 400)
    except LookupError:
            msg = "Address Already Is Registered."
            return make_response(error_msg.format(msg), 409)


@app.route('/api/ping/<btc_addr>', methods=["GET"])
def ping(btc_addr):
    # create Farmer object to represent user
    user = Farmer(btc_addr)

    # error template
    error_msg = "Ping Failed: {0}"

    # attempt to register the farmer/farming address
    try:
        user.ping()
        return make_response("Ping Accepted.", 200)
    except ValueError:
        msg = "Invalid BTC Address."
        return make_response(error_msg.format(msg), 400)
    except LookupError:
        msg = "Farmer not found."
        return make_response(error_msg.format(msg), 404)


@app.route('/api/online', methods=["GET"])
def online():  # pragma: no cover
    # maximum number of minutes since the last check in for
    # the farmer to be considered an online farmer
    online_time = 15  # minutes

    current_time = datetime.datetime.utcnow()
    time_ago = current_time - datetime.timedelta(minutes=online_time)

    online_farmers = db.session.query(Farmer).filter(Farmer.last_seen > time_ago).all()
    output = ""
    for farmer in online_farmers:
        last_seen = secs_to_mins((current_time - farmer.last_seen).seconds)
        last_audit = secs_to_mins((current_time - farmer.last_audit).seconds)
        text = "{0} |  Last Seen: {1} | Last Audit: {2}<br/>"
        output += text.format(farmer.btc_addr, last_seen, last_audit)
    return output

if __name__ == '__main__':  # pragma: no cover
    # Create Database
    db.create_all()

    # Run the Flask app
    app.run(
        host="0.0.0.0",
        port=int("5000"),
        debug=True
    )
