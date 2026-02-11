from sgfmill import sgf, sgf_moves


def sgf_to_grid(path: str):
    with open(path, "rb") as f:
        game = sgf.Sgf_game.from_bytes(f.read())

    # board and moves
    board_obj, moves = sgf_moves.get_setup_and_moves(game)

    # board_obj.board - list of lists. (None/'b'/'w')
    board_list = board_obj.board
    grid = [[0] * 19 for _ in range(19)]

    for y in range(19):
        for x in range(19):
            cell = board_list[y][x]
            if cell == 'b':
                grid[y][x] = 1
            elif cell == 'w':
                grid[y][x] = 2

    return grid


# print(sgf_to_grid("../uploads/sgf/01000.sgf"))
