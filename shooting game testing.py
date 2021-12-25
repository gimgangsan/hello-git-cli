import math
import time
import sys
import pygame
import random
from pygame.locals import QUIT,Rect,MOUSEBUTTONDOWN,KEYDOWN,KEYUP,K_w,K_a,K_d,K_s,MOUSEBUTTONDOWN,MOUSEMOTION,MOUSEBUTTONUP,K_SPACE

pygame.init()
pygame.key.set_repeat(5,5)
keys=[]
men=[]
bullets=[]
m_pos=(0,0)
mouse=False
surface=pygame.display.set_mode((1000,1000))
clock=pygame.time.Clock()

class moving_thing():
    def __init__(self,hp,speed,
                 rect,weapon): #체력 ,이동속도 ,움직이는 각도 ,사격 각도 ,크기및 위치 ,패턴 ,무기
        self.max_hp=hp
        self.hp=hp
        self.speed=speed
        self.rect=Rect(rect)
        self.angle=0
        self.s_angle=0
        self.weapon=weapon
    def move(self): #움직이기
        self.rect.centerx+=math.cos(self.angle)*self.speed
        self.rect.centery-=math.sin(self.angle)*self.speed
    def get_angle(self,point): #각도구하기
        x=math.atan2(abs(self.rect.centery-point[1]),abs(self.rect.centerx-point[0]))
        if point[0]>=self.rect.centerx:
            if point[1]>=self.rect.centery:
                return math.radians(360)-x
            else:
                return x
        else:
            if point[1]>=self.rect.centery:
                return math.radians(180)+x
            else:
                return math.radians(180)-x
    def get_distance(self,point1,point2):#거리 구하기
        x=abs(point1[0]-point2[0])
        y=abs(point1[1]-point2[1])
        return math.sqrt(x*x+y*y)
    def show_hp(self):
        decrease=(100-self.hp/self.max_hp*100)/100
        if decrease!=0:
            rect=Rect(0,0,self.rect.width/5*4,self.rect.height/5*4*decrease)
            rect.topleft=(self.rect.topleft[0]+self.rect.width/10,self.rect.topleft[1]+self.rect.height/10)
            pygame.draw.rect(surface,(255,255,255),rect)
    def bump(self):
        for man in men:
            if self.rect.colliderect(man.rect) and man!=self:
                self_big=self.rect.width+self.rect.height
                man_big=man.rect.width+man.rect.width
                if self_big>=man_big:
                    man.rect.centerx+=math.cos(self.get_angle(man.rect.center))*3
                    man.rect.centery-=math.sin(self.get_angle(man.rect.center))*3
    def pos_control(self):
        self.rect.centerx=min(max(0,self.rect.centerx),1000)
        self.rect.centery=min(max(0,self.rect.centery),1000)
    def invisible(self,invisible_time):
        if t-self.last_hit>=invisible_time:
            self.last_hit=time.time()
            for bullet in bullets:
                if self.rect.colliderect(bullet.rect) and bullet.penetrate>=0:
                    bullet.penetrate-=self.hp
                    self.hp-=bullet.damege

class hero(moving_thing):
    def __init__(self,hp,speed,rect,weapon):
        super().__init__(hp,speed,rect,weapon)
        self.last_hit=0
    def pattern(self): #주인공의 행동패턴
        self.pos_control()
        if len(keys)==1:
            if keys[0]==K_w:
                self.angle=math.radians(90)
            elif keys[0]==K_a:
                self.angle=math.radians(180)
            elif keys[0]==K_s:
                self.angle=math.radians(270)
            elif keys[0]==K_d:
                self.angle=math.radians(0)
            self.move()
        elif len(keys)>=2:
            if K_w in keys[:2] and K_a in keys[:2]:
                self.angle=math.radians(135)
            elif K_a in keys[:2] and K_s in keys[:2]:
                self.angle=math.radians(225)
            elif K_s in keys[:2] and K_d in keys[:2]:
                self.angle=math.radians(315)
            elif K_d in keys[:2] and K_w in keys[:2]:
                self.angle=math.radians(45)
            self.move()
        if mouse:
            self.weapon.shoot(self)
        pygame.draw.rect(surface,(0,0,0),self.rect)
        self.s_angle=self.get_angle(m_pos)
        muzzle=(self.rect.centerx+math.cos(self.s_angle)*40,
                self.rect.centery-math.sin(self.s_angle)*40)
        pygame.draw.line(surface,(255,0,0),self.rect.center,muzzle)
        pygame.draw.rect(surface,(0,0,0),(50,930,400*self.hp/self.max_hp,30))

class zombie(moving_thing):#좀비
    def __init__(self,hp,speed,rect,weapon):
        super().__init__(hp,speed,rect,weapon)
        self.last_hit=0
    def pattern(self):
        self.angle=self.get_angle(james.rect.center)
        self.s_angle=self.angle
        self.move()
        pygame.draw.rect(surface,(0,255,0),self.rect)
        self.show_hp()
        self.bump()
        self.pos_control
        self.invisible(0)




class normal_bullet(moving_thing):#일반 총알
    def __init__(self,damege,penetrate,speed,angle,rect,shooter):
        self.damege=damege
        self.penetrate=penetrate
        self.speed=speed
        self.angle=angle
        self.rect=Rect(rect)
        self.shooter=shooter
    def move_bullet(self):
        self.move()
        pygame.draw.rect(surface,(0,0,255),self.rect)
        
class rifle():#소총
    def __init__(self):
        self.shoot_time=0
    def shoot(self,who):
        if t-self.shoot_time>=0.05:
            self.shoot_time=time.time()
            fire=Rect(0,0,4,4)
            fire.center=who.rect.center
            bullets.append(normal_bullet(10,100,30,who.s_angle+math.radians(random.randint(-3,3)),fire,who))

def tick(): #프레임마다 발생하는 이벤트
    global m_pos,mouse
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
        elif event.type==MOUSEBUTTONDOWN:
            mouse=True
        elif event.type==MOUSEBUTTONUP:
            mouse=False
        elif event.type==MOUSEMOTION:
            m_pos=event.pos
        elif event.type==KEYDOWN:
            if not event.key in keys:
                keys.append(event.key)
        elif event.type==KEYUP:
            keys.remove(event.key)
    for man in men:
        man.pattern()
        if man.hp<=0:
            men.remove(man)
    for bullet in bullets:
        bullet.move_bullet()
        if bullet.penetrate<=0 or Rect(0,0,1000,1000).colliderect(bullet.rect)==False:
            bullets.remove(bullet)

def main():
    global james,t
    font=pygame.font.SysFont(None,100)
    game_over=font.render('game over',True,(255,0,0))
    clear=font.render('clear',True,(0,0,255))
    game_over_rect=game_over.get_rect()
    game_over_rect.center=(500,500)
    clear_rect=clear.get_rect()
    clear_rect.center=(500,500)
    james=hero(100,8,(490,490,20,20),rifle())
    men.append(james)
    for yee in range(10):
        men.append(zombie(120,4,(random.randint(0,1000),0,18,18),0))
    while True:
        t=time.time()
        surface.fill((255,255,255))
        tick()
        if not james in men:
            surface.blit(game_over,game_over_rect.topleft)
        elif james in men and len(men)==1:
            surface.blit(clear,clear_rect.topleft)
        pygame.display.update()
        clock.tick(60)
                   
if __name__=='__main__':
    main()
