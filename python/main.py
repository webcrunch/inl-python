# from localStoragePy import localStoragePy
from browser import window as w, document, ajax
from network_brython import send_url, timestamp_to_iso, connect, send, close
from dom_io import print as _print, input as _input
from datetime import datetime
from api_call import alf as call
# localStorage = localStoragePy('your-app-namespace', 'text')
# localStorage.setItem("user_name", "stig")
# data = localStorage.getItem("user_name")
# print(data)


# from pyfirmata import Arduino, util
# board = pyfirmata.Arduino('/ dev/ttyS4')
# board = Arduino('COM5')
# firmata_version = board.get_firmata_version()
# print("Connected to Firmata " +
#       str(firmata_version[0]) + "." + str(firmata_version[1]))

if w == None:
    quit('Can only be run in a web browser!')
# setting jquery to j
j = w.jQuery
fetch = w.fetch
color_pick_button = j('.colorGetter')
JSON = w.JSON
req = ajax.Ajax()
log_template = j('.loggs')
chat_template = j('.messages')
init_button = j('.init')
chatt_button = j('.chatt')
enter_room = j('.enter_chatt')
blink_button = j('.E_blink')
gradient_display = j('#gradient')


def on_complete(req):
    if req.status == 200 or req.status == 0:
        document["result"].html = req.text
    else:
        document["result"].html = "error " + req.text


def color_display(e):
    send(j('#head').val() + ' send color')
    # j("body").css("background-color", j('#head').val())


def write_log(time, user, message):
    time_string = timestamp_to_iso(time)
    print('time:', time, 'user:', user, 'message:', message)
    log_template.append(f'<li>{message}({time_string})</li>') if user is 'system' else log_template.append(
        f'<li>User {user} has done {message} ({time_string})</li>')


def blink_handling(e):
    send('pushed the blink button') if j(
        'input[name=gradient]:checked').length < 1 else send('pushed the blink button with gradient altered:' + j(".slider").val())
    # j("body").css("background-color", j('#head').val())


def chatt_cb(time, user, message):
    user = user.replace('\'', '')
    message = message.replace('.', ' ')
    message = message.replace('\'', '')
    time_string = timestamp_to_iso(time)
    chat_template.append(f'<li>{message}({time_string})</li>') if user is 'system' else chat_template.append(
        f'<li>{message}({time_string})</li>')
    write_log(time, user, message)


def action_cb(time, user, message):
    user = user.replace('\'', '')
    message = message.replace('.', '')
    message = message.replace('\'', '')
    # print('time:', time, 'user:', user, 'message:', message)
    write_log(time, message)


def set_a_log_test(e):
    j('.disclosed').toggle(200)  # .css("display", "flex")
    #


def post_command(url, data):
    log('posting stuff')
    log(data)
    # await (w.fetch(f'{url}', {
    #     'method': 'POST',
    #     'body': JSON.stringify({'message': data})
    # }))
    req.bind('complete', on_complete)
    # send a POST request to the url
    req.open('POST', url, True)
    req.set_header('content-type', 'application/x-www-form-urlencoded')
    # send data as a dictionary
    req.send({'color': data})


# def on_message(timestamp, user, message):
#     print(timestamp, user, message)
#     write_log(timestamp, message)

def handle_connection(e):
    name = j('#name').val()
    room = j('#room').val()
    connect(room, name, chatt_cb)


def gradient_check(e):
    j('.slidecontainer').css('visibility', 'visible') if \
        j('input[name=gradient]:checked').length else j('.slidecontainer').css('visibility', 'hidden')


def main_connect(e):
    name = 'muse'
    room = 'sting'
    connect(room, name, action_cb)


init_button.on('click', main_connect)
color_pick_button.on('click', color_display)
chatt_button.on('click', set_a_log_test)
enter_room.on('click', handle_connection)
blink_button.on('click', blink_handling)
gradient_display.on('click', gradient_check)


def log(string):
    print("herer")
    w.console.log(string)


async def send_command(url):
    print(url)
    response = await (await fetch(url)).json()
    log(response)


async def send_get_Data(url):
    api_url = url
    response = await (await fetch(api_url)).json()
