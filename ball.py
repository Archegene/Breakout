import pygame as pg
from settings import ball_x_speed, ball_y_speed, ball_radius, ball_color

class Ball:
    #followed tutorial to help create file
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.radius = ball_radius
        self.color = pg.Color(ball_color)
        self.x_speed = ball_x_speed
        self.y_speed = ball_y_speed

    def move(self):
        pg.draw.circle(self.screen, self.radius, [self.x, self.y], self.radius)
        self.y -= self.y_speed
        self.x -= self.x_speed

    def bounce_x(self):
        self.x_speed *= -1

    def bounce_y(self):
        self.y_speed *= -1

    def check_for_contact_on_x(self):
        if self.x - self.radius <= 0 or self.x + self.radius >= self.screen.get_width():
            self.bounce_x()

    def check_for_contact_on_y(self):
        if self.y + self.radius <= 0:
            self.bounce_y()
