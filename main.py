import pygame
from pyvidplayer2 import Video
import sys
import random
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
red = (255, 0, 0)
grey = (128, 128, 128)
# Background screen is running
running_screen = "Dealt"  # Main - Setting - Bet - Dealt - Play - End
# Game
Bots = 2
Selector = "Player"  # Dealer - Player
Bucks = 10000
Bucks_bet = 0
text_Bucks = "10.000"
counter_disapear = 0
Card = []
Card_picked = [False] * 53
Card_pos_player = [573, 727, 852, 971, 1100]
Card_pos_player_end = [675, 735, 805, 700, 800]
Card_pos_bot1_backside = [(-30, 302), (31, 412), (3, 375)]
Card_pos_bot2_backside = [(211, 454), (332, 548), (355, 549)]
Card_pos_bot3_backside = [(1250, 459), (1167, 461), (1088, 532)]
Card_pos_bot4_backside = [(1490, 316), (1400, 334), (1462, 312)]
Card_rot_bot1_backside = [-10, 80, -10]
Card_rot_bot2_backside = [-40, 0, -15]
Card_rot_bot3_backside = [-9, 30, 70]
Card_rot_bot4_backside = [0, 20, 0]
Card_pos_bot1_end = [30, 111, 188, 70, 150]
Card_pos_bot2_end = [336, 423, 497, 370, 477]
Card_pos_bot3_end = [1000, 1070, 1150, 1030, 1100]
Card_pos_bot4_end = [1310, 1382, 1438, 1350, 1402]
Points_pos = [785, 174, 471, 1117, 1427]
Points = [0] * 5
Have_cards = [2] * 5  # How many card does Player,Bots have
Bust = [False] * 5
winner = None


# Create object for other things(button, icon , vv.v..)
Up_arrow = pygame.image.load("data/other/up_arrow.png")
Up_arrow = pygame.transform.scale(Up_arrow, (50, 50))


# Video
def Dealt_vid():
    vid = Video(f"data/video/dealt/{Bots}bots.mp4")
    vid.resize(size=(1600, 900))
    while vid.active:
        if vid.draw(screen, (0, 0), force_draw=False):
            pygame.display.update()
        pygame.time.wait(16)


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
backside_card = pygame.transform.scale(backside_card, (110, 148))
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


def Display_card_player_playing():
    for card in range(Have_cards[0]):
        pygame.Surface.blit(
            screen, Card[Player[card] - 1], (Card_pos_player[card], 700)
        )


def Display_card_bots_backside():
    if Bots == 1:
        for card in range(Have_cards[2] - 2):
            temp_backside_card = pygame.transform.rotate(
                backside_card, Card_rot_bot2_backside[card]
            )
            screen.blit(temp_backside_card, Card_pos_bot2_backside[card])
    elif Bots == 2:
        for card in range(Have_cards[2] - 2):
            temp_backside_card = pygame.transform.rotate(
                backside_card, Card_rot_bot2_backside[card]
            )
            screen.blit(temp_backside_card, Card_pos_bot2_backside[card])
        for card in range(Have_cards[3] - 2):
            temp_backside_card = pygame.transform.rotate(
                backside_card, Card_rot_bot3_backside[card]
            )
            screen.blit(temp_backside_card, Card_pos_bot3_backside[card])
    else:
        for bot in range(1, Bots + 1):
            for card in range(Have_cards[bot] - 2):
                temp_rot = f"pygame.transform.rotate(backside_card,Card_rot_bot{bot}_backside[{card}])"
                temp_pos = f"screen.blit(temp_backside_card,Card_pos_bot{bot}_backside[{card}])"
                temp_backside_card = eval(temp_rot)
                exec(temp_pos)


def Display_card_end():
    # Display card player
    for card in range(Have_cards[0]):
        card_img = Card[Player[card] - 1]
        card_img = pygame.transform.scale(card_img, (110, 148))
        if card < 3:
            pygame.Surface.blit(screen, card_img, (Card_pos_player_end[card], 600))
        else:
            pygame.Surface.blit(screen, card_img, (Card_pos_player_end[card], 700))
    # Display card bots
    if Bots == 1:
        for card in range(Have_cards[2]):
            card_img = Card[Bot2[card] - 1]
            card_img = pygame.transform.scale(card_img, (110, 148))
            if card < 3:
                pygame.Surface.blit(screen, card_img, (Card_pos_bot2_end[card], 600))
            else:
                pygame.Surface.blit(screen, card_img, (Card_pos_bot2_end[card], 700))
    elif Bots == 2:
        for card in range(Have_cards[2]):
            card_img = Card[Bot2[card] - 1]
            card_img = pygame.transform.scale(card_img, (110, 148))
            if card < 3:
                pygame.Surface.blit(screen, card_img, (Card_pos_bot2_end[card], 600))
            else:
                pygame.Surface.blit(screen, card_img, (Card_pos_bot2_end[card], 700))
        for card in range(Have_cards[3]):
            card_img = Card[Bot3[card] - 1]
            card_img = pygame.transform.scale(card_img, (110, 148))
            if card < 3:
                pygame.Surface.blit(screen, card_img, (Card_pos_bot3_end[card], 600))
            else:
                pygame.Surface.blit(screen, card_img, (Card_pos_bot3_end[card], 700))
    else:
        for bot in range(1, Bots + 1):
            for card in range(Have_cards[bot]):
                cmd_card_img = f"Card[Bot{bot}[card] - 1]"
                card_img = eval(cmd_card_img)
                card_img = pygame.transform.scale(card_img, (110, 148))
                cmd_card_pos_1 = f"pygame.Surface.blit(screen, card_img, (Card_pos_bot{bot}_end[card], 600))"
                cmd_card_pos_2 = f"pygame.Surface.blit(screen, card_img, (Card_pos_bot{bot}_end[card], 700))"
                if card < 3:
                    exec(cmd_card_pos_1)
                else:
                    exec(cmd_card_pos_2)


def Display_points(x_y, whose, color):
    x = x_y[0]
    y = x_y[1]
    if five_cards(whose):
        text("Five Card", x, y, color, 50)
    elif black_jack(whose):
        text("Black Jack", x, y, color, 50)
    elif double_aces(whose):
        text("Double Aces", x, y, color, 50)
    elif Points[whose] <= 21:
        text(str(Points[whose]), x, y, color, 70)
    else:
        text("Bust", x, y, color, 70)


def Display_dealer():
    if Selector == "Player":
        if running_screen == "Play":
            screen.blit(Up_arrow, (303, 670))
            text("Dealer", 345, 732, white, 50)
        else:
            text("Dealer", 471, 494, white, 50)


# Gameplay----------------------------------------------------
Player = []
Bot1 = []
Bot2 = []
Bot3 = []
Bot4 = []
Dealted = False
Ace_points = [1, 10, 11]
Aces = [[], [], [], [], []]


# Top 1
def double_aces(whose):
    return len(Aces[whose]) == 2 and Have_cards[whose] == 2


# Top 2
def black_jack(whose):
    return Have_cards[whose] == 2 and Points[whose] == 21


# Top 3
def five_cards(whose):
    return Have_cards[whose] == 5 and Points[whose] <= 21


counter_time = 0


def Calculating():
    winner = None
    if Selector == "Player":
        # Convert speacial cards to points in rank(2 Aces > Aces_10 > 5 cards > normal > Bust)
        """ Note: We can access list points_player_bot by for range(0,1)
            but we should access global list with number in list points_player_bot, not number in loop"""
        points_player_bot = [0, 2]
        for whose in range(2):
            if double_aces(whose):
                points_player_bot[whose] = 100
            elif black_jack(whose):
                points_player_bot[whose] = 50
            elif five_cards(whose):
                points_player_bot[whose] = 40
            else:
                if Bust[points_player_bot[whose]] == False:
                    points_player_bot[whose] = Points[points_player_bot[whose]]
                else:
                    points_player_bot[whose] = 0
        if points_player_bot[0] > points_player_bot[1]:
            winner = "Win"
        elif points_player_bot[0] == points_player_bot[1]:
            winner = "Draw"
        else:
            winner = "Lose"
    # counter_disapear: Count how much time loop text Calculating
    # counter_time: Run while display another subprogram (that's why i dont use for or while loop)
    global counter_disapear, counter_time
    if counter_disapear < 3:
        if counter_time < 2:
            text("Calculating", 783, 253, white, 70)
        elif counter_time < 4:
            text("Calculating.", 783, 253, white, 70)
        elif counter_time < 6:
            text("Calculating..", 783, 253, white, 70)
        elif counter_time < 8:
            text("Calculating...", 783, 253, white, 70)
        elif counter_time < 10:
            text("Calculating....", 783, 253, white, 70)
        elif counter_time == 10:
            counter_disapear += 1
            counter_time = 0
        if counter_time < 10:
            counter_time += 1
    else:
        counter_disapear = 0
        counter_time = 0
        return winner


def Winner_light(winner):
    global counter_disapear, counter_time
    if Selector == "Player":
        if counter_disapear < 3:
            if winner == "Win":
                text("You win",790,260,white,70)
                if counter_time % 4 == 0:
                    Display_points([Points_pos[0], 564], 0, red)
                    Display_points([Points_pos[2], 564], 2, grey)
                elif counter_time % 4 != 0:
                    Display_points([Points_pos[0], 564], 0, white)
                    Display_points([Points_pos[2], 564], 2, white)
            elif winner == "Lose":
                text("You lose",790,260,white,70)
                if counter_time % 4 == 0:
                    Display_points([Points_pos[0], 564], 0, grey)
                    Display_points([Points_pos[2], 564], 2, red)
                elif counter_time % 4 != 0:
                    Display_points([Points_pos[0], 564], 0, white)
                    Display_points([Points_pos[2], 564], 2, white)
            else:
                text("Draw",790,260,white,70)
                if counter_time % 4 == 0:
                    Display_points([Points_pos[0], 564], 0, grey)
                    Display_points([Points_pos[2], 564], 2, grey)
                elif counter_time % 4 != 0:
                    Display_points([Points_pos[0], 564], 0, white)
                    Display_points([Points_pos[2], 564], 2, white)
            if counter_time == 20:
                counter_disapear += 1
                counter_time = 0
            else:
                counter_time += 1


def trans_card_to_points(card_num, index):
    global Have_special_card, Aces
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
        if Aces[index] == []:
            Aces[index].append(temp_ace)
        card_num = temp_ace
    return card_num


def Change_Ace(index):
    global Aces, Points
    for ace in range(len(Aces[index])):
        if Aces[index][ace] != 1:
            if Points[index] - 11 + 10 <= 21:
                Aces[index][ace] = 10
                Points[index] = Points[index] - 11 + 10
                break
            elif Points[0] - 11 + 1 <= 21:
                Aces[index][ace] = 1
                Points[index] = Points[index] - 11 + 1
                break
            else:
                Aces[index][ace] = 1
                Points[index] = Points[index] - 11 + 1


def Dealt_card():
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
            Points[i] += trans_card_to_points(a, i)
            Points[i] += trans_card_to_points(b, i)


def Hit():
    global Points, Have_cards, temp_max
    bunch_cards = pygame.image.load("data/card/Bunch_cards.png")
    bunch_cards = pygame.transform.scale(bunch_cards, (400, 400))
    text("Hit", 995, 191, white, 70)
    pygame.Surface.blit(screen, bunch_cards, (800, 150))
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
                    Points[0] > 21 and Aces[0] != []
                ):  # Mean Player busted but they're have ace(change ace's point)
                    Change_Ace(0)
                Player.append(new_card)
                if Points[0] > 21:
                    Bust[0] = True
                reset()


def Stay():
    pygame.draw.rect(screen, white, (576, 255, 250, 100), border_radius=20)
    text("Stay", 701, 303, black, 70)
    if 577 < x < 819:
        if 256 < y < 347:
            if Selector == "Dealer":
                if Points[0] < 15 and Have_cards[0] != 5:
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
                if Points[0] < 16 and Have_cards[0] != 5:
                    text(
                        "You're only stay when your points higher than 16",
                        630,
                        239,
                        white,
                        20,
                    )
                else:
                    return "End"


def Bot_hit():
    global Have_cards, Card_picked, Points, Bot1, Bot2, Bot3, Bot4
    for bot in range(1, 5):
        while Have_cards[bot] < 5 and Points[bot] <= 17:
            if Have_cards[bot] != 5 and Bust[bot] != True:
                Have_cards[bot] += 1
                new_card = random.randint(1, 52)
                while Card_picked[new_card] == True:
                    new_card = random.randint(1, 52)
                Card_picked[new_card] == True
                Points[bot] += trans_card_to_points(new_card, 0)
                if (
                    Points[bot] > 21 and Aces[bot] != []
                ):  # Mean Bot busted but they're have ace(change ace's point)
                    Change_Ace(bot)
                append_bot = f"Bot{bot}.append(new_card)"
                exec(append_bot)
                if Points[bot] > 21:
                    Bust[bot] = True


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
    global Dealted
    Dealt_vid()
    Dealt_card()
    return "Play"


def Play():
    global counter_disapear
    bg = pygame.image.load(f"data/screen/Playing/{Bots}bots.png")
    pygame.Surface.blit(screen, bg, (0, 0))
    text(f"You're bet {Bucks_bet} bucks", 783, 60, white, 70)
    Display_dealer()
    Display_chip()
    Display_points((783, 596), 0, white)
    Display_card_player_playing()
    if Selector == "Player":
        Hit()
        if Stay() == "End":
            Bot_hit()
            Display_card_bots_backside()
            text(
                f"Wait bots counting their cards:{50 - counter_disapear}",
                1280,
                166,
                white,
                30,
            )
            if counter_disapear == 50:
                counter_disapear = 0
                return "Summary"
            else:
                counter_disapear += 1
    return "Play"


def Summary():
    global winner
    bg = pygame.image.load(f"data/screen/Ending/{Bots}bots.png")
    pygame.Surface.blit(screen, bg, (0, 0))
    Display_dealer()
    text(f"You're bet {Bucks_bet} bucks", 783, 60, white, 70)
    # Display Points Player
    Display_points((Points_pos[0], 564), 0, white)
    # Display Points Bots
    if Bots < 3:
        # Ex:Bots = 1, loop (2 -> Bots + 1 = 2) cause start from 2 => loop (2 -> Bots + 2=2,3)
        start_bot = 2
        end_bot = Bots + 2
    else:
        # Ex:Bots = 3, loop (1 -> Bots + 2 = 1,2,3) cause start from 1 => loop (1 -> Bots + 1=1,2,3)
        start_bot = 1
        end_bot = Bots + 1
    for bot in range(start_bot, end_bot):
        Display_points((Points_pos[bot], 564), bot, white)
    Display_card_end()
    winner = Calculating()
    if winner != None:
        return "End"
    return "Summary"


def End():
    bg = pygame.image.load(f"data/screen/Ending/{Bots}bots.png")
    pygame.Surface.blit(screen, bg, (0, 0))
    Display_dealer()
    text(f"You're bet {Bucks_bet} bucks", 783, 60, white, 70)
    Winner_light(winner)
    Display_card_end()
    return "End"


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
    if running_screen == "Summary":
        running_screen = Summary()
    if running_screen == "End":
        running_screen = End()
    pygame.display.flip()
    fps.tick(60)
