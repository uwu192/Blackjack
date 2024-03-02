import pygame
import os
import sys

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
# Background screen is running
running_screen = "Screen_Bet"
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
# Game
Bots = 1
Selector = "Dealer"


# Subprogram of detail--------------------------------------------
# Reset x,y after clicked
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


def bet():
    text("Place your Bet", width // 2 + 350, height // 2 - 450, white, 60)


# Movement sprite--------------------------------------------
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.target_pos = None

    def update(self):
        if self.target_pos:
            # Find way and length
            direction = pygame.math.Vector2(self.target_pos) - pygame.math.Vector2(
                self.rect.center
            )
            # Distance will convert in pixel
            distance = direction.length()
            if distance > 1:
                direction.normalize_ip()
                self.rect.move_ip(direction * min(distance, 5))


# Make this for easier movement input-------------------------


# Using this Subprogam before loop to create object sprite
def create_sprite(image, pos):
    sprite = MovingSprite(image, pos)
    return sprite


# Using this Subprogram in loop to move the object sprite
def update_sprite(sprite, target_pos):
    sprite.target_pos = target_pos
    sprite.update()


chips = []
# Loop create object chip
directory = "data/chip"
x_position_add = 0
count_chip = 0
for chip in os.listdir(directory):
    """Create count_chip because bet chip bot at center so that after display 3 chips,
    we need add more space to not display chips on bet chip box"""
    if count_chip < 3:
        x_position_add += 200
        count_chip += 1
    else:
        x_position_add += 400
        count_chip = 0
    file_path = os.path.join(directory, chip)
    chip_img = pygame.image.load(file_path)
    chip_img = pygame.transform.scale(chip_img, (200, 200))
    chip = create_sprite(chip_img, (x_position_add, 700))
    chips.append(chip)


# Subprogram of screen---------------------------------------
def Main_screen():
    bg = pygame.image.load("data/screen/Main_screen.png")
    pygame.Surface.blit(screen, bg, (0, 0))
    # Enter Setting screen
    if (919 > x) and (x > 731):
        if 685 > y > 416:
            return "Screen_setting"
    return "Main"


def Setting_screen():
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
    # Enter Play screen
    if 970 > x > 610:
        if 874 > y > 763:
            return "Screen_play"
    return "Screen_setting"


def Bet_screen():
    bg = pygame.image.load("data/screen/Play_screen.png")
    pygame.Surface.blit(screen, bg, (0, 0))
    bet()
    for chip in chips:
        update_sprite(chip, (400, 300))
        screen.blit(chip.image, chip.rect)
    return "Bet_screen"


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            y = event.pos[1]
    if running_screen == "Main":
        running_screen = Main_screen()
    if running_screen == "Screen_setting":
        running_screen = Setting_screen()
    if running_screen == "Screen_Bet":
        running_screen = Bet_screen()
    pygame.display.flip()
    fps.tick(60)
