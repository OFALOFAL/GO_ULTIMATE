import pygame
from game import Game

def run(self, run, server_status, game_type, turn, host, move, board, times, game_summary, clients_info):
    def get_clicked_corner(tile: pygame.Rect):
        if pygame.mouse.get_pos()[0] < tile.x + tile.width / 2:
            if pygame.mouse.get_pos()[1] < tile.y + tile.height / 2:
                return 0
            else:
                return 2
        else:
            if pygame.mouse.get_pos()[1] < tile.y + tile.height / 2:
                return 1
            else:
                return 3

    self.draw(server_status, times, turn, clients_info, host)
    if game_summary:
        self.run_status['game_summary'] = True

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return 'exit', run

        if ev.type == pygame.MOUSEWHEEL:
            if self.game.game_type == game_type == 'SANDBOX':
                if ev.y > 1:
                    ev.y = 1
                if ev.y < -1:
                    ev.y = -1
                if self.currently_placing + ev.y == len(self.colors):
                    self.currently_placing = 0
                elif self.currently_placing + ev.y == -1:
                    self.currently_placing = len(self.colors) - 1
                else:
                    self.currently_placing += ev.y

        if ev.type == pygame.KEYDOWN and self.active:
            if ev.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]
            elif len(self.user_text) <= 9:
                self.user_text += ev.unicode

        mouse = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        if pygame.mouse.get_pressed()[0] and not self.clicked:
            if self.input_rect.contains(mouse):
                self.active = True
                self.input_color = self.COLOR_ACTIVE
            else:
                self.active = False
                self.input_color = self.COLOR_PASSIVE
            if self.run_status['game_summary']:
                if self.game_summary_exit_btn.contains(mouse):
                    self.run_status['game_summary'] = False
                    return 'end_game_summary', run
            if self.FLAG_BG.contains(mouse):
                try:
                    if len(clients_info) > 1:
                        return 'END_GAME', run
                except:
                    pass
            for game_type_manage in ((_[1], self.game_modes[x]) for x, _ in enumerate(self.game_modes_buttons[1:])):
                cbb_x_pos = [1431, 1473, 1531, 1573, 1631]
                if game_type_manage[0].contains(mouse):
                    if game_type_manage[1] == 'SANDBOX':
                        if self.game.tiles_ammount == 24:
                            self.choosen_board_bar.x = cbb_x_pos[4]
                        elif self.game.tiles_ammount == 18:
                            self.choosen_board_bar.x = cbb_x_pos[2]
                        elif self.game.tiles_ammount == 8:
                            self.choosen_board_bar.x = cbb_x_pos[0]
                    elif not game_type_manage[1] == 'GO NATIONS':
                        if self.game.tiles_ammount == 24:
                            self.choosen_board_size = 18
                            self.choosen_board_bar.x = cbb_x_pos[3]  # I have no idea why i have to repeat that
                        if self.game.tiles_ammount == 18:
                            self.choosen_board_bar.x = cbb_x_pos[3]  # (that)
                        elif self.game.tiles_ammount == 8:
                            self.choosen_board_bar.x = cbb_x_pos[1]
                    self.clicked = True
                    if game_type_manage[1] == 'GO NATIONS':
                        self.run_status['show_bar'] = True
                        self.game = Game(game_type_manage[1], players_limit=self.choosen_limit)
                    else:
                        self.run_status['show_bar'] = False
                        self.game = Game(game_type_manage[1], tiles_ammount=self.choosen_board_size)
                    self.game_mode_text = self.FONT_2.render(self.game.game_type, True, self.GOLD)
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
                for x, tab in enumerate([pygame.Rect((self.right_site_center - 117.5 + 100 * x, self.HEIGHT / 2 + self.HEIGHT / 4.5 - 10), (40, 40)) for x in range(3)]):
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
                    return 'connect', [self.game.game_type, self.game.players_limit, self.choosen_board_size, self.user_text]
            if self.exit_btn.contains(mouse):
                self.clicked = True
                self.run_status['exit_clicked_clicked'] = True
                return 'exit', True
            for i, row in enumerate(self.game.tiles):
                for j, tile in enumerate(row):
                    tile = pygame.Rect((j * self.game.tile_size + self.board_margin_left, i * self.game.tile_size + self.board_margin_top), (self.game.tile_size, self.game.tile_size))
                    if tile.contains(mouse):
                        self.clicked = True
                        corner = get_clicked_corner(tile)
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
                        corner = get_clicked_corner(tile)
                        if corner == 0:
                            return 'del', [i, j]
                        if corner == 1:
                            return 'del', [i, j + 1]
                        if corner == 2:
                            return 'del', [i + 1, j]
                        if corner == 3:
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
        pass

    return 'run', [run, self.game.game_type]