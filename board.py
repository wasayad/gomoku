import sys
import math
import pygame
from graphics import button


class Board:
    def __init__(self):
        run = True
        self.screen = pygame.display.set_mode((800, 500))

        self.pvp_img = pygame.image.load('ia.png').convert_alpha()
        self.pvc_img = pygame.image.load('player.png').convert_alpha()

        self.pvp_btn = button.Button(75, 200, self.pvp_img, 0.8)
        self.pvc_btn = button.Button(425, 200, self.pvc_img, 0.8)

        self.screen.fill((202, 228, 241))
        while run:
            if self.pvp_btn.draw(self.screen):
                self.start_game(0)
                break
            if self.pvc_btn.draw(self.screen):
                print('EXIT')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()

    def start_game(self, game_mod):
        run = True
        pygame.quit()
        self.screen = pygame.display.set_mode((1180, 1180))
        self.screen.fill((225, 215, 201))
        blockSize = 60 #Set the size of the grid block
        for x in range(50, 1130, blockSize):
            for y in range(50, 1130, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.screen, (189, 135, 57), rect, 0)
                pygame.draw.rect(self.screen, (0,0,0), rect, 1)
                if x == 590 and y == 590: 
                    pygame.draw.circle(self.screen, (0,0,0), (x, y), 7)
        #pygame.draw.line(self.screen,(255,255,255), (0, 49), (0, 1180))
        while run:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.draw.circle(self.screen, (255,255,255), (round((pygame.mouse.get_pos()[0] - 50) / 60) * 60 + 50, round((pygame.mouse.get_pos()[1] - 50) / 60) * 60 + 50), 15)
                    #print(round((pygame.mouse.get_pos()[0] - 50) / 60), round((pygame.mouse.get_pos()[1] - 50) / 60))
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        
