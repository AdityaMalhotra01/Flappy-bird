import pygame
import random 
import sys
from pygame.locals import *

FPS = 35
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = int(SCREENHEIGHT*0.8)
GAME_SPRITES = {}
GAME_SOUNDS={}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND =  'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
BASE = 'gallery/sprites/base.png'
FPSCLOCK = pygame.time.Clock()   

def welcomescreen():
    """
    this id for welcome screen
    """
    playerx = int(SCREENWIDTH/3)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'][0].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.25)
    basex = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['message'][0],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['message'][1],(messagex,messagey+200))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def maingame():
    score = 0
    playerx = int(SCREENWIDTH/3)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    newpipe1 = getrandompipe()
    newpipe2 = getrandompipe()

    upperpipes = [
        {'x':SCREENWIDTH+200,'y':newpipe1[0]['y']},
        {'x':SCREENWIDTH+200+int(SCREENWIDTH/2),'y':newpipe1[0]['y']}
    ]

    lowerpipes = [
        {'x':SCREENWIDTH+200,'y':newpipe1[1]['y']},
        {'x':SCREENWIDTH+200+int(SCREENWIDTH/2),'y':newpipe1[1]['y']}
    ]
    pipevelx = -4
    playervely = -9
    playermaxvely = 10
    playerminvely = -8
    playeraccy = 1

    playerflapaccv = -8
    playerflaped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery >0:
                    playervely = playerflapaccv
                    playerflaped = True
                    GAME_SOUNDS['wing'].play()

        crashtest = iscollide(playerx,playery,upperpipes,lowerpipes)

        if crashtest:
            return
        
        playermidpos = playerx + GAME_SPRITES['player'].get_width()/2 
        for pipe in upperpipes:
            pipemidpos = pipe['x']+GAME_SPRITES['pipe'][0].get_width()/2
            if pipemidpos<=playermidpos<pipemidpos+4:
                score += 1
                print(f'your score is {score}')
                GAME_SOUNDS['point'].play()

        if playervely < playermaxvely and not playerflaped:
            playervely+=playeraccy
        if playerflaped:
            playerflaped = False
        playerheight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playervely,GROUNDY - playery - playerheight)     

        for upperpipe, lowerpipe in zip(upperpipes,lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        if 0 <upperpipes[0]['x']<5:
            newpipe = getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])


        if upperpipes[0]['x'] < - GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        for upper, lower in zip(upperpipes,lowerpipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upper['x'],upper['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lower['x'],lower['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        mydigit = [int(x) for x in list(str(score))]
        WidthOfAllNumbers = 0
        for digit in mydigit:
            WidthOfAllNumbers += GAME_SPRITES['numbers'][0].get_width()
        xoffset = int((SCREENWIDTH-WidthOfAllNumbers)/2)
        for digit in mydigit:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,SCREENHEIGHT*0.12))
            xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def iscollide(playerx,playery,upperpipes,lowerpipes):
    playery = playery - int(GAME_SPRITES['player'].get_height()/2)
    playerx = playerx - int(GAME_SPRITES['player'].get_width()/2)
    if playery > GROUNDY - 38  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperpipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False
    
def getrandompipe():
    pipeheight = GAME_SPRITES['pipe'][0].get_height()
    offset = int(SCREENHEIGHT/3)
    randnum = random.randint(0,offset)
    y1 = -pipeheight+randnum
    y2 = y1 + pipeheight+offset
    x = SCREENWIDTH +10
    pipe = [
        {'x': x , 'y':y1},
        {'x': x , 'y':y2},
    ]
    return pipe




if __name__ == '__main__':
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
pygame.image.load('gallery/sprites/0.png'),
pygame.image.load('gallery/sprites/1.png'),
pygame.image.load('gallery/sprites/2.png'),     
pygame.image.load('gallery/sprites/3.png'),
pygame.image.load('gallery/sprites/4.png'),
pygame.image.load('gallery/sprites/5.png'),
pygame.image.load('gallery/sprites/6.png'),
pygame.image.load('gallery/sprites/7.png'),
pygame.image.load('gallery/sprites/8.png'),
pygame.image.load('gallery/sprites/9.png')
    )

GAME_SPRITES['message'] = [pygame.image.load('gallery/sprites/message1.png'),
                            pygame.image.load('gallery/sprites/message2.png')]

GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png')
GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load(PIPE),180), 
                        pygame.image.load(PIPE)
                        )

GAME_SOUNDS['die']=pygame.mixer.Sound('gallery/audio/die.wav')
GAME_SOUNDS['hit']=pygame.mixer.Sound('gallery/audio/hit.wav')
GAME_SOUNDS['point']=pygame.mixer.Sound('gallery/audio/point.wav')
GAME_SOUNDS['swoosh']=pygame.mixer.Sound('gallery/audio/swoosh.wav')
GAME_SOUNDS['wing']=pygame.mixer.Sound('gallery/audio/wing.wav')

GAME_SPRITES['background'] = pygame.image.load(BACKGROUND)
GAME_SPRITES['player'] = pygame.image.load(PLAYER)

while True:
    welcomescreen()
    maingame()