from tkinter import *


def initLevel0():
    print()


def initLevel1():
    for x1 in range(25, 425, 50):
        if x1 not in [175, 225]:
            bricks.append(can.create_rectangle(x1, 25, x1 + 25, 50, fill=BRICK_STRENGTH_1_COLOR))
    for x1 in range(25, 425, 50):
        if x1 not in [175, 225]:
            bricks.append(can.create_rectangle(x1, 125, x1 + 25, 150, fill=BRICK_STRENGTH_2_COLOR))
    for x1 in range(25, 425, 50):
        if x1 not in [175, 225]:
            bricks.append(can.create_rectangle(x1, 175, x1 + 25, 200, fill=BRICK_STRENGTH_1_COLOR))
    for x1 in range(175, 275, 50):
        bricks.append(can.create_rectangle(x1, 325, x1 + 25, 350, fill=BRICK_STRENGTH_1_COLOR))


def initBar():
    return can.create_rectangle(
        CANVAS_WIDTH / 2 - barSize / 2,
        CANVAS_HEIGHT - BAR_OFFSET_FROM_BOTTOM,
        CANVAS_WIDTH / 2 + barSize / 2,
        CANVAS_HEIGHT - (BAR_OFFSET_FROM_BOTTOM + 10),
        fill="white"
    )


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
    return can.create_oval(
        CANVAS_WIDTH / 2 - 5,
        CANVAS_HEIGHT - 150,
        CANVAS_WIDTH / 2 + 5,
        CANVAS_HEIGHT - 140,
        fill="white"
    )


def moveBall():
    checkBallCollisionsWithWalls()
    checkBallCollisionsWithBar()
    checkBallCollisionsWithBricks()
    can.move(ballId, ballHorizontalDirection, ballVerticalDirection)
    fen.after(ballSpeed, moveBall)


def checkBallCollisionsWithWalls():
    global ballHorizontalDirection, ballVerticalDirection
    ballCoords = can.coords(ballId)
    if ballCoords[0] <= 0:
        ballHorizontalDirection = BALL_DIRECTION_RIGHT
    if ballCoords[1] <= 0:
        ballVerticalDirection = BALL_DIRECTION_DOWN
    if ballCoords[2] >= CANVAS_WIDTH:
        ballHorizontalDirection = BALL_DIRECTION_LEFT
    if ballCoords[3] >= CANVAS_HEIGHT:
        ballVerticalDirection = BALL_DIRECTION_UP


def checkBallCollisionsWithBar():
    global ballVerticalDirection
    ballCoords = can.coords(ballId)
    if ballCoords[3] == CANVAS_HEIGHT - BAR_OFFSET_FROM_BOTTOM - 10 and ballVerticalDirection == BALL_DIRECTION_DOWN:
        barCoords = can.coords(barId)
        if barCoords[0] - 5 <= ballCoords[2] <= barCoords[2] + 5:
            ballVerticalDirection = BALL_DIRECTION_UP


def checkBallCollisionsWithBricks():
    global ballHorizontalDirection, ballVerticalDirection
    ballCoords = can.coords(ballId)
    for brickId in bricks:
            print()


# constants - do not change during the execution !
CANVAS_WIDTH = 425
CANVAS_HEIGHT = 700
BAR_OFFSET_FROM_BOTTOM = 100
BALL_DIRECTION_LEFT = -5
BALL_DIRECTION_RIGHT = 5
BALL_DIRECTION_UP = -5
BALL_DIRECTION_DOWN = 5
BRICK_STRENGTH_1_COLOR = "yellow"
BRICK_STRENGTH_2_COLOR = "green"

# variables - some values can be changed to tweak the gameplay
barId = None
barSize = 100
ballId = None
ballSpeed = 10
ballHorizontalDirection = BALL_DIRECTION_LEFT
ballVerticalDirection = BALL_DIRECTION_UP
bricks = []     # remaining bricks in the current level

# GUI
fen = Tk()
fen.title("Balle qui bouge")
fen.resizable(False, False)
can = Canvas(fen, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black")
backgroundImage = PhotoImage(file="images/bg1.gif")
can.create_image(0, 0, image=backgroundImage)
can.pack()

barId = initBar()
can.bind('<Motion>', onBarMoving)
ballId = initBall()
moveBall()
initLevel1()

fen.mainloop()
