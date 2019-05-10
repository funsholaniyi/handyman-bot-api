import json
import logging
import random

from flask import Flask
from flask import make_response
from flask import request

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')

app = Flask(__name__)


# all requests from dialogflow will go throught webhook function
@app.route('/webhook', methods=['POST'])
def webhook():
    # get dialogflow request
    req = request.get_json(silent=True, force=True)

    logger.info("Incoming request: %s", req)

    intent = get_intent_from_req(req)
    logger.info('Detected intent %s', intent)

    # user asks for today's special
    if intent == 'todays_special':

        # pick any :)
        response = {
            'fulfillmentText': 'Today we recommend {0}!'.format(random.choice(['Margherita', 'Salami'])),
        }
    else:
        # something went wrong here, we got unknow intent or request without intent
        response = {
            'fulfillmentText': 'Yeah, I\'m here but still learning, please wait for part 2 of this tutorial!',
        }

    res = create_response(response)

    return res


def get_intent_from_req(req):
    """ Get intent name from dialogflow request"""
    try:
        intent_name = req['queryResult']['intent']['displayName']
    except KeyError:
        return None

    return intent_name


def create_response(response):
    """ Creates a JSON with provided response parameters """

    # convert dictionary with our response to a JSON string
    res = json.dumps(response, indent=4)

    logger.info(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'

    return r


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0', threaded=True)
