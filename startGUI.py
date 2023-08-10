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
        while not choose:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    exit_rect = pygame.Rect(x + 200, y, 150, self.FONT_SIZE)
                    if exit_rect.collidepoint(event.pos):
                        choose = True
                        break
                    if not is_dropdown_open:
                        button_rect = pygame.Rect(x, y, 150, self.FONT_SIZE)
                        if button_rect.collidepoint(event.pos):
                            is_dropdown_open = True
                    else:
                        button_rect = pygame.Rect(x, y, 150, self.FONT_SIZE)
                        if button_rect.collidepoint(event.pos):
                            is_dropdown_open = False
                        for i, option in enumerate(options):
                            option_rect = pygame.Rect(x, y + (i + 1) * self.FONT_SIZE, 150, self.FONT_SIZE)
                            if option_rect.collidepoint(event.pos):
                                selected_option = option
                                is_dropdown_open = False
            screen.fill(self.WHITE)
            button_rect = pygame.Rect(x, y, 150, self.FONT_SIZE)
            pygame.draw.rect(screen, self.BLACK, button_rect, 1)
            pygame.draw.polygon(screen, self.BLACK, [[165, 47], [175, 47], [170, 55]], 1)
            self.draw_text(screen, string1, (x + 5, y + 3))
            button_rect_start = pygame.Rect(x + 200, y, 150, self.FONT_SIZE)
            pygame.draw.rect(screen, self.BLACK, button_rect_start, 1)
            self.draw_text(screen, continue_str, (x + 5 + 200, y + 3))
            if is_dropdown_open:
                for i, option in enumerate(options):
                    option_rect = pygame.Rect(x, y + (i + 1) * self.FONT_SIZE, 150, self.FONT_SIZE)
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
