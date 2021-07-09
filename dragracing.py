import pygame  # pip install pygame
import time  # standard library
import random  # standard library
import os # standard library

pygame.init()


# Player class for rock and car
class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, image_scale):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, image_scale)
        img.convert_alpha()
        img.set_colorkey((248, 244, 244))

        self.images.append(img)
        self.image = self.images[0]

        self.rect = self.image.get_rect()

        self.move_x = 0
        self.move_y = 0

    def control(self, x, y):
        self.move_x += x
        self.move_y += y

    def update(self):
        self.rect.x = self.rect.x + self.move_x
        self.rect.y = self.rect.y + self.move_y


# Paths to images
current_working_dir = os.path.dirname(os.path.abspath(__file__))
stage_path = current_working_dir + r'\stage.png'
car_path = current_working_dir + r'\car_sprite.png'
rock_path = current_working_dir + r'\rock.png'
icon_path = current_working_dir + r'\car.png'

# Screen width and height
screen_w = 800
screen_h = 600

# Initialize screen
screen = pygame.display.set_mode([screen_w, screen_h])
screen_box = screen.get_rect()
screen_fill = (255, 255, 255)

# Create sprite group
car_and_rock = pygame.sprite.Group()

# Create car image
car_image = pygame.image.load(car_path)
car_scaling = (int(860 / 8), int(1361 / 8))

# Create car sprite
car = Player(car_path, car_scaling)
car.rect.x = 0
car.rect.y = screen_h - 200
car_and_rock.add(car)

# Create rock image
rock_image = pygame.image.load(rock_path)
rock_scaling = (int(600 / 4), int(575 / 4))

# Create rock sprite
rock = Player(rock_path, rock_scaling)
rock.rect.x = 300
rock.rect.y = 0
car_and_rock.add(rock)

# Scale images
car_image = pygame.transform.scale(car_image, car_scaling)
rock_image = pygame.transform.scale(rock_image, rock_scaling)

# Stage
stage_image = pygame.image.load(stage_path)
stage_image = pygame.transform.scale(stage_image, (screen_w, 900))

stage_y = 0
stage_y2 = stage_image.get_width()

# FPS and velocity of sprites
fps = 750
vel = 2
score = 0

# Display screen
screen_title = "Drag Racing!"
screen.fill(screen_fill)
screen_icon = pygame.image.load(icon_path)
pygame.display.set_caption(screen_title)
pygame.display.set_icon(screen_icon)

# Game loop
running = True
while running:
    rock.move_y = vel
    time.sleep(1 / fps)

    stage_y -= vel
    stage_y2 -= vel

    if stage_y < stage_image.get_width() * -1:
        stage_y = stage_image.get_width()

    if stage_y2 < stage_image.get_width() * -1:
        stage_y2 = stage_image.get_width()

    screen.fill(screen_fill)
    car.update()
    rock.update()

    screen.blit(stage_image, (0, -stage_y))
    screen.blit(stage_image, (0, -stage_y2))

    if rock.rect.y > 600:
        rock.rect.y = -200
        rock.rect.x = random.randint(100, 600)
        score += 1
        vel += 0.5

    # Collision detection
    if pygame.Rect.colliderect(car.rect, rock.rect) or pygame.Rect.colliderect(rock.rect, car.rect):
        running = False

    score_font = pygame.font.Font(None, 50)
    score_surf = score_font.render("Score: " + str(score), True, (0, 0, 0))
    score_pos = [10, 10]
    screen.blit(score_surf, score_pos)

    for event in pygame.event.get():

        # Exit program using X button
        if event.type == pygame.QUIT:
            running = False

        # Car movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and car.move_x != -1:
                car.control(-vel, 0)
            if event.key == pygame.K_RIGHT and car.move_x != 1:
                car.control(vel, 0)

        # Stop car if let go of key
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                car.move_x = 0

    if car.rect.x < 100:
        car.rect.x = 100
    if car.rect.x > 600:
        car.rect.x = 600

    car_and_rock.draw(screen)
    pygame.display.flip()
    pygame.display.update()
