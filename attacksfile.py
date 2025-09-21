import pygame as pg
import random


class attacks_class():
    def __init__(self):
        self.group_long_h = pg.image.load("assets/attacks/long_atk_h_resized.png").convert_alpha()
        self.group_long_v = pg.image.load("assets/attacks/long_attack.png").convert_alpha()
        self.beam = pg.image.load("assets/attacks/beam.png").convert_alpha()
        self.single_bone_v = pg.image.load("assets/attacks/singlbone_vertical.png").convert_alpha()
        self.single_bone_h = pg.image.load("assets/attacks/singlbone_h.png").convert_alpha()
        self.longsingle_bone_v = pg.image.load("assets/attacks/singlverylongvertical.png").convert_alpha()
        self.bigbone_h = pg.image.load("assets/attacks/bigbone_h.png").convert_alpha()
        self.bigbone_v = pg.image.load("assets/attacks/bigbone_v.png").convert_alpha()

        self.attack_list_v = []
        self.last_attack_time_v = 0
        self.direction = 1
        self.speed = 3
        
        self.attack_list_h = []
        self.last_attack_time_h = 0

        self.long_bone_rect = None
        self.bigbone_r = None
        self.bigbone_l = None
    
    def normal_attack_h(self, setup, box, heart, transition):
        now = pg.time.get_ticks()
        self.transition = transition
        if now - self.last_attack_time_h > 350 and self.transition == False:
            choice = random.choice(["left","right"])
            if choice == "right":
                bone_rect = self.single_bone_h.get_rect(midleft = (box.right, random.randint(box.top+10, box.bottom-10)))
                dx = -self.speed
            elif choice == "left":
                bone_rect = self.single_bone_h.get_rect(midright = (box.left, random.randint(box.top+10, box.bottom-10)))
                dx = self.speed
            self.attack_list_h.append((bone_rect, dx))
            self.last_attack_time_h = now
        if self.attack_list_h:
            for i, dx in self.attack_list_h[:]:
                i.x += dx
                if i.colliderect(heart.heart_r):
                    if now > heart.invincible:
                        heart.hp -= 124
                        heart.invincible = now + 1500
                if i.right + 5 < box.left or i.left - 5 > box.right:
                    self.attack_list_h.remove((i,dx))
                if i.colliderect(box):
                    setup.screen.set_clip(box)
                    setup.screen.blit(self.single_bone_h, i)
                
        setup.screen.set_clip(None)


    def long_bone_attack(self, setup, box, heart, transition):
            now = pg.time.get_ticks()
            delay = 1000
            self.transition = transition
            if not hasattr(self, 'long_bone_rect') or (self.long_bone_rect == None):
                if self.transition == False:
                    self.top_bottom = random.choice(["top", "bottom"])
                    if self.top_bottom == "bottom":
                        self.long_bone_rect = self.group_long_h.get_rect(topleft=(box.left, box.bottom))
                        self.long_bone_dy = self.speed
                        self.target_y = random.randint(box.top + 100, box.bottom - 30)
                    else:
                        self.long_bone_rect = self.group_long_h.get_rect(bottomleft=(box.left, box.top))
                        self.long_bone_dy = -self.speed
                        self.target_y = random.randint(box.top + 30, box.bottom - 100)
                    self.showline = True
                    self.direction = 1
                    self.spawn_time = pg.time.get_ticks()
            
            if getattr(self, "showline", True):
                pg.draw.line(setup.screen, "white", (box.left, self.target_y), (box.right, self.target_y))
            
            

            if now -self.spawn_time > delay and self.long_bone_rect:
                self.long_bone_rect.y -= self.long_bone_dy
                if self.long_bone_rect and self.long_bone_rect.colliderect(box):
                    setup.screen.set_clip(box)
                    setup.screen.blit(self.group_long_h, self.long_bone_rect)

            if self.long_bone_rect and  self.direction == 1:
                if self.long_bone_rect.y <= self.target_y and self.top_bottom == "bottom":
                    self.long_bone_dy = -self.long_bone_dy
                    self.direction = 0
                    self.showline = False
                if self.long_bone_rect.bottom >= self.target_y and self.top_bottom == "top":
                    self.long_bone_dy = -self.long_bone_dy
                    self.direction = 0
                    self.showline = False
            if self.long_bone_rect:
                if self.long_bone_rect.colliderect(heart.heart_r):
                    if now > heart.invincible:
                        heart.hp -= 124
                        heart.invincible = now + 1500
                if self.long_bone_rect.top > box.bottom + 20 and self.direction == 0 and self.top_bottom == "bottom":
                    self.long_bone_rect = None
                elif self.long_bone_rect.bottom < box.top + 20 and self.direction == 0 and self.top_bottom == "top":
                    self.long_bone_rect = None
            setup.screen.set_clip(None)


    def normal_attack_v(self, setup, box, heart, transition):
        now = pg.time.get_ticks()
        self.transition = transition
        if now - self.last_attack_time_v > 350 and self.transition == False:
            choice = random.choice(["top", "bot"])
            if choice == "top":
                bone_rect = self.single_bone_v.get_rect(midbottom = (random.randint(box.left+10, box.right-10), box.top))
                dy = self.speed
            else:
                bone_rect = self.single_bone_v.get_rect(midtop = (random.randint(box.left+10, box.right-10), box.bottom))
                dy = -self.speed
            self.attack_list_v.append((bone_rect, dy))
            self.last_attack_time_v = now
        if self.attack_list_v:
            for bones, dy in self.attack_list_v[:]:
                bones.y += dy
                if bones.colliderect(heart.heart_r):
                    if now > heart.invincible:
                        heart.hp -= 124
                        heart.invincible = now + 1500
                
                if bones.top > box.bottom + 20 or bones.bottom < box.top - 20:
                    self.attack_list_v.remove((bones, dy))
                    
                if bones.colliderect(box):
                    setup.screen.set_clip(box)
                    setup.screen.blit(self.single_bone_v, bones)
                    
        setup.screen.set_clip(None)
        

    def bigbone_attack(self, setup, box, heart,transition):
        now = pg.time.get_ticks()
        self.transition = transition
        if not hasattr(self, "bigbone_r") or self.bigbone_r == None:
            if self.transition == False:
                self.bigbone_r = self.bigbone_v.get_rect(midleft = (box.right,(box.top + box.bottom)//2))
                self.bigbone_l = self.bigbone_v.get_rect(midright = (box.left, (box.top + box.bottom)//2))
                
                self.target_r = random.randint(box.right - 450, box.right - 25)
                self.target_l = self.target_r - 60
                self.condition = "moving"
                self.last = pg.time.get_ticks()
                self.wait_start = 0
        delay = 500
        if self.bigbone_r:
            if now - self.last > delay:
                self.bigbone_r.x -= 3
                self.bigbone_l.x += 3
                if self.bigbone_r.colliderect(box):
                    setup.screen.set_clip(box)
                    setup.screen.blit(self.bigbone_v, self.bigbone_r)
                if self.bigbone_l.colliderect(box):
                    setup.screen.set_clip(box)
                    setup.screen.blit(self.bigbone_v, self.bigbone_l)
            if self.bigbone_r.left <= self.target_r:
                self.bigbone_r.left = self.target_r
                
            if self.bigbone_l.right >= self.target_l:
                self.bigbone_l.right = self.target_l
            
            # if self.bigbone_l.colliderect(heart.heart_r) or self.bigbone_r.colliderect(heart.heart_r):
            #     if now > heart.invincible:
            #         heart.hp -= 32
            #         heart.invincible = now + 1500

            if heart.heart_r.x >= self.bigbone_r.left:
                heart.heart_r.x = self.bigbone_r.left
            if heart.heart_r.right <= self.bigbone_l.right :
                heart.heart_r.right = self.bigbone_l.right

            if self.bigbone_r.left <= self.target_r and self.bigbone_l.right >= self.target_l and self.condition == "moving":
                self.condition = "waiting"
                self.wait_start = now
            if self.condition == "waiting":
                if now - self.wait_start > 4000:
                    self.bigbone_r = None
                    self.bigbone_l = None
            
        setup.screen.set_clip(None)    
        

class heart_attack():
    def __init__(self):
        self.bomb = pg.image.load("assets/bomb.png").convert_alpha()
        self.bomb_r = None
        self.bomb_timer = pg.time.get_ticks()
        self.bombcount = 0
        self.bomb_damage = 35

        self.bullet = pg.image.load("assets/bullet.png").convert_alpha()
        self.bullet_count_img = pg.image.load("assets/bullet_show.png").convert_alpha()
        self.bullet_r = None
        self.bullet_timer = pg.time.get_ticks()
        self.bulletcount = 0
        self.bullet_damage = 50

        self.counter = pg.font.Font("assets/font/BebasNeue-Regular.ttf", 20)

        

    def bomb_spawn(self, setup, box, heart):
        now = pg.time.get_ticks()
        if self.bomb_r is None:
            if now - self.bomb_timer > 8000 : 
                self.bomb_r = self.bomb.get_rect(center = (random.randint(box.left + 10, box.right -10), random.randint(box.top + 10, box.bottom - 10)))
        if self.bomb_r:
            setup.screen.set_clip(box)
            setup.screen.blit(self.bomb, self.bomb_r)
            if self.bomb_r.colliderect(heart.heart_r):
                self.bombcount += 1
                self.bomb_r = None
                self.bomb_timer = now
        setup.screen.set_clip(None)
    
    def bullet_spawn(self, setup, box, heart):
        now = pg.time.get_ticks()
        if self.bullet_r is None:
            if now - self.bullet_timer > 10000 : 
                self.bullet_r = self.bullet.get_rect(center = (random.randint(box.left + 10, box.right -10), random.randint(box.top + 10, box.bottom - 10)))
        if self.bullet_r:
            setup.screen.set_clip(box)
            setup.screen.blit(self.bullet, self.bullet_r)
            if self.bullet_r.colliderect(heart.heart_r):
                self.bulletcount += 1
                self.bullet_r = None
                self.bullet_timer = now
        setup.screen.set_clip(None)

    def draw_bomb_count(self, setup, box, heart_box):
        bomb_r = self.bomb.get_rect(midtop = (heart_box.right + 60, box.bottom + 50))
        setup.screen.blit(self.bomb, bomb_r)
        bomb = self.counter.render(f"x{self.bombcount}", True, "white")
        bomb_rect = bomb.get_rect(topleft = (bomb_r.right , bomb_r.top + 10))
        setup.screen.blit(bomb, bomb_rect)

        bullet_r = self.bullet_count_img.get_rect(midbottom = (bomb_rect.right+40, bomb_r.bottom-3))
        setup.screen.blit(self.bullet_count_img, bullet_r)
        bullet = self.counter.render(f"x{self.bulletcount}", True, "white")
        bullet_rect = bomb.get_rect(topleft = (bullet_r.right + 3, bomb_r.top + 10))
        setup.screen.blit(bullet, bullet_rect)
    
    def apply_damage(self, boss, attack):
        if attack == "bomb":
            if self.bombcount >0:
                damage = ((self.bombcount**1.8)*self.bomb_damage)-(self.bombcount*self.bomb_damage)
                boss.hp -= damage
                self.bombcount = 0
        if attack == "bullet":
            if self.bulletcount >0:
                damage = self.bullet_damage * self.bulletcount*1.48
                boss.hp -= damage
                self.bulletcount -= 1





    
