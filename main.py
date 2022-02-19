from tkinter import *


def initBar():
    return cans[currentCan].create_rectangle(
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
    cans[currentCan].coords(
        barId,
        event.x - barSize / 2,
        CANVAS_HEIGHT - BAR_OFFSET_FROM_BOTTOM,
        event.x + barSize / 2,
        CANVAS_HEIGHT - (BAR_OFFSET_FROM_BOTTOM + 10)
    )


def initBall():
    return cans[currentCan].create_oval(
        (int((CANVAS_WIDTH / 2) / 5) * 5) - 5,
        CANVAS_HEIGHT - 150,
        (int((CANVAS_WIDTH / 2) / 5) * 5) + 5,
        CANVAS_HEIGHT - 140,
        fill="white"
    )


def moveBall():
    if stopMoveBall:
        return
    checkBallCollisionsWithWalls()
    checkBallCollisionsWithBar()
    checkBallCollisionsWithBricks()
    cans[currentCan].move(ballId, ballHorizontalDirection, ballVerticalDirection)
    win.after(ballSpeed, moveBall)


def checkBallCollisionsWithWalls():
    global ballHorizontalDirection, ballVerticalDirection
    ballCoords = cans[currentCan].coords(ballId)
    if ballCoords[X1] <= 0:
        ballHorizontalDirection = BALL_DIRECTION_RIGHT
    if ballCoords[Y1] <= 0:
        ballVerticalDirection = BALL_DIRECTION_DOWN
    if ballCoords[X2] >= CANVAS_WIDTH:
        ballHorizontalDirection = BALL_DIRECTION_LEFT
    if ballCoords[Y2] >= CANVAS_HEIGHT:
        ballVerticalDirection = BALL_DIRECTION_UP


def checkBallCollisionsWithBar():
    global ballVerticalDirection
    ballCoords = cans[currentCan].coords(ballId)
    if barId in cans[currentCan].find_overlapping(ballCoords[X1], ballCoords[Y1], ballCoords[X2], ballCoords[Y2]):
        ballVerticalDirection = BALL_DIRECTION_UP


def checkBallCollisionsWithBricks():
    global ballHorizontalDirection, ballVerticalDirection
    ballCoords = cans[currentCan].coords(ballId)
    for brickId in bricks:
        if brickId in cans[currentCan].find_overlapping(ballCoords[X1], ballCoords[Y1], ballCoords[X2], ballCoords[Y2]):
            brickCoords = cans[currentCan].coords(brickId)
            if ballCoords[X2] == brickCoords[X1]:
                ballHorizontalDirection = BALL_DIRECTION_LEFT
                hitBrick(brickId)
            if ballCoords[Y2] == brickCoords[Y1]:
                ballVerticalDirection = BALL_DIRECTION_UP
                hitBrick(brickId)
            if ballCoords[X1] == brickCoords[X2]:
                ballHorizontalDirection = BALL_DIRECTION_RIGHT
                hitBrick(brickId)
            if ballCoords[Y1] == brickCoords[Y2]:
                ballVerticalDirection = BALL_DIRECTION_DOWN
                hitBrick(brickId)


def hitBrick(brickId):
    if cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_3_COLOR:
        cans[currentCan].itemconfig(brickId, fill=BRICK_STRENGTH_2_COLOR)
    elif cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_2_COLOR:
        cans[currentCan].itemconfig(brickId, fill=BRICK_STRENGTH_1_COLOR)
    elif cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_1_COLOR:
        bricks.remove(brickId)
        cans[currentCan].delete(brickId)


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
BRICK_STRENGTH_3_COLOR = "blue"
X1 = 0
Y1 = 1
X2 = 2
Y2 = 3

# variables - some values can be changed to tweak the gameplay
backgroundImage = None
barId = None
barSize = 100
ballId = None
ballSpeed = 10
ballHorizontalDirection = BALL_DIRECTION_LEFT
ballVerticalDirection = BALL_DIRECTION_UP
bricks = []  # remaining bricks in the current level
stopMoveBall = None
cans = []
backgroundImages = []
currentCan = None

# GUI
win = Tk()
win.title("Casse-briques")
win.resizable(False, False)
homeFrame = None
level1Frame = None
level2Frame = None


def startLevel1():
    global currentCan, barId, ballId, stopMoveBall
    currentCan = 0
    cans[currentCan].create_image(0, 0, image=backgroundImages[currentCan])
    # create bricks
    for x1 in range(25, 425, 50):
        if x1 not in [175, 225]:
            bricks.append(cans[currentCan].create_rectangle(x1, 25, x1 + 25, 50, fill=BRICK_STRENGTH_1_COLOR))
    for x1 in range(25, 425, 50):
        if x1 not in [175, 225]:
            bricks.append(cans[currentCan].create_rectangle(x1, 125, x1 + 25, 150, fill=BRICK_STRENGTH_2_COLOR))
    for x1 in range(25, 425, 50):
        if x1 not in [175, 225]:
            bricks.append(cans[currentCan].create_rectangle(x1, 175, x1 + 25, 200, fill=BRICK_STRENGTH_1_COLOR))
    for x1 in range(175, 275, 50):
        bricks.append(cans[currentCan].create_rectangle(x1, 325, x1 + 25, 350, fill=BRICK_STRENGTH_1_COLOR))
    # create bar and ball
    barId = initBar()
    cans[currentCan].bind('<Motion>', onBarMoving)
    ballId = initBall()
    stopMoveBall = False
    moveBall()
    # display the frame
    level1Frame.tkraise()


def startLevel2():
    global currentCan, barId, ballId, stopMoveBall
    currentCan = 1
    cans[currentCan].create_image(0, 0, image=backgroundImages[currentCan])
    # create bricks
    for x1 in range(25, 425, 50):
        if x1 not in [175, 225]:
            bricks.append(cans[currentCan].create_rectangle(x1, 25, x1 + 25, 50, fill=BRICK_STRENGTH_2_COLOR))
    for x1 in range(25, 425, 50):
        bricks.append(cans[currentCan].create_rectangle(x1, 125, x1 + 25, 150, fill=BRICK_STRENGTH_3_COLOR))
    for x1 in range(25, 425, 50):
        bricks.append(cans[currentCan].create_rectangle(x1, 175, x1 + 25, 200, fill=BRICK_STRENGTH_2_COLOR))
    for x1 in range(175, 275, 50):
        if x1 not in [175, 225]:
            bricks.append(cans[currentCan].create_rectangle(x1, 325, x1 + 25, 350, fill=BRICK_STRENGTH_2_COLOR))
    # create bar and ball
    barId = initBar()
    cans[currentCan].bind('<Motion>', onBarMoving)
    ballId = initBall()
    stopMoveBall = False
    moveBall()
    # display the frame
    level2Frame.tkraise()


""" HOME FRAME """
homeFrame = Frame(win, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="black")
homeFrame.grid(row=0, column=0)
homeFrame.pack_propagate(False)
titleLbl = Label(homeFrame, text="CASSE-BRIQUES", fg="black", font="Andale 30 bold")
titleLbl.pack(pady=50)
startLvl1Btn = Button(homeFrame, text="Niveau 1", highlightbackground="black", activeforeground="gray", command=startLevel1)
startLvl1Btn.pack()
startLvl2Btn = Button(homeFrame, text="Niveau 2", highlightbackground="black", activeforeground="gray", command=startLevel2)
startLvl2Btn.pack()
exitBtn = Button(homeFrame, text="Quitter", highlightbackground="black", activeforeground="gray", command=win.destroy)
exitBtn.pack()

""" LEVEL 1 FRAME """
level1Frame = Frame(win, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
level1Frame.grid(row=0, column=0)
level1Frame.pack_propagate(False)
can = Canvas(level1Frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black", highlightthickness=0)
backgroundImage = PhotoImage(file="images/bg1.gif")
can.pack()
cans.append(can)
backgroundImages.append(backgroundImage)

""" LEVEL 2 FRAME """
level2Frame = Frame(win, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
level2Frame.grid(row=0, column=0)
level2Frame.pack_propagate(False)
can = Canvas(level2Frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black", highlightthickness=0)
backgroundImage = PhotoImage(file="images/bg2.gif")
can.pack()
cans.append(can)
backgroundImages.append(backgroundImage)


def exitLevel(event):
    global stopMoveBall, ballHorizontalDirection, ballVerticalDirection
    stopMoveBall = True
    cans[currentCan].delete('all')
    bricks.clear()
    ballHorizontalDirection = BALL_DIRECTION_LEFT
    ballVerticalDirection = BALL_DIRECTION_UP
    homeFrame.tkraise()


win.bind('<Escape>', exitLevel)
# launch the game
homeFrame.tkraise()
win.mainloop()
