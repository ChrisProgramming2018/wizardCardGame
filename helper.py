import copy
import random
import os
import sys


import pygame
import time
from pygame.locals import *

X = 2850
Y = 1850

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
        self.name = card
        self.image, self.rect = imageLoad(cardImage, 1)
        self.position = position
    
    def update(self):
        self.rect.center = self.position



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






class ExitButton(pygame.sprite.Sprite):
    """ Button to exit the game. """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = imageLoad("exit.png", 0)
        self.position = (50, 40)
        self.rect.center = self.position

    def update(self, mX, mY, click):
        self.image, self.rect = imageLoad("exit.png", 0)
        if self.rect.collidepoint(mX, mY) == 1 and click == 1:
            print("Exit Clicked ")
            sys.exit()

class StartButton(pygame.sprite.Sprite):
    """ Button to exit the game. """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = imageLoad("start.png", 0)
        self.position = (300, 1500)
        self.rect.center = self.position

    def update(self, mX, mY, click, game):
        self.rect.center = self.position
        print("Start update ", self.position)
        if self.rect.collidepoint(mX, mY) == 1 and click == 1:
            click = 0
            print("Start Clicked ")
            game.play = True
        return click





class Round():
    def __init__(self, deck, amountPlayer, playerCards, round_idx):
        print("Create Round")
        self.play = False 
        self.deck = copy.deepcopy(deck)
        self.amountPlayer = amountPlayer
        self.round_idx = round_idx
        self.powerfull_color = []  # color sprite
        self.key_list = []
        self.playerCards = playerCards
        self.pCardPos = (X - 400, Y - 120)
        self.powerCardPos = (X- 1450, Y - 1200)
        # save the scores of the game 
        self.table_of_truth = []
        self.total_score_players = []
        self.current_estimate = []
        self.current_wins = []
        for i in range(amountPlayer):
            self.total_score_players.append(0)
            self.current_estimate.append(0)
            self.current_wins.append(0)

    def set_key_list(self):
        for key in self.deck.keys():
            self.key_list.append(key)

    def set_power_card(self, screen):
        """ set and display the power card for the current round

        """
        print("Set power card")
        k = random.choice(self.key_list)
        self.key_list.remove(k)
        self.power_full_card_sprite = cardSprite(k, self.powerCardPos)
        self.powerfull_color = [k[0]]
        self.show_power_card(screen)
        print("Current Power is {} ".format(self.powerfull_color[0]))

    def show_power_card(self, screen):
        cards = pygame.sprite.Group()
        cards.add(self.power_full_card_sprite)
        self.power_full_card_sprite.update()
        print("Current Power is {} ".format(self.powerfull_color[0]))
        cards.draw(screen)

    def init_new_round(self, round_idx, player_list):
        self.round_idx = round_idx
        self.set_key_list()
        for player in player_list:
            cards = []
            cards_sprite = []
            for idx in range(round_idx):
                k = random.choice(self.key_list)
                self.key_list.remove(k)
                card = cardSprite(k, self.pCardPos)
                self.pCardPos = (self.pCardPos[0] - 150, self.pCardPos [1])
                cards.append(k)
                cards_sprite.append(card)
            print("player {} add cards {} ".format(player.name, len(cards)))
            player.set_cards(cards, cards_sprite)




class Player():
    def __init__(self, name, turn, idx, human=True):
        self.name = name
        self.human = human
        self.player_idx = idx
        self.points = 0
        self.current_cards = []
        self.current_cards_sprite = []
        self.current_win_estimate = 0
        self.turn = turn
        self.currend_played_card = None
       
    def set_cards(self, cards, cards_sprite):
        self.current_cards = cards
        self.current_cards_sprite = cards_sprite

    def show_current_cards(self, screen):
        """ Display current cards on screen """
        print("Update show current cards", self.name)
        print("Update show current cards", len(self.current_cards))

        cards = pygame.sprite.Group()
        for card in self.current_cards_sprite:
            print(self.name)
            card.update()
            cards.add(card)
        cards.draw(screen)

    def show_played_card(self, screen):
        cards = pygame.sprite.Group()
        cards.update()
        cards.add(self.currend_played_card)
        cards.draw(screen)
    
    def play_card(self):
        print("players cards {} ".format(self.current_cards))
        if not self.human:
            print("Comuter cards {} ".format(self.current_cards))
            return 
        while True:
            time.sleep(1)
            mX, mY, click = check_mous_click()
            print("payer choose card ", mX, mY)
            if mX == -1:
                continue
            for card in self.current_cards_sprite:
                if card.rect.collidepoint(mX, mY) == 1:
                    print(card.name)
                    card.position = (X -1000, Y - 1400)
                    card.update()
                    self.current_cards.remove(card.name)
                    self.current_cards_sprite.remove(card)
                    self.currend_played_card = card
            if self.currend_played_card is not None:
                print("players cards {} ".format(self.current_cards))
                break


    def set_amout_wins(self):
        """
        At each round the player has to chose how many wins he estimate
        In case he is the last person he is not allowed to choose the amount
        which will add to the total_amount of the current cards
        
        """
        # case he is last



        # case not last 



        self.current_win_estimate = 0



def check_mous_click():
    mX = -1
    mY = -1 
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                mX, mY = pygame.mouse.get_pos()
                click = 1
            elif event.type == MOUSEBUTTONUP:
                mX, mY = 0, 0
    print("mouse {} {} ".format(mX, mY))
    return mX, mY, 1 

