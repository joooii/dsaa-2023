"""
def get_maze_answer(maze : dict) -> list:
    미로에 대한 정보를 dict 타입으로 입력 받아서 해당 미로의 답을 반환한다.
    Args:
        maze (dict) : 미로에 대한 정보를 포함하고 있으며, 해당 정보는 위치 정보와 이동 가능한 방향에 대한 정보를 포함한다.
    Example:
        maze = {(1, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1},
                (2, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0},
                (3, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0},
                (1, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 0},
                (2, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1},
                (3, 2): {'E': 1, 'W': 1, 'N': 1, 'S': 0},
                (1, 3): {'E': 0, 'W': 1, 'N': 0, 'S': 1},
                (2, 3): {'E': 0, 'W': 0, 'N': 1, 'S': 1},
                (3, 3): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
    Returns:
        maze_solution (list) : `maze` 데이터를 바탕으로 최적의 이동 솔루션을 list 타입으로 출력한다.
                                list의 값은 공간 위치에 대한 정보를 포함한다.
    Example:
        >>> solution = get_maze_answer(maze)
        >>> solution
            [(3, 3), (3, 2), (2, 2), (2, 1), (1, 1)]

    
    return None
        """

class Stack():
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def peek(self):
        return self.items[-1] if self.items else None
        
    def is_empty(self):
        return len(self.items) == 0
    
    def top(self):
        if(self.is_empty()):
            return -1
        else:
            return self.items[-1]


maze = {(1, 1): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 1): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (3, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1}, (4, 1): {'E': 0, 'W': 0, 'N': 1, 'S': 1},
        (5, 1): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (1, 2): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0}, (3, 2): {'E': 1, 'W': 0, 'N': 0, 'S': 1}, (4, 2): {'E': 1, 'W': 0, 'N': 1, 'S': 0},
        (5, 2): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 3): {'E': 1, 'W': 0, 'N': 0, 'S': 0}, (2, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0},
        (3, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (5, 3): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (1, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0},
        (2, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (3, 4): {'E': 1, 'W': 1, 'N': 0, 'S': 0}, (4, 4): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (5, 4): {'E': 1, 'W': 1, 'N': 1, 'S': 0}, (1, 5): {'E': 0, 'W': 1, 'N': 0, 'S': 1}, (2, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 1}, (3, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0},
        (4, 5): {'E': 0, 'W': 0, 'N': 0, 'S': 1}, (5, 5): {'E': 0, 'W': 1, 'N': 1, 'S': 0}}
n = len(maze)


def find_maze_dimensions(maze):
    max_row = max(col_row[0] for col_row in maze.keys())
    max_col = max(col_row[1] for col_row in maze.keys())
    return max_row, max_col


def get_maze_answer(maze : dict) -> list:
    directions = {'E': (0, 1), 'W': (0, -1), 'N': (-1, 0), 'S': (1, 0)}

    n, m = find_maze_dimensions(maze)
    start = (n, m)
    target = (1, 1)

    path = Stack()
    path.push(start)
    visited = set()

    while not path.is_empty():
        current = path.top()
        visited.add(current)

        if current == target:
            return list(path.items)

        for direction, (dx, dy) in directions.items():
            if maze[current][direction]:
                next_cell = (current[0] + dx, current[1] + dy)
                if next_cell not in visited:
                    path.push(next_cell)
                    break
        else:
            path.pop()

    return []

solution = get_maze_answer(maze)
print(solution)