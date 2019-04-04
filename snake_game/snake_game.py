import random
import sys

import pygame
from pygame.locals import *

redColor = pygame.Color(255, 0, 0)
blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)
greyColor = pygame.Color(150, 150, 150)


class SnakeGame(object):
    def __init__(self):
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.playSurface = pygame.display.set_mode((640, 480))
        pygame.display.set_caption("Snake Game")

    def start(self):
        self.playSurface.fill(blackColor)
        start_font = pygame.font.SysFont("arial.ttf", 54)
        start_surf = start_font.render('Snake Game', True, greyColor)
        start_rect = start_surf.get_rect()
        start_rect.midtop = (320, 100)
        self.playSurface.blit(start_surf, start_rect)
        enter_font = pygame.font.SysFont("arial.ttf", 54)
        enter_surf = enter_font.render('Press Enter to Start', True, greyColor)
        enter_rect = enter_surf.get_rect()
        enter_rect.midtop = (320, 150)
        self.playSurface.blit(enter_surf, enter_rect)
        esc_font = pygame.font.SysFont("arial.ttf", 54)
        esc_surf = esc_font.render('Press Esc to Quit', True, greyColor)
        esc_rect = esc_surf.get_rect()
        esc_rect.midtop = (320, 200)
        self.playSurface.blit(esc_surf, esc_rect)
        pygame.display.flip()

        # 检测是否按了Enter开始游戏
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    # 判断键盘事件
                    if event.key == K_KP_ENTER or event.key == K_RETURN:
                        self.difficulty()
                        break
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))

    def difficulty(self):
        self.playSurface.fill(blackColor)
        diff_font = pygame.font.SysFont("arial.ttf", 54)
        diff_surf = diff_font.render('Input speed (0 - 9)', True, greyColor)
        diff_rect = diff_surf.get_rect()
        diff_rect.midtop = (320, 100)
        self.playSurface.blit(diff_surf, diff_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    # 判断键盘事件
                    # 键盘上方0-9，计算速度
                    if K_0 <= event.key <= K_9:
                        speed = 5 + 3 * (event.key - K_0)
                        self.start_game(speed)
                        break
                    # 小键盘0-9
                    elif K_KP0 <= event.key <= K_KP9:
                        speed = 5 + 3 * (event.key - K_KP0)
                        self.start_game(speed)
                        break
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))

    def start_game(self, speed):
        snake_position = [100, 100]  # 蛇头位置
        snake_segments = [[100, 100], [80, 100], [60, 100]]  # 蛇身体位置，初始为1单位
        berry_position = [300, 300]  # 果子位置
        berry_number = 1  # 果子个数为1
        direction = "right"  # 初始方向向右
        change_direction = direction
        score = 0  # 初始得分
        while True:
            # 检测按键
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    # 判断键盘事件
                    if event.key == K_RIGHT or event.key == ord("d"):
                        change_direction = 'right'
                    if event.key == K_LEFT or event.key == ord("a"):
                        change_direction = "left"
                    if event.key == K_UP or event.key == ord("w"):
                        change_direction = "up"
                    if event.key == K_DOWN or event.key == ord("s"):
                        change_direction = "down"
                    if event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))
            # 判断是否是输入了反方向
            if change_direction == "right" and not direction == "left":
                direction = change_direction
            if change_direction == "left" and not direction == "right":
                direction = change_direction
            if change_direction == "up" and not direction == "down":
                direction = change_direction
            if change_direction == "down" and not direction == "up":
                direction = change_direction
            # 根据方向移动蛇头坐标
            if direction == "right":
                snake_position[0] += 20
            if direction == "left":
                snake_position[0] -= 20
            if direction == "up":
                snake_position[1] -= 20
            if direction == "down":
                snake_position[1] += 20
            # 增加蛇的长度
            snake_segments.insert(0, list(snake_position))
            # 判断是否吃了果子
            if snake_position[0] == berry_position[0] and snake_position[1] == berry_position[1]:
                berry_number = 0
            else:
                snake_segments.pop()
            # 如果吃掉了果子，重新生成一个果子
            if berry_number == 0:
                x = random.randrange(1, 32)
                y = random.randrange(1, 24)
                berry_position = [int(x * 20), int(y * 20)]
                berry_number = 1
                score += int((speed - 5) / 3 + 1)

            # 绘制pygame显示层
            self.playSurface.fill(blackColor)
            for position in snake_segments:
                pygame.draw.rect(self.playSurface, whiteColor, Rect(position[0], position[1], 20, 20))
                pygame.draw.rect(self.playSurface, redColor,
                                 Rect(berry_position[0], berry_position[1], 20, 20))
            score_font = pygame.font.SysFont("arial.ttf", 24)
            score_surf = score_font.render("score:" + str(score), True, greyColor)
            score_rect = score_surf.get_rect()
            score_rect.midtop = (40, 0)
            self.playSurface.blit(score_surf, score_rect)
            # 刷新pygame显示层
            pygame.display.flip()
            # 判断是否死亡
            if snake_position[0] >= 640 or snake_position[0] <= 0:
                self.game_over(score)
            if snake_position[1] >= 480 or snake_position[1] <= 0:
                self.game_over(score)
            for snake_body in snake_segments[1:]:
                if snake_position[0] == snake_body[0] and snake_position[1] == snake_body[1]:
                    self.game_over(score)
            # 控制游戏速度
            self.fpsClock.tick(speed)

    def game_over(self, score):
        game_over_font = pygame.font.SysFont("arial.ttf", 54)
        game_over_surf = game_over_font.render('Game Over!', True, greyColor)
        game_over_rect = game_over_surf.get_rect()
        game_over_rect.midtop = (320, 10)
        self.playSurface.blit(game_over_surf, game_over_rect)
        score_font = pygame.font.SysFont("arial.ttf", 54)
        score_surf = score_font.render('Score:' + str(score), True, greyColor)
        score_rect = score_surf.get_rect()
        score_rect.midtop = (320, 50)
        self.playSurface.blit(score_surf, score_rect)
        enter_font = pygame.font.SysFont("arial.ttf", 54)
        enter_surf = enter_font.render('Press Enter to Start', True, greyColor)
        enter_rect = enter_surf.get_rect()
        enter_rect.midtop = (320, 150)
        self.playSurface.blit(enter_surf, enter_rect)
        esc_font = pygame.font.SysFont("arial.ttf", 54)
        esc_surf = esc_font.render('Press Esc to Quit', True, greyColor)
        esc_rect = esc_surf.get_rect()
        esc_rect.midtop = (320, 200)
        self.playSurface.blit(esc_surf, esc_rect)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    # 判断键盘事件
                    if event.key == K_KP_ENTER or event.key == K_RETURN:
                        self.difficulty()
                        break
                    elif event.key == K_ESCAPE:
                        pygame.event.post(pygame.event.Event(QUIT))


if __name__ == '__main__':
    game = SnakeGame()
    game.start()
