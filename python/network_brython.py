# SSE system for direct messaging
# [sends messages via sse.nodehill.com]
# (Brython version, works in a browser)

# Usage:
# from network_brython import connect, send, close

# connect(channel, user, event_handler)
#
#  Opens the network connection
#  - creates a channel if it doesn't exists
#  - joins the channel
#  - registers a function that will get all messages
#
#  Arguments:
#  * channel        string
#  * user           string
#  * handler        function that will receive
#				    (timestamp, user_name, message)
#                   * timestamp = milliseconds
#                      since new years eve 1970 GMT
#                   * user_name - string
#                   * message - any
#                      JSON serializable data type
#

# send(message)
#
#  Sends a message
#
#  Argument:
#  * message 	    any JSON serializable data type

# close()
#
#  Closes the network connection

from browser import window
from datetime import datetime
fetch = window.fetch
EventSource = window.EventSource
uri_encode = window.encodeURIComponent
JSON = window.JSON

channel_name = None
user_name = None
token = None
tokenD = {}
message_handler = None
evt_src = None
last_message_time = 0
serverURL = 'https://sse.nodehill.com'


def on_token(e):
    global user_name
    global token
    tokenD[user_name] = JSON.parse(e.data)
    token = JSON.parse(e.data)

# convert timestamp to iso date time format


def timestamp_to_iso(timestamp):
    return datetime.fromtimestamp(timestamp / 1000)\
        .isoformat().replace('T', ' ').split('.')[0]


def on_message(e):
    d = JSON.parse(e.data)
    global last_message_time
    timestamp = d.timestamp
    last_message_time = timestamp
    user = d.user
    message = d.data
    message_handler(timestamp, user, message)


def on_error(e):
    window.console.log('error', e.data)


def connect(channel, user, handler):
    global channel_name, user_name, message_handler, evt_src
    message_handler = handler
    channel_name = uri_encode(channel)
    user_name = uri_encode(user)
    evt_src = EventSource.new(f'{serverURL}' +
                              f'/api/listen/{channel_name}/' +
                              f'{user_name}/{last_message_time}')
    evt_src.addEventListener('message', on_message)
    evt_src.addEventListener('error', on_error)
    evt_src.addEventListener('token', on_token)


def send(message, user):
    fetch(f'{serverURL}/api/send/{tokenD[user]}', {
        'headers': {'Content-Type': 'application/json'},
        'method': 'POST',
        'body': JSON.stringify({'message': message})
    })


def send_url(url, message):
    fetch(f'{url}', {
        'headers': {'Content-Type': 'application/json'},
        'method': 'POST',
        'body': JSON.stringify({'message': message})
    })


def close():
    evt_src.close()
