import sys
import os
import json

import pygame as pg


from settings import *
from paddle import Paddle
from ball import Ball
from button import *
from bricks import Bricks
from scoreboard import Scoreboard, SCORES_FILE

pg.init()
screen = pg.display.set_mode((WIDTH,HEIGHT))



def font(size):
    return pg.font.SysFont('Arial', size)

def main_menu():
    pg.display.set_caption("Menu")

    while True:
        screen.fill("AntiqueWhite")

        MENU_MOUSE_POS = pg.mouse.get_pos()

        MENU_TEXT = font(50).render("MAIN MENU", True, (0,0,0))
        MENU_RECT = MENU_TEXT.get_rect(center = (200, 50))

        PLAY_BUTTON = Button(None, pos = (125, 150),
                                text_input = "PLAY", font = font(50), base_color="black", hovering_color = "white")

        LEADERBOARD_BUTTON = Button(None , pos = (240, 250), text_input = "LEADERBOARD",
                                font = font(50), base_color = "black", hovering_color = "white")
        QUIT_BUTTON = Button(None,pos = (125, 350), text_input = "QUIT", font = font(50),
                             base_color = "Black", hovering_color = "white")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, LEADERBOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if LEADERBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    leaderboard()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pg.quit()
                    sys.exit()
        pg.display.update()





def play():

    pg.display.set_caption("Breakout Game")

    clock = pg.time.Clock()

    pad = Paddle(paddle_x, paddle_y)
    ball = Ball(ball_x, ball_y, screen)
    bricks = Bricks(screen, brick_width, brick_height)
    score = Scoreboard(text_x, color, screen)
    score.set_high_score()


    while True:
        screen.fill(BG_Color)
        pad.appear(screen)
        bricks.show_bricks()
        score.show_scores()
        ball.move()

        ball.check_for_contact_on_x()
        ball.check_for_contact_on_y()


        for i, brick in enumerate(bricks.bricks):
            if brick.collidepoint(ball.x, ball.y - ball.radius) or brick.collidepoint(ball.x, ball.y + ball.radius):
                del bricks.bricks[i]
                del bricks.bricks_colors[i]
                ball.bounce_y()
                score.score += 1
                break


        if pad.rect.y < ball.y + ball.radius < pad.rect.y + pad.height and pad.rect.x < ball.x + ball.radius < pad.rect.x + pad.width:
            ball.bounce_y()
            ball.y = pad.y - ball.radius

        if ball.y + ball.radius >= 580:
            ball.y = pad.y - ball.radius
            pg.time.delay(2000)
            score.lives -=1
            ball.bounce_y()

        #check quit
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        #check for key presses
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            pad.move_right()
        if keys[pg.K_LEFT]:
            pad.move_left()

        if score.check_game_over() or len(bricks.bricks) == 0:
            if score.game_over():
                return

        pg.display.flip()

        #Frame Rate
        clock.tick(60)

def leaderboard():
    pg.display.set_caption("Leaderboard")

    title_font = font(50)
    entry_font = font(30)

    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                scores = json.load(f)
        except json.JSONDecodeError:
            scores = []

    else:
        scores = []



    while len(scores) < 10:
        scores.append({"name": "---", "score": "---"})

    running = True
    while running:
        screen.fill("AntiqueWhite")

        title_leaderboard = title_font.render("LEADERBOARD", True, (0 ,0 ,0))
        screen.blit(title_leaderboard, (WIDTH // 2 - title_leaderboard.get_width() // 2, 50))

        y = 150
        for i in range(10):
            name = scores[i]["name"]
            score = scores[i]["score"]
            entry_leaderboard = entry_font.render(f"{i+1}: {name} - {score}", True, (0, 0, 0))
            screen.blit(entry_leaderboard, (WIDTH // 2 - entry_leaderboard.get_width() // 2, y))
            y += 40

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                running = False
        pg.display.flip()


if __name__ == '__main__':
    main_menu()
