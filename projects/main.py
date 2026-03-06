import pygame
import json
import random

pygame.init()

#WIDTH, HEIGHT = 1000, 800
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
run = True
state = 'menu'

#word getting
def get_word():
    with open("words.json", "r") as f:
        words = json.load(f)
        word = random.choice(words)
        return word
        
    

#colours
gray = 	(21,45,50)
blue = 	(0,31,36)
light_green = (47,59,34)
dark_green = (5,45,10)
white = (255, 255, 255)
light_gray = (180, 180, 180)
lighter_gray = (210, 210, 210)
black = (0, 0, 0)

font = pygame.font.Font("FuzzyBubbles-Bold.ttf", 100)
font2 = pygame.font.Font("FuzzyBubbles-Bold.ttf", 75)
font3 = pygame.font.Font("FuzzyBubbles-Bold.ttf", 50)

#rects
daily_rect = pygame.rect.Rect(275, 200, 250, 100)
practice_rect = pygame.rect.Rect(200, 400, 300, 100)



rows = []
for j in range(6):
    row = {
        "cells": [],         
        "active": False
    }
    for i in range(5):
        rect = pygame.Rect(225 + i*70, 25 + j*80, 65, 65)
        cell = {"rect": rect, "colour": light_gray, "letter": ""}
        row["cells"].append(cell)
    rows.append(row)

rows[0]["active"] = True

def flash(row):
    for cell in row["cells"]:
        if cell["colour"] == light_gray:
            cell["colour"] = white
        else:
            cell["colour"] = light_gray

flash_event = pygame.USEREVENT
pygame.time.set_timer(flash_event, 500)

wordlock = False
guess = ""
guesses = []
active_changed = True

def check_word(word, guess):
    colours = []
    for letter in guess:
        if letter == word[guess.index(letter)]:
            colours.append("green")
        elif letter in word:
            colours.append("yellow")
            letters = list(word)
            letters[letters.index(letter)] = " "
            word = "".join(letters)
        else:
            colours.append("grey")
    return colours

word = get_word()

wincon = False
win = False

while run:
    for ev in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos()
        
        #events:
        if ev.type == pygame.QUIT:
            run = False
        #flashy flashy
        elif ev.type == flash_event:
            for i in range(6):
                if rows[i]["active"]:
                    flash(rows[i])
        #button press
        elif ev.type == pygame.MOUSEBUTTONDOWN:
            if daily_rect.collidepoint(mouse_pos):
                state = 'daily'
        #word input
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_BACKSPACE:
                guess = guess [:-1]
            elif ev.key == pygame.K_RETURN and len(guess) == 5:
                wordlock = True
            else:
                guess += ev.unicode
            if len(guess) > 5:
                guess = guess[:-1]
            guess = guess.upper()
    
    if state == 'menu':
        screen.fill(blue)
        screen.blit(font.render("Wordle", True, white), (225, 60))
        pygame.draw.rect(screen, gray, daily_rect)
        screen.blit(font2.render("Daily", True, white), (300, 205))
    
    elif state == 'daily':
        screen.fill(blue)

        #draw rects
        for row in rows:
            for cell in row["cells"]:
                pygame.draw.rect(screen, cell["colour"], cell["rect"], border_radius=3)
        #put letters in cells
        for row in rows:
            if row["active"]:
                for cell in row["cells"]:
                    index = row["cells"].index(cell)
                    if index < len(guess):
                        cell["letter"] = guess[index]
                    else:
                        cell["letter"] = ""  
            else:
                index2 = rows.index(row)
                try:
                    temp = guesses[index2]
                    for cell in row["cells"]:
                        index = row["cells"].index(cell)
                        cell["letter"] = temp[index]
                except IndexError:
                    for cell in row["cells"]:
                        cell["letter"] = ""
        
        #draw letters
        for row in rows:
            for cell in row["cells"]:
                text_surface = font3.render(cell["letter"], True, black)
                text_rect = text_surface.get_rect(center = cell["rect"].center)
                screen.blit(text_surface, text_rect)
            
        #if enter is pressed:
        if wordlock:
            active_changed = False
            colours = check_word(word, guess.lower())
            if colours == ["green", "green", "green", "green", "green"]:
                win = True
            for row in rows:
                if row["active"]:
                    for cell in row["cells"]:
                        cell["colour"] = colours[row["cells"].index(cell)]
            guesses.append(guess)
            guess = ""
            for row in rows:
                if row["active"] and not active_changed:
                    index = rows.index(row)
                    if index < len(rows) - 1 and index !=5:
                        row["active"] = False
                        rows[index+1]["active"] = True
                        active_changed = True
                        break
                    else:
                        wincon = True
            
            wordlock = False
    pygame.display.flip()
