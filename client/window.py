import pygame
import os
from games.game import Game
import random

class Window:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.game = Game('SANDBOX')
        self.DEF_FONT = pygame.font.SysFont('Corbel', 35)
        self.SMALL_FONT = pygame.font.SysFont('Corbel', 24)
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

        self.board_margin_left = 200
        self.board_margin_top = 44
        self.board_margin_right = self.board_margin_top

        self.CON_TEXT = self.DEF_FONT.render('Connect', True, self.BLACK)
        self.right_site_center = (self.WIDTH + self.WIDTH - self.WIDTH / 4 - 5) / 2 - self.board_margin_right / 2
        self.con_btn_pos = (self.right_site_center - 100, self.HEIGHT - self.HEIGHT / 4)
        self.con_btn = pygame.Rect(self.con_btn_pos, (200, 75))

        self.EXIT_TEXT = self.SMALL_FONT.render('EXIT', True, self.BLACK)
        self.exit_margin_right = 0
        self.exit_margin_top = 50
        self.exit_btn_pos = (self.WIDTH - 125 - self.exit_margin_right, self.exit_margin_top)
        self.exit_btn = pygame.Rect(self.exit_btn_pos, (70, 35))

        self.game_mode_text = self.DEF_FONT.render('S A N D B O X', True, self.GOLD)
        self.game_mode_btn = pygame.Rect((self.right_site_center - 150, self.HEIGHT / 5), (300, 50))

        self.right_border = pygame.Rect((self.WIDTH - self.WIDTH / 4, self.board_margin_top), (self.WIDTH / 4 - 48, self.HEIGHT - 2 * self.board_margin_top))
        self.right_border_s = pygame.Surface((self.WIDTH / 4 - 48, self.HEIGHT - 2 * self.board_margin_top))  # the size of your rect
        self.right_border_s.set_alpha(200)  # alpha level
        self.right_border_s.fill(self.WHITE)
        self.BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'BG_1.png')), (self.WIDTH, self.HEIGHT))
        self.colors = [self.BLACK, self.WHITE]
        for x in range(8 + 1):
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
        self.run_status = {'con_clicked': False, 'exit_clicked': False, 'sandbox_clicked': False, 'go_clicked': False}

    def draw(self, server_status, run_status):
        self.WIN.blit(self.BG_IMG, (0, 0))
        self.WIN.blit(self.right_border_s, self.right_border)
        pygame.draw.rect(self.WIN, self.DARK_GREY, self.game_mode_btn)
        self.WIN.blit(self.game_mode_text, (self.right_site_center - self.game_mode_text.get_width()/2, self.HEIGHT / 5 + 10))
        if server_status == 'CLOSED':
            pygame.draw.rect(self.WIN, self.RED, self.con_btn)
        elif self.run_status['con_clicked']:
            pygame.draw.rect(self.WIN, self.GREY, self.con_btn)
        else:
            pygame.draw.rect(self.WIN, self.GOLD, self.con_btn)
        self.WIN.blit(self.CON_TEXT, (self.right_site_center - self.CON_TEXT.get_width() / 2, self.HEIGHT - self.HEIGHT / 4 + self.CON_TEXT.get_height() / 2))
        if self.run_status['exit_clicked']:
            pygame.draw.rect(self.WIN, self.GREY, self.exit_btn)
        else:
            pygame.draw.rect(self.WIN, self.DARK_RED, self.exit_btn)
        self.WIN.blit(self.EXIT_TEXT, (self.exit_btn_pos[0] + self.exit_btn.width/2 - self.EXIT_TEXT.get_width()/2,
                                       self.exit_btn_pos[1] + self.exit_btn.height/2 - self.EXIT_TEXT.get_height()/2 + 3))
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

            if pygame.mouse.get_pressed()[0]:
                if self.con_btn.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    self.run_status['con_clicked'] = True
                    return 'connect', game_type
                if self.exit_btn.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    self.run_status['exit_clicked_clicked'] = True
                    return 'exit', True
                for i, row in enumerate(self.game.tiles):
                    for j, tile in enumerate(row):
                        tile = pygame.Rect((j * self.game.tile_size + self.board_margin_left, i * self.game.tile_size + self.board_margin_top), (self.game.tile_size, self.game.tile_size))
                        if tile.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                            match self.get_clicked_corner(tile):
                                case 0:
                                    return 'move', [i, j]
                                case 1:
                                    return 'move', [i, j + 1]
                                case 2:
                                    return 'move', [i + 1, j]
                                case 3:
                                    return 'move', [i + 1, j + 1]
            else:
                if self.con_btn.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                    self.run_status['con_clicked'] = False

            if pygame.mouse.get_pressed()[2]:
                for i, row in enumerate(self.game.tiles):
                    for j, tile in enumerate(row):
                        tile = pygame.Rect((j * self.game.tile_size + self.board_margin_left, i * self.game.tile_size + self.board_margin_top), (self.game.tile_size, self.game.tile_size))
                        if tile.contains(pygame.Rect(pygame.mouse.get_pos(), (1, 1))):
                            match self.get_clicked_corner(tile):
                                case 0:
                                    return 'DEL', [i, j]
                                case 1:
                                    return 'DEL', [i, j + 1]
                                case 2:
                                    return 'DEL', [i + 1, j]
                                case 3:
                                    return 'DEL', [i + 1, j + 1]

        if move[0]:
            self.game.add_move([self.currently_placing, move[1]])
        if move[0] == 'DEL':
            self.game.remove_move(move[1])


        return 'run', run
