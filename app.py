from flask import Flask, request, make_response, jsonify

from df_response_lib import facebook_response, fulfillment_response, actions_on_google_response
from handyman import HandyMan

app = Flask(__name__)
log = app.logger

fb = facebook_response()
aog = actions_on_google_response()
main_response = fulfillment_response()


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
        res = aog.simple_response(['I did not quite understand you.']),

    return create_response(res)


def search_handyman_around(req):
    parameters = req['queryResult']['parameters']
    handyman = HandyMan(parameters)
    try:
        results = handyman.get_list()
        print(results)
        results = ['Musa', 'Ahmed']
        aog_reply = aog.simple_response(['Recommended Handymen'])
        fb_reply = fb.quick_replies('Recommended Handymen', results)
    except Exception as e:
        aog_reply = aog.simple_response(['Sorry, I could not find any match.'])
        fb_reply = fb.text_response(['Sorry, I could not find any match.'])
    return [aog_reply, fb_reply]


def create_response(response_objs):
    return make_response(jsonify(main_response.fulfillment_messages(response_objs)))


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0', threaded=True)
