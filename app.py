import json
import random

from flask import Flask, request, make_response, jsonify

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

    if action == 'search-handyman-around':
        res = search_handyman_around(req)
    elif action == 'select-handyman-services':
        res = select_handyman_services(req)
    else:
        response = {
            'fulfillmentText': 'Today we recommend plumber {0}!'.format(random.choice(['Margherita', 'Salami'])),
        }
        res = create_response(response)
    return res

    print('Action: ' + action)
    print('Response: ' + res)

    return make_response(jsonify({'fulfillmentText': res}))


def select_handyman_services(req):
    response = {
        'fulfillmentText': 'Today we recommend plumber {0}!'.format(random.choice(['Margherita', 'Salami'])),
    }
    res = create_response(response)
    return res


def search_handyman_around(req):
    """Returns a string containing text with a response to the user
    with the weather forecast or a prompt for more information
    Takes the city for the forecast and (optional) dates
    uses the template responses found in weather_responses.py as templates
    """
    parameters = req['queryResult']['parameters']

    print('Dialogflow Parameters:')
    print(json.dumps(parameters, indent=4))

    response = {
        'fulfillmentText': 'Today we recommend plumber {0}!'.format(random.choice(['Margherita', 'Salami'])),
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
