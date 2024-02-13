import pygame
import os

def draw(self, server_status, times, turn, clients_info, host):
    self.WIN.blit(self.BG_IMG, (0, 0))
    self.WIN.blit(self.right_border_s, self.right_border)

    self.WIN.blit(self.SCORE_TABLE, (10, self.board_margin_top))
    for line in self.score_horizontal_lines:
        pygame.draw.rect(self.WIN, self.BLACK, line)
    for line in self.score_vertical_lines:
        pygame.draw.rect(self.WIN, self.BLACK, line)

    for x, color in enumerate(self.colors):
        pygame.draw.rect(self.WIN, self.GREY,
                         pygame.Rect((21, self.board_margin_top + 30 + 27 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10) -
                                      ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10)),
                                     (34, 34))
                         )
        pygame.draw.rect(self.WIN, color,
                         pygame.Rect((23, self.board_margin_top + 30 + 29 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10) -
                                      ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10)),
                                     (30, 30))
                         )

    self.WIN.blit(self.SCORE_TEXT_1, (87, self.board_margin_top + 1))
    self.WIN.blit(self.SCORE_TEXT_2, (78, self.board_margin_top + self.SCORE_TEXT_1.get_height()))
    self.WIN.blit(self.SCORE_TEXT_3, (24, self.board_margin_top + self.SCORE_TEXT_2.get_height() / 2 + 1))

    if not self.run_status['connected']:
        for x, tile_points in enumerate(self.game.tile_points):
            text = self.SMALL_FONT.render(str(tile_points), True, self.BLACK)
            self.WIN.blit(text,
                          (100 - text.get_width() / 2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10) -
                           ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10))
                          )

        for x, hand_points in enumerate(self.game.hand_points):
            text = self.SMALL_FONT.render(str(hand_points), True, self.BLACK)
            self.WIN.blit(text,
                          (155 - text.get_width() / 2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10) -
                           ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10))
                          )
    else:
        all_tile_points = [client['tile_points'] for client in clients_info]
        for _ in range(10 - len(all_tile_points)):
            all_tile_points.append('-')
        for x, tile_points in enumerate(all_tile_points):
            text = self.SMALL_FONT.render(str(tile_points), True, self.BLACK)
            self.WIN.blit(text,
                          (100 - text.get_width() / 2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10) -
                           ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10))
                          )

        all_hand_points = [client['hand_points'] for client in clients_info]
        for _ in range(10 - len(all_hand_points)):
            all_hand_points.append('-')
        for x, hand_points in enumerate(all_hand_points):
            text = self.SMALL_FONT.render(str(hand_points), True, self.BLACK)
            self.WIN.blit(text,
                          (155 - text.get_width() / 2, self.board_margin_top + 25 + 35 + (x + 1) * ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10) -
                           ((self.HEIGHT - 2 * self.board_margin_top - 20) / 10))
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
        elif self.game.game_type in ['GO | 5', 'GO | 10', 'GO | 30']:  # Double check becouse of errors...
            minutes = times[1][turn] // 60
            seconds = times[1][turn] - minutes * 60
            if minutes >= 0 and seconds >= 0:  # Triple check
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
                    if seconds < 10:
                        time_2 = self.FONT_2.render(str(int(minutes)) + ' : 0' + str(int(seconds)), True, self.BLACK)
                    else:
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
                self.WIN.blit(game_mode_text, (left_side_text - game_mode_text.get_width() / 2, self.HEIGHT / 5 + row * game_mode_text.get_height()))
            else:
                self.WIN.blit(game_mode_text, (right_side_text - game_mode_text.get_width() / 2, self.HEIGHT / 5 + row * game_mode_text.get_height()))
        for button in self.game_modes_buttons:
            self.WIN.blit(*button)

        self.WIN.blit(self.game_mode_text, (self.right_site_center - self.game_mode_text.get_width() / 2, self.HEIGHT / 5 + 15))
    else:
        top_margin = 300 / (len(clients_info) + 1)
        beetwen_space = (500 - 20 * len(clients_info)) / (len(clients_info) + 1)
        up_text = self.SMALL_FONT.render('        Name         Role       End   ', True, self.BLACK)
        self.WIN.blit(up_text, (self.right_site_center - up_text.get_width() / 2, self.game_modes_bg.y + 5))
        for x, client in enumerate(clients_info):
            color = pygame.Rect((self.right_site_center - 135, self.game_modes_bg.y + 1 + top_margin + (beetwen_space * x)), (20, 20))
            pygame.draw.rect(self.WIN, self.colors[client['turn']], color)
            name = self.SMALL_FONT.render(client['name'], True, self.BLACK)
            self.WIN.blit(name, (self.right_site_center - 60 - name.get_width() / 2, self.game_modes_bg.y + top_margin + (beetwen_space * x)))
            role = self.SMALL_FONT.render(client['role'], True, self.BLACK)
            self.WIN.blit(role, (self.right_site_center + 30 - role.get_width() / 2, self.game_modes_bg.y + top_margin + (beetwen_space * x)))
            if client['end_game']:
                end_game = self.SMALL_FONT.render('Yes', True, self.BLACK)
            else:
                end_game = self.SMALL_FONT.render('No', True, self.BLACK)
            self.WIN.blit(end_game, (self.right_site_center + 105 - end_game.get_width() / 2, self.game_modes_bg.y + top_margin + (beetwen_space * x)))
        if len(clients_info) == 0:
            wait_text = self.SMALL_FONT.render('Waiting for clients...', True, self.BLACK)
            self.WIN.blit(wait_text, (self.right_site_center - wait_text.get_width() / 2, self.HEIGHT / 2 - 50))

        self.WIN.blit(*self.game_modes_buttons[0])
        self.WIN.blit(self.game_mode_text, (self.right_site_center - self.game_mode_text.get_width() / 2, self.HEIGHT / 5 + 15))

    if self.run_status['show_bar']:
        self.player_limit_bar_bg.y = self.HEIGHT / 2 + self.HEIGHT / 4.5
        player_limit_text = self.MINI_FONT.render('Players limit', True, self.BLACK)
        self.WIN.blit(player_limit_text, (self.right_site_center - player_limit_text.get_width() / 2, self.HEIGHT / 2 + self.HEIGHT / 4.5 - 35))
        self.WIN.blit(self.player_limit_bar_s, self.player_limit_bar_bg)
        pygame.draw.rect(self.WIN, self.REDDISH, self.choosen_limit_bar)
        for x, tab in enumerate(self.player_limit_tabs):
            pygame.draw.rect(self.WIN, self.BLACK, tab)
            self.WIN.blit(self.MINI_FONT.render(str(x + 2), True, self.BLACK), (self.right_site_center - 125 + 30 * x, self.HEIGHT / 2 + self.HEIGHT / 4.5 + 25))

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
            self.WIN.blit(text, ((tab.x * 2 + tab.width) / 2 - text.get_width() / 2, (tab.y * 2 + tab.height) / 2 - text.get_height() / 2 - 2))
    elif self.game.game_type == 'SANDBOX':
        self.player_limit_bar_bg.y = self.HEIGHT / 2 + self.HEIGHT / 4.5 + 5
        board_size_text = self.MINI_FONT.render('Board size', True, self.BLACK)
        self.WIN.blit(board_size_text, (self.right_site_center - board_size_text.get_width() / 2, self.HEIGHT / 2 + self.HEIGHT / 4.5 - 35))
        self.WIN.blit(self.player_limit_bar_s, self.player_limit_bar_bg)
        sizes = ['9x9', '19x19', '24x24']
        pygame.draw.rect(self.WIN, self.REDDISH, self.choosen_board_bar)
        for x, tab in enumerate([pygame.Rect((self.right_site_center - 117.5 + 100 * x, self.HEIGHT / 2 + self.HEIGHT / 4.5 - 10), (40, 40)) for x in range(3)]):
            pygame.draw.rect(self.WIN, self.BLACK, tab)
            text = self.MINI_FONT.render(sizes[x], True, self.WHITE)
            self.WIN.blit(text, ((tab.x * 2 + tab.width) / 2 - text.get_width() / 2, (tab.y * 2 + tab.height) / 2 - text.get_height() / 2 - 2))

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
    self.WIN.blit(self.EXIT_TEXT, (self.exit_btn_pos[0] + self.exit_btn.width / 2 - self.EXIT_TEXT.get_width() / 2,
                                   self.exit_btn_pos[1] + self.exit_btn.height / 2 - self.EXIT_TEXT.get_height() / 2 + 3))

    if self.game.game_type == 'SANDBOX':
        self.WIN.blit(self.CURRENTLY_PLACING_TEXT, (self.right_site_center - self.CURRENTLY_PLACING_TEXT.get_width() / 2 - 30, self.HEIGHT / 5 - 60))
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
                                   (j * self.game.tile_size + (self.game.tile_size / 4) + self.board_margin_left - (1 / self.game.tiles_ammount * 450) / 2,
                                    i * self.game.tile_size + (self.game.tile_size / 4) + self.board_margin_top - (1 / self.game.tiles_ammount * 450) / 2),
                                   1 / self.game.tiles_ammount * 320
                                   )

    if self.run_status['game_summary']:
        self.game_summary_bg.height = 200 + len(clients_info) * 30
        self.game_summary_bg.y = self.HEIGHT / 2 - self.game_summary_bg.height / 2
        self.game_summary_exit_btn.y = self.game_summary_bg.y + self.game_summary_bg.height - self.game_summary_exit_btn.height - 10
        pygame.draw.rect(self.WIN, self.GREY, self.game_summary_bg)
        pygame.draw.rect(self.WIN, self.REDDISH, self.game_summary_exit_btn)
        self.WIN.blit(self.game_summary_exit_text, (self.game_summary_exit_btn.x + self.game_summary_exit_btn.width / 2 - self.game_summary_exit_text.get_width() / 2,
                                                    self.game_summary_exit_btn.y + self.game_summary_exit_btn.height / 2 - self.game_summary_exit_text.get_height() / 2))

        for x, _ in enumerate(clients_info):
            try:
                if times[x] <= 0:
                    client['tile_points'] = 0
                    client['hand_points'] = 0
            except:
                pass
        sorted_clients_info = [[client['tile_points'] + client['hand_points'], client['turn'], client['name']] for client in clients_info]
        n = len(sorted_clients_info)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if sorted_clients_info[j][0] < sorted_clients_info[j + 1][0]:
                    sorted_clients_info[j], sorted_clients_info[j + 1] = sorted_clients_info[j + 1], sorted_clients_info[j]
            if not swapped:
                break
        top_margin = 45
        end_game_text = self.FONT_2.render('GAME ENDED', True, self.BLACK)
        self.WIN.blit(end_game_text, (self.game_summary_bg.x + self.game_summary_bg.width / 2 - end_game_text.get_width() / 2,
                                      self.game_summary_bg.y + end_game_text.get_height() + 5))
        places = []
        for x, client in enumerate(sorted_clients_info):
            places.append(x + 1)
            if x > 0 and client[0] == sorted_clients_info[x - 1][0]:
                places[-1] = places[-2]
            if x == 0 or client[0] == sorted_clients_info[0][0]:
                pygame.draw.rect(self.WIN, self.GOLD, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)), (480, 30)))
            elif x % 2 == 0:
                pygame.draw.rect(self.WIN, self.LIGHT_GREY, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)), (480, 30)))
            else:
                pygame.draw.rect(self.WIN, self.WHITE, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)), (480, 30)))

            if not x == 0:
                pygame.draw.rect(self.WIN, self.BLACK, pygame.Rect((self.game_summary_bg.x + 10, self.game_summary_bg.y + top_margin + 30 * (x + 1)), (480, 1)))

            number_text = self.SMALL_FONT.render(str(places[-1]) + ')', True, self.BLACK)
            self.WIN.blit(number_text, (self.game_summary_bg.x + 50, self.game_summary_bg.y + top_margin + 30 * (x + 1) + 5))
            name_text = self.SMALL_FONT.render(client[2], True, self.BLACK)
            self.WIN.blit(name_text, (self.WIDTH / 2 + 20 - name_text.get_width() / 2, self.game_summary_bg.y + top_margin + 30 * (x + 1) + 5))
            points_text = self.SMALL_FONT.render('Points:' + str(client[0]), True, self.BLACK)
            self.WIN.blit(points_text, (self.WIDTH / 2 + 180 - points_text.get_width() / 2, self.game_summary_bg.y + top_margin + 30 * (x + 1) + 5))
            pygame.draw.rect(self.WIN, self.colors[client[1]], pygame.Rect((self.game_summary_bg.x + 20, self.game_summary_bg.y + top_margin + 30 * (x + 1) + 5), (20, 20)))

    if self.run_status['connected'] and len(clients_info) >= turn + 1:
        pygame.draw.rect(self.WIN, self.GREY, self.FLAG_BG)
        try:
            if clients_info[turn]['end_game']:
                self.WIN.blit(self.WHITE_FLAG, (self.game_modes_bg.x + self.game_modes_bg.width - 40, 195))
            else:
                self.WIN.blit(self.BLACK_FLAG, (self.game_modes_bg.x + self.game_modes_bg.width - 40, 195))
        except IndexError:
            self.WIN.blit(self.WHITE_FLAG, (self.game_modes_bg.x + self.game_modes_bg.width - 40, 195))

    pygame.draw.rect(self.WIN, self.input_color, self.input_rect)
    text_surface = self.name_font.render(self.user_text, True, (255, 255, 255))
    self.WIN.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))
    self.input_rect.w = max(140, text_surface.get_width() + 10)
    self.WIN.blit(self.NAME_TEXT, (self.right_site_center - 140, 51))

    pygame.display.update()