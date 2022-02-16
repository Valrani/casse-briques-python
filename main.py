from tkinter import *


def initBar():
    obj = can.create_rectangle(
        CANVAS_WIDTH / 2 - barSize / 2,
        CANVAS_HEIGHT - BAR_OFFSET_FROM_BOTTOM,
        CANVAS_WIDTH / 2 + barSize / 2,
        CANVAS_HEIGHT - (BAR_OFFSET_FROM_BOTTOM + 10),
        fill="white"
    )
    can.bind('<Motion>', onBarMoving)
    print("Bar created with coordinates", can.coords(obj))
    return obj


def onBarMoving(event):
    # collisions with walls
    if event.x - barSize / 2 <= 0 or event.x + barSize / 2 >= CANVAS_WIDTH:
        return
    # move the bar
    can.coords(
        barId,
        event.x - barSize / 2,
        CANVAS_HEIGHT - BAR_OFFSET_FROM_BOTTOM,
        event.x + barSize / 2,
        CANVAS_HEIGHT - (BAR_OFFSET_FROM_BOTTOM + 10)
    )


def initBall():
    obj = can.create_oval(
        CANVAS_WIDTH / 2 - 5,
        CANVAS_HEIGHT - 150,
        CANVAS_WIDTH / 2 + 5,
        CANVAS_HEIGHT - 140,
        fill="white"
    )
    print("Ball created with coordinates", can.coords(obj))
    return obj


def moveBall():
    global ballHorizontalDirection, ballVerticalDirection
    # collisions with walls
    ballCoords = can.coords(ballId)
    if ballCoords[0] <= 0:
        ballHorizontalDirection = BALL_DIRECTION_RIGHT
    if ballCoords[1] <= 0:
        ballVerticalDirection = BALL_DIRECTION_DOWN
    if ballCoords[2] >= CANVAS_WIDTH:
        ballHorizontalDirection = BALL_DIRECTION_LEFT
    if ballCoords[3] >= CANVAS_HEIGHT:
        ballVerticalDirection = BALL_DIRECTION_UP
    # collisions with bar
    if ballCoords[3] == CANVAS_HEIGHT - BAR_OFFSET_FROM_BOTTOM - 10 and ballVerticalDirection == BALL_DIRECTION_DOWN:
        barCoords = can.coords(barId)
        if barCoords[0] <= ballCoords[2] <= barCoords[2]:
            ballVerticalDirection = BALL_DIRECTION_UP
    # move the ball
    can.move(ballId, ballHorizontalDirection, ballVerticalDirection)
    fen.after(ballSpeed, moveBall)


# constants - do not change during the execution !
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 600
BAR_OFFSET_FROM_BOTTOM = 100
BALL_DIRECTION_LEFT = -5
BALL_DIRECTION_RIGHT = 5
BALL_DIRECTION_UP = -5
BALL_DIRECTION_DOWN = 5

# variables - some values can be changed to tweak the gameplay
barId = None
barSize = 100
ballId = None
ballSpeed = 10
ballHorizontalDirection = BALL_DIRECTION_LEFT
ballVerticalDirection = BALL_DIRECTION_UP

# GUI
fen = Tk()
fen.title("Balle qui bouge")
fen.resizable(False, False)
can = Canvas(fen, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
can.pack()

barId = initBar()
ballId = initBall()
moveBall()

fen.mainloop()
