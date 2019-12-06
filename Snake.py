# Snake Game

## Imports
#!pip install pygame

from pygame.locals import *
from random import randint
import pygame
import time

## Class
class Player:
    x = []
    y = []
    step = 64
    direction = 0
    length = 3

    updateCountMax = 2
    updateCount = 0

    def __init__(self, length=3):
        self.length = length
        for i in range(0,length):
            self.x.append(i*self.step*-1)
            self.y.append(0)

    def longer(self):
        self.x.append(self.x[-1])
        self.y.append(self.y[-1])
        self.length = self.length + 1

    def update(self):
        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            # update previous positions
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update position of head of snake
            if self.direction == 0:
                self.x[0] = self.x[0] + self.step
            if self.direction == 1:
                self.x[0] = self.x[0] - self.step
            if self.direction == 2:
                self.y[0] = self.y[0] - self.step
            if self.direction == 3:
                self.y[0] = self.y[0] + self.step

            self.updateCount = 0


    def moveRight(self):
        self.direction = 0
    def moveLeft(self):
        self.direction = 1
    def moveUp(self):
        self.direction = 2
    def moveDown(self):
        self.direction = 3 

    def draw(self, surface, image):
        for i in range(0,self.length):
            surface.blit(image,(self.x[i],self.y[i])) 


class Apple:
    x = 0
    y = 0
    step = 64

    def __init__(self,x,y):
        self.x = x * self.step
        self.y = y * self.step

    def draw(self, surface, image):
        surface.blit(image,(self.x, self.y)) 


class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 < x2+bsize:
            if y1 >= y2 and y1 < y2+bsize:
                return True
        return False


class App:
    windowWidth = 64*10
    windowHeight = 64*10
    player = 0
    apple = 0

    def __init__(self):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._apple_surf = None
        self.game = Game()
        self.player = Player(3) 
        self.apple = Apple(5,5)

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), 
                                                     pygame.HWSURFACE)
        pygame.display.set_caption('mySnake')
        self._running = True
        self._image_surf = pygame.image.load("redSquare.png").convert()
        self._apple_surf = pygame.image.load("greenSquare.png").convert()

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        # does snake eat apple?
        for i in range(0,self.player.length):
            if self.game.isCollision(self.apple.x,self.apple.y,
                                     self.player.x[i], self.player.y[i],
                                     self.player.step):
                # new apple
                self.apple.x = randint(0,9) * 64
                self.apple.y = randint(0,9) * 64
                # increse length
                self.player.longer()

        # does snake collide with itself?
        for i in range(2,self.player.length):
            if self.game.isCollision(self.player.x[0],self.player.y[0],
                                     self.player.x[i], self.player.y[i],
                                     self.player.step):
                print("You lose! Collision: ")
                print("x[0] (" + str(self.player.x[0]) + "," + str(self.player.y[0]) + ")")
                print("x[" + str(i) + "] (" + str(self.player.x[i]) + "," + str(self.player.y[i]) + ")")
                
                self._running = False
                exit(0)
        
        # does snake out of view?
        if self.player.x[0] < 0 or self.player.y[0] < 0 or self.player.x[0] >= self.windowWidth or self.player.y[0] >= self.windowHeight:
                print("You lose! out of bounds")
                self._running = False
                exit(0)

        pass

    def on_render(self):
        self._display_surf.fill((0,0,0))
        self.player.draw(self._display_surf, self._image_surf)
        self.apple.draw(self._display_surf, self._apple_surf)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.event.pump()
            keys = pygame.key.get_pressed() 

            if (keys[K_RIGHT]):
                if self.player.direction != 1: self.player.moveRight()
            if (keys[K_LEFT]):
                if self.player.direction != 0: self.player.moveLeft()
            if (keys[K_UP]):
                if self.player.direction != 3: self.player.moveUp()
            if (keys[K_DOWN]):
                if self.player.direction != 2: self.player.moveDown()
            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()
            time.sleep(50.0 / 1000.0);
        self.on_cleanup()


## Run the app
theApp = App()
theApp.on_execute()
