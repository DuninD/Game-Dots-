import pygame
import sys
import keyboard


class Account:
    def __init__(self, gui, save_data, gf):
        self.write_now = False
        self.current_text = ""
        if save_data is not None and len(save_data.data["users"]) > 0:
            for letter in [chr(x) for x in save_data.data["users"][0][0]]:
                self.current_text += letter
        self.gui = gui
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.save = save_data
        self.can_log_in = False
        self.gf = gf
        self.new = False
        self.can_join = False
        self.can_write = True
        self.new_char = ""

    def choose_account(self, screen, x, y):
        ready = False
        button_rect_start = pygame.Rect(x + 240, y, 150, 24)
        button_rect_new = pygame.Rect(x + 240, y + 30, 150, 24)
        field_rect = pygame.Rect(x + 30, y, 150, 24)
        self.save.data["users"].sort(key=lambda item: (-item[1], item[0]))
        while not ready:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect_start.collidepoint(event.pos) and self.can_log_in:
                        for item in self.save.data["users"]:
                            if item[0] == [ord(x) for x in self.current_text]:
                                self.save.data["users"].remove(item)
                                self.save.data["users"].insert(0, item)
                        self.save.write(self.save.data, 'users.json')
                        self.gf.current_player = [ord(x) for x in self.current_text]
                        ready = True
                        break
                    elif button_rect_start.collidepoint(event.pos) and self.can_join:
                        self.save.data["users"].insert(0, [[ord(x) for x in self.current_text], 0])
                        self.save.write(self.save.data, 'users.json')
                        self.gf.current_player = [ord(x) for x in self.current_text]
                        ready = True
                        break
                    elif button_rect_new.collidepoint(event.pos) and not self.new:
                        self.new = True
                        self.can_log_in = False
                        self.current_text = ""
                    elif button_rect_new.collidepoint(event.pos) and self.new:
                        self.new = False
                        self.current_text = ""
                elif event.type == pygame.KEYDOWN and self.can_write:
                    keyboard.hook(self.pressed_keys)
                    if len(self.new_char) == 1 and self.can_write and len(self.current_text) < 11:
                        self.current_text += self.new_char
                        self.can_write = False
                    elif self.new_char == "backspace":
                        self.current_text = self.current_text[:-1]
                elif event.type == pygame.KEYUP:
                    self.can_write = True
            screen.fill((255, 255, 255))
            self.gui.draw_text(screen, self.current_text, (x + 32, y + 2))
            pygame.draw.rect(screen, self.BLACK, button_rect_start, 1)
            pygame.draw.rect(screen, self.BLACK, button_rect_new, 1)
            if button_rect_start.collidepoint(pygame.mouse.get_pos()):
                self.gf.screen.fill((203, 203, 203), pygame.Rect(x + 241, y + 1, 148, 22))
            if button_rect_new.collidepoint(pygame.mouse.get_pos()):
                self.gf.screen.fill((203, 203, 203), pygame.Rect(x + 241, y + 31, 148, 22))
            for i, option in enumerate(self.save.data["users"]):
                username = ""
                score = option[1]
                for char in [chr(x) for x in option[0]]:
                    username += char
                option_rect = pygame.Rect(x + 500, 6 + y + (i + 1) * 24, 150, 24)
                option_rect_score = pygame.Rect(x + 650, 6 + y + (i + 1) * 24, 150, 24)
                pygame.draw.rect(screen, self.BLACK, option_rect, 1)
                pygame.draw.rect(screen, self.BLACK, option_rect_score, 1)
                self.gui.draw_text(screen, username, (x + 505, 9 + y + (i + 1) * 24))
                self.gui.draw_text(screen, str(score), (x + 655, 9 + y + (i + 1) * 24))
                self.gui.draw_text(screen, "Таблица лидеров", (x + 575, y))
            if not self.new:
                self.gui.draw_text(screen, "Войти", (x + 291, y + 3))
                self.gui.draw_text(screen, "Присоединиться", (x + 246, y + 3 + 30))
            else:
                self.gui.draw_text(screen, "Начать", (x + 289, y + 3))
                self.gui.draw_text(screen, "Назад", (x + 291, y + 3 + 30))
            if not self.new:
                self.gui.draw_text(screen, "Введите имя пользователя", (x, y - 30))
                if self.current_text == "":
                    pygame.draw.rect(screen, self.BLACK, field_rect, 1)
                    self.can_log_in = False
                elif [ord(x) for x in self.current_text] in [x[0] for x in self.save.data["users"]]:
                    pygame.draw.rect(screen, (0, 255, 0), field_rect, 1)
                    self.can_log_in = True
                else:
                    pygame.draw.rect(screen, (255, 0, 0), field_rect, 1)
                    self.can_log_in = False
            elif self.current_text == "":
                pygame.draw.rect(screen, (255, 0, 0), field_rect, 1)
                self.gui.draw_text(screen, "Недопустимое имя", (x + 29, y - 30))
                self.can_join = False
            elif [ord(x) for x in self.current_text] in [x[0] for x in self.save.data["users"]]:
                pygame.draw.rect(screen, (255, 0, 0), field_rect, 1)
                self.gui.draw_text(screen, "Такое имя уже существует", (x, y - 30))
                self.can_join = False
            else:
                pygame.draw.rect(screen, (0, 255, 0), field_rect, 1)
                self.gui.draw_text(screen, "Отличный никнейм!", (x + 23, y - 30))
                self.can_join = True
            if self.new and len(self.current_text) == 11:
                self.gui.draw_text(screen, "макс. количество символов", (x, y + 30))
            pygame.display.flip()

    def pressed_keys(self, e):
        self.new_char = e.name
