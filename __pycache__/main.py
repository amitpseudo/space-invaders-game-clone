import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Initialize the mixer
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load('bground.png')

# Background music
pygame.mixer.music.load('02. Select Your Ship.mp3')
pygame.mixer.music.play(-1)  # Play the music indefinitely

# Load game over sound effect
gameover_sound = pygame.mixer.Sound('gameover.wav')

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('arcade-game.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = pygame.image.load('monster.png')
enemyX = random.randint(0, 735)
enemyY = random.randint(20, 150)
enemyX_change = 1
enemyY_change = 40

# Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 3
bullet_state = "ready"
num_of_enemy = 1

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over Font
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(X, Y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (X, Y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(X, Y):
    screen.blit(playerImg, (X, Y))


def enemy(X, Y):
    screen.blit(enemyImg, (X, Y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
game_over = False
while running:

    # Fill the background
    screen.fill((0, 0, 0))

    # Draw the background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keystroke is pressed, check if left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    if not game_over:
        # Move player and boundaries
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Move enemy
        enemyX += enemyX_change
        if enemyX <= 0:
            enemyX_change = 1
            enemyY += enemyY_change
        elif enemyX >= 736:
            enemyX_change = -1
            enemyY += enemyY_change

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state == "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        # Collision detection
        collision = iscollision(enemyX, enemyY, bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX = random.randint(0, 735)
            enemyY = random.randint(20, 150)

        # Check if the enemy crosses the player (game over condition)
        if enemyY > playerY - 40:  # Assuming the enemy crosses near the player's y-coordinate
            gameover_sound.play()  # Play game over sound
            game_over = True

        # Draw player, enemy, and score
        player(playerX, playerY)
        enemy(enemyX, enemyY)
        show_score(textX, textY)

    else:
        # If game over, show game over text
        game_over_text()

    # Update the display
    pygame.display.update()
