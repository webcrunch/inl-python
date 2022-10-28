from browser import window as w, aio
from browser import document, ajax
from datetime import datetime
from network_brython import send_url
from dom_io import print as _print, input as _input

if w == None:
    quit('Can only be run in a web browser!')
# setting jquery to j
j = w.jQuery
fetch = w.fetch
button = j(".button")
color_pick_button = j('.colorGetter')
JSON = w.JSON
req = ajax.Ajax()


def on_complete(req):
    if req.status == 200 or req.status == 0:
        document["result"].html = req.text
    else:
        document["result"].html = "error " + req.text


def color_display(e):
    j("body").css("background-color", j('#head').val())


def button_click(e):
    print("Hej")
    aio.run(send_get_Data("localhost/test"))


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


button.on('click', button_click)
color_pick_button.on('click', color_display)


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


# ___________________________________________________________ chat from Thomas code

# def timestamp_to_iso(timestamp):
#     return datetime.fromtimestamp(timestamp / 1000)\
#         .isoformat().replace('T', ' ').split('.')[0]

# # listen to incoming messages and display them


# def on_message(timestamp, user, message):
#     time_string = timestamp_to_iso(timestamp)
#     j(f"""
#         <div class="shown alert alert-primary" role="alert">
#             <b>{time_string} {user}:</b>
#             <p>{message}</p>
#         </div>
#     """).appendTo('main')
#     j(window).scrollTop(10000000)  # scroll to bottom

# # send a message


# def send_message(e):
#     e.preventDefault()  # do not reload web page
#     message = j('form input.message').val()
#     send(message)
#     j('form input.message').val('')  # empty input field

# # create a form for input


# def create_form():
#     j("""
#         <form class="container-fluid p-3 px-5 position-fixed
#             bottom-0 bg-light">
#             <div class="input-group">
#             <input type="text" class="message form-control"
#                 placeholder="Write a message">
#             <button class="btn btn-primary"
#                 type="submit">Send</button>
#             </div>
#         </form>
#     """)\
#         .appendTo('body')\
#         .on('submit', send_message)


# async def main():
#     # _print('<h3>Chatten</h3>')
#     # # connect to channel
#     # connect(channel, user, on_message)
#     # j('main').empty()
#     # create_form()

# aio.run(main())


# color_choosed = None
# color_picker_value = j('.color_chooser')
# blink_button = j('.E_blink')


# # async def button_send(status):
# #     api_url = "http://localhost/power/" + status
# #     response = await (await fetch(api_url)).json()
# #     w.console.log(response)


# # def test(ev):
# #     print(ev)
# #     aio.run(sendData(j('.color_chooser option:selected').val()))


# async def blink_function(ev):
#     print("eere")
#     # aio.run()


# # on.on('click', button_send('on'))
# # off.on('click', button_send('off'))
# # color_picker_value.on('change', test)
# # color_picker_value.change(function():
# #     print("Handler for .change() called.")

# blink_button.on('click', blink_function)


# # async def sendData(color):
# #     print(color)
# #     # api_url = "https://jsonplaceholder.typicode.com/todos/1"
# #     # response = await (await fetch(api_url)).json()
# #     response = await(await fetch("http://localhost:5000/color", {
# #         method: 'POST',
# #         headers:
# #             'Content-Type': 'application/json'
# #             // 'Content-Type': 'application/x-www-form-urlencoded',

# #         body: JSON.stringify({"color": color})
# #     })).json()
# #     w.console.log(response)
