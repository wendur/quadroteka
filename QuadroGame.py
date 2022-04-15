import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class QuadroGame:
    def __init__(self, size):
        super(QuadroGame, self).__init__()
        self.size = size
        self.level = 1
        self.fieldInit()

    def fieldInit(self):
        self.field = self.load_level(self.level)

        self.center = Point(2, 2)
        self.colums = 0
        self.moves = 0
        self.turns = 0

        self.shuffle()

        self.center = Point(2, 2)
        self.colums = 0
        self.moves = 0
        self.turns = 0

        self.win_cond = False

    def load_level(self, num):
        f = open('levels\level_' + str(num) + '.txt', 'r')
        field = []
        for row in f:
            field.append([int(x) for x in row.strip().split(" ")])
        f.close()
        return field


    def shuffle(self):
        for i in range(100):
            random.choice([self.up, self.down, self.left, self.right, self.clockwise, self.counter_clockwise])()

    def check_win(self):
        col_count = 0
        for i in range(self.size):
            temp = self.field[0][i]
            flag = True
            for j in range(self.size):
                if self.field[j][i] != temp:
                    flag = False
                    break
            if flag:
                col_count += 1
        self.colums = col_count
        if col_count == self.size:
            self.win_cond = True

    def up(self):
        if self.center.y > 1:
            self.center.y -= 1
            self.moves += 1

    def down(self):
        if self.center.y < 3:
            self.center.y += 1
            self.moves += 1

    def right(self):
        if self.center.x < 3:
            self.center.x += 1
            self.moves += 1

    def left(self):
        if self.center.x > 1:
            self.center.x -= 1
            self.moves += 1

    def clockwise(self):
        self.field[self.center.y - 1][self.center.x - 1], self.field[self.center.y + 1][self.center.x - 1], self.field[self.center.y + 1][self.center.x + 1], self.field[self.center.y - 1][self.center.x + 1] =\
            self.field[self.center.y + 1][self.center.x - 1], self.field[self.center.y + 1][self.center.x + 1], self.field[self.center.y - 1][self.center.x + 1], self.field[self.center.y - 1][self.center.x - 1]

        self.field[self.center.y - 1][self.center.x], self.field[self.center.y][self.center.x - 1], self.field[self.center.y + 1][self.center.x], self.field[self.center.y][self.center.x + 1] = \
            self.field[self.center.y][self.center.x - 1], self.field[self.center.y + 1][self.center.x], self.field[self.center.y][self.center.x + 1], self.field[self.center.y - 1][self.center.x]
        self.turns += 1
        self.check_win()

    def counter_clockwise(self):
        self.field[self.center.y - 1][self.center.x - 1], self.field[self.center.y + 1][self.center.x - 1], self.field[self.center.y + 1][self.center.x + 1], self.field[self.center.y - 1][self.center.x + 1] = \
            self.field[self.center.y - 1][self.center.x + 1], self.field[self.center.y - 1][self.center.x - 1], self.field[self.center.y + 1][self.center.x - 1], self.field[self.center.y + 1][self.center.x + 1]

        self.field[self.center.y - 1][self.center.x], self.field[self.center.y][self.center.x - 1], self.field[self.center.y + 1][self.center.x], self.field[self.center.y][self.center.x + 1] = \
            self.field[self.center.y][self.center.x + 1], self.field[self.center.y - 1][self.center.x], self.field[self.center.y][self.center.x - 1], self.field[self.center.y + 1][self.center.x]
        self.turns += 1
        self.check_win()

    def reset_game(self):
        self.fieldInit()