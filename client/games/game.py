class Game:
    def __init__(self, game_type):
        self.game_type = game_type
        self.tiles_ammount = 18
        self.tile_size = 48 * 18 / self.tiles_ammount

        if self.game_type == 'SANDBOX':
            self.tiles_ammount = 18
            self.tiles = [[-1 for j in range(self.tiles_ammount)]
                          for i in range(self.tiles_ammount)]
            self.tile_size = 48 * 18 / self.tiles_ammount
            self.adjacencies = [[4 for j in range(self.tiles_ammount)]
                            for i in range(self.tiles_ammount)]


    def change_tile_ammount(self, new_ammount):
        if self.game_type == 'SANDBOX':
            self.tiles_ammount = new_ammount
            self.tile_size = 48 * 18 / self.tiles_ammount

    def add_move(self, move):
        if self.game_type == 'SANDBOX':
            if self.tiles[move[1][0]][move[1][1]] == -1:
                self.tiles[move[1][0]][move[1][1]] = move[0]
                self.update_board()

    def remove_move(self, move):
        if self.game_type == 'SANDBOX':
            self.tiles[move[0]][move[1]] = -1

    def update_board(self):
        for i, row in enumerate(self.tiles):
            for j, move in enumerate(row):
                if move != -1:
                    try:
                        if self.tiles[i - 1][j] not in [move, -1]:
                            self.adjacencies[i][j] -= 1
                        elif self.tiles[i - 1][j] == move:
                            self.adjacencies[i][j] += self.adjacencies[i - 1][j] - 1
                    except IndexError:
                        pass
                    try:
                        if self.tiles[i + 1][j] not in [move, -1]:
                            self.adjacencies[i][j] -= 1
                        elif self.tiles[i + 1][j] == move:
                            self.adjacencies[i][j] += self.adjacencies[i + 1][j] - 1
                    except IndexError:
                        pass
                    try:
                        if self.tiles[i][j - 1] not in [move, -1]:
                            self.adjacencies[i][j] -= 1
                        elif self.tiles[i][j - 1] == move:
                            self.adjacencies[i][j] += self.adjacencies[i][j - 1] - 1
                    except IndexError:
                        pass
                    try:
                        if self.tiles[i][j + 1] not in [move, -1]:
                            self.adjacencies[i][j] -= 1
                        elif self.tiles[i][j + 1] == move:
                            self.adjacencies[i][j] += self.adjacencies[i][j + 1] - 1
                    except IndexError:
                        pass

        for i, row in enumerate(self.adjacencies):
            for j, adjacency in enumerate(row):
                if adjacency < 1:
                    self.adjacencies[i][j] = 4
                    self.tiles[i][j] = -1
