class Game:
    def __init__(self, game_type, players_limit = 2, tiles_ammount = 18):
        self.players_limit = None
        self.tiles = None
        self.tile_points = None
        self.hand_points = None
        self.empty_groups = None
        self.tile_size = None
        self.tiles_ammount = None
        self.time = False

        self.game_type = game_type
        self.moves_list = []
        self.moves = 0

        if self.game_type == 'SANDBOX':
            self.setup_sandbox(tiles_ammount)
        elif self.game_type == 'GO':
            self.setup_go(False, tiles_ammount)
        elif self.game_type in ['GO | 5', 'GO | 10', 'GO | 30']:
            time = self.game_type.split('| ')[1]
            self.setup_go(int(time), tiles_ammount)
        elif self.game_type == 'GO NATIONS':
            self.setup_go_nations(players_limit)

    def setup_sandbox(self, tiles_ammount):
        self.players_limit = 10
        self.empty_groups = []
        self.hand_points = [0 for _ in range(10)]
        self.tile_points = [0 for _ in range(10)]
        self.tiles_ammount = tiles_ammount
        self.tiles = [[-1 for j in range(self.tiles_ammount + 1)]
                      for i in range(self.tiles_ammount + 1)]
        self.tile_size = 48 * 18 / self.tiles_ammount

    def setup_go_nations(self, players_limit):
        self.players_limit = players_limit
        self.empty_groups = []
        self.hand_points = [0 for _ in range(10)]
        self.tile_points = [0 for _ in range(10)]
        self.tiles_ammount = 24
        self.tiles = [[-1 for j in range(self.tiles_ammount + 1)]
                      for i in range(self.tiles_ammount + 1)]
        self.tile_size = 48 * 18 / self.tiles_ammount

    def setup_go(self, time, tiles_ammount):
        self.time = time
        self.players_limit = 2
        self.empty_groups = []
        self.hand_points = [0 for _ in range(10)]
        self.tile_points = [0 for _ in range(10)]
        self.tiles_ammount = tiles_ammount
        self.tiles = [[-1 for j in range(self.tiles_ammount + 1)]
                      for i in range(self.tiles_ammount + 1)]
        self.tile_size = 48 * 18 / self.tiles_ammount

    def change_tile_ammount(self, new_ammount):
        if self.game_type == 'SANDBOX':
            self.tiles_ammount = new_ammount
            self.tile_size = 48 * 18 / self.tiles_ammount

    def add_move(self, move):
        valid = False
        if self.game_type == 'SANDBOX':
            try:
                if self.tiles[move[1][0]][move[1][1]] == -1:
                    valid = self.update_board(self.tiles.copy(), move)
                    self.count_tile_points()
            except IndexError:
                pass
        if valid:
            self.moves += 1
            self.moves_list.append(move)
        return valid

    def remove_move(self, move):
        if self.game_type == 'SANDBOX':
            try:
                for i, _move in enumerate(self.moves_list):
                    coordinates = _move[1]
                    if coordinates == list(move):
                        del self.moves_list[i]
                self.tiles[move[0]][move[1]] = -1
            except IndexError:
                pass
        self.count_tile_points()

    def remove_enclosed_groups(self, tiles, by_group, current_color, new_move):
        moves_to_reset = []
        valid = True
        for color, groups in enumerate(by_group):
            for group in groups:
                if self.is_enclosed(tiles, group):
                    if new_move in group:
                        valid = False   # set valid to False becouse the move would be suicide
                        for color_, groups_ in enumerate(by_group):
                            for group_ in groups_:
                                enclosed_with_last, enclosing_tiles = self.is_enclosed_with_last(tiles, group_, new_move, get_enclosing_tiles=True)
                                if enclosed_with_last and new_move not in group_:
                                    moves_by_color = {}
                                    for key, value in self.moves_list:
                                        if key in moves_by_color:
                                            moves_by_color[key].append(tuple(value))
                                        else:
                                            moves_by_color[key] = [tuple(value)]

                                    try:
                                        last_self_move = moves_by_color[current_color][-1]
                                    except KeyError:
                                        last_self_move = None

                                    if new_move != last_self_move:
                                        valid = True    # turn valid back to True becouse of the prior rule
                    else:
                        for move in group:
                            moves_to_reset.append(move)


        # If move is valide -> update the real board, if not -> remove the last move
        if valid:
            for move in moves_to_reset:
                self.hand_points[current_color] += 1    # no other than last move could delete any group as those wolud be deleted in other turns
                tiles[move[0]][move[1]] = -1
            self.tiles = tiles
        else:
            tiles[new_move[0]][new_move[1]] = -1
        return valid

    def is_enclosed(self, tiles, group, get_enclosing_tiles=False):
        enclosing_tiles = []
        enclosed = True
        for move in group:
            i, j = move[0], move[1]
            adj_moves = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
            for adj in adj_moves:
                if -1 not in adj and self.tiles_ammount + 1 not in adj:
                    try:
                        if tiles[adj[0]][adj[1]] == -1:
                            if not get_enclosing_tiles:
                                return False
                            else:
                                enclosed = False
                    except IndexError:
                        pass
                    enclosing_tiles.append(adj)

        return enclosed, enclosing_tiles if get_enclosing_tiles else enclosed

    def is_enclosed_with_last(self, tiles, group, last_move, get_enclosing_tiles=False):
        enclosed, enclosing_tiles = self.is_enclosed(tiles, group, get_enclosing_tiles=True)
        enclosed_with_last = enclosed and last_move in enclosing_tiles
        return enclosed_with_last, enclosing_tiles if get_enclosing_tiles else enclosed_with_last

    def update_board(self, tiles, new_move):

        tiles[new_move[1][0]][new_move[1][1]] = new_move[0]

        by_color = [[] for _ in range(11)]
        empty_moves = []
        for i, row in enumerate(tiles):
            for j, move in enumerate(row):
                if move != -1:
                    by_color[move].append([i, j])
                else:
                    empty_moves.append([i, j])

        by_group = [[] for _ in range(11)]
        visited = set()
        def dfs(color, move, visited):
            group = [move]
            visited.add(move)
            adj_moves = [(move[0] - 1, move[1]), (move[0] + 1, move[1]), (move[0], move[1] - 1), (move[0], move[1] + 1)]
            for adj in adj_moves:
                if adj in visited or adj[0] in [-1, self.tiles_ammount+1] or adj[1] in [-1, self.tiles_ammount+1]:
                    continue

                adj_color = tiles[adj[0]][adj[1]]
                if adj_color == color:
                    group.extend(dfs(color, adj, visited))

            return group

        for color, moves in enumerate(by_color):
            for move in moves:
                if tuple(move) not in visited:
                    group = dfs(color, tuple(move), visited)
                    by_group[color].append(group)

        empty_visited = set()
        self.empty_groups = []
        for move in empty_moves:
            if tuple(move) not in empty_visited:
                group = dfs(-1, tuple(move), empty_visited)
                self.empty_groups.append(group)

        return self.remove_enclosed_groups(tiles, by_group, current_color=new_move[0], new_move=tuple(new_move[1]))

    def count_tile_points(self):
        self.tile_points = [0 for _ in range(10)]
        for group in self.empty_groups:
            colors = []
            for move in group:
                adj_moves = [(move[0] - 1, move[1]), (move[0] + 1, move[1]), (move[0], move[1] - 1), (move[0], move[1] + 1)]
                for adj in adj_moves:
                    if -1 not in [adj[0], adj[1]] and self.tiles_ammount + 1 not in [adj[0], adj[1]]:
                        try:
                            if self.tiles[adj[0]][adj[1]] not in [*colors, -1]:
                                    colors.append(self.tiles[adj[0]][adj[1]])
                        except IndexError:
                            pass
            if len(colors) == 1:
                self.tile_points[colors[0]] += len(group)
