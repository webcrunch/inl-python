from os import system
from browser import window as w, aio
from browser import document, ajax
from network_brython import send_url, timestamp_to_iso, connect, send, close
from dom_io import print as _print, input as _input
# from pyfirmata import Arduino, util
from datetime import datetime

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
button = j(".button")
color_pick_button = j('.colorGetter')
JSON = w.JSON
req = ajax.Ajax()
log_template = j('.loggs')
chatt_button = j('.chatt')
enter_room = j('.enter_chatt')
blink_button = j('.E_blink')


def on_complete(req):
    if req.status == 200 or req.status == 0:
        document["result"].html = req.text
    else:
        document["result"].html = "error " + req.text


def color_display(e):
    send(j('#head').val() + ' send color')
    # j("body").css("background-color", j('#head').val())


def blink(e):
    send('pushed the blink button')
    # j("body").css("background-color", j('#head').val())


def chatt_cb(time, user, message):
    print(time, user, message)
    write_log(time, user, message)


def action_cb(time, user, message):
    print('time', time, 'user', user, 'message', message)
    write_log(time, message)


def write_log(time, user, message):
    time_string = timestamp_to_iso(time)
    log_template.append(f'<li>{message}({time_string})</li>') if user is 'system' else log_template.append(
        f'<li>User {user} has done {message} ({time_string})</li>')


def set_a_log_test(e):
    j('.disclosed').toggle(200)  # .css("display", "flex")
    #


def button_click(e):
    print("Hej")


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
    connect(room, name, action_cb)


def main_connection():
    name = 'alfa'
    room = 'beta'
    connect(room, name, chatt_cb)
    # close()


button.on('click', button_click)
color_pick_button.on('click', color_display)
chatt_button.on('click', set_a_log_test)
enter_room.on('click', handle_connection)
blink_button.on('click', blink)
# j(document).ready(main_connection)


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

main_connection()
