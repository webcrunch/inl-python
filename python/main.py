from browser import window as w, aio
if w == None:
    quit('Can only be run in a web browser!')
# setting jquery to j
j = w.jQuery
fetch = w.fetch
button = j(".button")
off = j('.off')
on = j('on')
color_choosed = None
color_picker_value = j('.color_chooser')
blink_button = j('.E_blink')


def button_click(e):
    print("Hej")
    aio.run(send_get_Data())


# async def button_send(status):
#     api_url = "http://localhost/power/" + status
#     response = await (await fetch(api_url)).json()
#     w.console.log(response)


def test(ev):
    print(ev)
    aio.run(sendData(j('.color_chooser option:selected').val()))


async def blink_function(ev):
    print("eere")
    # aio.run()


# on.on('click', button_send('on'))
# off.on('click', button_send('off'))
color_picker_value.on('change', test)
# color_picker_value.change(function():
#     print("Handler for .change() called.")
button.on('click', button_click)
blink_button.on('click', blink_function)


async def send_get_Data(url):
    api_url = url
    response = await (await fetch(api_url)).json()


async def sendData(color):
    print(color)
    # api_url = "https://jsonplaceholder.typicode.com/todos/1"
    # response = await (await fetch(api_url)).json()
    response = await(await fetch("http://localhost:5000/color", {
        method: 'POST',
        headers:
            'Content-Type': 'application/json'
            // 'Content-Type': 'application/x-www-form-urlencoded',

        body: JSON.stringify({"color": color})
    })).json()
    w.console.log(response)
