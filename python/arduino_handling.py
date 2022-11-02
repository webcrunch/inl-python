# 6,5 RED
# 3,6 GREEN
# 3,5 BLUE
# 5 PURPLE
# 6 YELLOW
# 3 CYAN
# 0,0,0 WHITE
# 1,1,1 BLACK
import time
from pyfirmata import Arduino, util, pyfirmata
color_dict = {
    "black": {'R': 1, 'G': 1, 'B': 1},
    "white": {'R': 0, 'G': 0, 'B': 0},
    "green": {'R': 1, 'G': 0, 'B': 1},
    "red": {'R': 1, 'G': 1, 'B': 0},
    "blue": {'R': 0, 'G': 1, 'B': 1},
    "purple": {'R': 0, 'G': 1, 'B': 0},
    "yellow": {'R': 1, 'G': 0, 'B': 0},
    "cyan": {'R': 0, 'G': 0, 'B': 1},
}
board = Arduino('COM5')


def blink(handling=6):
    global board
    # turn(False)
    # time.sleep(1)
    # turn(True)
    # time.sleep(1)

    # turn(False)
    # time.sleep(1)
    # turn(True)
    # time.sleep(1)
    # turn(False)

    for i in range(handling):
        display_color("black")
        time.sleep(1)
        display_color("white")
        time.sleep(1)
        display_color("black")

#     for i in range(6):
#         print(i)
#         board.digital[13].write(1)
#         time.sleep(1)
#         board.digital[13].write(0)
#         time.sleep(1)


def display_color(color):
    global color_dict
    global board

    (r, g, b) = color_dict[color]
    r = color_dict[color][r]  # 6
    g = color_dict[color][g]  # 5
    b = color_dict[color][b]  # 3
    # board = Arduino('COM5')
    # firmata_version = board.get_firmata_version()
    # print(board.digital_ports)
    # print("Connected to Firmata " +
    #       str(firmata_version[0]) + "." + str(firmata_version[1]))
    board.digital[3].write(b)  # blue
    board.digital[5].write(g)  # green
    board.digital[6].write(r)  # red


def turn(state):
    display_color("black") if state is not True else display_color("white")


def queue_list(list, waiting):
    for r in list:

        if (r == "blink"):
            blink()
        else:
            display_color(r)

        time.sleep(waiting)


# queue_list(["yellow", "green", "blue", "red",
#            "cyan", "blink", "blink", "yellow", "green" , "yellow", "green", "blue", ], 1)


# queue_list(["blue", "blink", "blue", "blink", "blue", "blink", "blue",
#            "blink", "blue", "blink", "blue", "blink", "blue", "blink"], 2)

blink(1)
