import copy
import random
import os
import sys

import pygame
import time
from pygame.locals import *

from helper import imageLoad, soundLoad, display, display, playClick
from helper import ExitButton, createDeck, Round, Player, check_mous_click

pygame.font.init()
pygame.mixer.init()

X = 2850
Y = 1850

screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()


def main():
    """ """
    ###### INITIALIZATION BEGINS ######
    # This font is used to display text on the right-hand side of the screen
    textFont = pygame.font.Font(None, 128)
    textFont2 = pygame.font.Font(None, 90)
    # This sets up the background image, and its container rect
    background, backgroundRect = imageLoad("spielfeld_big.jpg", 0)

    # cards is the sprite group that will contain sprites for the dealer's cards
    cards = pygame.sprite.Group()
    # playerCards will serve the same purpose, but for the player
    playerCards = pygame.sprite.Group()
    cards = pygame.sprite.Group()

    # This creates instances of all the button sprites
    exitB = ExitButton()

    # This group containts the button sprites
    buttons = pygame.sprite.Group(exitB)

    # The 52 card deck is created
    deck = createDeck()

    # These are default values that will be changed later, but are required to be declared now
    # so that Python doesn't get confused
    playerHand, dealerHand, dCardPos, pCardPos = [],[],(),()
    mX, mY = 0, 0
    click = 0

    # The default funds start at $100.00, and the initial bet defaults to $10.00
    value = 0
    amountPlayer = 2
    max_rounds = 10
    pygame.event.clear()
    screen.blit(background, backgroundRect)
    displayFont = display(textFont, "Click on start to start the game.")
    # int game
    round_obj = Round(deck, amountPlayer, playerCards, 0)
    player1 = Player("Chris", idx=1, turn=0)
    player2 = Player("Com1", idx=2, turn=1 , human = False)
    playerList = [player1, player2]

    for round_idx in range(4, max_rounds):
        print("round {}".format(round_idx))
        round_obj.init_new_round(round_idx, [player1])
        round_obj.set_power_card(screen)
        player1.show_current_cards(screen)
        hpFont = pygame.font.Font.render(textFont, "Round: %i " %(round_idx), 3, (255,255,255), (0,0,0))
        screen.blit(hpFont, (1300, 80))
        updatedisplayScore(textFont2, screen, playerList)
        pygame.display.flip()
        exitB.update(mX, mY,click)
        if len(playerCards) is not 0:
            playerCards.update()
            playerCards.draw(screen)
            cards.update()
            cards.draw(screen)
        player1.play_card()
        player1.show_current_cards(screen)
        pygame.display.flip()
        time.sleep(5)
        print("click x {} y {} ".format(mX, mY))



def updatedisplayScore(textFont2, screen, playerList):
    """   """

    for idx, player in enumerate(playerList):
        scoreFont = pygame.font.Font.render(textFont2, "{}  has {} Points".format(player.name, player.points), 3, (255,255,255), (0,0,0))
        screen.blit(scoreFont, (X-700, Y- 1200 + (idx * 100)))














































if __name__ == "__main__":
    main()
