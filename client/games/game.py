class Game:
    def __init__(self, game_type):
        self.game_type = game_type
        self.tiles_ammount = 18
        self.tile_size = 48 * 18 / self.tiles_ammount

        if self.game_type == 'SANDBOX':
            self.tiles_ammount = 18
            self.tiles = [[-1 for j in range(self.tiles_ammount + 1)]
                          for i in range(self.tiles_ammount + 1)]
            self.tile_size = 48 * 18 / self.tiles_ammount
            self.adjacencies = [[4 for j in range(self.tiles_ammount + 1)]
                            for i in range(self.tiles_ammount + 1)]


    def change_tile_ammount(self, new_ammount):
        if self.game_type == 'SANDBOX':
            self.tiles_ammount = new_ammount
            self.tile_size = 48 * 18 / self.tiles_ammount

    def add_move(self, move):
        valid = False
        if self.game_type == 'SANDBOX':
            if self.tiles[move[1][0]][move[1][1]] == -1:
                valid = self.update_board(self.tiles.copy(), move)
        return valid

    def remove_move(self, move):
        if self.game_type == 'SANDBOX':
            if self.tiles[move[0]][move[1]] != -1:
                self.tiles[move[0]][move[1]] = -1

    def remove_enclosed_groups(self, tiles, by_group, last_move_info):
        moves_to_reset = []
        color, last_move = last_move_info
        last_move = tuple(last_move)
        valid = True

        for color, groups in enumerate(by_group):
            for group in groups:
                if self.is_enclosed(tiles, group):
                    if last_move not in group:
                        for move in group:
                            moves_to_reset.append(move)
                    elif last_move in group:
                        valid = False   # set valid to False becouse the move would be suicide
                        for color_, groups_ in enumerate(by_group):
                            for group_ in groups_:
                                if last_move not in group_ and self.is_enclosed_with_last(tiles, group_, last_move):
                                    valid = True    # turn valid back to True becouse of the prior rule
        # If move is valide -> update the real board, if not -> remove the last move
        if valid:
            for move in moves_to_reset:
                tiles[move[0]][move[1]] = -1
            self.tiles = tiles
        else:
            tiles[last_move[0]][last_move[1]] = -1
        return valid
    def is_enclosed_with_last(self, tiles, group, last_move):
        last_move_in_enclosing = False
        for move in group:
            i, j = move[0], move[1]
            last_move_in_enclosing = last_move == (i - 1, j) or last_move == (i + 1, j) or last_move == (i, j - 1) or last_move == (i, j + 1)
            try:
                if tiles[i - 1][j] == -1 or tiles[i + 1][j] == -1 or tiles[i][j - 1] == -1 or tiles[i][j + 1] == -1:
                    return False
            except IndexError:
                pass
        return True and last_move_in_enclosing

    def is_enclosed(self, tiles, group):
        for move in group:
            i, j = move[0], move[1]
            try:
                if tiles[i - 1][j] == -1 or tiles[i + 1][j] == -1 or tiles[i][j - 1] == -1 or tiles[i][j + 1] == -1:
                    return False
            except IndexError:
                pass
        return True

    def update_board(self, tiles, last_move):
        tiles[last_move[1][0]][last_move[1][1]] = last_move[0]

        by_color = [[] for _ in range(11)]
        for i, row in enumerate(tiles):
            for j, move in enumerate(row):
                if move != -1:
                    by_color[move].append([i, j])


        by_group = [[] for _ in range(11)]
        visited = set()

        def dfs(color, move):
            group = [move]
            visited.add(move)
            adj_moves = [(move[0] - 1, move[1]), (move[0] + 1, move[1]), (move[0], move[1] - 1), (move[0], move[1] + 1)]
            for adj in adj_moves:
                if adj in visited:
                    continue
                adj_color = tiles[adj[0]][adj[1]]
                if adj_color == color:
                    group.extend(dfs(color, adj))
            return group

        for color, moves in enumerate(by_color):
            for move in moves:
                if tuple(move) not in visited:
                    group = dfs(color, tuple(move))
                    by_group[color].append(group)

        return self.remove_enclosed_groups(tiles, by_group, last_move)
