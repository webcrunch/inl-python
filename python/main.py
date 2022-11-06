import time
import random
# from arduino_handling import queue_list, color_dict, blink
from browser import window as w, document, ajax, aio
from network_brython import send_url, timestamp_to_iso, connect, send, close
from dom_io import print as _print, input as _input
from datetime import datetime
# from arduino_handling import queue_list, color_dict
# from api_call import alf as call

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
chat_template = j('.chat_logs')
init_button = j('.init')
delete_connection = j('.display_button_unconnect')
connect_to_room = j('.enter_room')
chatt_button = j('.chatt')
enter_room = j('.enter_chatt')
queue = []
queue_button = j('.execute_queue')
send_chatt_message_button = j('.chatt_message')
disclosed_room = j('.disclosedRoom')
user_display = j('.user')
color_action_display = j('#color_action')
chatt_display = j('#chatt')
action_log_display = j('#action_log')
prgramming_button = j('#programing')
programming_queue_display = j('#programming_queue')


def on_complete(req):
    if req.status == 200 or req.status == 0:
        document["result"].html = req.text
    else:
        document["result"].html = "error " + req.text


def color_display(e):
    if j('input[name=programing]:checked').length > 0:
        j('.displayButton').toggle(200)  # .css("display", "flex")
        queue_template.append(
            f'<li>clicked on: <strong>{e.target.value} </strong>  and added it to the queue</li>')
        queue.append(e.target.value)
    else:
        send(f'send color:{e.target.value}')
        aio.run(send_command(f'{w.location.href}color/{e.target.value}'))


def write_log(time, user, message):
    time_string = timestamp_to_iso(time)
    log_template.append(f'<li>{message}({time_string})</li>') if user is 'system' else log_template.append(
        f'<li>User {user} has {message} ({time_string})</li>')


def action_cb(time, user, message):
    user = user.replace('\'', '')
    message = message.replace('.', '')
    message = message.replace('\'', '')
    message = message.split("½")
    if (len(message) == 2):
        chat_template.append(f'<li>{message}({timestamp_to_iso(time)})</li>') if user is 'system' else chat_template.append(
            f'<li>{user} has written: {message} ({timestamp_to_iso(time)})</li>')
    write_log(time=time, message=message, user=user)


def display_connection(e):
    disclosed_room.toggle(200)  # .css("display", "flex")


def check_checkBox(e):
    send('started a sequence ' if j(
        'input[name=programing]:checked').length > 0 else 'ended a secuence without execute it')


def fire_em_up(e):
    # uncheck the checkbox
    prgramming_button.prop("checked", False)
    aio.run(list_execution())
    queue_template.append()
    send("executed a sequence")


async def list_execution():
    for r in queue:
        aio.run(send_command(f'{w.location.href}color/{r}'))
        await aio.sleep(2)


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


def delete_connection(e):
    close()
    j('.display_button_unconnect').css("display", "none")
    j('.init').css("display", "flex")


def send_chatt_message(e):
    send(j('#room_message_sender').val() + "½chatt")
    j('#room_message_sender').val("")


async def send_command(url):
    response = await (await fetch(url)).json()


def main_connect(e):
    name = j('#name').val()
    room = j('#room').val()
    check_name = check_storage(name)
    if (check_name is not True):
        name = f'{name}_{random.randint(0, 9000)}'
        check_name = check_storage(name)
        connect(room, name, action_cb)
    else:
        connect(room, name, action_cb)
    delete_connection.css("display", "flex")
    init_button.css("display", "none")
    disclosed_room.css("display", "none")
    user_display.html(f'user:{name}')
    color_action_display.css("display", "none")
    chatt_display.css("display", "none")
    action_log_display.css("display", "none")
    programming_queue_display.css("display", "none")
    if (room == 'aurdrino'):
        color_action_display.toggle(200)  # .css("display", "flex")
        chatt_display.toggle(200)
        action_log_display.toggle(200)
        programming_queue_display.toggle(300)

    else:
        chatt_display.toggle(200)
        action_log_display.toggle(200)
    w.localStorage.setItem('date', datetime.today().strftime('%Y-%m-%d'))


connect_to_room.on('click', main_connect)
prgramming_button.on('click', check_checkBox)
action_from_buttons.on('click', color_display)
queue_button.on('click', fire_em_up)
send_chatt_message_button.on('click', send_chatt_message)
init_button.on('click', display_connection)


async def send_get_Data(url):
    api_url = url
    response = await (await fetch(api_url)).json()
