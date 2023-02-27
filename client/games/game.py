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
        if self.game_type == 'SANDBOX':
            if self.tiles[move[1][0]][move[1][1]] == -1:
                self.tiles[move[1][0]][move[1][1]] = move[0]
                self.update_board(move)

    def remove_move(self, move):
        if self.game_type == 'SANDBOX':
            self.tiles[move[0]][move[1]] = -1

    def remove_enclosed_groups(self, by_group, last_move):
        moves_to_reset = []
        for color, groups in enumerate(by_group):
            for group in groups:
                enclosed = self.is_enclosed(group)
                if enclosed and last_move not in group:
                    for move in group:
                        moves_to_reset.append(move)
                elif last_move in group and enclosed:
                    for groups_check in groups:
                        if all(self.is_enclosed_with_last(groups_check, last_move)) and last_move not in groups_check:
                            for move_ in groups_check:
                                moves_to_reset.append(move_)
        for move in moves_to_reset:
            self.tiles[move[0]][move[1]] = -1

    def is_enclosed_with_last(self, group, last_move):  #TODO: almost done, when fixed it'll be all easier...
        last_move_in_enclosing = False
        for move in group:
            i, j = move[0], move[1]
            corresponding = (self.tiles[i - 1][j], self.tiles[i + 1][j], self.tiles[i][j - 1], self.tiles[i][j + 1])
            if last_move in corresponding:
                last_move_in_enclosing = True
            try:
                if all((x == -1 for x in corresponding)):
                    return [False, last_move_in_enclosing]
            except IndexError:
                pass
        return [True, last_move_in_enclosing]

    def is_enclosed(self, group):
        for move in group:
            i, j = move[0], move[1]
            try:
                if self.tiles[i - 1][j] == -1 or self.tiles[i + 1][j] == -1 or self.tiles[i][j - 1] == -1 or self.tiles[i][j + 1] == -1:
                    return False
            except IndexError:
                pass
        return True

    def update_board(self, last_move):
        by_color = [[] for _ in range(11)]
        for i, row in enumerate(self.tiles):
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
                adj_color = self.tiles[adj[0]][adj[1]]
                if adj_color == color:
                    group.extend(dfs(color, adj))
            return group

        for color, moves in enumerate(by_color):
            for move in moves:
                if tuple(move) not in visited:
                    group = dfs(color, tuple(move))
                    by_group[color].append(group)

        self.remove_enclosed_groups(by_group, last_move)
