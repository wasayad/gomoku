import sys
import numpy as np

class GameRules:
    def __init__(self):
        self.board = np.zeros((19, 19), dtype = int)
        self.capture_count = {1: 0, 2: 0}
        
    def check_win(self, c):
        winner = self.check_five(c)
        if winner != 0:
            print("Player {0} win !".format("black" if winner % 2 else "white"))
            # exit(0)
        if self.capture_count[1] >= 10 or self.capture_count[2] >= 10:
            print("Player {0} win !".format("black" if self.capture_count[1] >= 10 else "white"))
            # exit(0)
        
    def place_stone(self, coordinates, player):
        if coordinates[0] < 0 or coordinates[0] > 18 or coordinates[1] < 0 or coordinates[1] > 18:
            return False
        if self.board[coordinates[1]][coordinates[0]] > 0:
            return False
        if self.double_three(coordinates, player) == False:
            return False
        self.board[coordinates[1]][coordinates[0]] = player
        self.check_win(coordinates)
        return True
    
    def capture(self, c):
        checker = [[1, 2, 2, 1], [2, 1, 1, 2]]
        for i in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
            tmp = [self.board[c[1]][c[0]]]
            cx = c[1]
            cy = c[0]
            for j in range(3):
                try:
                    cx += i[0]
                    cy += i[1]
                    tmp.append(self.board[cx][cy])
                except:
                    break
            if tmp in checker:
                self.board[c[1] + i[0]][c[0] + i[1]] = 0
                self.board[c[1] + i[0] * 2][c[0] + i[1] * 2] = 0
                self.capture_count[self.board[c[1]][c[0]]] += 2
                
    def check_five(self, c):
        checker = ["11111", "22222"]
        for i in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
            tmp = ''
            cx = c[1] + i[0] * 5
            cy = c[0] + i[1] * 5
            for j in range(10):
                cx -= i[0]
                cy -= i[1]
                try:
                    tmp += str(self.board[cx][cy])
                except:
                    pass
            if checker[0] in tmp or checker[1] in tmp:
                return 1 if checker[0] in tmp else 2
        return 0

    def check_three(self, three, player):
        checker = [['002200', '000220'], ['001100', '000110']]
        if three == checker[player][0] or three == checker[player][1]:
            return 1
        return 0

    def double_three(self, c, player):
        checker = []
        double_three = 0
        for i in [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
            cx = c[1] + i[0]
            cy = c[0] + i[1]
            if (cx < 0 or cx > 18 or cy < 0 or cy > 18):
                continue
            tmp = str(self.board[cx][cy])
            for j in range(5):
                cx -= i[0]
                cy -= i[1]
                try:
                    tmp += str(self.board[cx][cy])
                except:
                    pass
            checker.append(tmp)
        for i in checker:
            double_three += self.check_three(i, player % 2)
            if double_three == 2:
                return False
        return True