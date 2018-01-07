#!/usr/bin/env python
import json
import os

from flask import Flask, make_response, jsonify, request

from UkDatabaseAPI.database.mongo_db import MongoDB

SCHEDULER_NAME = "UkDatabaseScheduler"
"""str: Scheduler name."""

ARG_TEXT = "t"
ARG_POST_PUB_DATE = "d"
ARG_NUMBER_OF_RESULTS = "n_results"
"""str: URL arguments."""

# Flask app should start in global layout.
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    try:
        res = {"UkDatabaseAPI": "With UkDatabaseAPI you can find information about people!"}
        r = make_response(jsonify(res))
        r.headers['Content-Type'] = 'application/json'
        return r
    except Exception as e:
        print("Exception:", e)
        r = make_response(jsonify({"Error": "Error from the server"}))
        r.headers['Content-Type'] = 'application/json'
        return r


@app.route('/search', methods=['GET'])
def search():
    """Find information about people from the uk database site
    Examples:
        http://localhost:5000/search?t=john&d=25/12/2017-02/01/2018
        http://localhost:5000/search?t=london%20tom%20women&d=29/12/2017-
    Returns:
        Posts containing the text or/and within a time range.
    """
    try:
        text: str = request.args.get(ARG_TEXT)
        post_pub_date: str = request.args.get(ARG_POST_PUB_DATE)
        number_of_results = request.args.get(ARG_NUMBER_OF_RESULTS, type=int)
        res = make_search_result(text, post_pub_date, number_of_results)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        return r
    except AssertionError as e:
        r = make_response(jsonify({"Error": str(e)}))
        r.headers['Content-Type'] = 'application/json'
        return r

    except Exception as e:
        print("Exception:", e)
        r = make_response(jsonify({"Error": "Error from the server"}))
        r.headers['Content-Type'] = 'application/json'
        return r


def make_search_result(text, post_pub_date, number_of_results):
    """Search the database for result.
    Args:
        text: The text search criterion, from the URL argument.
        post_pub_date: The date or time range search criterion, from the URL argument.
        number_of_results: The number of results to return, from the URL argument.
    Returns:
        Posts containing the text or/and within a time range.
    """
    mongo_db = MongoDB()
    result = mongo_db.find_posts(text, post_pub_date, number_of_results)
    return result


@app.route("/" + SCHEDULER_NAME + "/customEndpoint", methods=['POST'])
def scheduler():
    """Pin the app every 5 min, to not let the heroku dynos sleep after 30 min."""
    message = {}  # Custom message.
    res = json.dumps(message, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


@app.errorhandler(404)
def not_found(error):
    """Not found error message."""
    print(error)
    return make_response(jsonify({"Error": "Not Found"}), 404)


@app.errorhandler(500)
def internal_server_error(error):
    """Internal server error message."""
    print(error)
    return make_response(jsonify({"Error": "Internal Server Error"}), 500)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port, host='0.0.0.0')
