# TODO: SPLIT ASSIST LIST BETWEEN ACTIVE AND INACTIVE

import pgzrun
import random
import pygame
import math

WIDTH = 2560
HEIGHT = 1440


ship = Actor('playership1_blue')
ship.x = 370
ship.y = 550
shipDefense = None

ufo = Actor('ufoblue')

laserList = []
laserSpeed = 10

laserListFoe = []
laserSpeedFoe = -10

assistList = []
assistListSpeed = -5
assistTime = 600

deathTimer = 5

orbitSpeed = 3

foeList = []
foeSpeed = 3.5

life = 999
score = 0
game_over = False
started = False


def on_mouse_down():
    print("Mouse button clicked")
    laser = Actor("laserblue15")
    laser.angle += 90
    laser.x = ship.x
    laser.y = ship.y
    laser.dead = 0
    laserList.append(laser)

def update():




    global score, game_over, life, started, testangle

    #if not started:


    if life <= 0:
        game_over = True
    if not game_over:
        checkForDebug()

        if keyboard.left or keyboard.a:
            ship.x = ship.x - 6
            if ship.x < 50:
                ship.x = 50
        if keyboard.right or keyboard.d:
            ship.x = ship.x + 6
            if ship.x > WIDTH - 50:
                ship.x = WIDTH - 50
        if keyboard.up or keyboard.w:
            ship.y = ship.y - 6
            if ship.y < 150:
                ship.y = 150
        if keyboard.down or keyboard.s:
            ship.y = ship.y + 6
            if ship.y > HEIGHT - 50:
                ship.y = HEIGHT - 50

        if random.randint(1, 700) == 1:
            spawnAssist()
        if random.randint(1, 40) == 1:
            spawnFoe()


        for foe in foeList:
            if foe.dead > deathTimer:
                foeList.remove(foe)
            elif foe.dead > 0:
                foe.dead += 1
            else:
                if random.randint(1, 100) == 1:
                    laser = Actor("laserred01")
                    laser.angle += 90
                    laser.x = foe.x
                    laser.y = foe.y
                    laser.dead = 0
                    laserListFoe.append(laser)
                foe.x = foe.x + (foe.direction * foeSpeed)
                if foe.x <= 20:
                    foe.direction = 1
                elif foe.x >= 2530:
                    foe.direction = -1

                if random.randint(1, 100) == 1:
                    laser = Actor("laserred01")
                    laser.angle += 90
                    laser.x = foe.x
                    laser.y = foe.y
                    laser.dead = 0
                    laserListFoe.append(laser)
                foe.x = foe.x + (foe.direction * foeSpeed)
                if foe.x <= 20:
                    foe.direction = 1
                elif foe.x >= 2530:
                    foe.direction = -1

        for assist in assistList:
            if assist.active == False:
                assist.y -= assistListSpeed
                if assist.y >= 1500:
                    assistList.remove(assist)
                elif assist.colliderect(ship):
                    assist.active = True
                    assist.angle = 0
                    assist.image = "ufoblue"
            elif assist.time >= assistTime:
                assistList.remove(assist)
            else:
                assist.time += 1
                assist.angle += 3
                placeSpriteAtAngle(ship, assist, assist.angle, 90)

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
                if laser.y >= 1500:
                    laserListFoe.remove(laser)
                for assist in assistList:
                    if laser.colliderect(assist) and assist.active == True:
                        laser.dead = 1
                        laser.image = "laserred08"

                if laser.colliderect(ship):
                    laser.dead = 1
                    life = life - 1
                    laser.image = "laserred08"

    print('x:' + str(ship.x) + ', y:' + str(ship.y))

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
        for assist in assistList:
            assist.draw()
        screen.draw.text('Score: ' + str(score), (15,10), color=(255,255,255), fontsize=30)
        screen.draw.text('Health: ' + str(life), (15,30), color=(255,255,255), fontsize=30)

def spawnAssist():
    assist = Actor('powerupblue_bolt')
    assist.x = random.randint(20, 2530)
    assist.y = 35
    if assist.y > 1500:
        assistList.remove(assist)
    assist.time = 0
    assist.active = False
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

def placeSpriteAtAngle(sourceSprite, targetSprite, angle, distance):
    sin = math.sin(math.radians(angle))
    cos = math.cos(math.radians(angle))
    a = distance * sin
    b = distance * cos
    newX = sourceSprite.x + b
    newY = sourceSprite.y + a
    targetSprite.x = newX
    targetSprite.y = newY

def checkForDebug():
    if keyboard.p:
        spawnAssist()


pgzrun.go() # Must be last line
