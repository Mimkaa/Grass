import pygame as pg
import math
from settings import *
vec=pg.Vector2

class Wind(pg.sprite.Sprite):
    def __init__(self,game,pos,width,height):
        self.hit_rect=pg.Rect(0,0,width,height)
        self.game=game
        self.groups=self.game.all_sprites
        super().__init__(self.groups)
        self.pos=vec(pos)
        self.hit_rect.center=self.pos
        self.vel=vec(0,0)
        self.speed=400
        self.image=pg.Surface((width,height),pg.SRCALPHA)
        self.rect=self.hit_rect.copy()
    def update(self):
        self.vel=vec(self.speed*self.game.dt,0)
        self.pos+=self.vel
        self.vel.x+=self.speed
        if self.pos.x>WIDTH:
            self.pos.x=0
        self.hit_rect.center=self.pos
        self.rect.center=self.pos



class Grass(pg.sprite.Sprite):
    def __init__(self,game,pos,points):
        self.group=game.all_sprites
        self.pos=vec(pos)
        self.originals=[vec(i) for i in points]
        self.points=[vec(i) for i in points]
        self.acc=0
        self.vel=0
        self.gravity=1
        self.angle=0
        self._layer = 1
        super().__init__(self.group)

    def wind_reaction(self,obj):
        if obj.hit_rect.colliderect(self.hit_rect):
            self.angle+=0.1

    def rotate_following(self,obj):
        self.hit_rect = pg.Rect(0, 0, 10, 10)
        self.hit_rect.center = self.pos
        if obj.hit_rect.colliderect(self.hit_rect) :
            # point_vec = ((self.pos) - obj.pos-vec(0,obj.rect.height/2)).normalize()
            if obj.dir_vec!=vec(0,-1):
                if ((self.pos) - vec(obj.hit_rect.center)).length()>0:
                    point_vec = ((self.pos) - vec(obj.hit_rect.center)).normalize()
                    self.angle=math.atan2(point_vec.x, point_vec.y)
            else:
                if (vec(obj.hit_rect.center)-(self.pos)).length()>0:
                    point_vec = (vec(obj.hit_rect.center)-(self.pos)).normalize()
                    self.angle=-math.atan2(point_vec.x, point_vec.y)

        else:

            force=self.gravity*math.sin(self.angle)
            self.acc=(-1*force)/100
            self.vel+=self.acc
            self.angle+=self.vel
            self.vel*=0.93
            if abs(self.vel)<0.00001:
                self.vel=0








    def update(self):

        for n, point in enumerate(self.points):
            self.points[n].x = (self.originals[n].x * math.cos(self.angle) - self.originals[n].y * math.sin(
                self.angle))
            self.points[n].y = (self.originals[n].x * math.sin(self.angle) + self.originals[n].y * math.cos(
                self.angle))

        x_vals=[v.x for v in self.points]
        y_vals=[v.y for v in self.points]
        min_x=min(x_vals)
        min_y=min(y_vals)
        max_x=max(x_vals)
        max_y=max(y_vals)
        width=max_x-min_x
        height=max_y-min_y
        self.image=pg.Surface((width,height),pg.SRCALPHA)
        self.rect=self.image.get_rect()

        # the center of the tri
        center_triangle=vec(0,0)
        for v in self.points:
            center_triangle+=v
        center_triangle/=3

        offset = self.rect.center - center_triangle
        draw_points = [v.copy() + offset for v in self.points]

        # displacing the tri by the extend of intersection with the rect

        sides=[vec(self.rect.topleft),vec(self.rect.topright),vec(self.rect.bottomright),vec(self.rect.bottomleft)]
        displacement=vec(0,0)

        new_center_triangle = vec(0, 0)
        for v in draw_points:
            new_center_triangle += v
        new_center_triangle /= 3

        for n, q in enumerate(draw_points):
            line_p1s=new_center_triangle
            line_p1e=draw_points[n]



            for n,v in enumerate(sides):
                line_p2s = sides[n]
                line_p2e = sides[(n + 1) % len(sides)]
                d = (line_p2e.x - line_p2s.x) * (line_p1s.y - line_p1e.y) - (line_p1s.x - line_p1e.x) * (
                            line_p2e.y - line_p2s.y)
                if d != 0:
                    t1 = ((line_p2s.y - line_p2e.y) * (line_p1s.x - line_p2s.x) + (line_p2e.x - line_p2s.x) * (
                                line_p1s.y - line_p2s.y)) / d
                    t2 = ((line_p1s.y - line_p1e.y) * (line_p1s.x - line_p2s.x) + (line_p1e.x - line_p1s.x) * (
                                line_p1s.y - line_p2s.y)) / d

                    if t1 >= 0 and t1 < 1. and t2 >= 0. and t2 < 1.:
                        displacement.x += (1 - t1) * (line_p1e.x - line_p1s.x)
                        displacement.y += (1 - t1) * (line_p1e.y - line_p1s.y)


        draw_points = [v.copy() - displacement for v in draw_points]
        pg.draw.polygon(self.image,GREEN,draw_points)
        pg.draw.polygon(self.image, BLACK, draw_points,1)
        self.rect.center=self.pos+center_triangle
        self.hit_rect=pg.Rect(0,0,10,10)
        self.hit_rect.center=self.pos














