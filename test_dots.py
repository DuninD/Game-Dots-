import unittest
import bots
from gameField import GameField
from gameLogic import GameLogic
from Player import Players
from logInGUI import Account
from unittest.mock import patch, Mock


class Tests(unittest.TestCase):
    @patch('random.randint', side_effect=[1, 2])
    def test_easy_bot_successful_move(self, mock_randint):
        game_logic_mock = Mock()
        computer = bots.Computer(24, game_logic_mock)
        game_logic_mock.gf.grid = [[None for _ in range(computer.grid_size)] for _ in range(computer.grid_size)]
        computer.easy_bot()
        mock_randint.assert_called_with(0, computer.grid_size - 1)
        game_logic_mock.next_move.assert_called_with(1, 2)

    @patch('random.randint', side_effect=[0, 0, 0, 1])
    def test_easy_bot_multiple_attempts(self, mock_randint):
        game_logic_mock = Mock()
        computer = bots.Computer(24, game_logic_mock)
        game_logic_mock.gf.grid = [[None for _ in range(computer.grid_size)] for _ in range(computer.grid_size)]
        computer.easy_bot()
        computer.easy_bot()
        mock_randint.assert_called_with(0, computer.grid_size - 1)
        self.assertEqual(game_logic_mock.next_move.call_count, 2)
        game_logic_mock.next_move.assert_called_with(0, 1)

    @patch('random.randint', side_effect=[0, 0, 1, 0])
    def test_hard_bot_successful_move(self, mock_randint):
        game_logic_mock = Mock()
        computer = bots.Computer(24, game_logic_mock)
        game_logic_mock.gf.grid_size = computer.grid_size
        game_logic_mock.gf.grid = [[None for _ in range(computer.grid_size)] for _ in range(computer.grid_size)]
        player_x, player_y = 1, 1
        computer.hard_bot(player_x, player_y)
        self.assertEqual(mock_randint.call_count, 4)
        game_logic_mock.next_move.assert_called()

    @patch('random.randint', side_effect=[0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1])
    def test_hard_bot_move_after_reset(self, mock_randint):
        game_logic_mock = Mock()
        computer = bots.Computer(24, game_logic_mock)
        game_logic_mock.gf.grid_size = computer.grid_size
        game_logic_mock.gf.grid = [[None for _ in range(computer.grid_size)] for _ in range(computer.grid_size)]
        game_logic_mock.gf.grid[4][2] = 1
        game_logic_mock.gf.grid[4][4] = 1
        player_x, player_y = 1, 1
        computer.count1 = 39
        computer.last = [(10, 10)]
        computer.hard_bot(player_x, player_y)
        computer.hard_bot(player_x, player_y)
        computer.hard_bot(player_x, player_y)
        self.assertEqual(mock_randint.call_count, 12)
        game_logic_mock.next_move.assert_called()

    def test_update_basic(self):
        gf = GameField(24, 3)
        grid_size = 10
        count_players = 2
        gf.update(grid_size, count_players)
        self.assertEqual(gf.grid_size, grid_size)
        self.assertEqual(gf.space, 800 // grid_size)
        self.assertEqual(len(gf.grid), grid_size)
        for row in gf.grid:
            self.assertEqual(len(row), grid_size)
            self.assertTrue(all(cell is None for cell in row))
        self.assertEqual(gf.radius, 5)
        self.assertEqual(gf.count_players, count_players)

    def test_update_different_values(self):
        gf = GameField(24, 2)
        grid_size = 6
        count_players = 3
        gf.update(grid_size, count_players)
        self.assertEqual(gf.grid_size, grid_size)
        self.assertEqual(gf.space, 800 // grid_size)
        self.assertEqual(len(gf.grid), grid_size)
        for row in gf.grid:
            self.assertEqual(len(row), grid_size)
            self.assertTrue(all(cell is None for cell in row))
        self.assertEqual(gf.radius, 5)
        self.assertEqual(gf.count_players, count_players)

    def test_find_loop_start_edge(self):
        game_logic = GameLogic(GameField(20, 2), None, None)
        grid_size = 20
        game_logic.gf.grid_size = grid_size
        game_logic.list_to_find_cycles = []
        game_logic.gf.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        game_logic.gf.grid[1][2] = 0
        game_logic.gf.grid[2][1] = 0
        game_logic.gf.grid[2][3] = 0
        game_logic.gf.grid[3][2] = 0
        player_color = 0
        start_edge = (1, 2)
        game_logic.find_loop(1, 2, player_color, [start_edge], start_edge)
        expected_path = [[(1, 2), (2, 1), (3, 2), (2, 3), (1, 2)], [(1, 2), (2, 3), (3, 2), (2, 1), (1, 2)]]
        self.assertEqual(expected_path, game_logic.list_to_find_cycles)

    def test_find_loop_no_cycle(self):
        game_logic = GameLogic(GameField(20, 2), None, None)
        grid_size = 20
        game_logic.gf.grid_size = grid_size
        game_logic.list_to_find_cycles = []
        game_logic.gf.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        player_color = 0
        start_edge = (0, 0)
        path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        game_logic.find_loop(4, 0, player_color, path, start_edge)
        self.assertNotIn(path, game_logic.list_to_find_cycles)

    def test_inside_is_enemy_no_enemy_dots(self):
        game_logic = GameLogic(GameField(20, 2), None, None)
        grid_size = 20
        game_logic.gf.grid_size = grid_size
        game_logic.gf.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        game_logic.CURRENT_PLAYER = 0
        path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
        min_x, max_x, min_y, max_y = 0, 4, 0, 0
        result = game_logic.inside_is_enemy(min_x, max_x, min_y, max_y, path)
        expected_inside_dots, expected_counter_enemy_dots, expected_count_our_color_inside_dots = [], 0, 0
        self.assertEqual(result, (expected_inside_dots, expected_counter_enemy_dots,
                                  expected_count_our_color_inside_dots))

    def test_inside_is_enemy_with_enemy_dots(self):
        game_logic = GameLogic(GameField(20, 2), None, None)
        grid_size = 20
        game_logic.gf.grid_size = grid_size
        game_logic.gf.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        game_logic.CURRENT_PLAYER = 0
        path = [(1, 2), (2, 1), (3, 2), (2, 3), (1, 2)]
        min_x, max_x, min_y, max_y = 1, 3, 1, 3
        game_logic.gf.grid[2][2] = 1
        game_logic.gf.grid[1][2] = 0
        game_logic.gf.grid[2][1] = 0
        game_logic.gf.grid[2][3] = 0
        game_logic.gf.grid[3][2] = 0
        result = game_logic.inside_is_enemy(min_x, max_x, min_y, max_y, path)
        expected_inside_dots = [(2, 2)]
        expected_counter_enemy_dots = 1
        expected_count_our_color_inside_dots = 0
        self.assertEqual(result, (expected_inside_dots, expected_counter_enemy_dots,
                                  expected_count_our_color_inside_dots))

    def test_point_in_polygon_inside(self):
        game_logic = GameLogic(GameField(20, 2), None, None)
        polygon = [(0, 0), (0, 4), (4, 4), (4, 0)]
        point_inside = (2, 2)
        result = game_logic.point_in_polygon(point_inside, polygon)
        self.assertTrue(result)

    def test_point_in_polygon_outside(self):
        game_logic = GameLogic(GameField(20, 2), None, None)
        polygon = [(0, 0), (0, 4), (4, 4), (4, 0)]
        point_outside = (5, 5)
        result = game_logic.point_in_polygon(point_outside, polygon)
        self.assertFalse(result)

    @patch('pygame.draw.line')
    def test_next_move_with_shortest_paths(self, _):
        game_logic = GameLogic(GameField(20, 2), Players(20, None), None)
        grid_size = 20
        game_logic.gf.grid_size = grid_size
        game_logic.gf.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        game_logic.gf.grid[0][1] = 0
        game_logic.gf.grid[2][1] = 0
        game_logic.gf.grid[3][1] = 0
        game_logic.gf.grid[4][1] = 0
        game_logic.gf.grid[1][2] = 0
        game_logic.gf.grid[1][3] = 0
        game_logic.gf.grid[1][4] = 0
        game_logic.gf.grid[2][5] = 0
        game_logic.gf.grid[3][4] = 0
        game_logic.gf.grid[3][3] = 0
        game_logic.gf.grid[4][3] = 0
        game_logic.gf.grid[5][2] = 0
        game_logic.gf.grid[1][1] = 1
        game_logic.gf.grid[2][4] = 1
        game_logic.gf.grid[4][2] = 1
        game_logic.CURRENT_PLAYER = 0
        result = [[(1, 0), (0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (3, 4), (3, 3), (4, 3), (5, 2), (4, 1), (3, 1),
                   (2, 1), (1, 0)],
                  [(1, 0), (0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (3, 4),
                   (4, 3), (5, 2), (4, 1), (3, 1), (2, 1), (1, 0)],
                  [(1, 0), (0, 1), (1, 2), (2, 1), (1, 0)],
                  [(1, 0), (2, 1), (1, 2), (0, 1), (1, 0)],
                  [(1, 0), (2, 1), (3, 1), (4, 1), (5, 2), (4, 3), (3, 3),
                   (3, 4), (2, 5), (1, 4), (1, 3), (1, 2), (0, 1), (1, 0)],
                  [(1, 0), (2, 1), (3, 1), (4, 1), (5, 2), (4, 3), (3, 4),
                   (2, 5), (1, 4), (1, 3), (1, 2), (0, 1), (1, 0)]]

        game_logic.next_move(1, 0)
        self.assertEqual(result, game_logic.list_to_find_cycles)

    @patch('pygame.draw.line')
    def test_next_move_without_shortest_paths(self, _):
        game_logic = GameLogic(GameField(20, 2), None, None)
        grid_size = 5
        game_logic.gf.grid_size = grid_size
        game_logic.gf.grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
        game_logic.CURRENT_PLAYER = 0
        game_logic.list_to_find_cycles = []
        game_logic.next_move(3, 0)
        self.assertEqual([], game_logic.list_to_find_cycles)

    def test_pressed_keys_a(self):
        lg = Account(None, None, None)
        mock_event = Mock()
        mock_event.name = 'A'
        lg.pressed_keys(mock_event)
        self.assertEqual(lg.new_char, 'A')

    def test_pressed_keys_w(self):
        lg = Account(None, None, None)
        mock_event = Mock()
        mock_event.name = 'W'
        lg.pressed_keys(mock_event)
        self.assertEqual(lg.new_char, 'W')

    def test_update_score_basic(self):
        players = Players(20, None)
        player = 1
        score = 3
        dots = [(2, 2), (3, 3)]
        players.update_score(player, score, dots)
        self.assertEqual(players.points[player], score)
        self.assertEqual(dots, players.catching_dots[player])

    def test_update_score_existing_dot(self):
        players = Players(20, None)
        player = 0
        score = 2
        dots = [(1, 1), (2, 2)]
        players.catching_dots[player] = [(1, 1), (3, 3)]
        players.update_score(player, score, dots)
        self.assertEqual(players.points[player], score)
        self.assertIn(dots[0], players.catching_dots[player])
        self.assertIn(dots[1], players.catching_dots[player])

    def test_update_score_empty_dot(self):
        players = Players(20, None)
        player = 1
        score = 1
        dots = []
        players.update_score(player, score, dots)
        self.assertEqual(players.points[player], 1)
        self.assertEqual([], players.catching_dots[player])
