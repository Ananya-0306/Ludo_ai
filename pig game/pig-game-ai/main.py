import pygame
import time

from button import Button
from const import POINTS_TO_WIN, SCORE_STOP
from const import TURN_HUMAN, TURN_BOT
from const import FONT_SIZE, WIN_FONT_SIZE
from mechanics import roll_dice


import random
from datetime import datetime

# Seed RNG
random.seed(datetime.now())


# Screen params
WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60


# Colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# pygame initialization
pygame.init()

# Screen settings
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Pig Dice Game')
clock = pygame.time.Clock()


# Show human stats at game screen
def print_human_stats(human_total, human_turn_score, screen, font):
    text = f'HUMAN\nTotal score: {human_total}\nTurn score: {human_turn_score}'
    offset = 0

    for line in text.split('\n'):
        rendered = font.render(line, 1, BLACK)
        screen.blit(rendered, (50, 100+4*offset))
        offset += FONT_SIZE



# Show bot stats at game screen
def print_bot_stats(bot_total, bot_turn_score, screen, font):
    text = f'BOT\nTotal score: {bot_total}\nTurn score: {bot_turn_score}'
    offset = 0

    for line in text.split('\n'):
        rendered = font.render(line, 1, BLACK)
        screen.blit(rendered, (600, 100+4*offset))
        offset += FONT_SIZE


# load images of dice
def load_dice_images(path):
    dct = dict()
    for i in range(1, 7):
        img = pygame.image.load(f'{path}dice{i}.png').convert()

        dct[i] = img
    
    return dct




# main game loop
def game():
    # Pre-loading of resource
    winner_font = pygame.font.Font('resources/font/consola.ttf', 40)
    status_font = pygame.font.Font('resources/font/consola.ttf', FONT_SIZE)
    dice_imgs = load_dice_images('resources/img/')

    # Gaming pre-settings
    human_total, bot_total = 0, 0
    human_turn_score, bot_turn_score = 0, 0 
    turn = TURN_HUMAN
    current_dice = 1

    # bot did not throw dice yet
    bot_times_thrown = 0  

    # Buttons initialize
    button_roll = Button(300, 400, 200, 50, color=RED, text='Roll')
    button_hold = Button(300, 500, 200, 50, color=BLUE, text='Hold')
    
    # Main cycle control
    running = True
    while running:
        # Fill the screen
        screen.fill(WHITE)
        # Draw buttons
        button_roll.draw(screen)
        button_hold.draw(screen)
        # Show statuses of human and bot
        print_human_stats(human_total, human_turn_score, screen, status_font)
        print_bot_stats(bot_total, bot_turn_score, screen, status_font)
        
        # Show current dice as a picture
        
        time.sleep(0.4)  # not so fast


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if turn == TURN_HUMAN:   # if it's a human to roll then reasonable to check pressing buttons
                
                    if button_roll.isOver(event.pos):
                        # do a barrel roll
                        score = roll_dice()  # throw a dice
                        human_turn_score += score   # add to score
                        current_dice = score       # change dice picture

                        if score == SCORE_STOP:   # if it's 1 on dice
                            human_turn_score = 0  # human gains nothing on this case
                            screen.blit(dice_imgs[current_dice], (350, 100))
                            pygame.display.flip()
                            time.sleep(0.5)
                            turn = TURN_BOT       # give turn to bot

                    
                    if button_hold.isOver(event.pos):
                        # hold back
                        human_total += human_turn_score  # save part of score gained
                        human_turn_score = 0      # make this turn zero
                        turn = TURN_BOT  # give turn to bot if end of move

        # After every check of human action, it's time for bot actions
        if turn == TURN_BOT:  # bot does things
            
            # (bot - human) points 
            difference = bot_total - human_total

            # strategy 1: situation is calm
            if difference >= -30:   # calm
                if bot_turn_score < 20 and bot_times_thrown < 4: # optimal strategy
                    score = roll_dice()   # throw dice
                    bot_times_thrown += 1  # increment times thrown
                    bot_turn_score += score  # add score
                    current_dice = score     # change dice picture

                    # Check if it's failure throw
                    if score == SCORE_STOP:
                        bot_turn_score = 0   # zero score for turn
                        bot_times_thrown = 0   # zero times thrown
                        turn = TURN_HUMAN   # give turn to human

                # Take what gained per turn
                else:
                    bot_total += bot_turn_score   # add score
                    bot_turn_score = 0   # zero per turn
                    bot_times_thrown = 0  # zero times thrown
                    turn = TURN_HUMAN   # give turn to human

            # strategy 2: situation comes out of control, need to risk
            else:
                if bot_turn_score < human_total/2 and bot_times_thrown < 6:
                    score = roll_dice()   # throw dice
                    bot_times_thrown += 1  # increase times of throw
                    bot_turn_score += score  # add score
                    current_dice = score

                    # If failure in risk
                    if score == SCORE_STOP:
                        bot_turn_score = 0 # zero for turn
                        bot_times_thrown = 0
                        turn = TURN_HUMAN
                
                # Take what gained
                else:
                    bot_total += bot_turn_score  # add score
                    bot_turn_score = 0  # zero for turn
                    bot_times_thrown = 0  # zero throws again
                    turn = TURN_HUMAN   # give turn to human

            
        screen.blit(dice_imgs[current_dice], (350, 100))
        
        

        # Game end if someone won
        if human_total >= POINTS_TO_WIN:
            turn = 'no one'
            text = 'Winner is HUMAN'
            rendered = winner_font.render(text, 1, BLACK)
            screen.blit(rendered, (225, 300))
        elif bot_total + bot_turn_score >= POINTS_TO_WIN:
            bot_total += bot_turn_score
            bot_turn_score = 0
            turn = 'no one'
            text = 'Winner is BOT'
            rendered = winner_font.render(text, 1, BLACK)
            screen.blit(rendered, (225, 300))





        clock.tick(FPS)
        pygame.display.flip()




# def print_winner(winner):
#     printing = True
#     while printing:
#         # Show winner
#         text = f'Winner is {winner}'
#         winner_font = pygame.font.Font('resources/font/consola.ttf', 40)
#         rendered = winner_font.render(text, 1, BLACK)
#         screen.blit(rendered, (225, 300)) 




# Play game
game()