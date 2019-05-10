import json

from flask import Flask, request, make_response

from df_response_lib import facebook_response
from handyman import HandyMan

app = Flask(__name__)
log = app.logger


@app.route('/', methods=['GET'])
def home():
    return 'it works'


# all requests from dialogflow will go throught webhook function
@app.route('/webhook', methods=['POST'])
def webhook():
    """This method handles the http requests for the Dialogflow webhook
    This is meant to be used in conjunction with the weather Dialogflow agent
    """
    req = request.get_json(silent=True, force=True)
    try:
        action = req.get('queryResult').get('action')
    except AttributeError:
        return 'json error'

    if action == 'get_service_list':
        res = search_handyman_around(req)
    else:
        response = {
            'fulfillmentText': 'I did not quite understand you.',
        }
        res = create_response(response)
    return res


def search_handyman_around(req):
    parameters = req['queryResult']['parameters']
    handyman = HandyMan(parameters)
    try:
        results = handyman.get_list()
        fb = facebook_response()
        results = ['Musa', 'Ahmed']
        reply = fb.quick_replies('Recommended Handymen', results)
        response = {
            'fulfillmentText': reply,
        }
        res = create_response(response)
        return res
    except Exception as e:
        response = {
            'fulfillmentText': 'Sorry, I could not find any match.',
        }
        res = create_response(response)
        return res


def create_response(response):
    """ Creates a JSON with provided response parameters """

    # convert dictionary with our response to a JSON string
    res = json.dumps(response, indent=4)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0', threaded=True)
