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
        for color, groups in enumerate(by_group):
            for group in groups:
                enclosed = self.is_enclosed(group)
                if len(group) == 1:
                    if group[0] == last_move:
                        print('ok')
                        continue
                    if enclosed:
                        self.tiles[group[0][0]][group[0][1]] = -1
                elif enclosed and last_move not in group:
                    for move in group:
                        self.tiles[move[0]][move[1]] = -1
                elif last_move in group and enclosed:
                    pass    # TODO: write here so if the last move was in the group it first checks if that last move coused other group to close

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
