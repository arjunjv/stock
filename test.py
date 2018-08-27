"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import boto3
import json
import requests
import csv
# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response_with_directive_noslot():
    print ('build_speechlet_response_with_directive_noslot')
    return{
        "outputSpeech" : None,
        "card" : None,
        "directive" : [
            {
                'type' : "Dialog.Deligate"
            }
        ],
        "reprompt" : None,
        "shouldEndSession" : False
    }



def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- Functions that control the skill's behavior ------------------


 ## Requests: a separate Python Library   http://docs.python-requests.org/en/master/
 ##           to install with Python PIP:
 ##              open a command prompt in your /src folder and type
 ##              pip install requests -t .



def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Stock Edge." \
                    "Can ask company stock price saying,"\
                    "Reliance stock price."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please tell me which company stock price you like to here saying, " \
                    "apples stock price."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Stock Edge. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_the_stock_symbol(cos_name):
    sample_reader = csv.reader(open('./symbol.csv'),quotechar='&')

    cos_name = cos_name.title()
    symbol = "NSE:"
   
    for row in sample_reader:
        if cos_name in row[1]:
            print (row[0],":",row[1])
            symbol = symbol + row[0].strip()
            cos_info = [row[1],symbol]
            return cos_info
    if symbol == "NSE:":
        print ("The requested company is not found")
        return 0
        
    #returns symbol and the copmany full name


def calling_the_alpha_ventage(cos_name):
    print("calling alpha ventage")
    cos_info = get_the_stock_symbol(cos_name)
    if cos_info == 0:
        return 0
        
    url = "https://www.alphavantage.co/query"
    function = "TIME_SERIES_DAILY_ADJUSTED"
    interval = "60min"
    outputsize = "full"
    api_key = "Q7DW5F7WK48Z7YRR" #   <-- goes here your API KEY
    print(cos_info[1])
    data = { "function": function,
         "symbol": cos_info[1],
         "interval": interval,
         "outputsize": outputsize,
         "apikey": api_key }
    page = requests.get(url, params = data)

    string = json.loads(str(page.text))
    date = string['Meta Data']['3. Last Refreshed']
    final = string['Time Series (Daily)'][date]['5. adjusted close']
    
    day_start  = string['Time Series (Daily)'][date]['1. open']

    # print(day_start)
    # print(final)
    
    percentile_change = (int((((float(final)-float(day_start))/float(day_start))*100)*100))/100
    cos_info.append(float(final))
    cos_info.append(date)
    cos_info.append(float(percentile_change))
    return cos_info
#    print ("The Price of %s on %s is %s, the day cahnge is %s"%(data['symbol'],date,final,percentile_change))


def call_to_add_to_my_wishlist(request, session):
    table_name = "stock_edge"

    get_stock_price(request['intent']['slots']['cos']['value'])
    
    
def current_market_price(request, session):
    session_attributes = {}
    should_end_session = False
    if ((request['dialogState'] == "STARTED") and (request['dialogState'] != "COMPLETED")):
        print ('STARTED or IN PROGRESS')
        #print(request['intent']['slots']['cos']['value'])
        if 'value' not in request['intent']['slots']['cos']:
            print("request to fill the slot")
            return build_response({}, build_speechlet_response_with_directive_noslot())
    cos_info = calling_the_alpha_ventage(request['intent']['slots']['cos']['value'])
    card_title = "Stock Price"
    reprompt_text = "Please tell me which company stock price you like to here saying, " \
                    "apples stock price "
                    
    if cos_info == 0:
        speech_output = "The Price of requested cos name is not matching with database"
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    else:
        
        speech_output = "The Price of "+ cos_info[0] + " on " + cos_info[3] +" is "+ str(cos_info[2])
        should_end_session = False
        return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def add_to_my_wishlist(request, session):
    session_attributes = {}
    reprompt_text = None
    if ((request['dialogState'] == "STARTED") and (request['dialogState'] != "COMPLETED")):
        print ('STARTED or IN PROGRESS')
        #print(request['intent']['slots']['cos']['value'])
        if 'value' not in request['intent']['slots']['cos']:
            print("code to request to fill the slot")
            return build_response({}, build_speechlet_response_with_directive_noslot())
    call_to_add_to_my_wishlist(request, session)
    
    

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
 
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "currentMarketPrice":
        return current_market_price(intent_request, session)
    elif intent_name == "addToMyWishlist":
        return add_to_my_wishlist(intent_request, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])



