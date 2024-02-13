import pygame
import os
from game import Game
import random

class Window:
    from .run import run
    from .draw import draw

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Go Ultimate')
        self.Icon = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'icon.png')), (32, 32))
        pygame.display.set_icon(self.Icon)

        self.game = Game('SANDBOX')
        self.DEF_FONT = pygame.font.SysFont('Corbel', 35)
        self.SMALL_FONT = pygame.font.SysFont('Corbel', 24)
        self.MINI_FONT = pygame.font.SysFont('Corbel', 16)

        self.FONT_2 = pygame.font.SysFont('Cabril', 35)
        self.SMALL_FONT_2 =  pygame.font.SysFont('Cabril', 24)
        self.MINI_FONT_2 = pygame.font.SysFont('Cabril', 16)

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
        self.COLOR_ACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_PASSIVE = pygame.Color('bisque3')

        self.board_margin_left = 250
        self.board_margin_top = 44
        self.board_margin_right = self.board_margin_top

        self.CON_TEXT = self.DEF_FONT.render('Connect', True, self.BLACK)
        self.RESET_TEXT = self.DEF_FONT.render('Reset', True, self.BLACK)
        self.right_site_center = (self.WIDTH + self.WIDTH - self.WIDTH / 4 - 5) / 2 - self.board_margin_right / 2
        self.con_btn_pos = (self.right_site_center - 100, self.HEIGHT - self.HEIGHT / 5)
        self.con_btn = pygame.Rect(self.con_btn_pos, (200, 75))

        self.EXIT_TEXT = self.SMALL_FONT.render('EXIT', True, self.BLACK)
        self.exit_margin_right = 0
        self.exit_margin_top = 50
        self.exit_btn_pos = (self.WIDTH - 125 - self.exit_margin_right, self.exit_margin_top)
        self.exit_btn = pygame.Rect(self.exit_btn_pos, (70, 35))

        self.game_mode_text = self.FONT_2.render('S A N D B O X', True, self.GOLD)
        self.game_mode_btn = pygame.Rect((self.right_site_center - 150, self.HEIGHT / 5), (300, 50))
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

        self.game_modes = ['GO', 'GO | 5', 'GO | 10', 'GO | 30', 'GO NATIONS', 'SANDBOX']
        self.game_modes_text = [self.SMALL_FONT_2.render(name, True, self.GOLD) for name in self.game_modes]
        top_surface = pygame.Surface((300, 50))
        top_surface.set_alpha(50)
        top_surface.fill(self.GREY)
        self.game_modes_buttons = [(top_surface, pygame.Rect((self.right_site_center - 150, self.HEIGHT / 5), (300, self.game_modes_bg.height / len(self.game_modes))))]
        row = 0
        for x, game_mode in enumerate(self.game_modes):
            if x % 2 == 0:
                row += 7
                surface = pygame.Surface((self.game_modes_bg.width/2, self.game_modes_bg.height/(len(self.game_modes)+2)))
                surface.set_alpha(50)
                surface.fill(self.GREY)
                rect = pygame.Rect((self.right_site_center - 150, self.HEIGHT / 5 + row * self.game_modes_text[0].get_height() - self.game_modes_bg.height/len(self.game_modes)/4),
                                   (150, self.game_modes_bg.height/len(self.game_modes)))
                self.game_modes_buttons.append((surface, rect))
            else:
                surface = pygame.Surface((self.game_modes_bg.width / 2, self.game_modes_bg.height / (len(self.game_modes) + 2)))
                surface.set_alpha(50)
                surface.fill(self.GREY)
                rect = pygame.Rect((self.right_site_center, self.HEIGHT / 5 + row * self.game_modes_text[0].get_height() - self.game_modes_bg.height / len(self.game_modes) / 4),
                                   (150, self.game_modes_bg.height / len(self.game_modes)))
                self.game_modes_buttons.append((surface, rect))

        self.player_limit_bar_s = pygame.Surface((300, 10))
        self.player_limit_bar_s.set_alpha(200)
        self.player_limit_bar_s.fill(self.LIGHT_GREY)
        self.player_limit_bar_bg = pygame.Rect((self.right_site_center - 150, self.HEIGHT/2 + self.HEIGHT/4.5), (300, 10))
        self.player_limit_tabs = [pygame.Rect((self.right_site_center - 125 + 30 * x, self.HEIGHT/2 + self.HEIGHT/4.5 - 10), (12, 30)) for x in range(9)]
        self.choosen_limit_bar = pygame.Rect((self.right_site_center - 127 + 30 * 8, self.HEIGHT/2 + self.HEIGHT/4.5 - 12), (16, 34))
        self.choosen_limit = 10

        self.choosen_board_size = 18
        self.choosen_board_bar = pygame.Rect((self.right_site_center - 117.5 + 100 - 2, self.HEIGHT/2 + self.HEIGHT/4.5 - 12), (44, 44))
        self.board_size_tabs = [pygame.Rect((self.right_site_center - 75 + 100 * x, self.HEIGHT/2 + self.HEIGHT/4.5 - 10), (40, 40)) for x in range(2)]

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
        self.run_status = {'con_clicked': False, 'exit_clicked': False, 'go_clicked': False, 'show_bar': False, 'connected': False, 'game_summary': False}
        self.last_move = []
        self.clicked = False
        self.clock = ((pygame.Rect((self.right_site_center - 200 - 5 - 150, self.HEIGHT - self.board_margin_top - 40), (150, 40)), self.BLACK),
                      (pygame.Rect((self.right_site_center - 200 - 5 - 145, self.HEIGHT - self.board_margin_top - 36), (140, 32)), self.LIGHT_GREY))
        self.enemy_clock = ((pygame.Rect((self.right_site_center - 200 - 5 - 150, self.board_margin_top), (150, 40)), self.BLACK),
                      (pygame.Rect((self.right_site_center - 200 - 5 - 145, self.board_margin_top + 4), (140, 32)), self.LIGHT_GREY))
        self.game_summary_bg = pygame.Rect((self.WIDTH/2 - 150, self.HEIGHT/2 - 250), (500, 500))
        self.game_summary_exit_btn = pygame.Rect((self.game_summary_bg.x + self.game_summary_bg.width/2 - 75, self.game_summary_bg.y + self.game_summary_bg.height - 45),
                                                 (150, 70))
        self.game_summary_exit_text = self.SMALL_FONT.render('EXIT', True, self.BLACK)

        self.WHITE_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'white_flag.png')), (30, 30))
        self.BLACK_FLAG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'black_flag.png')), (30, 30))
        self.FLAG_BG = pygame.Rect((self.game_modes_bg.x + self.game_modes_bg.width - 40, 195), (30, 30))

        self.name_font = pygame.font.Font(None, 32)
        self.user_text = ''

        self.NAME_TEXT = self.DEF_FONT.render('NAME:', True, self.BLACK)
        self.input_rect = pygame.Rect((self.right_site_center - 35, 50), (140, 32))
        self.input_color = self.COLOR_PASSIVE

        self.active = False
        self.last_game_type = self.game.game_type