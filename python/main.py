import time
import random

from browser import window as w, document, ajax
from network_brython import send_url, timestamp_to_iso, connect, send, close
from dom_io import print as _print, input as _input
from datetime import datetime
# from arduino_handling import queue_list, color_dict
from api_call import alf as call


if w == None:
    quit('Can only be run in a web browser!')
# setting jquery to j
j = w.jQuery
fetch = w.fetch
action_from_buttons = j('.pressed_button')
JSON = w.JSON
req = ajax.Ajax()
log_template = j('.loggs')
queue_template = j('.p_queue')
chat_template = j('.messages')
init_button = j('.init')
chatt_button = j('.chatt')
enter_room = j('.enter_chatt')
queue = []
queue_button = j('.execute_queue')


def on_complete(req):
    if req.status == 200 or req.status == 0:
        document["result"].html = req.text
    else:
        document["result"].html = "error " + req.text


def color_display(e):
    if j('input[name=programing]:checked').length > 0:
        queue_template.append(
            f'<li>clicked on: <strong>{e.target.value} </strong>  and added it to the queue</li>')
        queue.append(e.target.value)
        # p_queue
        # send("programming a sequence")
    else:
        w.console.log(e.target.value)
        # send(e.target.value + 'send color')
    # send(j('#head').val() + ' send color')
      # get the value of the button
    # j("body").css("background-color", j('#head').val())


def write_log(time, user, message):
    time_string = timestamp_to_iso(time)
    print('time:', time, 'user:', user, 'message:', message)
    log_template.append(f'<li>{message}({time_string})</li>') if user is 'system' else log_template.append(
        f'<li>User {user} has done {message} ({time_string})</li>')


# def blink_handling(e):
#     send('pushed the blink button') if j(
#         'input[name=gradient]:checked').length < 1 else send('pushed the blink button with gradient altered:' + j(".slider").val())
#     # j("body").css("background-color", j('#head').val())


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
    print('time:', time, 'user:', user, 'message:', message)
    write_log(time=time, message=message, user=user)


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


def check_checkBox(e):
    enim = 'started a sequence ' if j(
        'input[name=programing]:checked').length > 0 else 'ended a secuence without execute it'
    send(enim)


def fire_em_up(e):
    print(queue)
    j('#programing').prop("checked", False)
    send("ended a secuence and executed it")
    # queue_list(queue,2)
    # send("executed a sequence")


def check_storage(name):

    if (w.localStorage.getItem('usernames') ==
            None or w.localStorage.getItem('usernames') == ''):
        users = name
        w.localStorage.setItem('usernames', users)
        return True
    else:
        users = w.localStorage.getItem("usernames")
        if name in users:
            return False
        else:
            w.localStorage.setItem('usernames', f'{users},{name}')
            return True


# def on_message(timestamp, user, message):
#     print(timestamp, user, message)
#     write_log(timestamp, message)


def handle_connection(e):
    # w.localStorage.setItem('myCat', 'Tom')
    # cat = w.localStorage.getItem('myCat')
    # print(cat)
    check_name = check_storage(j('#name').val())
    name = j('#name').val()
    room = j('#room').val()
    # connect(room, name, chatt_cb)


def main_connect(e):
    name = 'auto_connect_user'
    room = 'auto_connect'
    check_name = check_storage(name)
    print(check_name)
    if (check_name is not True):
        name = f'{name}_{random.randint(0, 9000)}'
        check_name = check_storage(name)
        print(check_name)
        connect(room, name, action_cb)
    else:
        connect(room, name, action_cb)
    w.localStorage.setItem('date', datetime.today().strftime('%Y-%m-%d'))


j(document).ready(main_connect)
j('#programing').on('click', check_checkBox)
init_button.on('click', main_connect)
action_from_buttons.on('click', color_display)
chatt_button.on('click', set_a_log_test)
enter_room.on('click', handle_connection)
queue_button.on('click', fire_em_up)


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
