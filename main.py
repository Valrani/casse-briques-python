from tkinter import *


def initBall():
    return can.create_oval(
        CANVAS_WIDTH / 2 - 5,
        CANVAS_HEIGHT / 2 - 5,
        CANVAS_WIDTH / 2 + 5,
        CANVAS_HEIGHT / 2 + 5,
        fill="white"
    )


def moveBall():
    global ballHorizontalDirection, ballVerticalDirection
    # change ball direction if necessary
    coords = can.coords(ballId)
    if coords[0] <= 0:
        ballHorizontalDirection = BALL_DIRECTION_RIGHT
    if coords[1] <= 0:
        ballVerticalDirection = BALL_DIRECTION_DOWN
    if coords[2] >= CANVAS_WIDTH:
        ballHorizontalDirection = BALL_DIRECTION_LEFT
    if coords[3] >= CANVAS_HEIGHT:
        ballVerticalDirection = BALL_DIRECTION_UP
    # move the ball
    can.move(ballId, ballHorizontalDirection, ballVerticalDirection)
    fen.after(ballSpeed, moveBall)


# constants
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600

BALL_DIRECTION_LEFT = -5
BALL_DIRECTION_RIGHT = 5
BALL_DIRECTION_UP = -5
BALL_DIRECTION_DOWN = 5

# variables
ballId = None
ballSpeed = 15
ballHorizontalDirection = BALL_DIRECTION_LEFT
ballVerticalDirection = BALL_DIRECTION_UP

# GUI
fen = Tk()
fen.title("Balle qui bouge")
fen.resizable(False, False)
can = Canvas(fen, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
can.pack()

ballId = initBall()

#moveBall()

fen.mainloop()
