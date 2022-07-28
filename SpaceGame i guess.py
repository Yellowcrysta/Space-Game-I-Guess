import pgzrun
import random

WIDTH = 800
HEIGHT = 600


ship = Actor('playership1_blue')
ship.x = 370
ship.y = 550

laserList = []
laserSpeed = 10

laserListFoe = []
laserSpeedFoe = -10

assistList = []
assistListSpeed = 5

deathTimer = 5

foeList = []
foeSpeed = 3.5

life = 10
score = 0
game_over = False
started = False

def on_mouse_move(pos):
    ship.x = pos[0]

def on_mouse_down():
    print("Mouse button clicked")
    laser = Actor("laserblue15")
    laser.angle += 90
    laser.x = ship.x
    laser.y = ship.y
    laser.dead = 0
    laserList.append(laser)

def update():

    global score, game_over, life, started
    #if not started:

    if life <= 0:
        game_over = True
    if not game_over:
        if keyboard.left:
            ship.x = ship.x - 5
        if keyboard.right:
            ship.x = ship.x + 5

        if random.randint(1, 40) == 1:
            spawnFoe()

        for foe in foeList:
            if foe.dead > deathTimer:
                foeList.remove(foe)
            elif foe.dead > 0:
                foe.dead += 1
            else:
                if random.randint(1, 100) == 1:
                    print("Shot Fired")
                    laser = Actor("laserred01")
                    laser.angle += 90
                    laser.x = foe.x
                    laser.y = foe.y
                    laser.dead = 0
                    laserListFoe.append(laser)
                foe.x = foe.x + (foe.direction * foeSpeed)
                if foe.x <= 20:
                    foe.direction = 1
                elif foe.x >= 780:
                    foe.direction = -1

        for laser in laserList:
            if laser.dead > deathTimer:
                laserList.remove(laser)
            elif laser.dead > 0:
                laser.dead += 1
            else:
                laser.y -= laserSpeed
                if laser.y <= -20:
                    laserList.remove(laser)
                for foe in foeList:
                    if laser.colliderect(foe):
                        laser.dead = 1
                        foe.dead = 1
                        laser.image = "laserblue08"
                        foe.image = "spinner_hit"
                        score += 1

        for laser in laserListFoe:
            if laser.dead > deathTimer:
                laserListFoe.remove(laser)
            elif laser.dead > 0:
                laser.dead += 1
            else:
                laser.y -= laserSpeedFoe
                if laser.y >= 650:
                    laserListFoe.remove(laser)
                if laser.colliderect(ship):
                    laser.dead = 1
                    life = life - 1
                    laser.image = "laserred08"

def draw():
    screen.fill((80,0,70))
    if game_over:
        screen.draw.text('Game Over', (360, 300), color=(255,255,255), fontsize=60)
        screen.draw.text('Score: ' + str(score), (360, 350), color=(255,255,255), fontsize=60)
    else:
        for laser in laserList:
            laser.draw()
        for laser in laserListFoe:
            laser.draw()
        ship.draw()
        for foe in foeList:
            foe.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=30)
        screen.draw.text('Health: ' + str(life), (15,30), color=(255,255,255), fontsize=30)

def spawnAssist():
    assist = Actor('powerupblue_bolt')
    assist.x = random.randint(20, 780)
    assist.y = 35
    assist.direction = random.randint(0, 1)
    if assist.direction == 0:
        assist.direction = -1
    assistList.append(assist)

def spawnFoe():
    foe = Actor('spinner')
    foe.x = random.randint(20, 780)
    foe.y = 35
    foe.direction = random.randint(0, 1)
    foe.dead = 0
    if foe.direction == 0:
        foe.direction = -1
    foeList.append(foe)


pgzrun.go() # Must be last line
