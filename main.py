import pygame
import matplotlib as mpl
import requests
import sys
import threading
import time
import math
import random

pygame.init()

from pygame.locals import *

# Initialize Screen
win = pygame.display.set_mode((1500, 1000),0,32)
pygame.display.set_caption("Music Maker")

# Putting in a background image
background = pygame.image.load("backgroundImage.jpg").convert()

# Importing Sounds
noteA = pygame.mixer.Sound('a.wav')
noteBFlat = pygame.mixer.Sound('b_flat.wav')
noteB = pygame.mixer.Sound('b.wav')
noteC = pygame.mixer.Sound('c.wav')
noteCSharp = pygame.mixer.Sound('c#.wav')
noteD = pygame.mixer.Sound('d.wav')
noteEFlat = pygame.mixer.Sound('e_flat.wav')
noteE = pygame.mixer.Sound('e.wav')
noteF = pygame.mixer.Sound('f.wav')
noteFSharp = pygame.mixer.Sound('f#.wav')
noteG = pygame.mixer.Sound('g.wav')
noteGSharp = pygame.mixer.Sound('g#.wav')

start = time.perf_counter()

buttonsToNotes = {0:noteGSharp, 1:noteA, 2:noteBFlat, 3:noteB, 4:noteC, 5:noteCSharp, 6:noteD, 7:noteEFlat, 8:noteE, 9:noteF, 10:noteFSharp, 11:noteG}

# Button Class
class button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

#Expanding circles class
class expandingCircle():
    def __init__(self, color, x,y,radius):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        self.radius += 5

# Goes through buttons, checks which ones are selected and plays the corresponding sounds
def playOnce():
    counter = 0
    vel = 130

    global x

    for button in buttons:
        #print("Counter Value " + str(counter) + " Selected Counter: " + str(selected[counter]))
        
        #pygame.draw.rect(win, (255, 0, 255), (x, 0, 20, 1000))

        if selected[counter] == True:
            print("Play Sound Note " + str(counter))
            #pygame.mixer.Channel(counter%12).play(buttonsToNotes[counter%12])
            
            #Chooses random RGB values to create a random color for the circle effect
            red = random.randint(1,255)
            green = random.randint(1,255)
            blue = random.randint(1,255)

            highlights.append(expandingCircle((red, green, blue),button.x+15, button.y+15, 40))
            buttonsToNotes[counter%12].play()

        if counter % 12 == 0 and counter != 0:
            pygame.time.delay(700)
            x += vel
            highlights.clear()
        counter += 1

    x = 95

# Function to clear grid of buttons when called
def clearGrid():
    counter = 0
    
    for button in selected:
        selected[counter] = False
        counter += 1

# Updates screen
def redrawWindow():
    global x
    
    for button in buttons:
        button.draw(win, (0, 0, 0))
    playButton.draw(win, (0, 0 ,0))
    clearButton.draw(win, (0, 0 ,0))
    #pygame.draw.rect(win, (255, 0, 255), (x, 0, 20, 1000))

    for c in highlights:
        c.draw(win)

run = True

x = 95

# Creation of grid of buttons
buttons = []
selected = []
for row in range (12):
    for collumn in range (12):
        buttons.append(button((0, 255, 0), 130*row+100, 130*collumn+120, 30, 30, "MM"))
        selected.append(False)

# Creation of play and clear buttons
playButton = button((0, 255, 0), 675, 50, 90, 40, "Play!")
clearButton = button((0, 255, 0), 795, 50, 90, 40, "Clear!")
pygame.mixer.set_num_channels(12)

particles = []
highlights = []

# Main Function
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        # Ablility to quit window
        if event.type == pygame.QUIT:
            run = False

        # Detect if mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:      
            counter = -1
            
            if playButton.isOver(pos):
                print("Clicked Play Button")
                threading.Thread(target=playOnce).start()

            if clearButton.isOver(pos):
                print("Clicked Clear Button")
                clearGrid()
            
            for button in buttons:
                counter += 1
                
                if button.isOver(pos):
                    print("Clicked Button")
                    if selected[counter] == False:
                        button.color = (255, 0, 0)
                        selected[counter] = True

                    else:
                        button.color = (0, 255, 0)
                        selected[counter] = False
        
        # Detect when curson makes a motion
        if event.type == pygame.MOUSEMOTION:           
            counter = -1
            for button in buttons:           
                counter += 1
                
                if playButton.isOver(pos):
                    playButton.color = (255, 0 , 0)
                
                else:
                    playButton.color = (0, 255, 0)

                if clearButton.isOver(pos):
                    clearButton.color = (255, 0 , 0)
                
                else:
                    clearButton.color = (0, 255, 0)

                if button.isOver(pos):
                    if selected[counter] == False:
                        button.color = (0, 255, 0)

                else:
                    if selected[counter] == False:
                        button.color = (0, 0, 255)


    win.blit(background, (0,0))
    redrawWindow()

    # Particle effect
    mx, my = pygame.mouse.get_pos()
    particles.append([[mx, my], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])
 
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[2] -= 0.1
        particle[1][1] += 0.1
        pygame.draw.circle(win, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)

    pygame.display.update()

finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} second(s)')

pygame.quit()