import pygame
import sys


class StartGUI:
    def __init__(self, font_size, gf):
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.FONT_SIZE = font_size
        self.gf = gf

    def draw_text(self, surface, text, pos, color=(0, 0, 0)):
        font_size = self.FONT_SIZE
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, pos)

    def draw_dropdown(self, screen, string1, options, continue_str, selected_option, x, y):
        is_dropdown_open = False
        choose = False
        button_rect_exit = pygame.Rect(x + 200, y + 30, 150, 24)
        button_rect = pygame.Rect(x, y, 150, self.FONT_SIZE)
        exit_rect = pygame.Rect(x + 200, y, 150, self.FONT_SIZE)
        while not choose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_exit.collidepoint(event.pos) and not self.gf.is_game_mode:
                        if not self.gf.is_game_option:
                            self.gf.is_game_option = True
                        else:
                            self.gf.is_game_mode = True
                        choose = True
                        break
                    if exit_rect.collidepoint(event.pos):
                        if self.gf.is_game_mode:
                            self.gf.is_game_mode = False
                        elif self.gf.is_game_option:
                            self.gf.is_game_option = False
                        else:
                            self.gf.is_grid_size = False
                        choose = True
                        break
                    if not is_dropdown_open:
                        if button_rect.collidepoint(event.pos):
                            is_dropdown_open = True
                    else:
                        if button_rect.collidepoint(event.pos):
                            is_dropdown_open = False
                        for i, option in enumerate(options):
                            option_rect = pygame.Rect(x, y + (i + 1) * self.FONT_SIZE, 150, self.FONT_SIZE)
                            if option_rect.collidepoint(event.pos):
                                selected_option = option
                                is_dropdown_open = False
            screen.fill(self.WHITE)
            if button_rect.collidepoint(pygame.mouse.get_pos()):
                self.gf.screen.fill((203, 203, 203), pygame.Rect(x + 1, y + 1, 148, 22))
            if exit_rect.collidepoint(pygame.mouse.get_pos()):
                self.gf.screen.fill((203, 203, 203), pygame.Rect(x + 201, y + 1, 148, 22))
            pygame.draw.rect(screen, self.BLACK, button_rect, 1)
            pygame.draw.polygon(screen, self.BLACK, [[165, 47], [175, 47], [170, 55]], 1)
            self.draw_text(screen, string1, (x + 5, y + 3))
            pygame.draw.rect(screen, self.BLACK, exit_rect, 1)
            self.draw_text(screen, continue_str, (x + 226, y + 3))
            if not self.gf.is_game_mode:
                if button_rect_exit.collidepoint(pygame.mouse.get_pos()):
                    self.gf.screen.fill((203, 203, 203), pygame.Rect(x + 201, y + 31, 148, 22))
                pygame.draw.rect(screen, self.BLACK, button_rect_exit, 1)
                self.draw_text(screen, "Назад", (x + 251, y + 3 + 30))
            if is_dropdown_open:
                for i, option in enumerate(options):
                    option_rect = pygame.Rect(x, y + (i + 1) * self.FONT_SIZE, 150, self.FONT_SIZE)
                    if option_rect.collidepoint(pygame.mouse.get_pos()):
                        self.gf.screen.fill((203, 203, 203), pygame.Rect(x + 1, 1 + y + (i + 1) * 24, 148, 22))
                    pygame.draw.rect(screen, self.BLACK, option_rect, 1)
                    self.draw_text(screen, option, (x + 5, 3 + y + (i + 1) * self.FONT_SIZE))
            if selected_option:
                self.draw_text(screen, f"Выбрано: {selected_option}", (x + 5, y + (len(options) + 2) * self.FONT_SIZE))
                if len(options) == 3:
                    self.gf.update(self.gf.grid_size, int(selected_option))
                elif len(options) == 13:
                    self.gf.update(int(selected_option), self.gf.count_players)
                elif selected_option == "с друзьями":
                    self.gf.with_bot = False
                elif selected_option == "с компьютером":
                    self.gf.with_bot = True
                elif selected_option == "легко":
                    self.gf.with_easy_bot = True
                    self.gf.with_hard_bot = False
                elif selected_option == "тяжело":
                    self.gf.with_easy_bot = False
                    self.gf.with_hard_bot = True
            pygame.display.flip()
