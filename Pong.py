import pygame, sys, random
import button
import os

# General setup
pygame.init()
clock = pygame.time.Clock()

# Main Window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

# Colors
black = (0, 0, 0)
light_grey = (200, 200, 200)
light_blue = (173,216,230)
light_green =(144, 238, 144)
bg_color = pygame.Color((10, 60, 42))


# Game Rectangles
ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# Game Variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# Score Text
player_score = 0
opponent_score = 0
if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

#font variables
basic_font = pygame.font.Font('freesansbold.ttf', 32)
title_font = pygame.font.Font('freesansbold.ttf', 144)

# loading button images
play_img = pygame.image.load("images/play_button.png").convert_alpha()
quit_img = pygame.image.load("images/quit_button.png").convert_alpha()

#creating button instances
play_button = button.Button(555, 380, play_img, .5)
quit_button = button.Button(550, 530, quit_img, .5)

def HS_keeper() -> int:
    """
    This function records the high score and keeps track of it.
    :return: It returns the high score so it can be displayed on the screen.
    """
    global player_score, opponent_score, score, high_score
    if player_score > high_score:
        high_score = player_score
        with open('score.txt', 'w') as file:
            file.write(str(high_score))
    player_score = 0
    opponent_score = 0
    return high_score

def draw_text(text, title_font, light_grey, x, y) -> None:
    """
    This function helps draw text to the screen.
    :param text: Text you want to display.
    :param title_font: The font you want the text to be in.
    :param light_grey: The color of th text.
    :param x: The x position of the text.
    :param y: The y position of the text.
    """
    img = title_font.render(text, True, light_grey)
    screen.blit(img, (x, y))

def game_start():
    """
    This function intiates the game.
    """
    global player_score, player_speed, high_score, score, opponent_score

    def player_animation() -> None:
        """
        This function determines the player animation.
        """
        global player_speed

        if opponent_score != 0:
            player_speed = 0
        player.y += player_speed

        if player.top <= 0:
            player.top = 0
        if player.bottom >= screen_height:
            player.bottom = screen_height

    def ball_animation() -> None:
        """
        This funciton determines the ball animation.
        """
        global ball_speed_x, ball_speed_y, player_score, opponent_score, high_score, score

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= screen_height:
            ball_speed_y *= -1

        # Player Score
        if ball.left <= 0:
            ball_start()
            player_score += 1

        # Opponent Score
        if ball.right >= screen_width:
            ball_start()
            opponent_score += 1

        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1

    def opponent_ai() -> None:
        """
        This function determines what the opponent ai can do.
        """
        if opponent.top < ball.y:
            opponent.y += opponent_speed
        if opponent.bottom > ball.y:
            opponent.y -= opponent_speed

        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= screen_height:
            opponent.bottom = screen_height

    def ball_start() -> None:
        """
        This function controls how the ball starts.
        """
        global ball_speed_x, ball_speed_y

        ball.center = (screen_width / 2, screen_height / 2)
        ball_speed_y *= random.choice((1, -1))
        ball_speed_x *= random.choice((1, -1))

    while opponent_score == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                        player_speed -= 6
                if event.key == pygame.K_DOWN:
                        player_speed += 6
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player_speed += 6
                if event.key == pygame.K_DOWN:
                    player_speed -= 6
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()
            if event.type == pygame.QUIT:
                if score > high_score:
                    high_score = score
                    with open('score.txt', 'w') as file:
                        file.write(str(high_score))
                pygame.quit()
                quit()

        def pause() -> None:
            """
            This function pauses the game.
            """
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            return
                    if event.type == pygame.QUIT:
                        if opponent_score != 0:
                            if player_score > high_score:
                                high_score = player_score
                                with open('score.txt', 'w') as file:
                                    file.write(str(high_score))
                        pygame.quit()
                        quit()

        # Game Logic
        ball_animation()
        player_animation()
        opponent_ai()
        if opponent_score != 0:
            HS_keeper()
            start_screen()

        # Visuals
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_blue, player)
        pygame.draw.rect(screen, light_blue, opponent)
        pygame.draw.ellipse(screen, light_green, ball)
        pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))
        draw_text('High Score: ' + str(high_score), basic_font, light_grey, 660, 20)
        player_text = draw_text(f'Current score: {player_score}', basic_font, light_grey, 660, 70)
        pause_button = draw_text('Press the \'p\' to pause.', basic_font, light_grey, 660, 920)
        player_side_indicator = draw_text('Player side', basic_font, light_grey, 660, 440)
        pygame.display.flip()
        clock.tick(60)

def start_screen() -> None:
    """
    This function serves as the start screen when the code is started.
    """
    while True:
        pygame.event.clear()
        screen.fill((black))
        Start_screen = pygame.mouse.get_pos()
        draw_text("Menu", title_font, light_grey, 470, 200)
        if play_button.draw(screen):
            game_start()
            pygame.event.clear()
            break
        if quit_button.draw(screen):
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
start_screen()
