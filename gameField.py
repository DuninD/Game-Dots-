import pygame as pg


class GameField:
    def __init__(self, grid_size, count_players):
        self.win_width = 800
        self.win_height = 800
        self.grid_size = grid_size
        self.space = 800 // self.grid_size
        self.screen = pg.display.set_mode((self.win_width + 200, self.win_height))
        self.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.players = [(255, 0, 0), (0, 0, 255), (20, 250, 0), (176, 31, 249)]
        self.death_players = [(163, 102, 102), (146, 164, 206), (117, 161, 104), (129, 102, 138)]
        self.radius = 5
        self.count_players = count_players
        self.with_easy_bot = False
        self.with_hard_bot = False
        self.with_bot = False
        self.current_player = []
        self.is_game_mode = True
        self.is_game_option = True
        self.is_grid_size = True


    def update(self, grid_size, count_players):
        self.grid_size = grid_size
        self.space = 800 // self.grid_size
        self.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.radius = 5
        self.count_players = count_players

    def draw_grid(self):
        for x in range(self.space // 2, self.win_width, self.space):
            pg.draw.line(self.screen, (86, 175, 235), (x, 0), (x, self.win_height), 1)
        for y in range(self.space // 2, self.win_height, self.space):
            pg.draw.line(self.screen, (86, 175, 235), (0, y), (self.win_width, y), 1)

    def draw_circles(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = (100, 167, 243)
                if self.grid[i][j] is not None:
                    if self.grid[i][j] >= 0.5 and self.grid[i][j] <= 0.53:
                        if self.grid[i][j] == 0.5:
                            pg.draw.circle(self.screen, self.death_players[0], ((i * self.space) + self.space // 2, (
                                                                j * self.space) + self.space // 2), self.radius)
                        elif self.grid[i][j] == 0.51:
                            pg.draw.circle(self.screen, self.death_players[1], ((i * self.space) + self.space // 2, (
                                                                j * self.space) + self.space // 2), self.radius)
                        elif self.grid[i][j] == 0.52:
                            pg.draw.circle(self.screen, self.death_players[2], ((i * self.space) + self.space // 2, (
                                    j * self.space) + self.space // 2), self.radius)
                        else:
                            pg.draw.circle(self.screen, self.death_players[3], ((i * self.space) + self.space // 2, (
                                    j * self.space) + self.space // 2), self.radius)
                    else:
                        color = self.players[self.grid[i][j]]
                        pg.draw.circle(self.screen, color, ((i * self.space) + self.space // 2, (
                                j * self.space) + self.space // 2), self.radius)
