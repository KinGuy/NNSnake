# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 11:25:05 2019

@author: kinar
"""

# !pip install pygame

# imports
import pygame
import random
import time
# import numpy as np

# screen and block size
PIXEL_SIZE = 30
SCREEN_DIM = 20
SCREEN_SIZE = SCREEN_DIM*PIXEL_SIZE

# colors
R = (255,0,0)
G = (0,255,0)
W = (255,255,255)

class Snake:
    def __init__(self):
        self.history = [[SCREEN_SIZE/2-(SCREEN_SIZE/2)%PIXEL_SIZE, SCREEN_SIZE/2-(SCREEN_SIZE/2)%PIXEL_SIZE],
                 [SCREEN_SIZE/2-(SCREEN_SIZE/2)%PIXEL_SIZE, SCREEN_SIZE/2-(SCREEN_SIZE/2)%PIXEL_SIZE+PIXEL_SIZE],
                 [SCREEN_SIZE/2-(SCREEN_SIZE/2)%PIXEL_SIZE, SCREEN_SIZE/2-(SCREEN_SIZE/2)%PIXEL_SIZE+2*PIXEL_SIZE]
                ]
        self.direction = 0
        pass
    
    # snake movement: 0=up, 1=right, 2=down, 3=left
    def snakeMove(self):
        for i in range(len(self.history)-1,0,-1):
            self.history[i] = self.history[i-1][:]
        if self.direction == 0:
            self.history[0][1] = self.history[0][1] - PIXEL_SIZE
        elif self.direction == 1:
            self.history[0][0] = self.history[0][0] + PIXEL_SIZE
        elif self.direction == 2:
            self.history[0][1] = self.history[0][1] + PIXEL_SIZE
        elif self.direction == 3:
            self.history[0][0] = self.history[0][0] - PIXEL_SIZE
    
    # snake turn (left or right only)
    def snakeTurn(self):
        # get left or right key and turn the snake direction
        if pygame.key.get_pressed()[pygame.K_RIGHT]: 
            self.direction = (self.direction+1)%4
        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            self.direction = (self.direction-1)%4
            
    # grow the snake
    def grow(self):
        self.history.append(self.history[-1][:])
        pass
    
        

    # snake turn (all 4 directions)
#    def snakeTurn(self, keys):
        # get arrow key and move the snake to this direction
        # don't accept turn into itself
#        if (keys[pygame.K_UP]):
#            if self.direction != 2: self.direction = 0
#        if (keys[pygame.K_RIGHT]):
#            if self.direction != 3: self.direction = 1
#        if (keys[pygame.K_DOWN]):
#            if self.direction != 0: self.direction = 2
#        if (keys[pygame.K_LEFT]):
#            if self.direction != 1: self.direction = 3

class Apple:
    def __init__(self):
        # generate in random location
        self.appleRegenerate()
        pass
    
    def appleRegenerate(self):
        # regenerate in random location
        self.pos = [random.randrange(0, SCREEN_DIM)*PIXEL_SIZE, 
                    random.randrange(0, SCREEN_DIM)*PIXEL_SIZE]

class App:
    
    ALIVE = True
    SCORE = 0
    EAT_APPLE = 10
    
    def __init__(self):
        # start display with global params
        pygame.init()
        self.snakeDisplay = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
        pygame.display.set_caption('test')
        
        # TODO: move on top of all windows
        
        # generate snake and apple
        self.snake = Snake()
        self.apple = Apple()
        # don't regenerate on the snake itself
        while self.appleOnSnake(self.apple, self.snake):
            self.apple.appleRegenerate()
        
        # start main game loop
        self.mainLoop()
    
    # TODO: reset the game - don't close the window
    def reset(self):
        pass
    
    # draw a snake on the display
    def drawSnake(self, snake, surface):
        for i, tile in enumerate(snake.history):
            pygame.draw.rect(surface,
                 (50+((len(snake.history)-i)/(len(snake.history)))*(255-50),
                  50+((len(snake.history)-i)/(len(snake.history)))*(255-50),
                  50+((len(snake.history)-i)/(len(snake.history)))*(255-50)),
                 ((tile), (PIXEL_SIZE, PIXEL_SIZE))
                 )
    
    # draw the apple on the display
    def drawApple(self, apple, surface):
        pygame.draw.rect(surface,
             (0,255,0),
             ((self.apple.pos), (PIXEL_SIZE, PIXEL_SIZE))
             )
    
    # apple on snake
    def appleOnSnake(self, apple, snake):
        return apple.pos in snake.history
    
    # snake collisions and out of bounds
    def collision(self):
        # out of bounds - kill
        if  self.snake.history[0][0] < 0 or \
            self.snake.history[0][1] < 0 or \
            self.snake.history[0][0]+PIXEL_SIZE > SCREEN_SIZE or \
            self.snake.history[0][1]+PIXEL_SIZE > SCREEN_SIZE:
                self.ALIVE = False
                print('out of bounds!')
        
        # hit myself - kill
        if self.snake.history[0] in self.snake.history[1:]:
            self.ALIVE = False
            print('you hit yourself and died!')
            
        # eat apple - grow
        if self.snake.history[0] == self.apple.pos:
            self.snake.grow()
            self.SCORE = self.SCORE + int(self.EAT_APPLE * len(self.snake.history) * 0.5)
            self.apple.appleRegenerate()
    
    # show the number of steps to the wall in the direction of the snake
    def wallAhead(self):
        if self.snake.direction == 0:
            return int(self.snake.history[0][1]/PIXEL_SIZE)
        elif self.snake.direction == 1:
            return int((SCREEN_SIZE-self.snake.history[0][0]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 2:
            return int((SCREEN_SIZE-self.snake.history[0][1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 3:
            return int(self.snake.history[0][0]/PIXEL_SIZE)
    # show the number of steps to the snake in the direction of the snake
    def snakeAhead(self):
        if self.snake.direction == 0:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][0] == tail[0] and \
                    self.snake.history[0][1] > tail[1]:
                        return int((self.snake.history[0][1]-tail[1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 1:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][1] == tail[1] and \
                    self.snake.history[0][0] < tail[0]:
                        return int((tail[0]-self.snake.history[0][0]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 2:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][0] == tail[0] and \
                    self.snake.history[0][1] < tail[1]:
                        return int((tail[1]-self.snake.history[0][1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 3:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][1] == tail[1] and \
                    self.snake.history[0][0] > tail[0]:
                        return int((self.snake.history[0][0]-tail[0]-PIXEL_SIZE)/PIXEL_SIZE)
    # show the number of steps to the wall on the right
    def wallRight(self):
        if self.snake.direction == 3:
            return int(self.snake.history[0][1]/PIXEL_SIZE)
        elif self.snake.direction == 0:
            return int((SCREEN_SIZE-self.snake.history[0][0]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 1:
            return int((SCREEN_SIZE-self.snake.history[0][1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 2:
            return int(self.snake.history[0][0]/PIXEL_SIZE)
    # show the number of steps to the snake on the right
    def snakeRight(self):
        if self.snake.direction == 3:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][0] == tail[0] and \
                    self.snake.history[0][1] > tail[1]:
                        return int((self.snake.history[0][1]-tail[1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 0:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][1] == tail[1] and \
                    self.snake.history[0][0] < tail[0]:
                        return int((tail[0]-self.snake.history[0][0]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 1:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][0] == tail[0] and \
                    self.snake.history[0][1] < tail[1]:
                        return int((tail[1]-self.snake.history[0][1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 2:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][1] == tail[1] and \
                    self.snake.history[0][0] > tail[0]:
                        return int((self.snake.history[0][0]-tail[0]-PIXEL_SIZE)/PIXEL_SIZE)
    # show the number of steps to the wall on the left
    def wallLeft(self):
        if self.snake.direction == 1:
            return int(self.snake.history[0][1]/PIXEL_SIZE)
        elif self.snake.direction == 2:
            return int((SCREEN_SIZE-self.snake.history[0][0]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 3:
            return int((SCREEN_SIZE-self.snake.history[0][1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 0:
            return int(self.snake.history[0][0]/PIXEL_SIZE)
    # show the number of steps to the snake on the left
    def snakeLeft(self):
        if self.snake.direction == 1:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][0] == tail[0] and \
                    self.snake.history[0][1] > tail[1]:
                        return int((self.snake.history[0][1]-tail[1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 2:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][1] == tail[1] and \
                    self.snake.history[0][0] < tail[0]:
                        return int((tail[0]-self.snake.history[0][0]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 3:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][0] == tail[0] and \
                    self.snake.history[0][1] < tail[1]:
                        return int((tail[1]-self.snake.history[0][1]-PIXEL_SIZE)/PIXEL_SIZE)
        elif self.snake.direction == 0:
            for tail in self.snake.history[1:]:
                if self.snake.history[0][1] == tail[1] and \
                    self.snake.history[0][0] > tail[0]:
                        return int((self.snake.history[0][0]-tail[0]-PIXEL_SIZE)/PIXEL_SIZE)

    # TODO: distance to apple (2D)
    def disToAppleX(self):
        return int((self.apple.pos[0]-self.snake.history[0][0])/PIXEL_SIZE)
    def disToAppleY(self):
        return int((self.apple.pos[1]-self.snake.history[0][1])/PIXEL_SIZE)
    
    # loop until end of game
    def mainLoop(self):
        while self.ALIVE:
            time.sleep(150/1000)
            pygame.event.pump()
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.ALIVE = False
            self.snake.snakeTurn()
            self.snake.snakeMove()
            self.Score()
            self.collision()
            self.redraw()
#            print('up:', int(self.snake.history[0][1]/PIXEL_SIZE),'right:',int((SCREEN_SIZE-self.snake.history[0][0]-PIXEL_SIZE)/PIXEL_SIZE),'down',int((SCREEN_SIZE-self.snake.history[0][1]-PIXEL_SIZE)/PIXEL_SIZE),'left',int(self.snake.history[0][0]/PIXEL_SIZE))
            print('forword:',self.wallAhead(),self.snakeAhead(),'right:',self.wallRight(),self.snakeRight(),'left:',self.wallLeft(),self.snakeLeft(),'apple:',self.disToAppleX(),self.disToAppleY())
        # when dead
        self.stopApp()
        print('score:', self.SCORE)
                
    
    # TODO: keep score
    def Score(self):
        self.SCORE = self.SCORE + 1
        pygame.display.set_caption('snake score: '+str(self.SCORE))
        pass
    
    # refrash display
    def redraw(self):
        self.snakeDisplay.fill((0,0,0))
        self.drawApple(self.apple, self.snakeDisplay)
        self.drawSnake(self.snake, self.snakeDisplay)
        pygame.display.flip()
    
    # exit function
    def stopApp(self):
        pygame.quit()
    
    
