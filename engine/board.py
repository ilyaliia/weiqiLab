 
class Board:
    def __init__(self, grid):
        if grid is None:
            # grid = [[0] * 19 for _ in range(19)]
            grid = [[0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 2, 1, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

    def on_board(self, x: int, y: int) -> bool:
        return 0 <= x < self.size and 0 <= y < self.size
    
    def count_liberties(self, group: set, grid=None) -> int:
            if grid is None:
                grid = self.grid

            liberties = set()
            
            for gx, gy in group:
                for nx, ny in [(gx-1, gy), (gx+1, gy), (gx, gy-1), (gx, gy+1)]:
                    if self.on_board(nx, ny) and grid[ny][nx] == 0:
                        liberties.add((nx, ny))
            
            return len(liberties)
    
    def find_group(self, x: int, y: int, player_number: int, grid=None) -> bool:
            
            if grid is None:
                grid = self.grid

            group = set()           
            stack = [(x, y)]      
            
            while stack:
                cx, cy = stack.pop()
                if (cx, cy) in group:
                    continue         

                if not self.on_board(cx, cy):
                    continue
                
                if grid[cy][cx] != player_number:
                    continue
                
                group.add((cx, cy))
                
                # Добавляем всех 4 соседей в стек для проверки
                stack.extend([
                    (cx-1, cy),  # левый сосед
                    (cx+1, cy),  # правый сосед
                    (cx, cy-1),  # верхний сосед
                    (cx, cy+1)   # нижний сосед
                ]) 
            print("Group found:", group)
            return group
        
    def is_move_legal(self, x: int, y: int, player_number: int) -> bool:


        def is_enemy_stone(px: int, py: int, pn: int) -> bool:
            if not self.on_board(px, py):
                return False
            return self.grid[py][px] != 0 and self.grid[py][px] != pn
        
        def enemy(pn: int) -> int:
            return 1 if pn == 2 else 2

        
        
            
            

        if not self.on_board(x, y):
            return False
        if self.grid[y][x] != 0:
            return False
        if player_number != self.current_player:
            return False

        checked_points = set()
        can_capture_enemy = False

        for dx, dy in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if is_enemy_stone(dx, dy, player_number):
                print("Enemy stone beside")
                
                #Получить группу камней со стороны, где стоит вражеский камень
                enemy_group = frozenset(self.find_group(dx, dy, enemy(player_number)))

                #Получиьть группу камней от игрока, который делает ход, для проверки на суицид
                # player_group = frozenset(find_group(x, y, player_number))

                if enemy_group in checked_points:
                    continue
                
                checked_points.add(enemy_group)

                print(self.count_liberties(enemy_group), "Liberties of enemy group")
                
                if self.count_liberties(enemy_group) == 0:
                    can_capture_enemy = True  

        temp_grid = [row[:] for row in self.grid]
        temp_grid[y][x] = player_number

        for dx, dy in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if self.on_board(dx, dy) and temp_grid[dy][dx] == enemy(player_number):
                enemy_group = self.find_group(dx, dy, enemy(player_number))
                if self.count_liberties(enemy_group) == 1:
                    for gx, gy in enemy_group:
                        temp_grid[gy][gx] = 0

        original_grid = self.grid
        self.grid = temp_grid
        
        my_group = self.find_group(x, y, player_number)
        my_liberties = self.count_liberties(my_group)
        
        self.grid = original_grid

        if my_liberties > 0:
            print(f"Move is legal - has {my_liberties} liberties")
            return True
        
        if can_capture_enemy:
            print("Move is legal - captures enemy")
            return True
        
        print("Suicide move - no liberties and no captures")
        return False
           
                
    def make_move(self, x: int, y: int, player_number: int):
        if not self.is_move_legal(x, y, player_number):
            return False

        new_grid = [row[:] for row in self.grid]
        new_grid[y][x] = player_number

        captured = []
        enemy_color = 1 if player_number == 2 else 2
        checked_groups = set()
        
        # Проверяем соседние группы врага
        for dx, dy in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if self.on_board(dx, dy) and new_grid[dy][dx] == enemy_color:
                enemy_group = frozenset(self.find_group(dx, dy, enemy_color, new_grid))
                
                if enemy_group in checked_groups:
                    continue
                
                checked_groups.add(enemy_group)
                
                # Если группа захвачена - снимаем
                if self.count_liberties(set(enemy_group), new_grid) == 0:
                    for gx, gy in enemy_group:
                        new_grid[gy][gx] = 0
                        captured.append((gx, gy))
        
        # Обновляем состояние
        self.grid = new_grid
        self.current_player = 1 if player_number == 2 else 2
        self.captures[player_number] += len(captured)
        for line in new_grid:
            print(line)
        return new_grid, captured

    

b = Board(None)
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
