import pygame
import random

# Game settings
WIDTH = 480
HEIGHT = 600
FPS = 60

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Define a new event type for spawning PowerUps
POWERUP_SPAWN = pygame.USEREVENT + 1

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.Surface((50, 50))
        self.image = self.original_image.copy()
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shrink(self):
        self.image = pygame.transform.scale(self.original_image, (25, 25))
        self.image.fill(WHITE)  # Fill the new surface with a color
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset_size(self):
        self.image = self.original_image.copy()
        self.image.fill(WHITE)  # Fill the new surface with a color
        self.rect = self.image.get_rect(center=self.rect.center)

class Block(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        block_size = random.randint(20, 50)  # Random size between 20 and 50
        self.image = pygame.Surface((block_size, block_size))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        powerup_size = 30  # Fixed size for power-ups
        self.image = pygame.Surface((powerup_size, powerup_size))
        self.image.fill(GREEN)  # Green color for power-ups
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

def main_menu():
    menu_font = pygame.font.Font(None, 50)
    start_button = pygame.Rect(WIDTH / 2 - 70, HEIGHT / 2 - 20, 140, 40)  # Define a button area
    while True:
        screen.fill((0, 0, 0))
        text = menu_font.render("Start", True, WHITE)
        pygame.draw.rect(screen, GREEN, start_button)  # Draw the button
        screen.blit(text, [WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                if start_button.collidepoint(event.pos):  # Check if click is within button area
                    return
            if event.type == pygame.KEYDOWN:  # Check for key press
                if event.key == pygame.K_UP:  # Check if up arrow key is pressed
                    return

def pause_menu():
    menu_font = pygame.font.Font(None, 50)
    resume_button = pygame.Rect(WIDTH / 2 - 70, HEIGHT / 2 - 70, 140, 40)  # Define a button area
    quit_button = pygame.Rect(WIDTH / 2 - 70, HEIGHT / 2 + 20, 140, 40)  # Define a button area
    while True:
        screen.fill((0, 0, 0))
        resume_text = menu_font.render("Resume", True, WHITE)
        quit_text = menu_font.render("Quit", True, WHITE)
        pygame.draw.rect(screen, GREEN, resume_button)  # Draw the button
        pygame.draw.rect(screen, RED, quit_button)  # Draw the button
        screen.blit(resume_text, [WIDTH / 2 - resume_text.get_width() / 2, HEIGHT / 2 - 70 + resume_text.get_height() / 2])
        screen.blit(quit_text, [WIDTH / 2 - quit_text.get_width() / 2, HEIGHT / 2 + 20 + quit_text.get_height() / 2])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse click
                if resume_button.collidepoint(event.pos):  # Check if click is within button area
                    return
                if quit_button.collidepoint(event.pos):  # Check if click is within button area
                    pygame.quit()
                    quit()
            if event.type == pygame.KEYDOWN:  # Check for key press
                if event.key == pygame.K_p:  # Check if "P" key is pressed
                    return

# Game loop
running = True
while running:
    all_sprites = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)
    for i in range(8):
        b = Block()
        all_sprites.add(b)
        blocks.add(b)

    # Set a timer to spawn a PowerUp every 15 seconds
    pygame.time.set_timer(POWERUP_SPAWN, 15000)

    # Call the main_menu function before the game loop
    main_menu()

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game when the "P" key is pressed
                    pause_menu()
            if event.type == pygame.USEREVENT:
                player.reset_size()
            if event.type == POWERUP_SPAWN:  # Spawn a new PowerUp
                p = PowerUp()
                all_sprites.add(p)
                powerups.add(p)

        all_sprites.update()

        hits = pygame.sprite.spritecollide(player, blocks, False)
        if hits:
            break

        powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
        for powerup in powerup_hits:
            player.shrink()
            pygame.time.set_timer(pygame.USEREVENT, 10000)  # Reset size after 10 seconds

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    if not running:
        break

pygame.quit()
