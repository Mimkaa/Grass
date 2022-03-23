import pygame as pg
import sys
from settings import *
from objects import *
from os import path
from testing import *
import random
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.draw_rects=False
        self.draw_hit_rects=False

    def load_data(self):
        self.font=path.join("PixelatedRegular-aLKm.ttf")
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        # do not create with vectors if you wanna create a copy later as the copy will contain the reference to the same vector hence the originals will be changing  too
        #self.grass=Grass([WIDTH//2,HEIGHT//2],[[0,100],[25,0],[50,100]])
        #self.grass = Grass([WIDTH // 2, HEIGHT // 2], [[-25, 50], [0, -50], [25, 50]])
        self.grass=[]
        for i in range(50):
            self.grass.append(Grass(self,[WIDTH // 2+(random.randint(-100,100)), HEIGHT // 2+(random.randint(-100,100))], [[-5, 0], [0, -100], [5, 0]]))
        self.object=Testing(self,vec(100,100))
        self.wind=Wind(self,(WIDTH/2,HEIGHT/2),WIDTH/20,HEIGHT)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        # layer management
        for spr in self.all_sprites:

                self.all_sprites.change_layer(spr, spr.hit_rect.bottom)

        for g in self.grass:
            #g.update()
            g.rotate_following(self.object)
            g.wind_reaction(self.wind)



    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        for spr in self.all_sprites:
            self.screen.blit(spr.image,spr.rect)
        #
        # for g in self.grass:
        #     pg.draw.polygon(self.screen,GREEN,g.points)
        if self.draw_rects:
            for spr in self.all_sprites:
                pg.draw.rect(self.screen,RED,spr.rect,1)

        if self.draw_hit_rects:
            for spr in self.all_sprites:
                pg.draw.rect(self.screen, BLUE, spr.hit_rect, 1)

        # fps
        self.draw_text(str(int(self.clock.get_fps())), self.font, 40, WHITE, 50, 50, align="center")

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key==pg.K_r:
                    self.draw_rects=not self.draw_rects
                if event.key == pg.K_h:
                    self.draw_hit_rects = not self.draw_hit_rects
                



# create the game object
g = Game()
g.new()
g.run()
