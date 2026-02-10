 
class Board:
    def __init__(self, grid):
        if grid is None:
            # grid = [[0] * 19 for _ in range(19)]
            grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.grid = grid
        # print(, "GRID")

        size = 19  # to fix
        self.size = size
        self.captures = {1: 0, 2: 0}
        self.ko_position = None
        self.current_player = 2
        self.move_history = []
    
    def is_enemy_stone(self, x: int, y: int, player_number: int) -> bool:
        return self.grid[y][x] != 0 and self.grid[y][x] != player_number
    
    def is_move_legal(self, x: int, y: int, player_number: int) -> bool:
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return False
        if self.grid[y][x] != 0:
            return False
        if player_number != self.current_player:
            return False
        # return True

        cursor_x = x
        cursor_y = y

        #Проверка сверху
        print(self.grid[cursor_y][cursor_x-1])
        if self.is_enemy_stone(cursor_x-1, cursor_y, player_number):
            print("gg")
        return True
           
                
    def make_move(self, x: int, y: int, player_number: int):
        if not self.is_move_legal(x, y, player_number):
            return False

        new_grid = [row[:] for row in self.grid]
        new_grid[y][x] = player_number

        captured = []

        #Смена игрока после хода
        self.current_player = 1 if self.current_player == 2 else 2
        self.move_history.append((x, y, player_number))
        for line in new_grid:
            print(line)
        return new_grid, captured

    

b = Board(None)

# b.is_move_legal(3,2,2)

b.make_move(2,1,2)
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
