# FN + F5 to run


import pygame, random, math, time, json

# -INGAME-
# BLOB
from Blob import *

# ENEMIES
from Enemy import *
from Whirlpool import *
from Shooter import *
from FastEnemy import *
from Bullet import *

# OTHER
from Bar import *
from PowerUp import *
from EnemyBullet import *
from Food import *
from Effect import *

# -OUT OF GAME-
from Button import *
from TextBox import *
from Switch import *
from User import *
from Message import *

pygame.init()
screen = pygame.display.set_mode([1000, 1000])
pygame.font.init()
# choossse font5
fontPath = "Poppins/Poppins-Regular.ttf"
tinyFont = pygame.font.Font(fontPath, 30)
smallFont = pygame.font.Font(fontPath, 40)
smallerFont = pygame.font.Font(fontPath, 50)
font = pygame.font.Font(fontPath, 65)
bigFont = pygame.font.Font(fontPath, 80)
colorTheme = (115, 225, 255)

# Message Lists
deathList = [
    "wrecked",
    "destroyed",
    "wasted",
    "demolished",
    "annihilated",
    "obliterated",
    "eliminated",
    "disintegrated",
    "exterminated",
    "deleted",
    "terminated",
    "neutralized",
]
encourageList = [
    [
        "Did you break your hand or something?",
        "That was complete garbage",
        "Why are you even trying...",
        "It's easy to do better than that",
        "Your baaaaaaad",
        "That was painful to watch",
    ],
    [
        "That was pretty bad",
        "You can definitely do better",
        "Just... do better",
        "Try harder",
    ],
    [
        "Ok, I guess",
        "Meh",
        "That's pretty to average",
        "Pretty typical",
        "A normal score",
    ],
    [
        "That was pretty good!",
        "Good job!",
        "That was actually pretty good!",
        "That's almost at your highscore!",
        "You almost beat your highscore!",
    ],
    [
        "Awesome!",
        "Super!",
        "Spectacular!",
        "Fantastic!",
        "Wonderful!",
        "Splendid!",
        "Awesome job!",
        "Wonderful job!",
        "Spectacularily done!",
        "Fantastically done!",
        "Simply Splendid",
    ],
]
greetingList = [
    "Welcome, ",
    "Hello ",
    "Good to see you again, ",
    "Hello again, ",
    "Greetings",
    "Welcome back",
    " Welcome home, human",
]

# Loading Images
colorPaletteImage = pygame.image.load("colorPalette.jpg")
colorPaletteRect = colorPaletteImage.get_rect()
colorPaletteRect.x = screen.get_width() / 2 - colorPaletteRect.width / 2 + 100
colorPaletteRect.y = 450
chosenColor = None


def placingText(side, font, text):
    fontSize = font.size(text)[0]
    if side == "left":
        return 30
    elif side == "right":
        return 950 - fontSize
    elif side == "middle":
        return 475 - fontSize / 2


# State Button Dictionary
stateButtonDict = {
    0: [
        Button(
            screen, (placingText("middle", bigFont, "START"), 400), "START", bigFont
        ),
        Button(
            screen,
            (placingText("left", smallFont, "INSTRUCTIONS"), 600),
            "INSTRUCTIONS",
            smallFont,
        ),
        Button(
            screen,
            (placingText("right", smallFont, "LEADERBOARDS"), 600),
            "LEADERBOARDS",
            smallFont,
        ),
        Button(screen, (30, 700), "LOGIN", font),
        Button(screen, (380, 700), "CREATE ACCOUNT", font),
    ],
    1: [Button(screen, (30, 770), "HOME", smallerFont)],
    2: [Button(screen, (30, 770), "HOME", smallerFont)],
    3: [
        Button(screen, (333, 400), "START", bigFont),
        Button(
            screen,
            (placingText("left", smallFont, "INSTRUCTIONS"), 600),
            "INSTRUCTIONS",
            smallFont,
        ),
        Button(
            screen,
            (placingText("right", smallFont, "LEADERBOARDS"), 600),
            "LEADERBOARDS",
            smallFont,
        ),
        Button(screen, (30, 700), "LOGOUT", font),
        Button(screen, (placingText("right", font, "SETTINGS"), 700), "SETTINGS", font),
    ],
    4: [],
    5: [
        Button(screen, (30, 770), "HOME", smallerFont),
        Button(screen, (293, 600), "LEADERBOARDS", smallFont),
    ],
    6: [
        Button(screen, (30, 770), "HOME", smallerFont),
        Button(screen, (372, 600), "LOGIN", font),
        Switch(screen, (840, 345, 50, 50), tempText="HIDE", tempFont=tinyFont),
    ],
    7: [
        Button(screen, (30, 770), "HOME", smallerFont),
        Button(screen, (338, 750), "CREATE", font),
        Switch(screen, (840, 345, 50, 50), tempText="HIDE", tempFont=tinyFont),
    ],
    8: [
        Button(screen, (30, 770), "HOME", smallerFont),
        Button(screen, (390, 750), "SAVE", font),
        Switch(screen, (840, 345, 50, 50), tempText="HIDE", tempFont=tinyFont),
        Button(screen, (757, 770), "DELETE", smallFont),
    ],
}

stateTextBoxDict = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: [],
    6: [
        TextBox(screen, (200, 200, 600, 100), font, "USERNAME"),
        TextBox(screen, (200, 320, 600, 100), font, "PASSWORD"),
    ],
    7: [
        TextBox(screen, (200, 200, 600, 100), font, "USERNAME"),
        TextBox(screen, (200, 320, 600, 100), font, "PASSWORD"),
    ],
    8: [
        TextBox(screen, (200, 200, 600, 100), font, "NEW USERNAME"),
        TextBox(screen, (200, 320, 600, 100), font, "NEW PASSWORD"),
    ],
}

messageList = []
leaderboard = {}

# The state of the game
# 0 = start screen not logged in
# 1 = instrucshuns (instructions) screen
# 2 = just leaderboard
# 3 = start screen logged in
# 4 = game
# 5 = gameover
# 6 = login
# 7 = new/create account
# 8 = edit/delete account
state = 0
transition = [0, 0]
currentUser = None

# ALL THE FUNCTIONS
# ALL THE FUNCTIONS
# ALL THE FUNCTIONS
def loadData():
    usersDataFile = open("usersData.txt", "r")
    userList = []
    for line in usersDataFile:
        data = json.loads(line)
        name = data["name"]
        password = data["password"]
        color = data["color"]
        scoreList = data["scoreList"]
        timePlayed = data["timePlayed"]
        userList.append(User(name, password, color, scoreList, timePlayed))
    usersDataFile.close()
    return userList


def login(name, password):
    for user in userList:
        if user.name == name and user.password == password:
            return user
    return None


def createAccount(name, password):
    global chosenColor
    user = User(name, password, chosenColor, [], 0)
    for otherUser in userList:
        if otherUser.name == user.name:
            return None
    if chosenColor is None:
        return None
    chosenColor = None
    userList.append(user)
    saveData(userList)
    return user


def editAccount(name, password, user):
    global chosenColor
    for otherUser in userList:
        if otherUser != user and otherUser.name == name:
            return None
    userList.remove(user)
    if len(name) > 0:
        newName = name
    else:
        newName = user.name
    if len(password) > 0:
        newPassword = password
    else:
        newPassword = user.password
    if chosenColor is not None:
        newColor = chosenColor
    else:
        newColor = user.color
    newUser = User(newName, newPassword, newColor, user.scoreList, user.timePlayed)
    userList.append(newUser)
    saveData(userList)
    return newUser


def saveData(userList):
    usersDataFile = open("usersData.txt", "w")
    for user in userList:
        usersDataFile.write(json.dumps(user) + "\n")
    usersDataFile.close()


def leaderboard(userList):
    userScore = {}
    leaderboard = {}
    for user in userList:
        if len(user.scoreList) > 0:
            userScore.update({max(user.scoreList): user.name})
    scoreList = sorted(userScore, reverse=True)
    for score in scoreList:
        for user in userScore:
            if score == user:
                leaderboard.update({userScore[user]: score})
    return leaderboard


# Checks if left mouse down click is inside Buhtttohn
def leftMouseEventInButton(mouseDownEvent, rect):
    return mouseDownEvent.button == 1 and rect.collidepoint(mouseDownEvent.pos)


def initBullets():
    bullet = Bullet(screen, blob)
    spammer = Spammer(screen, blob)
    sniper = Sniper(screen, blob)
    grenade = Grenade(screen, blob)
    rocket = RocketLauncher(screen, blob)
    bulletTypes.append(bullet)
    bulletTypes.append(spammer)
    bulletTypes.append(sniper)
    bulletTypes.append(grenade)
    bulletTypes.append(rocket)


# Makes a rect with rounded corners (https://www.pygame.org/project-AAfilledroundedRect-2349-.html)
def roundedRect(surface, rect, color, radius=0.7):
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, (0, 0, 0), circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)

    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius)
    radius.topright = rect.topright
    rectangle.blit(circle, radius)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius)

    rectangle.fill((0, 0, 0), rect.inflate(-radius.w, 0))
    rectangle.fill((0, 0, 0), rect.inflate(0, -radius.h))

    rectangle.fill(color, special_flags=pygame.BLEND_RGBA_MAX)
    rectangle.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MIN)

    return surface.blit(rectangle, pos)


# Make text thaht fits on screen (https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame)


def blitText(surface, text, pos, font, color=pygame.Color("black")):
    words = [
        word.split(" ") for word in text.splitlines()
    ]  # 2D array where each row is a list of words.
    space = font.size(" ")[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def makeFood(foodQuantity, x=0, y=0, deathReward=False, color=(0, 0, 0)):
    for i in range(foodQuantity):
        # make food X, Y and color
        randomXSpeed = random.randint(-50, 50)
        randomYSpeed = random.randint(-50, 50)
        randomX = x + randomXSpeed if deathReward else random.randint(0, 1000)
        randomY = y + randomYSpeed if deathReward else random.randint(0, 1000)
        randomColor = (
            color
            if deathReward
            else (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
        )
        # create food
        blobFood = Food(screen, randomX, randomY, randomColor)
        if deathReward:
            blobFood.xSpeed = randomXSpeed / 3
            blobFood.ySpeed = randomYSpeed / 3
        foodList.append(blobFood)


def makePower(powerQuantity):
    for i in range(powerQuantity):
        # make food X, Y and color
        randomX = random.randint(0, 1000)
        randomY = random.randint(0, 1000)
        percent = random.randint(1, 100)
        # Percent of power
        if percent > 0 and percent < 21:
            # LIGHT BLUE
            color = (100, 0, 0)
            powerType = "speed"
        elif percent > 20 and percent < 41:
            # LIGHT GREEN
            color = (100, 0, 100)
            powerType = "nokill"
        elif percent > 40 and percent < 61:
            # RED
            color = (0, 100, 71)
            powerType = "spam"
        elif percent > 60 and percent < 91:
            # IDK
            color = (0, 10, 94)
            powerType = "damage"
        elif percent > 90:
            # DARKISH TURKLE (PRULPLE [PURPLE])
            color = (42, 94, 0)
            powerType = "god"
        # create power
        blobPower = PowerUp(screen, randomX, randomY, color, powerType)
        powerUpList.append(blobPower)


def makeEnemy(enemyQuantity, difficulty):
    for i in range(enemyQuantity):
        # make enemy X, Y and color
        randomX = random.randint(0, 1000)
        randomY = random.randint(0, 1000)
        randomColor = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        # create baddy
        percent = random.randint(0, 100)
        if percent < 21:
            enemy = Whirlpool(screen, randomX, randomY, randomColor, difficulty)
            enemyList.append(enemy)
        elif percent > 20 and percent < 41:
            enemy = Shooter(screen, randomX, randomY, randomColor, difficulty)
            enemyList.append(enemy)
        elif percent > 40 and percent < 61:
            name = random.choice(
                [
                    "Mosquito",
                    "Piranha",
                    "Wasp",
                    "Hornet",
                    "Mosquito Blob",
                    "Piranha Blob",
                    "Wasp Blob",
                    "Hornet Blob",
                ]
            )
            for i in range(1, random.randint(6, 8)):
                enemy = FastEnemy(
                    screen,
                    randomX + random.randint(-100, 100),
                    randomY + random.randint(-100, 100),
                    randomColor,
                    difficulty,
                )
                enemy.nameList = [name]
                enemyList.append(enemy)
        else:
            enemy = Enemy(screen, randomX, randomY, randomColor, difficulty)
            enemyList.append(enemy)


# INITIALIZEING STUFF

userList = loadData()

startTime = time.time()
score = 0
lastHit = 0
bulletName = "Edible salami"
gameOver = font.render("GAME OVER", False, (255, 255, 255))
leaderboardTitle = bigFont.render("LEADERBOARD", False, (255, 255, 255))
loginTitle = bigFont.render("LOGIN", False, (255, 255, 255))
settingsTitle = bigFont.render("SETTINGS", False, (255, 255, 255))
createTitle = font.render("CREATE NEW ACCOUNT", False, (255, 255, 255))
start = font.render("START", False, (255, 255, 255))
title = bigFont.render("WORLD OF BLOB", False, (255, 255, 255))
userText = smallFont.render("NOT LOGGED IN", False, (50, 50, 50))

instructionString = """Welcome to the world of blob! Use your mouse to control where the blob in the middle goes! Avoid your enemies and knock them down with your almighty arsenal of weapons - press space to shoot, and use the arrow keys or W & S to change your weapon!

Types of enemies:
- Frog - hops around randomly, sometimes towards you to squash you. Doesn't have too much health.
- Squid - follows you, pulls you in with whirlpool once in a while. Has pretty high health.
- Cannon - stalks you and spams bullets towards you. Has very high health, so watch out!
- Wasps - Fly around at high speeds in swarms and sting you, but barely have any health

Types of bullets:
- Shooter - medium damage, medium fire rate, good knockback, no splash
- Spammer - low damage, high fire rate, medium knockback, no splash
- Sniper - very high damage, low fire rate, high knockback, no splash
- Grenader - medium-high damage, low fire rate, no knockback, big splash after a time
- Rocketier - high damage, very low fire rate, no knockback, big splash upon impact"""

gridList = []
for i in range(100, 901, 100):
    gridList.append(((random.randint(-100, 100), i), (random.randint(900, 1100), i)))
    gridList.append(((i, random.randint(-100, 100)), (i, random.randint(900, 1100))))


# making blobolicous, aka blob, with light blue body and white eyes and 50 radius
blob = Blob(screen, colorTheme, (0, 0, 0), 50, 0, 0)
difficutly = 0.5

dev = False
godPower = False
speedPower = False
immunityPower = False
damagePower = False
reloadPower = False
lastEnemySpawn = 0
lastFoodSpawn = 0
lastPowerSpawn = 0
powerUpStart = 0
enemySpawnDelay = 0.5
foodSpawnDelay = 0.5
powerSpawnDelay = 0.5
powerUpDuration = 5
powerBar = Bar(screen, 250, 50, (115, 225, 255), 5, "PowerUpBar", 500, 30)
ammo = 200
shellCost = 3
enemyKills = 0
enemyTrack = {}

bulletTypes = []
currentBullet = 0
foodList = []
enemyList = []
bulletList = []
powerUpList = []
enemyBulletList = []
effectList = []
makeFood(30)

# INIT FUNCTION
def reset():
    global effectList, difficulty, state, ammo, lastHit, startTime, score, blob, dev, godPower, speedPower, immunityPower, damagePower, reloadPower, lastEnemySpawn, lastFoodSpawn, lastPowerSpawn, powerUpStart, enemySpawnDelay, foodSpawnDelay, powerSpawnDelay, powerUpDuration, powerBar, ammo, shellCost, enemyKills, enemyTrack, startButtonPress, bulletTypes, currentBullet, foodList, enemyList, bulletList, powerUpList, enemyBulletList

    # Change State to game state
    state = 4

    # making blobolicous, aka blob, with light blue body and black eyes and 50 radius
    blob = Blob(screen, colorTheme, (0, 0, 0), 50, 500, 500)
    difficulty = 0.5

    startTime = time.time()
    score = 0
    lastHit = 0

    dev = False
    godPower = False
    speedPower = False
    immunityPower = False
    damagePower = False
    reloadPower = False
    lastEnemySpawn = 0
    lastPowerSpawn = 0
    powerUpStart = 0
    enemySpawnDelay = 0.5
    foodSpawnDelay = 0.5
    powerSpawnDelay = 0.5
    powerUpDuration = 5
    powerBar = Bar(screen, 250, 50, (115, 225, 255), 5, "PowerUpBar", 500, 30)
    ammo = 200
    shellCost = 3
    enemyKills = 0
    enemyTrack = {}
    startButtonPress = False

    bulletTypes = []
    currentBullet = 0
    initBullets()

    foodList = []
    enemyList = []
    bulletList = []
    powerUpList = []
    enemyBulletList = []
    effectList = []
    makeFood(30)


def transformPoint(point):
    return point[0] - blob.x + int(screen.get_width() / 2), point[1] - blob.y + int(
        screen.get_height() / 2
    )


# Message
def message(text, time=2, tempType="info"):
    messageList.append(
        Message(screen, smallFont, text, tempTime=time, tempType=tempType)
    )


# Clear all messages - finish the current one
def clearMessage(finish=True):
    global messageList
    if len(messageList) > 0 and finish:
        current = messageList[0]
        current.showTime = None
        messageList = [current]
    else:
        messageList = []


def drawEverything():
    screen.fill((0, 0, 0))
    # 0 = start screen not logged in
    # 1 = instrucshuns (instructions) screen
    # 2 = just leaderboard
    # 3 = start screen logged in
    # 4 = game
    # 5 = gameover
    # 6 = login
    # 7 = new/create account
    # 8 = edit/delete account
    # START SCREEN STATE

    if state == 0:
        screen.blit(title, (500 - bigFont.size("WORLD OF BLOB")[0] / 2, 100))
        screen.blit(userText, (10, 10))

    if state == 1:
        blitText(screen, instructionString, (10, 10), tinyFont, color=(255, 255, 255))

    if state == 2:
        # LEADERBOARD
        screen.blit(leaderboardTitle, (500 - bigFont.size("LEADERBOARD")[0] / 2, 30))
        for userScore, count in zip(leaderboard, range(10)):
            # Outline
            if count == 9 and currentUser is not None:
                # Making text and rect outline
                outline = colorTheme
                countText = smallerFont.render(
                    (str(list(leaderboard).index(currentUser.name) + 1) + "."),
                    False,
                    (255, 255, 255),
                )
                nameText = smallerFont.render(currentUser.name, False, (255, 255, 255))
                pointText = smallerFont.render(
                    str(max(currentUser.scoreList)), False, (255, 255, 255)
                )
                # Drawing rects
                roundedRect(
                    screen, (90, 150 + count * 60, 820, 50), outline, radius=0.4
                )
                roundedRect(
                    screen, (94, 154 + count * 60, 812, 42), (0, 0, 0), radius=0.4
                )

            else:
                # Making rect outline
                outline = (255, 255, 255)
                for user in userList:
                    if user.name == userScore:
                        outline = user.color
                        break
                # Making text
                countText = smallerFont.render(
                    (str(count + 1) + "."), False, (255, 255, 255)
                )
                nameText = smallerFont.render(userScore, False, (255, 255, 255))
                pointText = smallerFont.render(
                    str(leaderboard[userScore]), False, (255, 255, 255)
                )
                # Drawing rects
                roundedRect(
                    screen, (100, 150 + count * 60, 800, 50), outline, radius=0.4
                )
                roundedRect(
                    screen, (104, 154 + count * 60, 792, 42), (0, 0, 0), radius=0.4
                )
            # Blitting Text
            screen.blit(countText, (115, 155 + count * 60))
            screen.blit(nameText, (250, 155 + count * 60))
            screen.blit(
                pointText,
                (
                    885 - smallerFont.size(str(leaderboard[userScore]))[0],
                    155 + count * 60,
                ),
            )

    if state == 3:
        screen.blit(title, (500 - bigFont.size("WORLD OF BLOB")[0] / 2, 100))
        screen.blit(userText, (10, 10))

    elif state == 4 or state == 5:
        screen.fill(
            (
                min(255, blob.shake * 3),
                min(255, blob.shake * 3),
                min(255, blob.shake * 3),
            )
        )
        # Draw in-game stuff n' things
        for bullet in bulletList:
            bullet.draw(blob.x, blob.y)
        for line in gridList:
            pygame.draw.line(
                screen,
                (255, 255, 255),
                transformPoint(line[0]),
                transformPoint(line[1]),
            )
        for bullet in enemyBulletList:
            bullet.draw(blob.x, blob.y)
        for power in powerUpList:
            power.draw(blob.x, blob.y)
        for enemy in enemyList:
            enemy.draw(blob.x, blob.y)
        for food in foodList:
            food.draw(blob.x, blob.y)
        for effect in effectList:
            effect.draw(blob.x, blob.y)

        if state == 4:
            # Draw blob
            blob.draw()
            # Hide mouse and draw target
            pygame.mouse.set_visible(False)
            pygame.draw.circle(screen, colorTheme, pygame.mouse.get_pos(), 15)
            pygame.draw.circle(screen, (0, 0, 0), pygame.mouse.get_pos(), 12)

            # Draw bullet type and ammo coutn
            screen.blit(bulletName, (100, 700))
            screen.blit(ammoText, (500, 700))

        if state == 5:
            # Draw gameover
            screen.blit(gameOver, (300, 450))
            # Show mouse
            pygame.mouse.set_visible(True)

        # Draw Score
        screen.blit(score, (480, 300))
        # Draw currentPower and power bar
        if state == 4:
            screen.blit(currentPower, (320, 100))
            if not dev and (
                godPower or speedPower or immunityPower or reloadPower or damagePower
            ):
                powerBar.draw(5 - (time.time() - powerUpStart), color=colorTheme)

    # DARW login screen
    if state == 6:
        stateTextBoxDict[state][1].hide = stateButtonDict[state][2].on
        screen.blit(loginTitle, (placingText("middle", bigFont, "LOGIN") + 25, 100))

    # DARW settingz screen
    if state == 7:
        stateTextBoxDict[state][1].hide = stateButtonDict[state][2].on
        screen.blit(
            createTitle, (placingText("middle", font, "CREATE NEW ACCOUNT") + 25, 100)
        )
        # Drawing Color Palette
        screen.blit(colorPaletteImage, (colorPaletteRect.x, colorPaletteRect.y))
        if chosenColor is None:
            label = tinyFont.render("NO COLOR THEME", False, (100, 100, 100))
            screen.blit(label, (180, 450))
        else:
            roundedRect(screen, (250, 550, 70, 70), (100, 100, 100), 0.4)
            roundedRect(screen, (255, 555, 60, 60), chosenColor, 0.4)
            label = tinyFont.render("COLOR THEME", False, chosenColor)
            screen.blit(label, (210, 450))

    # DARW settingz screen
    if state == 8:
        stateTextBoxDict[state][1].hide = stateButtonDict[state][2].on
        screen.blit(
            settingsTitle, (placingText("middle", bigFont, "SETTINGS") + 25, 100)
        )
        # Drawing Color Palette
        screen.blit(colorPaletteImage, (colorPaletteRect.x, colorPaletteRect.y))
        if chosenColor is None:
            label = tinyFont.render("NEW COLOR THEME", False, (100, 100, 100))
            screen.blit(label, (170, 450))
        else:
            roundedRect(screen, (250, 550, 70, 70), (100, 100, 100), 0.4)
            roundedRect(screen, (255, 555, 60, 60), chosenColor, 0.4)
            label = tinyFont.render("COLOR THEME", False, chosenColor)
            screen.blit(label, (210, 450))

    # DRaw dem buttons and dem textbawxes (textboxes)
    for box in stateTextBoxDict[state]:
        box.draw(colorTheme)
    for button in stateButtonDict[state]:
        button.draw(colorTheme)

    # Draw game open transitions
    if state == 4 and transition[0] > 9:
        pygame.draw.rect(
            screen, (0, 0, 0), (0, 0, 1000, 500 - (transition[0] - 9) * 50)
        )
        pygame.draw.rect(
            screen,
            (0, 0, 0),
            (0, 500 + (transition[0] - 9) * 50, 1000, 500 - (transition[0] - 9) * 50),
        )

    # Draw and delete messages
    for message in messageList:
        if message.showTime == None:
            messageList.remove(message)
    if len(messageList) > 0:
        if state == 4:
            messageList[0].drawMove(colorTheme, len(messageList))
        else:
            messageList[0].drawMove(colorTheme, 1)

    # Update display
    pygame.display.update()


def checkCollision(blob, food, offset):
    # the food radius + the distance from food to blob <= the radius of blob then return true
    foodRadius = food.radius
    blobRadius = blob.radius
    # diff foodx and blobx squared + diff foody and bloby squared = distance squared
    # find distance

    diffX = food.x - blob.x
    diffY = food.y - blob.y

    distance = math.sqrt(diffX ** 2 + diffY ** 2)
    return distance + offset <= blobRadius


running = True
leaderboard(userList)
while running:
    time.sleep(0.03)
    # dayli lyfe ov blob
    if state == 4:
        # increase difficulty
        if (difficulty - 0.5) * 200 + 50 < round(time.time() - startTime + enemyKills):
            difficulty += 0.25
            message("You leveled up!")
            message("Enemies are stronger now")
        blob.tick(dev, godPower)
        if not blob.isAlive:
            totalScore = round(time.time() - startTime + enemyKills)
            makeFood(int(totalScore / 3), blob.x, blob.y, colorTheme)
            clearMessage()
            if blob.lastEnemy == ["Hunger", "Starvation"]:
                message("You died of " + random.choice(blob.lastEnemy))
            else:
                message(
                    "You got "
                    + random.choice(deathList)
                    + " by a "
                    + random.choice(blob.lastEnemy)
                )
            message("Your score was " + str(totalScore))
            if currentUser is None:
                message("Login to save your progress!")
            else:
                currentUser.scoreList.append(totalScore)
                saveData(userList)
                if len(currentUser.scoreList) == 1:
                    message("First time playing, right?")
                    message("Pretty good, for a newbie")
                elif max(currentUser.scoreList) == totalScore:
                    message("You beat your highscore!")
                    message(random.choice(encourageList[4]))
                elif max(currentUser.scoreList) - totalScore < totalScore - sum(
                    currentUser.scoreList
                ) / len(currentUser.scoreList):
                    chance = random.randint(1, 2)
                    if chance == 1:
                        numberMessage = (
                            str(round((totalScore / max(currentUser.scoreList)) * 100))
                            + "% of your"
                        )
                    if chance == 2:
                        numberMessage = (
                            str(round((max(currentUser.scoreList) - totalScore)))
                            + " points away from your"
                        )
                    message("That's about " + numberMessage + " highscore!")
                    message(random.choice(encourageList[3]))
                elif totalScore > sum(currentUser.scoreList) / len(
                    currentUser.scoreList
                ):
                    chance = random.randint(1, 2)
                    if chance == 1:
                        numberMessage = (
                            str(
                                round(
                                    (
                                        sum(currentUser.scoreList)
                                        / len(currentUser.scoreList)
                                        / totalScore
                                    )
                                )
                                * 100
                                - 100
                            )
                            + "% "
                        )
                    elif chance == 2:
                        numberMessage = (
                            str(
                                round(
                                    (
                                        totalScore
                                        - sum(currentUser.scoreList)
                                        / len(currentUser.scoreList)
                                    )
                                )
                            )
                            + " points "
                        )
                    message("That's about " + numberMessage + " above average")
                    message(random.choice(encourageList[2]))
                elif totalScore < sum(currentUser.scoreList) / len(
                    currentUser.scoreList
                ):
                    # TODO: finish below average feedback
                    message(random.choice(encourageList[1]))
            state = 5

    # Check for godPowerMODE
    if dev or godPower:
        currentPower = font.render("GODMODE", False, colorTheme)
    elif speedPower:
        currentPower = font.render("FASTMODE", False, colorTheme)
    elif immunityPower:
        currentPower = font.render("NOKILL", False, colorTheme)
    elif reloadPower:
        currentPower = font.render("SPAMMODE", False, colorTheme)
    elif damagePower:
        currentPower = font.render("HIDAMAGE", False, colorTheme)
    else:
        currentPower = font.render("", False, colorTheme)

    # Count score and make enemyTuhrak

    if state == 4:
        score = font.render(
            str(round(time.time() - startTime + enemyKills)), False, (255, 255, 255)
        )
    elif state == 5:
        # If blawb is ded then wuhrul or Shuftter eminei tuhrak big 'E' emninte
        for enemy in enemyTrack:
            if random.randint(0, 100) == 1:
                enemyTrack[enemy] = enemyList[random.randint(0, len(enemyList) - 1)]
                while not isinstance(enemyTrack[enemy], Enemy):
                    enemyTrack[enemy] = enemyList[random.randint(0, len(enemyList) - 1)]

    # Draw bullet type and ammo
    if state == 4:
        if currentBullet == 0:
            bulletName = font.render("Shooter", False, (255, 255, 255))
            shellCost = 3
            ammoText = font.render(
                (str(round(ammo / shellCost)) + " balls"), False, (255, 255, 255)
            )
        elif currentBullet == 1:
            bulletName = font.render("Sprayer", False, (255, 255, 255))
            shellCost = 1
            ammoText = font.render(
                (str(round(ammo / shellCost)) + " minies"), False, (255, 255, 255)
            )
        elif currentBullet == 2:
            bulletName = font.render("Sniper", False, (255, 255, 255))
            shellCost = 5
            ammoText = font.render(
                (str(round(ammo / shellCost)) + " snipsters"), False, (255, 255, 255)
            )
        elif currentBullet == 3:
            bulletName = font.render("Grenader", False, (255, 255, 255))
            shellCost = 8
            ammoText = font.render(
                (str(round(ammo / shellCost)) + " grenades"), False, (255, 255, 255)
            )
        elif currentBullet == 4:
            bulletName = font.render("Rocketier", False, (255, 255, 255))
            shellCost = 15
            ammoText = font.render(
                (str(round(ammo / shellCost)) + " rockets"), False, (255, 255, 255)
            )

    # Drawing everything
    drawEverything()

    # Moving blob
    blob.move(effectList)

    # CHECKING STUFF N' THINGS

    # Checki5ng if food is inside endimie, if it is then DELETE food
    # Chickeng if blob is inside endiminey, if it is then OUCH the blob
    # Checking if enemy touching bullet, if so then OUCH the enemy
    # Chcking if health too big
    for enemy in enemyList:
        if isinstance(enemy, Whirlpool):
            enemy.pull(foodList, blob)
        elif isinstance(enemy, Shooter):
            enemy.shoot(screen, enemyBulletList)
        for blobFood in foodList:
            if checkCollision(enemy, blobFood, 5) and not isinstance(enemy, FastEnemy):
                foodList.remove(blobFood)
                enemy.value += 1
                enemy.health += 3
        if (
            checkCollision(enemy, blob, -50)
            and not dev
            and not godPower
            and not immunityPower
        ):
            blob.takeDamage(enemy.damage, enemy)
        for bullet in bulletList:
            if checkCollision(enemy, bullet, -bullet.radius):
                enemy.takeDamage(
                    bullet.damage * 3
                    if damagePower or dev or godPower
                    else bullet.damage,
                    bullet,
                )
                if bullet.canDestroy == 1:
                    if not isinstance(enemy, FastEnemy):
                        bulletList.remove(bullet)
                else:
                    bullet.xSpeed = 0
                    bullet.ySpeed = 0
        if enemy.health > enemy.maxHealth:
            enemy.health = enemy.maxHealth

    # Cheking if blawb is tuching enemy bullet
    for bullet in enemyBulletList:
        if (
            checkCollision(bullet, blob, -50)
            and not dev
            and not godPower
            and not immunityPower
        ):
            blob.takeDamage(0 if dev else 10, bullet)
            enemyBulletList.remove(bullet)

    # Chiccking if pollutwe(bullet) is out of bounds if so then DELETE
    for bullet in bulletList:
        if (
            bullet.x > screen.get_width()
            or bullet.x < 0
            or bullet.y > screen.get_height()
            or bullet.y < 0
        ):
            bulletList.remove(bullet)
        # Making explosions dissapear
        if bullet.radius > 150:
            bullet.transparency -= 20
        if bullet.transparency <= 0:
            bulletList.remove(bullet)
    # Cheking if enmine bollaut is out of bounds
    for bullet in enemyBulletList:
        if (
            bullet.x > screen.get_width()
            or bullet.x < 0
            or bullet.y > screen.get_height()
            or bullet.y < 0
            or (bullet.xSpeed == 0 and bullet.ySpeed == 0)
        ):
            enemyBulletList.remove(bullet)

    # Checking if blob can be fast with fastPOwer
    if speedPower or godPower or dev:
        blob.speed = 0.05
    else:
        blob.speed = 0.01

    # Chaekcing if food is inside blob, or attracted to blob (who is a very pretty "person")
    if state == 4:
        for blobFood in foodList:
            if checkCollision(blob, blobFood, -80):
                blobFood.goToBlob(blob.x, blob.y)
            if checkCollision(blob, blobFood, 10):
                foodList.remove(blobFood)
                blob.eat()
                blob.brightness += 6
                ammo += 1
        # Chekfsaasfking if powerUP is insssideed of ZE Blawb
        for power in powerUpList:
            if (
                checkCollision(blob, power, -10)
                and time.time() - powerUpStart < powerUpDuration
            ):
                blob.shake += 30
                powerUpList.remove(power)
                percent = random.randint(1, 100)
                # Percent of power
                if power.type == "speed":
                    speedPower = True
                elif power.type == "nokill":
                    immunityPower = True
                elif power.type == "spam":
                    reloadPower = True
                elif power.type == "god":
                    godPower = True
                elif power.type == "damage":
                    damagePower = True
                powerUpStart = time.time()

    # Move emenie and check for delete if no health, creating food
    if state == 4 or state == 5:
        for enemy in enemyList:
            if (
                isinstance(enemy, Whirlpool)
                or isinstance(enemy, Shooter)
                or isinstance(enemy, FastEnemy)
            ) and not blob.isAlive:
                if enemy not in enemyTrack:
                    enemyTrack[enemy] = enemyList[random.randint(0, len(enemyList) - 1)]
                    while not isinstance(enemyTrack[enemy], Enemy):
                        enemyTrack[enemy] = enemyList[
                            random.randint(0, len(enemyList) - 1)
                        ]
                enemy.move(enemyTrack[enemy].x, enemyTrack[enemy].y)
            else:
                enemy.move(blob.x, blob.y)
            # Chek Helath
            if enemy.health <= 0:
                enemy.targetRadius = 1
            if enemy.health <= 0 and enemy.radius == 1:
                makeFood(enemy.value, enemy.x, enemy.y, True, enemy.color)
                enemyList.remove(enemy)
                enemyKills += enemy.points
                if state == 4:
                    message(
                        "You "
                        + random.choice(deathList)
                        + " a "
                        + random.choice(enemy.nameList)
                    )

        # Move Food and checking if out of bounds
        for food in foodList:
            food.move()

        # Move effects
        for effect in effectList:
            effect.move()
            if effect.radius == 0:
                effectList.remove(effect)

        # Move pollat(bullet)
        for bullet in bulletList:
            bullet.move(effectList)
        for bullet in enemyBulletList:
            bullet.move(effectList)

        # Making new food and enemy
        if time.time() - lastFoodSpawn > foodSpawnDelay:
            makeFood(1)
            foodSpawnDelay = random.uniform(0.5, 1)
            lastFoodSpawn = time.time()
        if time.time() - lastEnemySpawn > enemySpawnDelay:
            makeEnemy(1, difficulty)
            enemySpawnDelay = random.uniform(3, 8)
            lastEnemySpawn = time.time()
        if time.time() - lastPowerSpawn > powerSpawnDelay:
            makePower(1)
            powerSpawnDelay = random.uniform(10, 20)
            lastPowerSpawn = time.time()
        if time.time() - powerUpStart > powerUpDuration:
            godPower = False
            speedPower = False
            immunityPower = False
            reloadPower = False
            damagePower = False
            powerUpStart = time.time()

    # TRansition
    if transition[0] > 0 and transition[0] < 10:
        for button in stateButtonDict[state]:
            button.transition(0.1)
        transition[0] += 1
        if transition[0] == 10:
            for button in stateButtonDict[state]:
                button.drawRect = button.rect.copy()
            for box in stateTextBoxDict[state]:
                box.drawRect = box.rect.copy()
            state = transition[1]
            # Reset Game
            if state == 4:
                reset()
            # Reset Text in text boxes
            if state in [6, 7, 8]:
                for box in stateTextBoxDict[state]:
                    box.text = ""
            for button in stateButtonDict[state]:
                button.drawRect.x += button.transitionDistance
    if transition[0] > 9:
        transition[0] += 1
        for button in stateButtonDict[state]:
            button.transition(-0.1)
        if transition[0] == 20:
            transition = [0, 0]

    # X'ing out of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        # Checking for key or moose pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
            if state == 4:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    currentBullet = (currentBullet + 1) % len(bulletTypes)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    currentBullet = (
                        (currentBullet - 1)
                        if currentBullet > 0
                        else currentBullet + len(bulletTypes) - 1
                    )
                if event.key == pygame.K_o:
                    dev = not dev
            for box in stateTextBoxDict[state]:
                if box.focus:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_TAB:
                        box.focus = False
                        # Goes to next box in list
                        if state == 6:
                            if box.noText == "USERNAME":
                                stateTextBoxDict[state][1].focus = True
                        if state == 7:
                            if box.noText == "USERNAME":
                                stateTextBoxDict[state][1].focus = True
                    elif event.key == pygame.K_BACKSPACE:
                        box.text = box.text[:-1]
                    elif len(box.text) <= 15:
                        box.text += event.unicode
                    break

        # Checking if mouse pressed and released in restart buhtttonh
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in stateButtonDict[state]:
                if button.clickedDown(event):
                    break
            for box in stateTextBoxDict[state]:
                if box.clickedDown(event):
                    break
            if state == 7 or state == 8:
                if colorPaletteRect.collidepoint(pygame.mouse.get_pos()):
                    chosenColor = screen.get_at(pygame.mouse.get_pos())
                    chosenColor = tuple(chosenColor)
        if event.type == pygame.MOUSEBUTTONUP and transition[0] < 1:
            for box in stateTextBoxDict[state]:
                focused = box.clickedUp(event)
                if focused is not None:
                    box.blinkerCount = 0
            for button in stateButtonDict[state]:
                pressed = button.clickedUp(event)
                if pressed is not None:
                    # What to do if buttons pressed
                    if state == 0:
                        if pressed == "START":
                            message("The game has started")
                            transition = [1, 4]
                        if pressed == "INSTRUCTIONS":
                            transition = [1, 1]
                        if pressed == "LEADERBOARDS":
                            leaderboard = leaderboard(userList)
                            transition = [1, 2]
                        if pressed == "LOGIN":
                            transition = [1, 6]
                        if pressed == "CREATE ACCOUNT":
                            transition = [1, 7]
                        break
                    if state in [1, 2, 5, 6, 7, 8] and pressed == "HOME":
                        chosenColor = None
                        if currentUser is None:
                            transition = [1, 0]
                        else:
                            transition = [1, 3]
                        break

                    if state == 3:
                        if pressed == "START":
                            transition = [1, 4]
                        if pressed == "INSTRUCTIONS":
                            transition = [1, 1]
                        if pressed == "LEADERBOARDS":
                            leaderboard = leaderboard(userList)
                            transition = [1, 2]
                        if pressed == "LOGOUT":
                            currentUser = None
                            colorTheme = (115, 225, 255)
                            userText = smallFont.render(
                                "NOT LOGGED IN", False, (50, 50, 50)
                            )
                            transition = [1, 0]
                        if pressed == "SETTINGS":
                            transition = [1, 8]
                        break
                    if state == 5:
                        if pressed == "LEADERBOARDS":
                            leaderboard = leaderboard(userList)
                            transition = [1, 2]
                        break
                    if state == 6:
                        if pressed == "LOGIN":
                            name = stateTextBoxDict[6][0].text
                            password = stateTextBoxDict[6][1].text
                            currentUser = login(name, password)
                            if currentUser is None:
                                message(
                                    "Wrong Username/Password Combination",
                                    tempType="error",
                                )
                            else:
                                transition = [1, 3]
                                colorTheme = currentUser.color
                                userText = smallFont.render(
                                    currentUser.name, False, colorTheme
                                )
                                message(random.choice(greetingList) + currentUser.name)
                        break
                    if state == 7:
                        if pressed == "CREATE":
                            # create account
                            name = stateTextBoxDict[7][0].text
                            password = stateTextBoxDict[7][1].text
                            currentUser = createAccount(name, password)
                            if currentUser is None:
                                if name == "" and password == "":
                                    message(
                                        "You didn't enter a username or password",
                                        tempType="error",
                                    )
                                elif name == "":
                                    message(
                                        "You didn't enter a username", tempType="error"
                                    )
                                elif password == "":
                                    message(
                                        "You didn't enter a password", tempType="error"
                                    )
                                elif chosenColor == None:
                                    message(
                                        "You didn't select a color", tempType="error"
                                    )
                                    message("Click the color palette to choose it")
                                else:
                                    message("Username Already Exists", tempType="error")
                            else:
                                message("Account Successfully Created!")
                                transition = [1, 3]
                                colorTheme = currentUser.color
                                userText = smallFont.render(
                                    currentUser.name, False, colorTheme
                                )
                        break
                    if state == 8:
                        if pressed == "SAVE":
                            name = stateTextBoxDict[8][0].text
                            password = stateTextBoxDict[8][1].text
                            tempUser = editAccount(name, password, currentUser)
                            if tempUser is None:
                                message("Username Already Exists", tempType="error")
                            else:
                                currentUser = tempUser
                                transition = [1, 3]
                                colorTheme = currentUser.color
                                userText = smallFont.render(
                                    currentUser.name, False, colorTheme
                                )

                        if pressed == "DELETE":
                            userList.remove(currentUser)
                            saveData(userList)
                            currentUser = None
                            transition = [1, 0]
                            colorTheme = (115, 225, 255)
                            userText = smallFont.render(
                                "NOT LOGGED IN", False, (50, 50, 50)
                            )
                        break

    # shoot pollats
    keys = pygame.key.get_pressed()
    # See if time is gud
    currentTime = time.time()
    if (
        keys[pygame.K_SPACE]
        and state == 4
        and (
            currentTime - lastHit > bulletTypes[currentBullet].reload
            or dev
            or godPower
            or reloadPower
        )
    ):
        lastHit = currentTime
        if currentBullet == 0 and (ammo >= 3 or godPower or dev or reloadPower):
            bulletList.append(Bullet(screen, blob))
            if not (godPower or dev or reloadPower):
                ammo -= shellCost
        elif currentBullet == 1 and (ammo >= 1 or godPower or dev or reloadPower):
            bulletList.append(Spammer(screen, blob))
            if not (godPower or dev or reloadPower):
                ammo -= shellCost
        elif currentBullet == 2 and (ammo >= 5 or godPower or dev or reloadPower):
            bulletList.append(Sniper(screen, blob))
            if not (godPower or dev or reloadPower):
                ammo -= shellCost
        elif currentBullet == 3 and (ammo >= 8 or godPower or dev or reloadPower):
            bulletList.append(Grenade(screen, blob))
            if not (godPower or dev or reloadPower):
                ammo -= shellCost
        elif currentBullet == 4 and (ammo >= 10 or godPower or dev or reloadPower):
            bulletList.append(RocketLauncher(screen, blob))
            if not (godPower or dev or reloadPower):
                ammo -= shellCost
