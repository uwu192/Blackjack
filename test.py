import pygame
import sys
import os

# Khởi tạo Pygame
pygame.init()

# Cài đặt màn hình và các thông số khác
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BG_COLOR = (255, 255, 255)


# Hàm con để tạo sprite
def create_sprite(image, pos):
    sprite = MovingSprite(image, pos)
    return sprite


# Hàm con để cập nhật vị trí của sprite
def update_sprite(sprite, target_pos):
    sprite.target_pos = target_pos
    sprite.update()


# Tạo một lớp Sprite cho đối tượng cần di chuyển
class MovingSprite(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.target_pos = None

    def update(self):
        if self.target_pos:
            # Tính toán hướng và khoảng cách tới điểm đích
            direction = pygame.math.Vector2(self.target_pos) - pygame.math.Vector2(
                self.rect.center
            )
            distance = direction.length()
            # Nếu khoảng cách lớn hơn 1 pixel, tiến hành di chuyển
            if distance > 1:
                direction.normalize_ip()
                self.rect.move_ip(
                    direction * min(distance, 5)
                )  # Chỉ di chuyển tối đa 5 pixel mỗi lần cập nhật


# Khởi tạo màn hình
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Sprite")

# Đường dẫn đến thư mục chứa các sprite
sprite_folder = "data/chip"

# Kiểm tra xem thư mục có tồn tại không
if not os.path.exists(sprite_folder):
    print("Thư mục không tồn tại.")
    pygame.quit()
    sys.exit()

# Tạo một danh sách để lưu trữ các sprite
sprites = []

# Duyệt qua tất cả các tệp trong thư mục sprite và tạo sprite cho mỗi tệp
for file_name in os.listdir(sprite_folder):
    if file_name.endswith(".png"):  # Chỉ xử lý các tệp PNG
        file_path = os.path.join(sprite_folder, file_name)
        sprite_image = pygame.image.load(file_path).convert_alpha()
        sprite = create_sprite(
            sprite_image, (100, 100)
        )  # Đặt vị trí ban đầu ở (100, 100)
        sprites.append(sprite)

# Vòng lặp chính
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BG_COLOR)

    # Cập nhật và vẽ tất cả các sprite
    for sprite in sprites:
        update_sprite(sprite, (400, 300))  # Cập nhật vị trí đích cho mỗi sprite
        screen.blit(sprite.image, sprite.rect)  # Vẽ sprite ở vị trí mới

    # Kiểm tra sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
