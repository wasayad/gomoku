from lib2to3 import pygram
import sys
import math
import pygame
from game_rules import GameRules
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
        gamerules = GameRules()
        color = [(0,0,0), (255,255,255)]
        rounds = 1
        pygame.quit()

        surface = pygame.surface.Surface((590, 590))
        hover_ball = pygame.surface.Surface((590, 590))
        self.screen = pygame.display.set_mode((590, 590))

        surface.fill((225, 215, 201))
        hover_ball.set_alpha(128)
        
        
        blockSize = 30 #Set the size of the grid block

        #draw map
        for x in range(50, 565, blockSize):
            for y in range(50, 565, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(surface, (189, 135, 57), rect, 0)
                pygame.draw.rect(surface, (0,0,0), rect, 1)
                if x == 295 and y == 295: 
                    pygame.draw.circle(surface, (0,0,0), (x, y), 7)
                    
        # securiser les bordures de map, empecher la superposition de point
        while run:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(surface, (0,0))
            hover_ball.blit(surface, (0,0))
            pygame.draw.circle(hover_ball, color[rounds % 2], (round((mouse_pos[0] - 50) / 30) * 30 + 50, round((mouse_pos[1] - 50) / 30) * 30 + 50), 15)
            self.screen.blit(hover_ball, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    if gamerules.place_stone((round((pygame.mouse.get_pos()[0] - 50) / 30), round((pygame.mouse.get_pos()[1] - 50) / 30)), rounds % 2 + 1):
                        pygame.draw.circle(surface, color[rounds % 2], (round((pygame.mouse.get_pos()[0] - 50) / 30) * 30 + 50, round((pygame.mouse.get_pos()[1] - 50) / 30) * 30 + 50), 15)
                        gamerules.capture((round((pygame.mouse.get_pos()[0] - 50) / 30), round((pygame.mouse.get_pos()[1] - 50) / 30)))
                        rounds += 1
                if event.type == pygame.QUIT:
                    run = False
            pygame.display.update()
        
