from typing import List, Tuple


class Board:
    def __init__(self, grid):
        self.grid = grid
        print(grid, "GRID")

        size = 19 # to fix
        self.size = size
        self.captures = {1: 0, 2: 0}
        self.ko_position = None
        self.current_player = 1
        self.move_history = []

    # def is_move_legal(self, x: int, y: int, color: str) -> bool:
    #     if x < 0 or x >= self.size or y < 0 or y >= self.size:
    #         return False
    #     if self.grid[x][y] is not None:
    #         return False
    #     if color != self.current_player:
    #         return False
    #     return True

    def make_move(self, x: int, y: int, color: int) -> bool:
        # if not self.is_move_legal(x, y, color):
        #     return False

        self.grid[x][y] = color # error
        self.current_player = 1 if self.current_player == 2 else 2
        self.move_history.append((x, y, color))
        return True

#
# b = Board()
#
# print(b.make_move(x=3, y=3, color="B"))
# print(b.grid[3][3])
# print(b.current_player)
#
# print("=========")
#
# print(b.make_move(x=4, y=4, color="W"))
# print(b.grid[4][4])
# print(b.current_player)
