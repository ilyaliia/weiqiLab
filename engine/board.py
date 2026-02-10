 
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
        self.current_player = 1
        self.move_history = []
    
    def enemy_color(self, color):
        if color == 1:
            return 2
        elif color == 2:
            return 1

    def is_move_legal(self, x: int, y: int, color: int) -> bool:
        # if x < 0 or x >= self.size or y < 0 or y >= self.size:
        #     return False
        # if self.grid[y][x] != 0:
        #     return False
        # if color != self.current_player:
        #     return False
        # # return True

        cursor_x = x
        cursor_y = y

        #Проверка сверху
        print(self.grid[cursor_y][cursor_x-1])
        if self.grid[cursor_y][cursor_x-1] == enemy_color(color):
            print("gg")
        
        for i in self.checked_stones:
            print(i)


    # def check_move(self, x: int, y: int, color: int):
    #     checked_stones = [[0] * 19 for _ in range(19)]
        
    #     cursor_x = 0
    #     cursor_y = 0
        
    #     for line in self.grid:
    #         for point in line:
    #             if self.grid[cursor_x+1][cursor_y] == enemy_color(color):
    #                 checked_stones[cursor_x][cursor_y] = 1
    #             cursor_x += 1
    #         cursor_y += 1

        
                

        

    def make_move(self, x: int, y: int, color: int):
        if not self.is_move_legal(x, y, color):
            return False

        new_grid = [row[:] for row in self.grid]
        new_grid[y][x] = color

        captured = []

        self.current_player = 1 if self.current_player == 2 else 2
        self.move_history.append((x, y, color))
        return new_grid, captured

    

b = Board(None)

b.is_move_legal(3,2,2)
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
