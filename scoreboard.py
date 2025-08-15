import sys


import pygame as pg
import json
import os


SCORES_FILE = "scores.json"

#most parts used a guide, implemented the saving of scores for a scoreboard
class Scoreboard:
    def __init__(self, x, color, screen):
        self.screen = screen
        self.color = color
        self.x = x
        self.score = 0
        self.high_score = 0
        self.lives = 2
        self.font = pg.font.SysFont("arial", 20)

    def show_scores(self):
        score_text = self.font.render(f"Score: {self.score}", True, self.color)
        high_score_text = self.font.render(f"High score: {self.high_score}", True, self.color)
        lives_text = self.font.render(f"Lives: {self.lives}", True, self.color)

        score_text_rect = score_text.get_rect(topleft = (self.x, 10))
        high_score_text_rect = high_score_text.get_rect(topleft = (self.x, 30))
        lives_text_rect = lives_text.get_rect(topleft = (self.x, 70))

        self.screen.blit(score_text,score_text_rect )
        self.screen.blit(high_score_text, high_score_text_rect )
        self.screen.blit(lives_text, lives_text_rect )

    def check_game_over(self):
        if self.lives == 0:
            return True
        return False

    def game_over(self):
        game_over_color = "blue"
        game_over_font = pg.font.SysFont("Arial", 30)
        game_over_text = game_over_font.render("Game Over!", True, game_over_color)
        self.screen.blit(game_over_text, (50, 300))
        pg.display.flip()

        pg.time.delay(1000)


        player_name = self.text_input("Enter you name")
        self.save_score(player_name, self.score)
        self.record_high_score()

        return True

    def save_score(self, player_name, score):
        if os.path.exists(SCORES_FILE):
            with open(SCORES_FILE, "r") as f:
                scores = json.load(f)
        else:
            scores = []

        scores.append({"name": player_name, "score": score})

        scores = sorted(scores, key = lambda x:x["score"], reverse = True)

        with open(SCORES_FILE, "w") as f:
            json.dump(scores, f, indent = 4)

    def text_input(self, prompt):
        font = pg.font.SysFont("arial", 30)
        input_txt = ""
        active = True

        while active:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        active = False
                    elif event.key == pg.K_BACKSPACE:
                        input_txt = input_txt[:-1]
                    else:
                        input_txt += event.unicode

                    self.screen.fill((0, 0, 0))
                    prompt_surface = font.render(prompt, True, (255, 255, 255))
                    input_surface = font.render(input_txt, True, (0, 255, 0))

                    self.screen.blit(prompt_surface, (50, 200))
                    self.screen.blit(input_surface, (50, 250))
                    pg.display.flip()

        return input_txt

    def set_high_score(self):
        try:
            with open("records.txt", "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            with open("records.txt", "w") as data:
                data.write("0")
                score = 0
        else:
            score = lines[0]

            self.high_score = int(score)

    def record_high_score(self):
        if self.score > self.high_score:
            with open("records.txt", "w") as file:
                file.write(f"{self.score}")


