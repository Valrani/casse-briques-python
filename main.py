from tkinter import *


"""""""""""""""""""""""""""""""""""""""
""""""""""""" CONSTANTS """"""""""""""
"""""""""""""""""""""""""""""""""""""""

CANVAS_WIDTH = 425
CANVAS_HEIGHT = 700
BAR_OFFSET_FROM_BOTTOM = 100
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
    global ballDirectionH, ballDirectionV
    ballDirectionH = ballDirectionLeft
    ballDirectionV = ballDirectionUp
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
    if looseLifeAfterExecution:
        looseLife()
    if winAfterExecution:
        win()
    window.after(ballSpeed, moveBall)


def checkBallCollisionsWithWalls():
    global ballDirectionH, ballDirectionV, looseLifeAfterExecution
    ballCoords = cans[currentCan].coords(ballId)
    if ballCoords[X1] <= 0:
        ballDirectionH = ballDirectionRight
    if ballCoords[Y1] <= 0:
        ballDirectionV = ballDirectionDown
    if ballCoords[X2] >= CANVAS_WIDTH:
        ballDirectionH = ballDirectionLeft
    if ballCoords[Y2] >= CANVAS_HEIGHT:
        looseLifeAfterExecution = True


def checkBallCollisionsWithBar():
    global ballDirectionH, ballDirectionV, ballDirectionLeft, ballDirectionRight, ballDirectionUp, ballDirectionDown
    ballCoords = cans[currentCan].coords(ballId)
    if barId in cans[currentCan].find_overlapping(ballCoords[X1], ballCoords[Y1], ballCoords[X2], ballCoords[Y2]):
        # change ball angle, depending on where the ball touch the bar (in the center or on the sides)
        barCoords = cans[currentCan].coords(barId)
        if barCoords[X1] + 20 < ballCoords[X2] - 5 < barCoords[X2] - 20:
            ballDirectionLeft = -3
            ballDirectionRight = 3
            ballDirectionUp = -5
            ballDirectionDown = 5
        else:
            ballDirectionLeft = -5
            ballDirectionRight = 5
            ballDirectionUp = -5
            ballDirectionDown = 5
        ballDirectionV = ballDirectionUp
        ballDirectionH = ballDirectionLeft if ballDirectionH < 0 else ballDirectionRight


def checkBallCollisionsWithBricks():
    global ballDirectionH, ballDirectionV
    ballCoords = cans[currentCan].coords(ballId)
    for brickId in bricks:
        if brickId in cans[currentCan].find_overlapping(ballCoords[X1], ballCoords[Y1], ballCoords[X2], ballCoords[Y2]):
            brickCoords = cans[currentCan].coords(brickId)
            if ballCoords[X2] - brickCoords[X1] in range(-3, 3):
                ballDirectionH = ballDirectionLeft
                hitBrick(brickId)
            elif ballCoords[Y2] - brickCoords[Y1] in range(-3, 3):
                ballDirectionV = ballDirectionUp
                hitBrick(brickId)
            elif ballCoords[X1] - brickCoords[X2] in range(-3, 3):
                ballDirectionH = ballDirectionRight
                hitBrick(brickId)
            elif ballCoords[Y1] - brickCoords[Y2] in range(-3, 3):
                ballDirectionV = ballDirectionDown
                hitBrick(brickId)


def hitBrick(brickId):
    global winAfterExecution
    if cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_3_COLOR:
        cans[currentCan].itemconfig(brickId, fill=BRICK_STRENGTH_2_COLOR)
    elif cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_2_COLOR:
        cans[currentCan].itemconfig(brickId, fill=BRICK_STRENGTH_1_COLOR)
    elif cans[currentCan].itemcget(brickId, "fill") == BRICK_STRENGTH_1_COLOR:
        bricks.remove(brickId)
        cans[currentCan].delete(brickId)
        if len(bricks) <= 0:
            winAfterExecution = True


def looseLife():
    global lives, ballId, looseLifeAfterExecution
    lives -= 1
    cans[currentCan].delete(ballId)
    ballId = initBall()
    if lives <= 0:
        exitLevel(None)
        looseTxtLbl["text"] = "Il ne restait que " + str(len(bricks)) + " briques..."
        looseFrame.tkraise()
    looseLifeAfterExecution = False


def win():
    global currentLvl, highestLvl, winAfterExecution
    if currentLvl == highestLvl:
        highestLvl += 1
        unlockNextLevel()
    exitLevel(None)
    winAfterExecution = False


"""""""""""""""""""""""""""""""""""""""
""""""""""""" VARIABLES """"""""""""""
"""""""""""""""""""""""""""""""""""""""

barId = None
barSize = 100
ballId = None
ballSpeed = 10
# default ball speeds
ballDirectionLeft = -5
ballDirectionRight = 5
ballDirectionUp = -5
ballDirectionDown = 5
ballDirectionH = ballDirectionLeft
ballDirectionV = ballDirectionUp
# True to stop the execution of moveBall()
ballStop = None
# remaining bricks in the current level
bricks = []
# the canvas, where cans[0] is the level 1 canvas, [1] is the level 2 canvas etc.
cans = []
# same thing but with the canvas background images
backgroundImages = []
# the current canvas displayed, i.e. the position in cans, starts at 0.
currentCan = None
# remaining lives for the current level
lives = None
# used to execute the looseLife() function at the end of moveBall()
looseLifeAfterExecution = False
# used to execute the win() function at the end of moveBall()
winAfterExecution = False
# the highest level beaten by the player, starts at 1.
highestLvl = 1
# the level currently played, starts at 1.
currentLvl = None

# GUI
window = Tk()
window.title("Casse-briques")
window.resizable(False, False)
window.iconbitmap("images/icon.ico")
homeFrame = None
looseFrame = None
level1Frame = None
level2Frame = None
level3Frame = None

"""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""" FRAMES AND LEVELS MANAGEMENT """"""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""


def startLevel1():
    setupLevel(1)
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
    setupLevel(2)
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


def startLevel3():
    setupLevel(3)
    for x1 in range(25, 425, 50):
        bricks.append(cans[currentCan].create_rectangle(x1, 25, x1 + 25, 50, fill=BRICK_STRENGTH_3_COLOR))
    for x1 in range(25, 425, 50):
        if x1 not in [25, 50, 400, 425]:
            bricks.append(cans[currentCan].create_rectangle(x1, 125, x1 + 25, 150, fill=BRICK_STRENGTH_3_COLOR))
    for x1 in range(25, 425, 50):
        if x1 not in [25, 50, 400, 425]:
            bricks.append(cans[currentCan].create_rectangle(x1, 175, x1 + 25, 200, fill=BRICK_STRENGTH_2_COLOR))
    for x1 in range(175, 275, 50):
        bricks.append(cans[currentCan].create_rectangle(x1, 325, x1 + 25, 350, fill=BRICK_STRENGTH_3_COLOR))
    level3Frame.tkraise()


def setupLevel(lvl):
    """ Initialize the background image, bar and ball for the current canvas. """
    global currentCan, barId, ballId, ballStop, lives, currentLvl
    currentCan = lvl - 1
    currentLvl = lvl
    cans[currentCan].create_image(0, 0, image=backgroundImages[currentCan])
    bricks.clear()
    lives = LIVES
    barId = initBar()
    cans[currentCan].bind('<Motion>', onBarMoving)
    ballId = initBall()
    ballStop = False
    moveBall()


def exitLevel(event):
    """ Clean the canvas, stop and reset the ball, display the home frame. """
    global ballStop, currentLvl
    ballStop = True
    currentLvl = None
    cans[currentCan].delete('all')
    homeFrame.tkraise()


def unlockNextLevel():
    global startLvl2Btn, startLvl3Btn
    if highestLvl == 2:
        startLvl2Btn["state"] = NORMAL
    elif highestLvl == 3:
        startLvl3Btn["state"] = NORMAL


""" HOME FRAME """
homeFrame = Frame(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="black")
homeFrame.grid(row=0, column=0)
homeFrame.pack_propagate(False)
titleLbl = Label(homeFrame, text="CASSE-BRIQUES", fg="black", font="Andale 30 bold")
titleLbl.pack(pady=50)
startLvl1Btn = Button(homeFrame, text="Niveau 1", highlightbackground="black", activeforeground="gray",
                      height=2, width=10, font="Andale 18", command=startLevel1)
startLvl1Btn.pack()
startLvl2Btn = Button(homeFrame, text="Niveau 2", highlightbackground="black", activeforeground="gray",
                      height=2, width=10, font="Andale 18", command=startLevel2)
if highestLvl < 2:
    startLvl2Btn["state"] = DISABLED
startLvl2Btn.pack()
startLvl3Btn = Button(homeFrame, text="Niveau 3", highlightbackground="black", activeforeground="gray",
                      height=2, width=10, font="Andale 18", command=startLevel3)
if highestLvl < 3:
    startLvl3Btn["state"] = DISABLED
startLvl3Btn.pack()

exitBtn = Button(homeFrame, text="Quitter", highlightbackground="black", activeforeground="gray", height=2, width=10,
                 font="Andale 18", command=window.destroy)
exitBtn.pack(pady=50)

""" LOOSE FRAME """
looseFrame = Frame(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="black")
looseFrame.grid(row=0, column=0)
looseFrame.pack_propagate(False)
looseTitleLbl = Label(looseFrame, text="Perdu...", fg="red", font="Andale 24 bold")
looseTitleLbl.pack(pady=50)
looseTxtLbl = Label(looseFrame, fg="black", font="Andale 16")
looseTxtLbl.pack(pady=50)
returnBtn = Button(looseFrame, text="Retour", highlightbackground="black", activeforeground="gray", height=2, width=10,
                 font="Andale 18", command=lambda: homeFrame.tkraise())
returnBtn.pack(pady=50)


""" LEVEL 1 FRAME """
level1Frame = Frame(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
level1Frame.grid(row=0, column=0)
level1Frame.pack_propagate(False)
can = Canvas(level1Frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black", highlightthickness=0)
backgroundImage = PhotoImage(file="images/bg1.gif")
can.pack()
cans.append(can)
backgroundImages.append(backgroundImage)

""" LEVEL 2 FRAME """
level2Frame = Frame(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
level2Frame.grid(row=0, column=0)
level2Frame.pack_propagate(False)
can = Canvas(level2Frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black", highlightthickness=0)
backgroundImage = PhotoImage(file="images/bg2.gif")
can.pack()
cans.append(can)
backgroundImages.append(backgroundImage)

""" LEVEL 3 FRAME """
level3Frame = Frame(window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
level3Frame.grid(row=0, column=0)
level3Frame.pack_propagate(False)
can = Canvas(level3Frame, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="black", highlightthickness=0)
backgroundImage = PhotoImage(file="images/bg3.gif")
can.pack()
cans.append(can)
backgroundImages.append(backgroundImage)

"""""""""""""""""""""""""""""""""""""""""""""""""""
"""""""""""""""" SOME MORE THINGS """"""""""""""""
"""""""""""""""""""""""""""""""""""""""""""""""""""

window.bind('<Escape>', exitLevel)
homeFrame.tkraise()
window.mainloop()
