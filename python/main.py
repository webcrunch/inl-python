from browser import window as w, aio
if w == None:
    quit('Can only be run in a web browser!')
# setting jquery to j
j = w.jQuery
fetch = w.fetch


def button_click(e):
    print("Hej")
    aio.run(sendData())


j(".button").on('click', button_click)


async def sendData():
    api_url = "https://jsonplaceholder.typicode.com/todos/1"
    response = await (await fetch(api_url)).json()
    w.console.log(response)
