import pygame as pg
import sys
import bots
import datetime


class GameLogic:
    def __init__(self, gf, players, save):
        self.CURRENT_PLAYER = 0
        self.list_to_find_cycles = []
        self.gf = gf
        self.players = players
        self.save = save
        self.to_menu = False

    def find_loop(self, i, j, player_color, path, start_edge):
        incoming_path = path.copy()
        if path[-1] == start_edge and len(path) > 4:
            self.list_to_find_cycles.append(path)
        elif self.gf.grid[i][j] == player_color and (path.count((i, j)) == 1 or (i, j) == start_edge) and \
                path.count(start_edge) < 2:
            for delta_i in range(-1, 2, 1):
                for delta_j in range(-1, 2, 1):
                    if (delta_i != 0 or delta_j != 0) and 0 <= i + delta_i <= self.gf.grid_size - 1 and \
                            0 <= j + delta_j <= self.gf.grid_size - 1:
                        new_path = incoming_path.copy()
                        new_path.append((i + delta_i, j + delta_j))
                        self.find_loop(i + delta_i, j + delta_j, player_color, new_path, start_edge)

    def inside_is_enemy(self, min_x, max_x, min_y, max_y, path):
        can_draw = False
        counter_enemy_dots = 0
        count_our_color_inside_dots = 0
        inside_dots = []
        for i in range(min_x + 1, max_x):
            for j in range(min_y, max_y + 1):
                if (i, j) not in path and self.point_in_polygon((i, j), path):
                    inside_dots.append((i, j))
                    if self.gf.grid[i][j] == self.CURRENT_PLAYER:
                        count_our_color_inside_dots += 1
                    elif self.gf.grid[i][j] is not None and self.gf.grid[i][j] != 0.5 + self.CURRENT_PLAYER * 0.01:
                        counter_enemy_dots += 1
                    if self.gf.grid[i][j] is not None and self.gf.grid[i][j] % 1 == 0 and \
                            self.gf.grid[i][j] != self.CURRENT_PLAYER:
                        can_draw = True
        if can_draw:
            return inside_dots, counter_enemy_dots, count_our_color_inside_dots
        return [], 0, 0

    def point_in_polygon(self, point, poly):
        x, y = point
        path_length = len(poly)
        j = path_length - 1
        is_inside = False
        for i in range(path_length):
            if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                    (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) / (poly[j][1] - poly[i][1])):
                is_inside = not is_inside
            j = i
        return is_inside

    def game_loop(self):
        computer = bots.Computer(self.gf.grid_size, self)
        self.players.draw_result()
        button_rect_exit = pg.Rect(728, 660, 150, 24)
        timer = datetime.datetime.today()
        while not self.to_menu:
            current_time = datetime.datetime.today()
            delta_time = (current_time - timer).seconds
            timer_count = 300 - int(delta_time)
            minutes = timer_count // 60
            seconds = timer_count % 60
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_exit.collidepoint(event.pos):
                        self.to_menu = True
                        self.gf.is_game_mode = True
                        self.gf.is_game_option = True
                        self.gf.is_grid_size = True
                        break
                    x, y = pg.mouse.get_pos()
                    i = round((x - self.gf.space // 2) / self.gf.space)
                    j = round((y - self.gf.space // 2) / self.gf.space)
                    if i < self.gf.grid_size and self.gf.grid[i][j] is None and timer_count > 0:
                        self.next_move(i, j)
                        if self.gf.with_easy_bot:
                            computer.easy_bot()
                        elif self.gf.with_hard_bot:
                            for item in self.save.data["users"]:
                                if item[0] == self.gf.current_player:
                                    item[1] = max(
                                        self.players.points[(self.CURRENT_PLAYER - 1) % self.gf.count_players], item[1])
                                    self.save.write(self.save.data, 'users.json')
                            computer.hard_bot(i, j)
                        self.players.draw_result()
            self.gf.draw_circles()
            self.gf.screen.fill((255, 250, 250), [[730, 300], [999, 770]])
            if timer_count > 0:
                self.gf.screen.blit(pg.font.Font(None, 24).render(str(minutes) + ":" + str(seconds), True, (0, 0, 0)),
                                    (788, 633))
            else:
                self.gf.screen.blit(pg.font.Font(None, 24).render("Игра окончена", True, (0, 0, 0)),
                                    (748, 633))
            if button_rect_exit.collidepoint(pg.mouse.get_pos()):
                self.gf.screen.fill((203, 203, 203), pg.Rect(729, 661, 148, 22))
            self.gf.screen.blit(pg.font.Font(None, 24).render("Выйти в меню", True, (0, 0, 0)), (748, 663))
            pg.draw.rect(self.gf.screen, (0, 0, 0), button_rect_exit, 1)
            pg.display.flip()

    def next_move(self, i, j):
        if i < self.gf.grid_size and self.gf.grid[i][j] is None:
            self.list_to_find_cycles = []
            self.gf.grid[i][j] = self.CURRENT_PLAYER
            self.find_loop(i, j, self.CURRENT_PLAYER, [(i, j)], (i, j))
            shortest_paths = []
            for path in self.list_to_find_cycles:
                x_index = [x[0] for x in path]
                y_index = [y[1] for y in path]
                path_info = self.inside_is_enemy(min(x_index), max(x_index), min(y_index), max(y_index),
                                                 path)
                current_all_inside_dots = path_info[0]
                current_score = path_info[1]
                current_count_our_color_inside = path_info[2]
                if current_score > 0:
                    if len(shortest_paths) == 0:
                        shortest_paths.append((path, current_score, current_all_inside_dots,
                                               current_count_our_color_inside))
                    else:
                        analog = ()
                        for pref_path in shortest_paths:
                            if analog != ():
                                break
                            for dot in pref_path[2]:
                                if dot in current_all_inside_dots:
                                    analog = pref_path
                                    break
                        if len(analog) == 0:
                            shortest_paths.append((path, current_score, current_all_inside_dots,
                                                   current_count_our_color_inside))
                        else:
                            if current_score > analog[1]:
                                shortest_paths.remove(analog)
                                shortest_paths.append((path, current_score, current_all_inside_dots,
                                                       current_count_our_color_inside))
                            elif current_score == analog[1] and current_count_our_color_inside < analog[3]:
                                shortest_paths.remove(analog)
                                shortest_paths.append((path, current_score, current_all_inside_dots,
                                                       current_count_our_color_inside))
                            elif current_score == analog[1] and current_count_our_color_inside == analog[3] \
                                    and len(path) < len(analog[0]):
                                shortest_paths.remove(analog)
                                shortest_paths.append((path, current_score, current_all_inside_dots,
                                                       current_count_our_color_inside))
            if len(shortest_paths) != 0:
                self.players.grid = self.gf.grid.copy()
                for item in shortest_paths:
                    shortest_path = item[0]
                    self.players.update_score(self.CURRENT_PLAYER, item[1], item[2])
                    for i in range(len(shortest_path) - 1):
                        pg.draw.line(self.gf.screen, (0, 0, 0),
                                     (self.gf.space // 2 + shortest_path[i][0] * self.gf.space,
                                      self.gf.space // 2 + shortest_path[i][1] * self.gf.space),
                                     (self.gf.space // 2 + shortest_path[i + 1][0] * self.gf.space,
                                      self.gf.space // 2 + shortest_path[i + 1][1] * self.gf.space), 2)
                    for dot in item[2]:
                        if self.gf.grid[dot[0]][dot[1]] is not None:
                            if self.gf.grid[dot[0]][dot[1]] == 0 or self.gf.grid[dot[0]][dot[1]] >= 1:
                                self.gf.grid[dot[0]][dot[1]] = 0.5 + self.gf.grid[dot[0]][dot[1]] * 0.01

            self.CURRENT_PLAYER = (self.CURRENT_PLAYER + 1) % self.gf.count_players
