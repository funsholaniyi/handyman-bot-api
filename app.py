from flask import Flask, request, make_response, jsonify

from df_response_lib import facebook_response, fulfillment_response
from handyman import HandyMan

app = Flask(__name__)
log = app.logger

fb = facebook_response()
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
        tex_obj = main_response.fulfillment_text('Handy man results')
        return create_response(tex_obj, res)
    else:
        text_obj = main_response.fulfillment_text('I did not quite understand you.')
        return create_response(text_obj)


def search_handyman_around(req):
    parameters = req['queryResult']['parameters']
    handyman = HandyMan(parameters)
    options = []
    try:
        results = handyman.get_list()
        for result in results:
            title = result['username'] + ' (' + str(result['rating']) + ' Star rating)'
            subtitle = 'Base rate: NGN' + str(result['baseRate']) + ', Hourly rate: NGN' + str(result['hourlyRate'])
            buttons = [{'title': 'Book Now', 'url': 'https://optimistic-sammet-47aefd.netlify.com/?handyman=' + result['_id']}]
            options.append(fb.card_response(title, buttons, subtitle, img_url='http://chittagongit.com/images/generic-profile-icon/generic-profile-icon-10.jpg'))
    except Exception as e:
        options = [fb.text_response(['Sorry, I could not find any match at this time.'])]
    if not options: options = [fb.text_response(['Sorry, I could not find any match.'])]
    return main_response.fulfillment_messages(options)


def create_response(text_obj, response_objects=None):
    return make_response(jsonify(main_response.main_response(text_obj, response_objects)))


if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0', threaded=True)
