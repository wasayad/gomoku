import sys
import numpy as np

from game_rules import GameRules

class Node:
    def __init__(self, board, last_move, player, eval_board):
        self.board = board
        self.evaluation_board = eval_board
        self.gain = 0
        self.last_move = tuple(last_move)
        self.player = player
        
    def check_capture(self, c, player):
        checker = ["2100", "1220"]
        for i in [[(-1, -1), (1, 1)], [(0, -1), (0, 1)], [(1, 0), (-1, 0)], [(1, -1), (-1, 1)]]:
            for vector in i:
                cx = c[1]
                cy = c[0]
                tmp = str(self.board[cx][cy])
                for j in range(5):
                    cx -= vector[0]
                    cy -= vector[1]
                    if (cx < 0 or cx > 18 or cy < 0 or cy > 18):
                        break
                    try:
                        tmp += str(self.board[cx][cy])
                    except:
                        pass
                print(tmp)
                    
                    
    def calculate_price(self, value, p, move):
        for i in [[(-1, -1), (1, 1)], [(0, -1), (0, 1)], [(1, 0), (-1, 0)], [(1, -1), (-1, 1)]]:
            ratio = 1
            for vector in i:
                cx = move[0]
                cy = move[1]
                for j in range(4):
                    cx -= vector[0]
                    cy -= vector[1]
                    if (cx < 0 or cx > 18 or cy < 0 or cy > 18):
                        break
                    if self.board[cy][cx] != p and self.board[cy][cx] != 0:
                        break
                    if self.board[cy][cx] == p:
                        ratio += 4
            for vector in i:
                cx = move[0]
                cy = move[1]
                self.evaluation_board[cy][cx] = 5 if p == 1 else -5
                for j in range(4):
                    cx -= vector[0]
                    cy -= vector[1]
                    if (cx < 0 or cx > 18 or cy < 0 or cy > 18):
                        break
                    if self.board[cy][cx] != p and self.board[cy][cx] != 0:
                        break
                    if self.board[cy][cx] == 0:
                        self.evaluation_board[cy][cx] += abs((j - 4) * ratio) * value

    def get_pos(self, gamerules):
        atk = (0, 0)
        counter = (0, 0)
        for y in range(19):
            for x in range(19):
                if self.evaluation_board[y][x] <= self.evaluation_board[counter[1]][counter[0]] and self.board[y][x] == 0 and gamerules.double_three((y, x), 2):
                    counter = (x, y)
                if (self.evaluation_board[y][x] != 0 and self.evaluation_board[atk[1]][atk[0]] < self.evaluation_board[y][x] and self.board[y][x] == 0) and gamerules.double_three((y, x), 2):
                    atk = (x,y)
        if abs(self.evaluation_board[counter[1]][counter[0]]) > self.evaluation_board[atk[1]][atk[0]]:
            self.last_move = counter
            return counter
        self.last_move = atk
        return atk
    
class Ia:
    def __init__(self, player):
        self.node = Node(0, (0,0), player, np.full((19,19), 0, (int)))
        self.board = 0
    
    def play(self, board, rounds, gamerules):
        if (rounds == 2):
            self.node.last_move = (9,9)
            self.node.board = board
            self.node.calculate_price(1, 1, self.node.last_move)
            return (9, 9)
        else:
            self.node.board = board
            self.node.get_pos(gamerules)
            self.node.evaluation_board = np.full((19,19), 0, (int))
            self.node.check_capture(self.node.last_move, 1)
            for y in range(19):
                for x in range(19):
                    if self.node.board[y][x] == 2:
                        self.node.calculate_price(-1, 2, (x,y))
                    elif self.node.board[y][x] == 1:
                        self.node.calculate_price(1, 1, (x,y))
            #print("__________________")
            #print(self.node.evaluation_board)
        return self.node.last_move