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

    def draw(self, server_status, run_status, times, turn, clients_info, game_summary):
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

        if not self.run_status['connected']:
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
        else:
            all_tile_points = [client['tile_points'] for client in clients_info]
            for _ in range(10 - len(all_tile_points)):
                all_tile_points.append('-')
            for x, tile_points in enumerate(all_tile_points):
                text = self.SMALL_FONT.render(str(tile_points), True, self.BLACK)
                self.WIN.blit(text,
                              (100 - text.get_width()/2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20)/10) -
                               ((self.HEIGHT - 2 * self.board_margin_top - 20)/10))
                              )

            all_hand_points = [client['hand_points'] for client in clients_info]
            for _ in range(10 - len(all_hand_points)):
                all_hand_points.append('-')
            for x, hand_points in enumerate(all_hand_points):
                text = self.SMALL_FONT.render(str(hand_points), True, self.BLACK)
                self.WIN.blit(text,
                              (155 - text.get_width()/2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20)/10) -
                               ((self.HEIGHT - 2 * self.board_margin_top - 20)/10))
                              )

        if self.game.game_type not in ['SANDBOX', 'GO', 'GO NATIONS']:
            for piece in self.clock:
                pygame.draw.rect(self.WIN, piece[1], piece[0])
            for piece in self.enemy_clock:
                pygame.draw.rect(self.WIN, piece[1], piece[0])
            if not self.run_status['connected'] or not times[0]:
                time = self.FONT_2.render(str(self.game.time) + ' : 00', True, self.BLACK)
                self.WIN.blit(time, ((self.clock[0][0].x * 2 + self.clock[0][0].width) / 2 - time.get_width() / 2,
                                     (self.clock[0][0].y * 2 + self.clock[0][0].height) / 2 - time.get_height() / 2))
                self.WIN.blit(time, ((self.enemy_clock[0][0].x * 2 + self.enemy_clock[0][0].width) / 2 - time.get_width() / 2,
                                     (self.enemy_clock[0][0].y * 2 + self.enemy_clock[0][0].height) / 2 - time.get_height() / 2))
            else:
                minutes = times[1][turn] // 60
                seconds = times[1][turn] - minutes * 60
                if seconds:
                    if seconds < 10:
                        time_1 = self.FONT_2.render(str(int(minutes)) + ' : 0' + str(int(seconds)), True, self.BLACK)
                    else:
                        time_1 = self.FONT_2.render(str(int(minutes)) + ' : ' + str(int(seconds)), True, self.BLACK)
                else:
                    time_1 = self.FONT_2.render(str(int(minutes)) + ' : 00', True, self.BLACK)
                if turn == 0:
                    minutes = times[1][1] // 60
                    seconds = times[1][1] - minutes * 60
                else:
                    minutes = times[1][0] // 60
                    seconds = times[1][0] - minutes * 60
                if seconds:
                    time_2 = self.FONT_2.render(str(int(minutes)) + ' : ' + str(int(seconds)), True, self.BLACK)
                else:
                    time_2 = self.FONT_2.render(str(int(minutes)) + ' : 00', True, self.BLACK)
                self.WIN.blit(time_1, ((self.clock[0][0].x * 2 + self.clock[0][0].width) / 2 - time_2.get_width() / 2,
                                       (self.clock[0][0].y * 2 + self.clock[0][0].height) / 2 - time_2.get_height() / 2))
                self.WIN.blit(time_2, ((self.enemy_clock[0][0].x * 2 + self.enemy_clock[0][0].width) / 2 - time_1.get_width() / 2,
                                       (self.enemy_clock[0][0].y * 2 + self.enemy_clock[0][0].height) / 2 - time_1.get_height() / 2))


        left_side_text = self.right_site_center - 65
        right_side_text = self.right_site_center + 75
        pygame.draw.rect(self.WIN, self.REDDISH, self.game_modes_bg)
        pygame.draw.rect(self.WIN, self.REDDISH, self.game_mode_btn)
        if not self.run_status['connected']:
            row = 0
            for x, game_mode_text in enumerate(self.game_modes_text):
                if x % 2 == 0:
                    row += 7
                    self.WIN.blit(game_mode_text, (left_side_text - game_mode_text.get_width()/2, self.HEIGHT / 5 + row * game_mode_text.get_height()))
                else:
                    self.WIN.blit(game_mode_text, (right_side_text - game_mode_text.get_width()/2, self.HEIGHT / 5 + row * game_mode_text.get_height()))
            for button in self.game_modes_buttons:
                self.WIN.blit(*button)

            self.WIN.blit(self.game_mode_text, (self.right_site_center - self.game_mode_text.get_width()/2, self.HEIGHT / 5 + 15))
        else:
            top_margin = 300/(len(clients_info)+1)
            beetwen_space = (500 - 20 * len(clients_info))/(len(clients_info)+1)
            up_text= self.SMALL_FONT.render('        Name         Role       End   ', True, self.BLACK)
            self.WIN.blit(up_text, (self.right_site_center - up_text.get_width()/2, self.game_modes_bg.y + 5))
            for x, client in enumerate(clients_info):
                color = pygame.Rect((self.right_site_center - 135, self.game_modes_bg.y + 1 + top_margin + (beetwen_space * x)), (20, 20))
                pygame.draw.rect(self.WIN, self.colors[client['turn']], color)
                name = self.SMALL_FONT.render('Client: '+str(client['id']), True, self.BLACK)    # TODO: change it to use name when added max name len 9
                self.WIN.blit(name, (self.right_site_center - 140 + name.get_width()/2, self.game_modes_bg.y + top_margin + (beetwen_space * x)))
                role = self.SMALL_FONT.render(client['role'], True, self.BLACK)
                self.WIN.blit(role, (self.right_site_center + 30 - role.get_width()/2, self.game_modes_bg.y + top_margin + (beetwen_space * x)))
                if client['end_game']:
                    end_game = self.SMALL_FONT.render('Yes', True, self.BLACK)
                else:
                    end_game = self.SMALL_FONT.render('No', True, self.BLACK)
                self.WIN.blit(end_game, (self.right_site_center + 105 - end_game.get_width()/2, self.game_modes_bg.y + top_margin + (beetwen_space * x)))
            if len(clients_info) == 0:
                wait_text = self.SMALL_FONT.render('Waiting for clients...', True, self.BLACK)
                self.WIN.blit(wait_text, (self.right_site_center - wait_text.get_width()/2, self.HEIGHT/2 - 50))

            self.WIN.blit(*self.game_modes_buttons[0])
            self.WIN.blit(self.game_mode_text, (self.right_site_center - self.game_mode_text.get_width() / 2, self.HEIGHT / 5 + 15))

        if self.run_status['show_bar']:
            self.player_limit_bar_bg.y = self.HEIGHT/2 + self.HEIGHT/4.5
            player_limit_text = self.MINI_FONT.render('Players limit', True, self.BLACK)
            self.WIN.blit(player_limit_text, (self.right_site_center - player_limit_text.get_width()/2, self.HEIGHT/2 + self.HEIGHT/4.5 - 35))
            self.WIN.blit(self.player_limit_bar_s, self.player_limit_bar_bg)
            pygame.draw.rect(self.WIN, self.REDDISH, self.choosen_limit_bar)
            for x, tab in enumerate(self.player_limit_tabs):
                pygame.draw.rect(self.WIN, self.BLACK, tab)
                self.WIN.blit(self.MINI_FONT.render(str(x + 2), True, self.BLACK), (self.right_site_center - 125 + 30 * x, self.HEIGHT/2 + self.HEIGHT/4.5 + 25))

        if self.game.game_type in ['GO', 'GO | 5', 'GO | 10', 'GO | 30']:
            self.player_limit_bar_bg.y = self.HEIGHT / 2 + self.HEIGHT / 4.5 + 5
            board_size_text = self.MINI_FONT.render('Board size', True, self.BLACK)
            self.WIN.blit(board_size_text, (self.right_site_center - board_size_text.get_width() / 2, self.HEIGHT / 2 + self.HEIGHT / 4.5 - 35))
            self.WIN.blit(self.player_limit_bar_s, self.player_limit_bar_bg)
            sizes = ['9x9', '19x19']
            pygame.draw.rect(self.WIN, self.REDDISH, self.choosen_board_bar)
            for x, tab in enumerate(self.board_size_tabs):
                pygame.draw.rect(self.WIN, self.BLACK, tab)
                text = self.MINI_FONT.render(sizes[x], True, self.WHITE)
                self.WIN.blit(text, ((tab.x * 2 + tab.width)/2 - text.get_width()/2, (tab.y * 2 + tab.height)/2 - text.get_height()/2 - 2))
        elif self.game.game_type == 'SANDBOX':
            self.player_limit_bar_bg.y = self.HEIGHT / 2 + self.HEIGHT / 4.5 + 5
            board_size_text = self.MINI_FONT.render('Board size', True, self.BLACK)
            self.WIN.blit(board_size_text, (self.right_site_center - board_size_text.get_width() / 2, self.HEIGHT / 2 + self.HEIGHT / 4.5 - 35))
            self.WIN.blit(self.player_limit_bar_s, self.player_limit_bar_bg)
            sizes = ['9x9', '19x19', '24x24']
            pygame.draw.rect(self.WIN, self.REDDISH, self.choosen_board_bar)
            for x, tab in enumerate([pygame.Rect((self.right_site_center - 117.5 + 100 * x, self.HEIGHT/2 + self.HEIGHT/4.5 - 10), (40, 40)) for x in range(3)]):
                pygame.draw.rect(self.WIN, self.BLACK, tab)
                text = self.MINI_FONT.render(sizes[x], True, self.WHITE)
                self.WIN.blit(text, ((tab.x * 2 + tab.width)/2 - text.get_width()/2, (tab.y * 2 + tab.height)/2 - text.get_height()/2 - 2))

        if self.game.game_type == 'SANDBOX':
            if self.run_status['con_clicked']:
                pygame.draw.rect(self.WIN, self.GREY, self.con_btn)
            else:
                pygame.draw.rect(self.WIN, self.GOLD, self.con_btn)
        else:
            if server_status == 'CLOSED':
                pygame.draw.rect(self.WIN, self.RED, self.con_btn)
            elif self.run_status['connected']:
                pygame.draw.rect(self.WIN, self.GREEN, self.con_btn)
            elif self.run_status['con_clicked']:
                pygame.draw.rect(self.WIN, self.GREY, self.con_btn)
            else:
                pygame.draw.rect(self.WIN, self.GOLD, self.con_btn)

        if self.game.game_type == 'SANDBOX':
            self.WIN.blit(self.RESET_TEXT, (self.right_site_center - self.RESET_TEXT.get_width() / 2, self.HEIGHT - self.HEIGHT / 5 + self.RESET_TEXT.get_height() / 2))
        else:
            self.WIN.blit(self.CON_TEXT, (self.right_site_center - self.CON_TEXT.get_width() / 2, self.HEIGHT - self.HEIGHT / 5 + self.CON_TEXT.get_height() / 2))
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
                    pygame.draw.circle(self.WIN, self.colors[move],
                                       (j * self.game.tile_size + (self.game.tile_size / 4) + self.board_margin_left - (1/self.game.tiles_ammount * 450) / 2,
                                        i * self.game.tile_size + (self.game.tile_size / 4) + self.board_margin_top - (1/self.game.tiles_ammount * 450) / 2),
                                       1/self.game.tiles_ammount * 320
                                       )

        if self.run_status['game_summary']:
            self.game_summary_bg.height = 200 + len(clients_info) * 30
            self.game_summary_bg.y = self.HEIGHT/2 - self.game_summary_bg.height/2
            self.game_summary_exit_btn.y = self.game_summary_bg.y + self.game_summary_bg.height - self.game_summary_exit_btn.height - 10
            pygame.draw.rect(self.WIN, self.GREY, self.game_summary_bg)
            pygame.draw.rect(self.WIN, self.REDDISH, self.game_summary_exit_btn)
            self.WIN.blit(self.game_summary_exit_text, (self.game_summary_exit_btn.x + self.game_summary_exit_btn.width/2 - self.game_summary_exit_text.get_width()/2,
                                                        self.game_summary_exit_btn.y + self.game_summary_exit_btn.height/2 - self.game_summary_exit_text.get_height()/2))

            sorted_clients_info = [[client['tile_points']+client['hand_points'], client['turn']] for client in clients_info]
            n = len(sorted_clients_info)
            for i in range(n):
                swapped = False
                for j in range(0, n - i - 1):
                    if sorted_clients_info[j][0] > sorted_clients_info[j + 1][0]:
                        sorted_clients_info[j], sorted_clients_info[j + 1] = sorted_clients_info[j + 1], sorted_clients_info[j]
                if not swapped:
                    break
            top_margin = 45
            end_game_text = self.FONT_2.render('GAME ENDED', True, self.BLACK)
            self.WIN.blit(end_game_text, (self.game_summary_bg.x + self.game_summary_bg.width/2 - end_game_text.get_width()/2,
                                          self.game_summary_bg.y + end_game_text.get_height() + 5))
            places = []
            for x, client in enumerate(sorted_clients_info):
                places.append(x+1)
                if x > 0 and client[0] == sorted_clients_info[x-1][0]:
                    places[-1] = places[-2]
                if x == 0 or client[0] == sorted_clients_info[0][0]:
                    pygame.draw.rect(self.WIN, self.GOLD, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)),(480, 30)))
                elif x % 2 == 0:
                    pygame.draw.rect(self.WIN, self.LIGHT_GREY, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)),(480, 30)))
                else:
                    pygame.draw.rect(self.WIN, self.WHITE, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)),(480, 30)))

                if not x == 0:
                    pygame.draw.rect(self.WIN, self.BLACK, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)), (480, 1)))

                # TODO: change it to use name when added max name len 9
                number_text = self.SMALL_FONT.render(str(places[-1])+')', True, self.BLACK)
                self.WIN.blit(number_text, (self.game_summary_bg.x + 50, self.game_summary_bg.y + top_margin + 30 * (x + 1) + 5))
                points_text = self.SMALL_FONT.render('Client: '+str(client[1])+'          Points:'+str(client[0]), True, self.BLACK)
                self.WIN.blit(points_text, (self.WIDTH/2, self.game_summary_bg.y + top_margin + 30 * (x + 1) + 5))
                pygame.draw.rect(self.WIN, self.colors[client[1]], pygame.Rect((self.game_summary_bg.x + 20, self.game_summary_bg.y + top_margin + 30 * (x + 1) + 5), (20, 20)))

        if self.run_status['connected'] and len(clients_info) >= turn+1:
            pygame.draw.rect(self.WIN, self.GREY, self.FLAG_BG)
            if clients_info[turn]['end_game']:
                self.WIN.blit(self.WHITE_FLAG, (self.game_modes_bg.x + self.game_modes_bg.width - 40, 195))
            else:
                self.WIN.blit(self.BLACK_FLAG, (self.game_modes_bg.x + self.game_modes_bg.width - 40, 195))

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

    def run(self, run, server_status, game_type, turn, move, board, times, game_summary, clients_info):
        self.draw(server_status, self.run_status, times, turn, clients_info, game_summary)
        if game_summary:
            self.run_status['game_summary'] = True

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
            
            mouse = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                if self.run_status['game_summary']:
                    if self.game_summary_exit_btn.contains(mouse):
                        self.run_status['game_summary'] = False
                        return 'end_game_summary', run
                if self.FLAG_BG.contains(mouse):
                    return 'END_GAME', run
                for game_type_manage in ((_[1], self.game_modes[x]) for x, _ in enumerate(self.game_modes_buttons[1:])):
                    if game_type_manage[0].contains(mouse):
                        if self.game.game_type == 'SANDBOX' and not game_type_manage[1] == 'SANDBOX':
                            if self.game.tiles_ammount == 24:
                                self.choosen_board_size = 18
                                self.choosen_board_bar.x -= 57.5
                            elif self.game.tiles_ammount == 18:
                                self.choosen_board_bar.x += 42.5
                            elif self.game.tiles_ammount == 8:
                                self.choosen_board_bar.x += 42.5
                        elif not self.game.game_type == 'SANDBOX' and game_type_manage[1] == 'SANDBOX':
                            if self.game.tiles_ammount == 18:
                                self.choosen_board_bar.x -= 42
                            elif self.game.tiles_ammount == 8:
                                self.choosen_board_bar.x -= 42
                        self.clicked = True
                        if game_type_manage[1] == 'GO NATIONS':
                            self.run_status['show_bar'] = True
                            self.game = Game(game_type_manage[1], players_limit=self.choosen_limit)
                        else:
                            self.run_status['show_bar'] = False
                            self.game = Game(game_type_manage[1], tiles_ammount=self.choosen_board_size)
                if self.run_status['show_bar']:
                    for x, tab in enumerate(self.player_limit_tabs):
                        if tab.contains(mouse) and not self.run_status['connected']:
                            self.clicked = True
                            self.choosen_limit = x + 2
                            self.choosen_limit_bar.x = self.right_site_center - 127 + 30 * x
                            self.game = Game('GO NATIONS', players_limit=self.choosen_limit)
                            self.choosen_board_size = self.game.tiles_ammount
                if self.game.game_type in ['GO', 'GO | 5', 'GO | 10', 'GO | 30']:
                    sizes = [8, 18]
                    for x, tab in enumerate(self.board_size_tabs):
                        if tab.contains(mouse) and not self.run_status['connected']:
                            self.clicked = True
                            self.choosen_board_bar.x = tab.x - 2
                            self.choosen_board_size = sizes[x]
                            self.game = Game(self.game.game_type, tiles_ammount=self.choosen_board_size)
                elif self.game.game_type == 'SANDBOX':
                    sizes = [8, 18, 24]
                    for x, tab in enumerate([pygame.Rect((self.right_site_center - 117.5 + 100 * x, self.HEIGHT/2 + self.HEIGHT/4.5 - 10), (40, 40)) for x in range(3)]):
                        if tab.contains(mouse):
                            self.clicked = True
                            self.choosen_board_bar.x = tab.x - 2
                            self.choosen_board_size = sizes[x]
                            self.game = Game(self.game.game_type, tiles_ammount=self.choosen_board_size)
                if self.con_btn.contains(mouse):
                    self.clicked = True
                    self.run_status['con_clicked'] = True
                    if self.game.game_type == 'SANDBOX':
                        self.game.setup_sandbox(self.game.tiles_ammount)
                    elif self.run_status['connected']:
                        return 'disconnect', [self.game.game_type, False, False]
                    else:
                        return 'connect', [self.game.game_type, self.game.players_limit, self.choosen_board_size]
                if self.exit_btn.contains(mouse):
                    self.clicked = True
                    self.run_status['exit_clicked_clicked'] = True
                    return 'exit', True
                for i, row in enumerate(self.game.tiles):
                    for j, tile in enumerate(row):
                        tile = pygame.Rect((j * self.game.tile_size + self.board_margin_left, i * self.game.tile_size + self.board_margin_top), (self.game.tile_size, self.game.tile_size))
                        if tile.contains(mouse):
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
            elif ev.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
                self.run_status['con_clicked'] = False

            if pygame.mouse.get_pressed()[2]:
                for i, row in enumerate(self.game.tiles):
                    for j, tile in enumerate(row):
                        tile = pygame.Rect((j * self.game.tile_size + self.board_margin_left, i * self.game.tile_size + self.board_margin_top), (self.game.tile_size, self.game.tile_size))
                        if tile.contains(mouse):
                            corner = self.get_clicked_corner(tile)
                            if corner ==  0:
                                return 'del', [i, j]
                            if corner ==  1:
                                return 'del', [i, j + 1]
                            if corner ==  2:
                                return 'del', [i + 1, j]
                            if corner ==  3:
                                return 'del', [i + 1, j + 1]

        if move[0] == 'MOVE':
            if self.last_move != move[1]:
                self.last_move = move[1]
                valid = self.game.add_move([self.currently_placing, move[1]])
        if move[0] == 'DEL':
            self.game.remove_move(move[1])
            self.last_move = []
        if move == 'CHANGE_MOVE':
            pass

        if board[0]:
            self.game.tiles = board[1]

        if server_status == 'CONNECTED':
            self.run_status['connected'] = True
        elif server_status == 'DISCONNECTED':
            self.run_status['connected'] = False

        if game_summary:
            self.run_status['connected'] = False

        if server_status == 'END_GAME_REQ':
            pass    # TODO: change to ask player if he wants to end the game

        return 'run', [run, self.game.game_type]
