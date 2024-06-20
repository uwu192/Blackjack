import pygame
import sys
import random
from moviepy.editor import *
import math

pygame.init()
# x and y is the position clicked
x = 0
y = 0
# screen variable
height = 1600
width = 900
# set logo and screen
pygame.display.set_caption("BLACKJACK🃏")
screen = pygame.display.set_mode((height, width))


# fps
fps = pygame.time.Clock()
# Color
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
# Background screen is running
running_screen = "Dealt"
# Game
Bots = 1
Selector = "Player"
Bucks = 10000
Bucks_bet = 0
text_Bucks = "10.000"
counter_disapear = 0
Card = []
Card_picked = [False] * 53
Card_pos = [573, 727, 852, 971, 1100]
Points = [0] * 5
Have_cards = [2] * 5  # How many card does Player,Bots have
Bust = [False] * 5


# Video
def Dealt_vid(bots):
    temp_link = f"data/video/dealt/{bots}bots.mp4"
    vid_dealt = VideoFileClip(temp_link)
    return vid_dealt


# Subprogram of detail--------------------------------------------
# Reset x,y after clicked(or else it'll contain x,y and loop infinity if they meet func if else)
def reset():
    global x, y
    x = 0
    y = 0


# Get text
def text(Contain, x_text, y_text, color, size):
    pygame.font.init()
    font = pygame.font.Font("data/font.ttf", size)
    text = font.render(Contain, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x_text, y_text)
    screen.blit(text, text_rect)


# Create dot in text(Ex:10000 -> 10.000)
def Bucks_dot(Bucks):
    counter = 0
    text_Bucks = str(Bucks)
    chars = len(text_Bucks)
    for char in range(chars - 1, -1, -1):
        counter += 1
        if counter % 3 == 0 and char > 0:
            text_Bucks = text_Bucks[:char] + "." + text_Bucks[char:]
    return text_Bucks


def Bet_text():
    text(f"Bucks:{Bucks_dot(Bucks)}", 800, 231, black, 80)
    text("Place your Bet", width // 2 + 350, height // 2 - 450, white, 60)


def Not_enough_text():
    global counter_disapear
    if counter_disapear < 50:
        text("Not enough bucks!!!", 771, 57, green, 100)
        counter_disapear += 1
    else:
        counter_disapear = 0
        reset()


# Movement sprite--------------------------------------------
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.target_pos = None

    def update(self):
        if self.target_pos:
            # Find way and length to pos
            direction = pygame.math.Vector2(self.target_pos) - pygame.math.Vector2(
                self.rect.center
            )
            # Distance will convert in pixel
            distance = direction.length()
            if distance > 1:
                direction.normalize_ip()
                # (Dis, speed)
                self.rect.move_ip(direction * min(distance, 50))


# Make this for easier movement input-------------------------


# Using this Subprogam before loop to create object sprite
def create_sprite(image, pos):
    sprite = MovingSprite(image, pos)
    return sprite


# Using this Subprogram in loop to move the object sprite
def update_sprite(sprite, target_pos):
    sprite.target_pos = target_pos
    sprite.update()


# Create object chip---------------------------------------
# Player can create more object in one chip
pos_bet_1 = []
pos_bet_2 = []
pos_bet_3 = []
pos_bet_4 = []
pos_bet_5 = []
pos_bet_6 = []
chips_1 = []
chips_2 = []
chips_3 = []
chips_4 = []
chips_5 = []
chips_6 = []
x_list = [199, 407, 586, 1028, 1191, 1394]
scale_x_chip = 0


def create_5():
    global chips
    chip_img = pygame.image.load("data/chip/1.png")
    chip_img = pygame.transform.scale(chip_img, (200, 200))
    chip = create_sprite(chip_img, (x_list[0], 700))
    chips_1.append(chip)
    pos_bet_1.append((random.randint(771, 816), random.randint(608, 793)))


def create_10():
    global chips
    chip_img = pygame.image.load("data/chip/2.png")
    chip_img = pygame.transform.scale(chip_img, (200, 200))
    chip = create_sprite(chip_img, (x_list[1], 700))
    chips_2.append(chip)
    pos_bet_2.append((random.randint(771, 816), random.randint(608, 793)))


def create_50():
    global chips
    chip_img = pygame.image.load("data/chip/3.png")
    chip_img = pygame.transform.scale(chip_img, (200, 200))
    chip = create_sprite(chip_img, (x_list[2], 700))
    chips_3.append(chip)
    pos_bet_3.append((random.randint(771, 816), random.randint(608, 793)))


def create_100():
    global chips
    chip_img = pygame.image.load("data/chip/4.png")
    chip_img = pygame.transform.scale(chip_img, (200, 200))
    chip = create_sprite(chip_img, (x_list[3], 700))
    chips_4.append(chip)
    pos_bet_4.append((random.randint(771, 816), random.randint(608, 793)))


def create_1k():
    global chips
    chip_img = pygame.image.load("data/chip/5.png")
    chip_img = pygame.transform.scale(chip_img, (200, 200))
    chip = create_sprite(chip_img, (x_list[4], 700))
    chips_5.append(chip)
    pos_bet_5.append((random.randint(771, 816), random.randint(608, 793)))


def create_10k():
    global chips
    chip_img = pygame.image.load("data/chip/6.png")
    chip_img = pygame.transform.scale(chip_img, (200, 200))
    chip = create_sprite(chip_img, (x_list[5], 700))
    chips_6.append(chip)
    pos_bet_6.append((random.randint(771, 816), random.randint(608, 793)))


chips_moved = [False] * 6


# Create object for Cards-----------------------------------------------
def create_card():
    for num in range(1, 53):
        card_img = pygame.image.load(f"data/card/{num}.png")
        card_img = pygame.transform.scale(card_img, (200, 270))
        Card.append(card_img)


backside_card = pygame.image.load("data/card/Backside.png")
create_card()


# If player clicked chip(screen, not object), create object for that chip
def Select_chips():
    global Bucks, Bucks_bet
    if 105 < x < 284:
        if 630 < y < 761:
            if Bucks - 5 >= 0:
                Bucks_bet += 5
                Bucks -= 5
                create_5()
                chips_moved[0] = True
                reset()
            else:
                Not_enough_text()
    if 314 < x < 482:
        if 625 < y < 784:
            if Bucks - 10 >= 0:
                Bucks_bet += 10
                Bucks -= 10
                create_10()
                chips_moved[1] = True
                reset()
            else:
                Not_enough_text()
    if 519 < x < 652:
        if 623 < y < 785:
            if Bucks - 50 >= 0:
                Bucks_bet += 50
                Bucks -= 50
                create_50()
                chips_moved[2] = True
                reset()
            else:
                Not_enough_text()
    if 928 < x < 1074:
        if 615 < y < 747:
            if Bucks - 100 >= 0:
                Bucks_bet += 100
                Bucks -= 100
                create_100()
                chips_moved[3] = True
                reset()
            else:
                Not_enough_text()
    if 1117 < x < 1282:
        if 618 < y < 762:
            if Bucks - 1000 >= 0:
                Bucks_bet += 1000
                Bucks -= 1000
                create_1k()
                chips_moved[4] = True
                reset()
            else:
                Not_enough_text()
    if 1312 < x < 1467:
        if 632 < y < 784:
            if Bucks - 10000 >= 0:
                Bucks_bet += 10000
                Bucks -= 10000
                create_10k()
                chips_moved[5] = True
                reset()
            else:
                Not_enough_text()


def Display_chip():
    if chips_moved[0] == True:
        for chip in range(len(chips_1)):
            update_sprite(chips_1[chip], (pos_bet_1[chip]))
            screen.blit(chips_1[chip].image, chips_1[chip].rect)
    if chips_moved[1] == True:
        for chip in range(len(chips_2)):
            update_sprite(chips_2[chip], (pos_bet_2[chip]))
            screen.blit(chips_2[chip].image, chips_2[chip].rect)
    if chips_moved[2] == True:
        for chip in range(len(chips_3)):
            update_sprite(chips_3[chip], (pos_bet_3[chip]))
            screen.blit(chips_3[chip].image, chips_3[chip].rect)
    if chips_moved[3] == True:
        for chip in range(len(chips_4)):
            update_sprite(chips_4[chip], (pos_bet_4[chip]))
            screen.blit(chips_4[chip].image, chips_4[chip].rect)
    if chips_moved[4] == True:
        for chip in range(len(chips_5)):
            update_sprite(chips_5[chip], (pos_bet_5[chip]))
            screen.blit(chips_5[chip].image, chips_5[chip].rect)
    if chips_moved[5] == True:
        for chip in range(len(chips_6)):
            update_sprite(chips_6[chip], (pos_bet_6[chip]))
            screen.blit(chips_6[chip].image, chips_6[chip].rect)


# Gameplay----------------------------------------------------
Player = []
Bot1 = []
Bot2 = []
Bot3 = []
Bot4 = []
Dealted_card = False
Ace_points = [1, 10, 11]
temp_max = []  # Highest points Ace can reach(if Player have more than 2 ace)


def trans_card_to_points(card_num, index):
    global Have_special_card, temp_max
    if card_num <= 36:  # 1 -> 10
        card_num /= 4
        card_num = math.ceil(card_num + 1)
    elif card_num <= 48:  # 10 -> K
        card_num = 10
    else:  # Ace
        temp_ace = 0
        for point in Ace_points:
            card_num = Points[index] + point
            if card_num > temp_ace and card_num <= 21:
                temp_ace = point
        if temp_max == []:
            temp_max.append(temp_ace)
        print(f"T:{temp_max}")
        card_num = temp_ace
    return card_num


# Subprogram of screen---------------------------------------
def Main():
    bg = pygame.image.load("data/screen/Main_screen.png")
    pygame.Surface.blit(screen, bg, (0, 0))
    # Enter Setting screen
    if (919 > x) and (x > 731):
        if 685 > y > 416:
            return "Setting"
    return "Main"


def Setting():
    global Bots
    global Selector
    if Selector == "Dealer":
        bg = pygame.image.load("data/screen/Setting_screen(Dealer).png")
    else:
        bg = pygame.image.load("data/screen/Setting_screen(Player).png")
    pygame.Surface.blit(screen, bg, (0, 0))
    text(str(Bots), 840, 460, white, 100)
    Bots = int(Bots)
    # Role pick
    if 1259 > x > 1038:
        if 709 > y > 579:
            Selector = "Player"
    if 968 > x > 739:
        if 702 > y > 584:
            Selector = "Dealer"
    # Add or remove bots
    if 1104 > x > 1021:
        if 423 > y > 352:
            if Bots < 4:
                Bots += 1
                reset()
    if 1081 > x > 1024:
        if 535 > y > 483:
            if Bots > 1:
                Bots -= 1
                reset()
    # Enter Bet screen
    if 970 > x > 610:
        if 874 > y > 763:
            return "Bet"
    return "Setting"


def Bet():
    global counter_1, counter_2, counter_3, counter_4, counter_5, counter_6
    bg = pygame.image.load("data/screen/Bet_screen.png")
    pygame.Surface.blit(screen, bg, (0, 0))
    Bet_text()
    Select_chips()
    Display_chip()
    # Enter Play screen
    if 122 < x < 415:
        if 57 < y < 202:
            if Bucks_bet == 0:
                text("Bet some bucks!!!", 200, 300, white, 20)
                return "Bet"
            else:
                return "Dealt"
    return "Bet"


def Dealt():
    global Dealted_card, Player_points
    dealt_vid = Dealt_vid(Bots)
    dealt_vid = dealt_vid.resize(width=1600, height=900)
    dealt_vid.preview()
    if Dealted_card == False:
        for i in range(5):
            a = random.randint(1, 52)
            b = random.randint(1, 52)
            while Card_picked[a] == True or Card_picked[b] == True or a == b:
                a = random.randint(1, 52)
                b = random.randint(1, 52)
            Card_picked[a] = True
            Card_picked[b] = True
            if i == 0:  # Player
                Player.append(a)
                Points[0] += trans_card_to_points(a, 0)
                Player.append(b)
                Points[0] += trans_card_to_points(b, 0)
            else:  # Bots
                Bot_card_a = f"Bot{i}.append(a)"
                Bot_card_b = f"Bot{i}.append(b)"
                exec(Bot_card_a)
                exec(Bot_card_b)
        Dealted_card = True
    return "Play"


def Play():
    global Bust, Have_cards, Points, temp_max
    bg = pygame.image.load(f"data/screen/Playing/{Bots}bots.png")
    bunch_cards = pygame.image.load("data/card/Bunch_cards.png")
    bunch_cards = pygame.transform.scale(bunch_cards, (400, 400))
    pygame.Surface.blit(screen, bg, (0, 0))
    text(f"You're bet {Bucks_bet} bucks", 783, 60, white, 70)
    Display_chip()
    if Have_cards[0] == 5 and Points[0] <= 21:
        text("Five Card", 785, 603, white, 70)
    elif Points[0] <= 21:
        text(str(Points[0]), 785, 603, white, 70)
    else:
        text("Bust", 785, 603, white, 70)
        Bust[0] = True
    text("Hit", 995, 191, white, 70)
    pygame.Surface.blit(screen, bunch_cards, (800, 150))
    pygame.draw.rect(screen, white, (576, 255, 250, 100), border_radius=20)
    text("Stay", 701, 303, black, 70)
    for card in range(len(Player)):
        pygame.Surface.blit(screen, Card[Player[card] - 1], (Card_pos[card], 700))
    # Hit
    if 912 < x < 1088:
        if 231 < y < 493:
            if Bust[0] == False and Have_cards[0] != 5:
                Have_cards[0] += 1
                new_card = random.randint(1, 52)
                while Card_picked[new_card] == True:
                    new_card = random.randint(1, 52)
                Card_picked[new_card] == True
                Points[0] += trans_card_to_points(new_card, 0)
                if (
                    Points[0] > 21 and temp_max != []
                ):  # Mean Player busted but they're have ace
                    for index in range(len(temp_max)):
                        if temp_max[index] != 1:
                            if Points[0] - 11 + 10 <= 21:
                                temp_max[index] = 10
                                Points[0] = Points[0] - 11 + 10
                                break
                            elif Points[0] - 11 + 1 <= 21:
                                temp_max[index] = 1
                                Points[0] = Points[0] - 11 + 1
                                break
                            else:
                                temp_max[index] = 1
                                Points[0] = Points[0] - 11 + 1
                Player.append(new_card)
                print(Points[0])
                print(temp_max)
                reset()
    # Stay
    if 577 < x < 819:
        if 256 < y < 347:
            if Selector == "Dealer":
                if Points[0] < 15:
                    text(
                        "You're only stay when your points higher than 15",
                        703,
                        239,
                        white,
                        20,
                    )
                else:
                    return "End"
            else:
                if Points[0] < 16:
                    text(
                        "You're only stay when your points higher than 16",
                        630,
                        239,
                        white,
                        20,
                    )
                else:
                    return "End"
    return "Play"


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
            print(x, y)
    if running_screen == "Main":
        running_screen = Main()
    if running_screen == "Setting":
        running_screen = Setting()
    if running_screen == "Bet":
        running_screen = Bet()
    if running_screen == "Dealt":
        running_screen = Dealt()
    if running_screen == "Play":
        running_screen = Play()
    pygame.display.flip()
    fps.tick(60)
