from tkinter import *

"""""""""""""""""""""""""""""""""""""""
""""""""""""" CONSTANTS """"""""""""""
"""""""""""""""""""""""""""""""""""""""

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
LIVES = 3
X1 = 0
Y1 = 1
X2 = 2
Y2 = 3

"""""""""""""""""""""""""""""""""""""""""
""""""""""""" GAME METHODS """"""""""""""
"""""""""""""""""""""""""""""""""""""""""


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
    if ballStop:
        return
    checkBallCollisionsWithWalls()
    checkBallCollisionsWithBar()
    checkBallCollisionsWithBricks()
    cans[currentCan].move(ballId, ballDirectionH, ballDirectionV)
    win.after(ballSpeed, moveBall)


def checkBallCollisionsWithWalls():
    global ballDirectionH, ballDirectionV
    ballCoords = cans[currentCan].coords(ballId)
    if ballCoords[X1] <= 0:
        ballDirectionH = BALL_DIRECTION_RIGHT
    if ballCoords[Y1] <= 0:
        ballDirectionV = BALL_DIRECTION_DOWN
    if ballCoords[X2] >= CANVAS_WIDTH:
        ballDirectionH = BALL_DIRECTION_LEFT
    if ballCoords[Y2] >= CANVAS_HEIGHT:
        looseLife()
        ballDirectionV = BALL_DIRECTION_UP


def checkBallCollisionsWithBar():
    global ballDirectionV
    ballCoords = cans[currentCan].coords(ballId)
    if barId in cans[currentCan].find_overlapping(ballCoords[X1], ballCoords[Y1], ballCoords[X2], ballCoords[Y2]):
        ballDirectionV = BALL_DIRECTION_UP


def checkBallCollisionsWithBricks():
    global ballDirectionH, ballDirectionV
    ballCoords = cans[currentCan].coords(ballId)
    for brickId in bricks:
        if brickId in cans[currentCan].find_overlapping(ballCoords[X1], ballCoords[Y1], ballCoords[X2], ballCoords[Y2]):
            brickCoords = cans[currentCan].coords(brickId)
            if ballCoords[X2] == brickCoords[X1]:
                ballDirectionH = BALL_DIRECTION_LEFT
                hitBrick(brickId)
            if ballCoords[Y2] == brickCoords[Y1]:
                ballDirectionV = BALL_DIRECTION_UP
                hitBrick(brickId)
            if ballCoords[X1] == brickCoords[X2]:
                ballDirectionH = BALL_DIRECTION_RIGHT
                hitBrick(brickId)
            if ballCoords[Y1] == brickCoords[Y2]:
                ballDirectionV = BALL_DIRECTION_DOWN
                hitBrick(brickId)


def hitBrick(brickId):
    if cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_3_COLOR:
        cans[currentCan].itemconfig(brickId, fill=BRICK_STRENGTH_2_COLOR)
    elif cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_2_COLOR:
        cans[currentCan].itemconfig(brickId, fill=BRICK_STRENGTH_1_COLOR)
    elif cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_1_COLOR:
        bricks.remove(brickId)
        cans[currentCan].delete(brickId)


def looseLife():
    global lives
    lives -= 1
    if lives <= 0:
        exitLevel(None)


"""""""""""""""""""""""""""""""""""""""
""""""""""""" VARIABLES """"""""""""""
"""""""""""""""""""""""""""""""""""""""

barId = None
barSize = 100
ballId = None
ballSpeed = 10
ballDirectionH = BALL_DIRECTION_LEFT
ballDirectionV = BALL_DIRECTION_UP
# True to stop the execution of moveBall()
ballStop = None
# remaining bricks in the current level
bricks = []
# the canvas, where cans[0] is the level 1 canvas, [1] is the level 2 canvas etc.
cans = []
# same thing but with the canvas background images
backgroundImages = []
# the current canvas displayed, i.e. the position in cans
currentCan = None
# remaining lives for the current level
lives = None
# GUI
win = Tk()
win.title("Casse-briques")
win.resizable(False, False)
win.iconbitmap("images/icon.ico")
homeFrame = None
level1Frame = None
level2Frame = None

"""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""" FRAMES AND LEVELS MANAGEMENT """"""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""


def startLevel1():
    setupLevel(0)
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
    level1Frame.tkraise()


def startLevel2():
    setupLevel(1)
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
    level2Frame.tkraise()


def setupLevel(lvlIndice):
    """ Initialize the background image, bar and ball for the current canvas. """
    global currentCan, barId, ballId, ballStop, lives
    currentCan = lvlIndice
    cans[currentCan].create_image(0, 0, image=backgroundImages[currentCan])
    lives = LIVES
    barId = initBar()
    cans[currentCan].bind('<Motion>', onBarMoving)
    ballId = initBall()
    ballStop = False
    moveBall()


def exitLevel(event):
    """ Clean the canvas, stop and reset the ball, display the home frame. """
    global ballStop, ballDirectionH, ballDirectionV
    ballStop = True
    cans[currentCan].delete('all')
    bricks.clear()
    ballDirectionH = BALL_DIRECTION_LEFT
    ballDirectionV = BALL_DIRECTION_UP
    homeFrame.tkraise()


""" HOME FRAME """
homeFrame = Frame(win, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="black")
homeFrame.grid(row=0, column=0)
homeFrame.pack_propagate(False)
titleLbl = Label(homeFrame, text="CASSE-BRIQUES", fg="black", font="Andale 30 bold")
titleLbl.pack(pady=50)
startLvl1Btn = Button(homeFrame, text="Niveau 1", highlightbackground="black", activeforeground="gray",
                      command=startLevel1)
startLvl1Btn.pack()
startLvl2Btn = Button(homeFrame, text="Niveau 2", highlightbackground="black", activeforeground="gray",
                      command=startLevel2)
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

"""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""" SOME MORE THINGS """"""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

win.bind('<Escape>', exitLevel)
homeFrame.tkraise()
win.mainloop()
