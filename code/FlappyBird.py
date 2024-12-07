# Flappy Bird 

import pygame
from sys import exit
import random

FPS = 30
fpsClock = pygame.time.Clock()

class Bird(object):
    def __init__(self, scene):
        self.image = pygame.image.load('bird-src/bird.png')
        self.main_scene = scene
        self.size_x = 80
        self.size_y = 60
        self.x = 40
        self.y = 120
        
    def action(self, jump = 4):
        self.y = self.y + jump
        if self.y > 520:
            self.y = 520
        if self.y < 0:
            self.y = 0
    
    def draw(self):
        self.main_scene.scene.blit(self.image, (self.x, self.y))
        

class GameBackground(object):
    def __init__(self, scene):
        #加载两张相同的图片，实现地图滚动
        self.image1 = pygame.image.load('bird-src/background.jpg')
        self.image2 = pygame.image.load('bird-src/background.jpg')
        # 保存场景对象
        self.main_scene = scene
        # 辅助移动地图
        self.x1 = 0
        self.x2 = self.main_scene.size[1]
        self.speed = 4
        #柱子图
        self.pillar = pygame.image.load('bird-src/pillar.png')
        self.pillar_nums = 1
        self.pillar_positions_x = [800]
        self.pillar_positions_y = [-200]
        
    # 计算地图绘制坐标
    def action(self, addPillar = False):
        #计算柱子新位置
        for i in range(0, self.pillar_nums):
            self.pillar_positions_x[i] -= self.speed
            
        if self.pillar_nums > 0 and self.pillar_positions_x[0] + 100 < 0:
            del self.pillar_positions_x[0]
            del self.pillar_positions_y[0]
            self.pillar_nums -= 1
            
        if addPillar:
            self.pillar_nums += 1
            self.pillar_positions_x.append(800)
            self.pillar_positions_y.append(random.randint(-400, 0))
            
        #地图
        self.x1 = self.x1 - self.speed
        self.x2 = self.x2 - self.speed
        if self.x1 <= -self.main_scene.size[1]:
            self.x1 = 0
        if self.x2 <= 0:
            self.x2 = self.main_scene.size[1]
    
    # 绘制地图
    def draw(self):
        self.main_scene.scene.blit(self.image1, (self.x1, 0))
        self.main_scene.scene.blit(self.image2, (self.x2, 0))
        for i in range(0, self.pillar_nums):
            self.main_scene.scene.blit(self.pillar, (self.pillar_positions_x[i], self.pillar_positions_y[i]))
            
#主场景
class MainScene(object):
    def __init__(self):
        self.size = (800, 600)
        self.scene = pygame.display.set_mode([self.size[0], self.size[1]])
        self.point = 0
        pygame.display.set_caption("Flappy Bird v1.0      得分："+ str(int(self.point)))
        self.pause = False
        #创建地图对象
        self.map = GameBackground(self)
        #创建鸟对象
        self.bird = Bird(self)
        self.lose = False
        
    def draw_elements(self):
        self.map.draw()
        self.bird.draw()
        pygame.display.set_caption("Flappy Bird      score: "+str(float('%.2f' % self.point)))
        
    def action_elements(self, addPillar = False):
        self.map.action(addPillar)
        self.bird.action()
            
    def detect_conlision(self):
        #只要检查第一个柱子
        if self.map.pillar_positions_x[0] <= self.bird.size_x + self.bird.x and self.map.pillar_positions_x[0] >= -60:
            if self.map.pillar_positions_y[0] + 400 < self.bird.y and self.bird.y < self.map.pillar_positions_y[0] + 600:
                if self.map.pillar_positions_x[0] == -60:
                    return 1
            else:
                return -1
        return 0
    
    # 主循环
    def run_scene(self):
        #放音乐
        pygame.mixer.init()
        music_bg = pygame.mixer.Sound('bird-src/Jibbs-ChainHangLow.mp3')
        music_bg.play(loops=-1) #播放音乐（loops=-1循环播放）
        music_shoot = pygame.mixer.Sound('mp3/shoot.mp3')
        music_score = pygame.mixer.Sound('mp3/score.mp3')

        now = 0
        while True:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.action(-60)
                        music_shoot.play()
 
            # 不暂停
            if self.pause == False and self.lose == False:
                if now == 90:
                    self.action_elements(True) 
                    now = 0
                else:
                    self.action_elements(False)
                    now += 1
                #绘制元素图片
                self.draw_elements()
                # 碰撞检测
                state = self.detect_conlision()
                if state == 1:
                    self.point += 1
                    music_score.play()
                elif state == -1:
                    pygame.display.set_caption("Flappy Bird Game Over  Score:" + str(float('%.2f' % self.point)))
                    self.lose = True
                    music_bg.stop()
                    
                pygame.display.update()
                fpsClock.tick(FPS)
                

if __name__ == "__main__":
    mainScene = MainScene()
    mainScene.run_scene()