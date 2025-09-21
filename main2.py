import pygame as pg
import sys
import random
from attacksfile import attacks_class
from attacksfile import heart_attack


class Setup():
    def __init__(self):
        self.display_width = 800
        self.display_height = 800
        self.screen = pg.display.set_mode((self.display_width,self.display_height))
        self.font_hp = pg.font.Font("assets/font/BebasNeue-Regular.ttf", 30)
        self.intro_font = pg.font.Font("assets/font/PressStart2P-Regular.ttf", 40)

        self.box_width = 600
        self.box_height = 300

        self.game_name = "Undertale_lite"
        self.game_active = True
        self.game_over = False
    
    def Intro(self):
        if self.game_active == False and self.game_over == False:
            introheadline = self.intro_font.render(self.game_name, True, "white")
            text_width, text_height = self.intro_font.size(self.game_name)
            x = (self.display_width - text_width)//2
            y = self.display_height // 4
            self.screen.fill("black")
            self.screen.blit(introheadline, (x,y))


class undertale():
    def __init__(self):
        self.s = Setup()
        self.h = heart()
        self.a = attacks_class()
        self.a_t = heart_attack()
        self.b = Boss()
        
        
        self.whitebox = pg.Rect((self.s.display_width - 600)//2, 350, self.s.box_width, self.s.box_height)
        self.last_attack = pg.time.get_ticks()
        self.current_atk = None
        self.transition = False
        self.attack_list = [(self.a.bigbone_attack, self.a.normal_attack_h),
                            (self.a.normal_attack_h, self.a.normal_attack_v),
                            (self.a.long_bone_attack, self.a.normal_attack_v)
                            ]



    def update(self):
        self.h.movement()
        self.h.box_limit(self.whitebox)
        now = pg.time.get_ticks()
        self.b.boss_show(self.s)
        self.b.boss_hp_show(self.s, self.whitebox)
        self.h.spawn_hp(self.s, self.whitebox)
        self.a_t.bomb_spawn(self.s, self.whitebox, self.h)
        self.a_t.bullet_spawn(self.s, self.whitebox, self.h)
        if now - self.last_attack > 10000 or self.current_atk == None:
            if now - self.last_attack > 10000:
                 self.transition = True
            if not self.a.attack_list_h and not self.a.attack_list_v:
                if not self.a.long_bone_rect and not self.a.bigbone_r:
                    self.current_atk = random.choice(self.attack_list)
                    self.last_attack = now
                    self.transition = False
        for atk in self.current_atk:
                atk(self.s, self.whitebox, self.h, self.transition)
        # self.h.show_hp(self.s, self.whitebox)

    
    def mainloop(self):
        clock = pg.time.Clock()
        pg.display.set_caption("untertale")
        while True:
            for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        letter = event.unicode
                        if letter == "e":
                            self.a_t.apply_damage(self.b, "bomb")
                        elif letter == "r":
                            self.a_t.apply_damage(self.b, "bullet")
                    
            
            if self.s.game_active == True:
                self.s.screen.fill("black")
                self.s.screen.blit(self.h.heart, self.h.heart_r)
                pg.draw.rect(self.s.screen, color= "white", rect = self.whitebox, width= 3)
                self.h.draw_health_bar(self.s, self.whitebox)
                self.a_t.draw_bomb_count(self.s, self.whitebox, self.h.health_bar_box)
                self.update()
            
            if self.s.game_active == False:
                self.s.Intro()


            pg.display.update()
            clock.tick(60)

class heart():
    def __init__(self):
        self.heart = pg.image.load("assets/heart_t.png").convert_alpha()
        self.heart_r = self.heart.get_rect(center = (Setup().display_width/2, 600))

        self.heart_hp = pg.image.load("assets/heart_refill.png").convert_alpha()
        self.heart_hp_r = None
        
        self.health_bar_box = None
        
        self.heart_invi = pg.image.load("assets/heart_invic.png").convert_alpha()
        self.heart_invic = None
        
        self.heart_spawn = pg.time.get_ticks()
        self.heart_invi_spawn = pg.time.get_ticks()

        self.max_hp = 1000
        self.hp = 1000
        self.invincible = 0
        self.speed = 4
        self.diagonal = False
    def movement(self):
            dx, dy = 0,0
            key = pg.key.get_pressed()
            self.diagonal = True
            if key[pg.K_LEFT] or key[pg.K_a]:
                dx -= self.speed
            if key[pg.K_RIGHT] or key[pg.K_d]:
                 dx += self.speed
            if key[pg.K_UP] or key[pg.K_w]:
                 dy -= self.speed
            if key[pg.K_DOWN] or key[pg.K_s]:
                 dy += self.speed
            if dx !=0 and dy != 0 :
                dx *= 0.707
                dy *= 0.707 
            self.heart_r.x += dx
            self.heart_r.y += dy
            
    def box_limit(self, box):
        if self.heart_r.right > box.right - 3:
            self.heart_r.right = box.right - 3
        if self.heart_r.top < box.top + 3:
            self.heart_r.top = box.top + 3
        if self.heart_r.bottom > box.bottom - 3:
             self.heart_r.bottom = box.bottom - 3
        if self.heart_r.left < box.left + 3:
             self.heart_r.left = box.left + 3


    def draw_health_bar(self, setup, box):
        if self.hp >= 1000:
            self.hp = 1000
        if self.hp <= 0:
            setup.game_active = False
            self.hp = 0
        self.health_bar_box = pg.Rect(box.left, box.bottom + 50, 200, 30)
        pg.draw.rect(setup.screen, color= "white", rect= self.health_bar_box, width=2)
        health = pg.Rect(box.left + 10 , box.bottom + 60, 180*(self.hp/self.max_hp) , 10)
        pg.draw.rect(setup.screen, color= "white", rect= health)


    def spawn_hp(self, setup, box):
        now = pg.time.get_ticks()
        if self.heart_hp_r is None:
            if now - self.heart_spawn > 6000:
                self.heart_hp_r = self.heart_hp.get_rect(center = (random.randint(box.left + 10 , box.right - 10), random.randint(box.top +10, box.bottom -10)))
        if self.heart_invic is None:
             if now - self.heart_invi_spawn > 6500:
                self.heart_invic = self.heart_invi.get_rect(center = (random.randint(box.left + 10 , box.right - 10), random.randint(box.top +10, box.bottom -10)))
        if self.heart_hp_r:
            setup.screen.set_clip(box)
            setup.screen.blit(self.heart_hp, self.heart_hp_r)
            
            if self.heart_hp_r.colliderect(self.heart_r):
                self.hp += 84
                self.heart_spawn = now
                self.heart_hp_r = None
        if self.heart_invic:
            setup.screen.set_clip(box)
            setup.screen.blit(self.heart_invi, self.heart_invic)
            if self.heart_invic.colliderect(self.heart_r):
                self.invincible = now + 1500
                self.heart_invi_spawn = now
                self.heart_invic = None
        setup.screen.set_clip(None)

class Boss():
    def __init__(self):
        # self.boss_1 = pg.image.load("assets/boss/boss_front.png").convert_alpha()
        self.boss_2 = pg.image.load("assets/boss/boss_side_2.png").convert_alpha()
        self.boss_3 = pg.image.load("assets/boss/boss_side1.png").convert_alpha()
        self.boss_4 = pg.image.load("assets/boss/boss_side_3.png").convert_alpha()
        
        self.show_list = []
        self.show_list.extend([self.boss_3, self.boss_2, self.boss_4])
        self.transition = pg.time.get_ticks()
        self.hp = 5000
        self.max_hp = 5000
        
        self.index = 0
        self.loop = 1
    def boss_show(self, setup):
        now = pg.time.get_ticks()
        if now - self.transition > 2000:
            self.index += self.loop
            if self.index == 3 :
                self.index = 0
            self.transition = now
        boss = self.show_list[self.index].get_rect(midtop = (setup.display_width/2, 30))
        setup.screen.blit(self.show_list[self.index], boss)


    def boss_hp_show(self, setup, box):
        self.health_bar_box = pg.Rect(box.left, box.top -100, setup.box_width, 30)
        pg.draw.rect(setup.screen, color= "white", rect= self.health_bar_box, width=2)
        health = pg.Rect(box.left + 10 , box.top -90 , (setup.box_width-20)*(self.hp/self.max_hp) , 10)
        pg.draw.rect(setup.screen, color= "white", rect= health)
        
        


                    

        


    



if __name__ == "__main__":
    pg.init()
    game = undertale()
    game.mainloop()