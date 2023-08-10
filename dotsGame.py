import pygame as pg
import Player
import gameField
import logInGUI
import save
import startGUI
import gameLogic


class GameDots:
    def __init__(self):
        self.play_game()

    def play_game(self):
        pg.init()
        pg.display.set_caption('Dots')
        gf = gameField.GameField(20, 2)
        gui0 = startGUI.StartGUI(24, gf)
        users = save.SavingSystem()
        acc = logInGUI.Account(gui0, users, gf)
        acc.choose_account(gf.screen, 30, 40)
        gui0.draw_dropdown(gf.screen, "Режим игры", ["с друзьями", "с компьютером"], "Продолжить", "с друзьями", 30, 40)
        if gf.with_bot:
            gui1 = startGUI.StartGUI(24, gf)
            gui1.draw_dropdown(gf.screen, "Сложность", ["легко", "тяжело"], "Продолжить", "легко", 30, 40)
        else:
            gui1 = startGUI.StartGUI(24, gf)
            gui1.draw_dropdown(gf.screen, "Кол-во игроков", ["2", "3", "4"], "Продолжить", "2", 30, 40)
        gui2 = startGUI.StartGUI(24, gf)
        gui2.draw_dropdown(gf.screen, "Размер поля", ["10", "13", "15", "18", "21", "23", "26",
                                                      "28", "31", "33", "36", "38", "40"], "Начать игру", "10", 30, 40)
        players = Player.Players(gf.grid_size, gui0)
        game = gameLogic.GameLogic(gf, players, users)
        gf.screen.fill((255, 250, 250))
        gf.draw_grid()
        game.game_loop()
