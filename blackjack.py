#!/usr/bin/python
# Glackjack Version 1.0, Copyright 2008 Allan Lavell
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

import random
import os
import sys

import pygame
import time
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

X = 1850
Y = 850

screen = pygame.display.set_mode((X, Y))
clock = pygame.time.Clock()

###### SYSTEM FUNCTIONS BEGIN #######
def imageLoad(name, card):
    """ Function for loading an image. Makes sure the game is compatible across multiple OS'es, as it
    uses the os.path.join function to get he full filename. It then tries to load the image,
    and raises an exception if it can't, so the user will know specifically what's going if the image loading
    does not work. """
    
    if card == 1:
        fullname = os.path.join("images/cards/", name)
    else: fullname = os.path.join('images', name)
    
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print('Cannot load image:', name)
        raise SystemExit
    image = image.convert()
    
    return image, image.get_rect()
        
def soundLoad(name):
    """ Same idea as the imageLoad function. """
    
    fullName = os.path.join('sounds', name)
    try: sound = pygame.mixer.Sound(fullName)
    except pygame.error:
        print('Cannot load sound:', name)
        raise SystemExit
    return sound

def display(font, sentence):
    """ Displays text at the bottom of the screen, informing the player of what is going on."""
    
    displayFont = pygame.font.Font.render(font, sentence, 1, (255,255,255), (0,0,0)) 
    return displayFont

def playClick():
    clickSound = soundLoad("click2.wav")
    clickSound.play()
###### SYSTEM FUNCTIONS END #######
class cardSprite(pygame.sprite.Sprite):
    """ Sprite that displays a specific card. """
    def __init__(self, card, position):
        pygame.sprite.Sprite.__init__(self)
        cardImage = card + ".png"
        self.image, self.rect = imageLoad(cardImage, 1)
        self.position = position
    def update(self):
        self.rect.center = self.position
            
###### MAIN GAME FUNCTION BEGINS ######
def mainGame():
    """ Function that contains all the game logic. """
    
    def gameOver():
        """ Displays a game over screen in its own little loop. It is called when it has been determined that the player's funds have
        run out. All the player can do from this screen is exit the game."""
        
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit()

            # Fill the screen with black
            screen.fill((0,0,0))
            
            # Render "Game Over" sentence on the screen
            oFont = pygame.font.Font(None, 50)
            displayFont = pygame.font.Font.render(oFont, "Game over! You're outta cash!", 1, (255,255,255), (0,0,0)) 
            screen.blit(displayFont, (X, y))
            
            # Update the display
            pygame.display.flip()
            
    ######## DECK FUNCTIONS BEGIN ########
    def shuffle(deck):
        """ Shuffles the deck using an implementation of the Fisher-Yates shuffling algorithm. n is equal to the length of the
        deck - 1 (because accessing lists starts at 0 instead of 1). While n is greater than 0, a random number k between 0
        and n is generated, and the card in the deck that is represented by the offset n is swapped with the card in the deck
        represented by the offset k. n is then decreased by 1, and the loop continues. """
        
        n = len(deck) - 1
        while n > 0:
            k = random.randint(0, n)
            deck[k], deck[n] = deck[n], deck[k]
            n -= 1

        return deck        
                        
    def createDeck():
        """ Creates a default deck which contains all 52 cards and returns it. """

        deck = ['B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11', 'B12', 'B13']
        deck1 = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13']
        deck2 = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12', 'R13']
        deck3 = ['Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Y10', 'Y11', 'Y12', 'Y13']
        values = range(1,14)
        deck_dict = {} 
        deck_dict2 = {} 
        deck_dict3 = {} 
        deck_dict4 = {} 
        for d, v in zip(deck, values):
            deck_dict.update({d:v})
        
        for d, v in zip(deck1, values):
            deck_dict2.update({d:v})
        for d, v in zip(deck2, values):
            deck_dict3.update({d:v})
        for d, v in zip(deck3, values):
            deck_dict4.update({d:v})
        deck_dict.update(deck_dict2)
        deck_dict.update(deck_dict3)
        deck_dict.update(deck_dict4)
        print("deck dict ", deck_dict)
        return deck_dict

    def returnFromDead(deck, deadDeck):
        """ Appends the cards from the deadDeck to the deck that is in play. This is called when the main deck
        has been emptied. """
        
        for card in deadDeck:
            deck.append(card)
        del deadDeck[:]
        deck = shuffle(deck)

        return deck, deadDeck
        
    def deckDeal(deck, deadDeck):
        """ Shuffles the deck, takes the top 4 cards off the deck, appends them to the player's and dealer's hands, and
        returns the player's and dealer's hands. """

        deck = shuffle(deck)
        dealerHand, playerHand = [], []

        cardsToDeal = 4

        while cardsToDeal > 0:
            if len(deck) == 0:
                deck, deadDeck = returnFromDead(deck, deadDeck)

            # deal the first card to the player, second to dealer, 3rd to player, 4th to dealer, based on divisibility (it starts at 4, so it's even first)
            if cardsToDeal % 2 == 0: playerHand.append(deck[0])
            else: dealerHand.append(deck[0])
            
            del deck[0]
            cardsToDeal -= 1
            
        return deck, deadDeck, playerHand, dealerHand

    def hit(deck, deadDeck, hand):
        """ Checks to see if the deck is gone, in which case it takes the cards from
        the dead deck (cards that have been played and discarded)
        and shuffles them in. Then if the player is hitting, it gives
        a card to the player, or if the dealer is hitting, gives one to the dealer."""

        # if the deck is empty, shuffle in the dead deck
        if len(deck) == 0:
            deck, deadDeck = returnFromDead(deck, deadDeck)

        hand.append(deck[0])
        del deck[0]

        return deck, deadDeck, hand


    def endRound(deck, playerHand, dealerHand, deadDeck, funds, moneyGained, moneyLost, cards, cardSprite):
        """ Called at the end of a round to determine what happens to the cards, the moneyz gained or lost,
        and such. It also shows the dealer's hand to the player, by deleting the old sprites and showing all the cards. """
        pass

        #return deck, playerHand, dealerHand, deadDeck, funds, roundEnd 
    
    
    ######## SPRITE FUNCTIONS BEGIN ##########
    class cardSprite(pygame.sprite.Sprite):
        """ Sprite that displays a specific card. """
        
        def __init__(self, card, position):
            pygame.sprite.Sprite.__init__(self)
            cardImage = card + ".png"
            self.image, self.rect = imageLoad(cardImage, 1)
            self.position = position
        def update(self):
            self.rect.center = self.position
            
    class hitButton(pygame.sprite.Sprite):
        """ Button that allows player to hit (take another card from the deck). """
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("hit-grey.png", 0)
            self.position = (735, 400)
            
        def update(self, mX, mY, deck, deadDeck, playerHand, cards, pCardPos, roundEnd, cardSprite, click):
            """ If the button is clicked and the round is NOT over, Hits the player with a new card from the deck. It then creates a sprite
            for the card and displays it. """
            
            if roundEnd == 0: self.image, self.rect = imageLoad("hit.png", 0)
            else: self.image, self.rect = imageLoad("hit-grey.png", 0)
            
            self.position = (735, 400)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                if roundEnd == 0: 
                    playClick()
                    deck, deadDeck, playerHand = hit(deck, deadDeck, playerHand)

                    currentCard = len(playerHand) - 1
                    card = cardSprite(playerHand[currentCard], pCardPos)
                    cards.add(card)
                    pCardPos = (pCardPos[0] - 80, pCardPos[1])
                
                    click = 0
                
            return deck, deadDeck, playerHand, pCardPos, click
            
    class standButton(pygame.sprite.Sprite):
        """ Button that allows the player to stand (not take any more cards). """
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("stand-grey.png", 0)
            self.position = (735, 365)
            
        def update(self, mX, mY, deck, deadDeck, playerHand, dealerHand, cards, pCardPos, roundEnd, cardSprite, funds, bet, displayFont):
            """ If the button is clicked and the round is NOT over, let the player stand (take no more cards). """
            
            if roundEnd == 0: self.image, self.rect = imageLoad("stand.png", 0)
            else: self.image, self.rect = imageLoad("stand-grey.png", 0)
            
            self.position = (735, 365)
            self.rect.center = self.position
            
            if self.rect.collidepoint(mX, mY) == 1:
                if roundEnd == 0: 
                    playClick()
                    deck, deadDeck, roundEnd, funds, displayFont = compareHands(deck, deadDeck, playerHand, dealerHand, funds, bet, cards, cardSprite)
                
            return deck, deadDeck, roundEnd, funds, playerHand, deadDeck, pCardPos, displayFont 
            
    class betButtonDown(pygame.sprite.Sprite):
        """ Button that allows player to decrease his bet (in between hands only). """
        
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("down.png", 0)
            self.position = (710, 255)
        
        def update(self, mX, mY, value, click):
            if roundEnd == 1: self.image, self.rect = imageLoad("down.png", 0)
            else: self.image, self.rect = imageLoad("down-grey.png", 0)

            self.position = (760, 255)
            self.rect.center = self.position
            print("down button", self.rect.center)
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                print("Button Clicked ")
                value -= 1
                click = 0
            return value, click

    class betButtonUp(pygame.sprite.Sprite):
        """ Button that allows player to increase his bet (in between hands only). """

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("up.png", 0)
            self.position = (710, 255)
       
        def update(self, mX, mY, value, click):
            
            if roundEnd == 1: self.image, self.rect = imageLoad("up.png", 0)
            else: self.image, self.rect = imageLoad("up-grey.png", 0)

            self.position = (710, 255)
            self.rect.center = self.position
            print("pos button", self.rect.center)
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                print("Button up Clicked ")
                value += 1
                click = 0
            return value, click

    class ExitButton(pygame.sprite.Sprite):
        """ Button that allows player to increase his bet (in between hands only). """

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image, self.rect = imageLoad("exit.png", 0)
            self.position = (710, 355)
       
        def update(self, mX, mY, click):
            self.image, self.rect = imageLoad("exit.png", 0)
            self.position = (710, 355)
            self.rect.center = self.position
            print("pos button", self.rect.center)
            if self.rect.collidepoint(mX, mY) == 1 and click == 1:
                print("Exit Clicked ")
                sys.exit()
            
    ###### SPRITE FUNCTIONS END ######
         
    ###### INITIALIZATION BEGINS ######
    # This font is used to display text on the right-hand side of the screen
    textFont = pygame.font.Font(None, 28)

    # This sets up the background image, and its container rect
    background, backgroundRect = imageLoad("spielfeld_big.jpg", 0)
    
    # cards is the sprite group that will contain sprites for the dealer's cards
    cards = pygame.sprite.Group()
    # playerCards will serve the same purpose, but for the player
    playerCards = pygame.sprite.Group()
    cards = pygame.sprite.Group()

    # This creates instances of all the button sprites
    bbU = betButtonUp()
    bbD = betButtonDown()
    exitB = ExitButton()
    
    # This group containts the button sprites
    buttons = pygame.sprite.Group(bbU, bbD, exitB)

    # The 52 card deck is created
    deck = createDeck()
    # The dead deck will contain cards that have been discarded
    deadDeck = []

    # These are default values that will be changed later, but are required to be declared now
    # so that Python doesn't get confused
    playerHand, dealerHand, dCardPos, pCardPos = [],[],(),()
    mX, mY = 0, 0
    click = 0

    # The default funds start at $100.00, and the initial bet defaults to $10.00
    value = 0
    bet = 10.00

    # This is a counter that counts the number of rounds played in a given session
    handsPlayed = 0

    # When the cards have been dealt, roundEnd is zero.
    #In between rounds, it is equal to onev
    roundEnd = 1
    
    # firstTime is a variable that is only used once, to display the initial
    # message at the bottom, then it is set to zero for the duration of the program.
    firstTime = 1
    ###### INITILIZATION ENDS ########
    
    ###### MAIN GAME LOOP BEGINS #######
    round_idx = 0
    handsPlayed = 0
    amountPlayer = 2
    max_rounds = 10
    while True:
        round_idx +=1
        pygame.event.clear()
        screen.blit(background, backgroundRect)
        
        displayFont = display(textFont, "Click on start to start the game.")
        
        for round_idx in range(max_rounds):
            screen.blit(displayFont, (100,444))
            fundsFont = pygame.font.Font.render(textFont, "Card win estimate: $%.2f" %(value), 1, (255,255,255), (0,0,0))
            screen.blit(fundsFont, (663,205))
            hpFont = pygame.font.Font.render(textFont, "Round: %i " %(round_idx), 1, (255,255,255), (0,0,0))
            screen.blit(hpFont, (663, 180))
            print("new")
            playerCards = showCards(deck, playerCards, round_idx);
            buttons.draw(screen)
            pygame.display.flip()
            value, click = bbU.update(mX, mY, value, click)
            value, click = bbD.update(mX, mY, value, click)
            exitB.update(mX, mY,click)
            print("click", click)
            # event_wait = pygame.event.wait()
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mX, mY = pygame.mouse.get_pos()
                        click = 1
                    elif event.type == MOUSEBUTTONUP:
                        mX, mY = 0, 0
                        click = 0
            if len(playerCards) is not 0:
                playerCards.update()
                playerCards.draw(screen)
                cards.update()
                cards.draw(screen)
            time.sleep(2)
            print("click x {} y {} ".format(mX, mY))
        
    ###### MAIN GAME LOOP ENDS ######
###### MAIN GAME FUNCTION ENDS ######


def setCardEstimate():
    """ """
    pass 

def showCards(deck_dict, playerCards,round_idx):
    print(" show cards ")
    dCardPos = (450, 470)
    pCardPos = (X - 400, Y - 120)
    #pCardPos = (1400, 680)
    playerCards.empty()
    key_list = []
    playerHand = []
    for key in deck_dict.keys() :
        key_list.append(key)
    
    for idx in range(round_idx):
        playerHand.append(random.choice(key_list))
    for x in playerHand:
        card = cardSprite(x, pCardPos)
        pCardPos = (pCardPos[0] - 150, pCardPos [1])
        playerCards.add(card)

    return playerCards


if __name__ == "__main__":
    mainGame()
