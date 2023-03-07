import pygame
import os
from game import Game
import random

class Window:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.game = Game('SANDBOX')
        self.DEF_FONT = pygame.font.SysFont('Corbel', 35)
        self.SMALL_FONT = pygame.font.SysFont('Corbel', 24)
        self.MINI_FONT = pygame.font.SysFont('Corbel', 16)

        self.WIDTH = 1800
        self.HEIGHT = 950
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.LIGHT_GREY = (211,211,211)
        self.GREY = (128,128,128)
        self.DARK_GREY = (105,105,105)
        self.RED = (255, 0, 0)
        self.DARK_RED = (200, 30, 30)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GOLD = (212, 175, 55)
        self.REDDISH = (255, 61, 13)

        self.board_margin_left = 200
        self.board_margin_top = 44
        self.board_margin_right = self.board_margin_top

        self.CON_TEXT = self.DEF_FONT.render('Connect', True, self.BLACK)
        self.RESET_TEXT = self.DEF_FONT.render('Reset', True, self.BLACK)
        self.right_site_center = (self.WIDTH + self.WIDTH - self.WIDTH / 4 - 5) / 2 - self.board_margin_right / 2
        self.con_btn_pos = (self.right_site_center - 100, self.HEIGHT - self.HEIGHT / 4)
        self.con_btn = pygame.Rect(self.con_btn_pos, (200, 75))

        self.EXIT_TEXT = self.SMALL_FONT.render('EXIT', True, self.BLACK)
        self.exit_margin_right = 0
        self.exit_margin_top = 50
        self.exit_btn_pos = (self.WIDTH - 125 - self.exit_margin_right, self.exit_margin_top)
        self.exit_btn = pygame.Rect(self.exit_btn_pos, (70, 35))

        self.game_mode_text = self.DEF_FONT.render('S A N D B O X', True, self.GOLD)
        self.game_mode_btn = pygame.Rect((self.right_site_center - 150, self.HEIGHT / 5), (300, 50))    # TODO: make the button to be able to change mode
        self.game_modes_bg = pygame.Rect((self.right_site_center - 150, self.HEIGHT / 5 + self.game_mode_btn.height), (300, 400))

        self.CURRENTLY_PLACING_TEXT = self.SMALL_FONT.render('CURRENTLY PLACING:', True, self.BLACK)
        self.currently_placing_color = pygame.Rect((self.WIDTH - 150 - self.exit_margin_right, self.HEIGHT / 5 - 70), (35, 35))
        self.CURRENTLY_PLACING_COLOR_BG = pygame.Rect((self.WIDTH - 150 - self.exit_margin_right - 5, self.HEIGHT / 5 - 70 - 5), (45, 45))

        self.SCORE_TABLE = pygame.Surface((175, self.HEIGHT - 2 * self.board_margin_top))
        self.SCORE_TABLE.set_alpha(300)
        self.SCORE_TABLE.fill(self.WHITE)

        self.score_horizontal_lines = [
            pygame.Rect((10 + 175/3, self.board_margin_top), (3, self.HEIGHT - 2 * self.board_margin_top)),
            pygame.Rect((10 + 2 * (175/3), self.board_margin_top), (3, self.HEIGHT - 2 * self.board_margin_top))
        ]

        self.score_vertical_lines = [
            pygame.Rect((10, self.board_margin_top + 30 + (x + 1) * (self.HEIGHT - 2 * self.board_margin_top - 20)/10), (175, 3))
            for x in range(9)
        ]
        self.score_vertical_lines.append(pygame.Rect((10, self.board_margin_top + 35), (175, 3)))

        self.SCORE_TEXT_1 = self.MINI_FONT.render('tile           hand', True, self.BLACK)
        self.SCORE_TEXT_2 = self.MINI_FONT.render('points       points', True, self.BLACK)
        self.SCORE_TEXT_3 = self.MINI_FONT.render('color', True, self.BLACK)

        self.right_border = pygame.Rect((self.WIDTH - self.WIDTH / 4, self.board_margin_top), (self.WIDTH / 4 - 48, self.HEIGHT - 2 * self.board_margin_top))
        self.right_border_s = pygame.Surface((self.WIDTH / 4 - 48, self.HEIGHT - 2 * self.board_margin_top))
        self.right_border_s.set_alpha(200)
        self.right_border_s.fill(self.WHITE)

        self.game_modes = ['SANDBOX', 'GO', 'GO 5', 'GO 10', 'GO NATIONS']
        self.game_modes_text = [self.SMALL_FONT.render(name, True, self.GOLD) for name in self.game_modes]

        self.BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'BG_1.png')), (self.WIDTH, self.HEIGHT))
        self.colors = [self.BLACK, self.WHITE]
        for x in range(8):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            valid = False
            while not valid:
                for added_color in self.colors:
                    if (added_color[0] - 30 < color[0] < added_color[0] + 30) and \
                            (added_color[1] - 30 < color[1] < added_color[1] + 30) and \
                            (added_color[2] - 30 < color[2] < added_color[2] + 30):
                        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        break
                valid = True
            self.colors.append(color)
        self.currently_placing = 0
        self.run_status = {'con_clicked': False, 'exit_clicked': False, 'game_mode_clicked': False, 'go_clicked': False}
        self.last_move = []
        self.clicked = False

    def draw(self, server_status, run_status):
        self.WIN.blit(self.BG_IMG, (0, 0))
        self.WIN.blit(self.right_border_s, self.right_border)
        self.WIN.blit(self.SCORE_TABLE, (10, self.board_margin_top))

        for line in self.score_horizontal_lines:
            pygame.draw.rect(self.WIN, self.BLACK, line)

        for line in self.score_vertical_lines:
            pygame.draw.rect(self.WIN, self.BLACK, line)

        for x, color in enumerate(self.colors):
            pygame.draw.rect(self.WIN, self.GREY,
                                pygame.Rect((21, self.board_margin_top + 30 + 27 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20)/10) -
                                             ((self.HEIGHT - 2 * self.board_margin_top - 20)/10)),
                                (34, 34))
                             )
            pygame.draw.rect(self.WIN, color,
                                pygame.Rect((23, self.board_margin_top + 30 + 29 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20)/10) -
                                             ((self.HEIGHT - 2 * self.board_margin_top - 20)/10)),
                                (30, 30))
                             )

        self.WIN.blit(self.SCORE_TEXT_1, (87, self.board_margin_top + 1))
        self.WIN.blit(self.SCORE_TEXT_2, (78, self.board_margin_top + self.SCORE_TEXT_1.get_height()))
        self.WIN.blit(self.SCORE_TEXT_3, (24, self.board_margin_top + self.SCORE_TEXT_2.get_height()/2 + 1))

        for x, tile_points in enumerate(self.game.tile_points):
            text = self.SMALL_FONT.render(str(tile_points), True, self.BLACK)
            self.WIN.blit(text,
                          (100 - text.get_width()/2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20)/10) -
                                             ((self.HEIGHT - 2 * self.board_margin_top - 20)/10))
                          )

        for x, hand_points in enumerate(self.game.hand_points):
            text = self.SMALL_FONT.render(str(hand_points), True, self.BLACK)
            self.WIN.blit(text,
                          (155 - text.get_width()/2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20)/10) -
                                             ((self.HEIGHT - 2 * self.board_margin_top - 20)/10))
                          )


        if self.run_status['game_mode_clicked']:
            pygame.draw.rect(self.WIN, self.REDDISH, self.game_modes_bg)
            pygame.draw.rect(self.WIN, self.REDDISH, self.game_mode_btn)
            row = 0
            for x, game_mode_text in enumerate(self.game_modes_text):
                if x % 2 == 0:
                    row += 1
                    self.WIN.blit(game_mode_text, (self.right_site_center + game_mode_text.get_width() + 10, self.HEIGHT / 5 + 100 + row * game_mode_text.get_height()))
                else:
                    self.WIN.blit(game_mode_text, (self.right_site_center - game_mode_text.get_width() - 10, self.HEIGHT / 5 + 100 + row * game_mode_text.get_height()))
        else:
            pygame.draw.rect(self.WIN, self.DARK_GREY, self.game_mode_btn)

        self.WIN.blit(self.game_mode_text, (self.right_site_center - self.game_mode_text.get_width()/2, self.HEIGHT / 5 + 10))

        if server_status == 'CLOSED':
            pygame.draw.rect(self.WIN, self.RED, self.con_btn)
        elif self.run_status['con_clicked']:
            pygame.draw.rect(self.WIN, self.GREY, self.con_btn)
        else:
            pygame.draw.rect(self.WIN, self.GOLD, self.con_btn)

        if self.game.game_type == 'SANDBOX':
            self.WIN.blit(self.RESET_TEXT, (self.right_site_center - self.RESET_TEXT.get_width() / 2, self.HEIGHT - self.HEIGHT / 4 + self.RESET_TEXT.get_height() / 2))
        else:
            self.WIN.blit(self.CON_TEXT, (self.right_site_center - self.CON_TEXT.get_width() / 2, self.HEIGHT - self.HEIGHT / 4 + self.CON_TEXT.get_height() / 2))
        if self.run_status['exit_clicked']:
            pygame.draw.rect(self.WIN, self.GREY, self.exit_btn)
        else:
            pygame.draw.rect(self.WIN, self.DARK_RED, self.exit_btn)
        self.WIN.blit(self.EXIT_TEXT, (self.exit_btn_pos[0] + self.exit_btn.width/2 - self.EXIT_TEXT.get_width()/2,
                                       self.exit_btn_pos[1] + self.exit_btn.height/2 - self.EXIT_TEXT.get_height()/2 + 3))
        self.WIN.blit(self.CURRENTLY_PLACING_TEXT, (self.right_site_center - self.CURRENTLY_PLACING_TEXT.get_width()/2 - 30, self.HEIGHT / 5 - 60))
        pygame.draw.rect(self.WIN, self.GREY, self.CURRENTLY_PLACING_COLOR_BG)
        pygame.draw.rect(self.WIN, self.colors[self.currently_placing], self.currently_placing_color)

        for i in range(self.game.tiles_ammount):
            for j in range(self.game.tiles_ammount):
                self.WIN.blit(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'tile_1.png')), (self.game.tile_size, self.game.tile_size)),
                              (i * self.game.tile_size + self.board_margin_left, j * self.game.tile_size + self.board_margin_top))

        for i, row in enumerate(self.game.tiles):
            for j, move in enumerate(row):
                if move != -1:
                    pygame.draw.rect(self.WIN, self.colors[move], pygame.Rect(
                        (j * self.game.tile_size + self.board_margin_left - (self.game.tiles_ammount / 0.9) / 2,
                         i * self.game.tile_size + self.board_margin_top - (self.game.tiles_ammount / 0.9) / 2),
                                                                       (self.game.tiles_ammount / 0.9, self.game.tiles_ammount / 0.9)
                    ))

        pygame.display.update()

    @staticmethod
    def get_clicked_corner(tile: pygame.Rect):
        if pygame.mouse.get_pos()[0] < tile.x + tile.width/2:
            if pygame.mouse.get_pos()[1] < tile.y + tile.height/2:
                return 0
            else:
                return 2
        else:
            if pygame.mouse.get_pos()[1] < tile.y + tile.height/2:
                return 1
            else:
                return 3

    def run(self, run, server_status, game_type, move):
        self.draw(server_status, self.run_status)

        for ev in pygame.event.get():

            if ev.type == pygame.MOUSEWHEEL:
                if self.game.game_type == game_type == 'SANDBOX':
                    if ev.y > 1:
                        ev.y = 1
                    if ev.y < -1:
                        ev.y = -1
                    if self.currently_placing + ev.y == len(self.colors):
                        self.currently_placing = 0
                    elif self.currently_placing + ev.y == -1:
                        self.currently_placing = len(self.colors) -1
                    else:
                        self.currently_placing += ev.y

            if ev.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0] and not self.clicked:   # TODO: reset clicks when clicked outside of any button
                if self.con_btn.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    self.clicked = True
                    self.run_status['con_clicked'] = True
                    if self.game.game_type == 'SANDBOX':
                        self.game.setup_sandbox()
                    else:
                        return 'connect', game_type
                if self.exit_btn.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    self.clicked = True
                    self.run_status['exit_clicked_clicked'] = True
                    return 'exit', True
                if self.game_mode_btn.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    self.clicked = True
                    self.run_status['game_mode_clicked'] = not self.run_status['game_mode_clicked']
                for i, row in enumerate(self.game.tiles):
                    for j, tile in enumerate(row):
                        tile = pygame.Rect((j * self.game.tile_size + self.board_margin_left, i * self.game.tile_size + self.board_margin_top), (self.game.tile_size, self.game.tile_size))
                        if tile.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                            self.clicked = True
                            corner = self.get_clicked_corner(tile)
                            if corner == 0:
                                return 'move', [i, j]
                            elif corner == 1:
                                return 'move', [i, j + 1]
                            elif corner == 2:
                                return 'move', [i + 1, j]
                            elif corner == 3:
                                return 'move', [i + 1, j + 1]
            elif self.clicked:
                self.clicked = False

            if pygame.mouse.get_pressed()[2]:
                for i, row in enumerate(self.game.tiles):
                    for j, tile in enumerate(row):
                        tile = pygame.Rect((j * self.game.tile_size + self.board_margin_left, i * self.game.tile_size + self.board_margin_top), (self.game.tile_size, self.game.tile_size))
                        if tile.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                            corner = self.get_clicked_corner(tile)
                            if corner ==  0:
                                return 'DEL', [i, j]
                            if corner ==  1:
                                return 'DEL', [i, j + 1]
                            if corner ==  2:
                                return 'DEL', [i + 1, j]
                            if corner ==  3:
                                return 'DEL', [i + 1, j + 1]

        if move[0] == 'MOVE':
            if self.last_move != move[1]:
                self.last_move = move[1]
                valid = self.game.add_move([self.currently_placing, move[1]])
        if move[0] == 'DEL':
            self.game.remove_move(move[1])
            self.last_move = []

        return 'run', run
