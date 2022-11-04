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
users = {'auto': '', 'chatt': ''}
chat_template = j('.chat_logs')
# init_button = j('.init')
chatt_button = j('.chatt')
enter_room = j('.enter_chatt')
queue = []
queue_button = j('.execute_queue')
send_chatt_message_button = j('.chatt_message')


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
        # if e.target.value != 'blink' and e.target.value != 'rainbow':
        send(f'send color:{e.target.value}', users['auto'])
        aio.run(send_command(f'{w.location.href}color/{e.target.value}'))
        # elif e.target.value == 'blink':
        # else:
        # print(f'{w.location.href}{e.target.value}')
        #     send(f'make it blink')
        #     aio.run(send_command(f'{w.location.href}{e.target.value}'))

        # elif e.target.value == 'rainbow':
        #     print("here")
        #     send(f'send color:{e.target.value}')
        #     aio.run(send_command(f'{w.location.href}{e.target.value}'))

    # send(j('#head').val() + ' send color')
  # get the value of the button
    # j("body").css("background-color", j('#head').val())


def write_log(time, user, message):
    time_string = timestamp_to_iso(time)
    log_template.append(f'<li>{message}({time_string})</li>') if user is 'system' else log_template.append(
        f'<li>User {user} has {message} ({time_string})</li>')


# def blink_handling(e):
#     send('pushed the blink button') if j(
#         'input[name=gradient]:checked').length < 1 else send('pushed the blink button with gradient altered:' + j(".slider").val())
#     # j("body").css("background-color", j('#head').val())


def chatt_cb(time, user, message):
    user = user.replace('\'', '')
    message = message.replace('.', ' ')
    message = message.replace('\'', '')
    if (j('.disclosed_chatt').css("display") is not 'flex'):
        j('.disclosed_chatt').css("display", "flex")
    time_string = timestamp_to_iso(time)
    chat_template.append(f'<li>{message}({time_string})</li>') if user is 'system' else chat_template.append(
        f'<li>{user} has written: {message} ({time_string})</li>')
    write_log(time, user, message)


def action_cb(time, user, message):
    user = user.replace('\'', '')
    message = message.replace('.', '')
    message = message.replace('\'', '')
    write_log(time=time, message=message, user=user)


def set_a_log_test(e):
    j('.disclosed').toggle(200)  # .css("display", "flex")


def check_checkBox(e):
    send('started a sequence ' if j(
        'input[name=programing]:checked').length > 0 else 'ended a secuence without execute it', users['auto'])


def fire_em_up(e):
    # uncheck the checkbox
    j('#programing').prop("checked", False)
    aio.run(list_execution())
    queue_template.append()
    send("executed a sequence")


async def list_execution():
    for r in queue:
        aio.run(send_command(f'{w.location.href}color/{r}'))
        # if (r == 'blink'):
        #     aio.run(send_command(f'{w.location.href}{r}'))
        #     pass
        # elif (r == 'rainbow'):
        #     aio.run(send_command(f'{w.location.href}{r}'))
        # else:

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


def handle_connection(e):
    name = j('#name').val()
    room = j('#room').val()
    check_name = check_storage(name)
    if (check_name is not True):
        name = f'{name}_{random.randint(0, 9000)}'
        check_name = check_storage(name)
    connect(room, name, chatt_cb)
    users['chatt'] = name
    j('.chatt_user').append(f'user:{name}')


def send_chatt_message(e):
    send(j('#room_message_sender').val(), users['chatt'])
    j('#room_message_sender').val("")


async def send_command(url):
    response = await (await fetch(url)).json()


def main_connect(e):
    name = 'auto_connect_user'
    room = 'auto_connect'
    check_name = check_storage(name)
    if (check_name is not True):
        name = f'{name}_{random.randint(0, 9000)}'
        check_name = check_storage(name)
        connect(room, name, action_cb)
    else:
        connect(room, name, action_cb)

    users['auto'] = name
    j('.user').append(f'user:{name}')
    w.localStorage.setItem('date', datetime.today().strftime('%Y-%m-%d'))


j(document).ready(main_connect)
j('#programing').on('click', check_checkBox)
action_from_buttons.on('click', color_display)
chatt_button.on('click', set_a_log_test)
enter_room.on('click', handle_connection)
queue_button.on('click', fire_em_up)
send_chatt_message_button.on('click', send_chatt_message)


async def send_get_Data(url):
    api_url = url
    response = await (await fetch(api_url)).json()
