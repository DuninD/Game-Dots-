class Players:
    def __init__(self, grid_size, gui):
        self.points = [0, 0, 0, 0]
        self.catching_dots = {0: [], 1: [], 2: [], 3: []}
        self.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        self.gui = gui

    def update_score(self, player, score, dots):
        self.points[player] += score
        for dot in dots:
            for item in self.catching_dots.items():
                if dot in item[1]:
                    item[1].remove(dot)
                    if self.grid[dot[0]][dot[1]] is not None and self.grid[dot[0]][dot[1]] != 0.5 + item[0] * 0.01:
                        self.points[item[0]] -= 1
            self.catching_dots[player].append(dot)

    def draw_result(self):
        self.gui.gf.screen.fill((255, 250, 250), [[840, 40], [999, 190]])
        if self.gui.gf.with_bot:
            self.gui.draw_text(self.gui.gf.screen, f"Ваши очки:    {self.points[0]}", (840, 40), (255, 0, 0))
            self.gui.draw_text(self.gui.gf.screen, f"Компьютер:    {self.points[1]}", (840, 90), (0, 0, 255))
        else:
            self.gui.draw_text(self.gui.gf.screen, f"Игрок 1:    {self.points[0]}", (840, 40), (255, 0, 0))
            self.gui.draw_text(self.gui.gf.screen, f"Игрок 2:    {self.points[1]}", (840, 90), (0, 0, 255))
            if self.gui.gf.count_players > 2:
                self.gui.draw_text(self.gui.gf.screen, f"Игрок 3:    {self.points[2]}", (840, 140), (20, 250, 0))
                if self.gui.gf.count_players == 4:
                    self.gui.draw_text(self.gui.gf.screen, f"Игрок 4:    {self.points[3]}", (840, 190), (176, 31, 249))


