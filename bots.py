import random

class Computer:
    def __init__(self, grid_size, game_logic):
        self.grid_size = grid_size
        self.game_logic = game_logic
        self.last_x = 1000
        self.last_y = 1000
        self.count = 0
        self.count1 = 0
        self.last = []
        self.i = -1

    def easy_bot(self):
        while True:
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.game_logic.gf.grid[x][y] is None:
                self.game_logic.next_move(x, y)
                break

    def hard_bot(self, player_x, player_y):
        self.i = -1
        self.count1 = 0
        self.count = 0
        while True:
            delta_i = random.randint(-1, 1)
            delta_j = random.randint(-1, 1)
            self.count1 += 1
            if self.count1 == 40:
                self.count1 = 0
                self.last_x = self.last[self.i][0]
                self.last_y = self.last[self.i][1]
                self.i -= 1
                if self.i == -len(self.last) - 1:
                    self.last_x = 1000
            if self.last_x == 1000:
                if (delta_i != 0 or delta_j != 0) and 0 <= player_x + delta_i <= self.game_logic.gf.grid_size - 1\
                                                 and 0 <= player_y + delta_j <= self.game_logic.gf.grid_size - 1:
                    if self.game_logic.gf.grid[player_x + delta_i][player_y + delta_j] is None:
                        self.last_x = player_x + delta_i
                        self.last_y = player_y + delta_j
                        self.last.append((self.last_x, self.last_y))
                        self.game_logic.next_move(self.last_x, self.last_y)
                        return
            elif (delta_i != 0 or delta_j != 0) and 0 <= self.last_x + delta_i <= self.game_logic.gf.grid_size - 1 and\
                    0 <= self.last_y + delta_j <= self.game_logic.gf.grid_size - 1 and \
                    self.game_logic.gf.grid[self.last_x + delta_i][self.last_y + delta_j] is None:
                while True:
                    di = random.randint(-1, 1)
                    dj = random.randint(-1, 1)
                    self.count += 1
                    if self.count == 40:
                        self.count = 0
                        break
                    if (di != 0 or dj != 0) and 0 <= self.last_x + delta_i + di <= self.game_logic.gf.grid_size - 1 and\
                        0 <= self.last_y + delta_j + dj <= self.game_logic.gf.grid_size - 1 and \
                            self.game_logic.gf.grid[self.last_x + delta_i + di][self.last_y + delta_j + dj] is not None\
                            and self.game_logic.gf.grid[self.last_x + delta_i + di][self.last_y + delta_j + dj] % 1 \
                            == 0 and self.game_logic.gf.grid[self.last_x + delta_i + di][self.last_y + delta_j + dj] \
                            != self.game_logic.CURRENT_PLAYER:
                        self.last_x += delta_i
                        self.last_y += delta_j
                        self.last.append((self.last_x, self.last_y))
                        self.game_logic.next_move(self.last_x, self.last_y)
                        return
