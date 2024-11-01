from collections import deque
from queue import PriorityQueue

def is_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def get_moves(board):
    moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                moves.append((row, col))
    return moves

def apply_move(board, move, player):
    new_board = [row[:] for row in board]
    new_board[move[0]][move[1]] = player
    return new_board

def dfs(board):
    stack = [(board, [])] # Stack for DFS
    while stack:
        current_board, moves = stack.pop()

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "O")
            if is_win(new_board, "O"):
                return moves + [move]

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "X")
            if is_win(new_board, "X"):
                return moves + [move]

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "O")
            stack.append((new_board, moves + [move]))
    
    return None # Placeholder return to ensure returning at all possible paths of the function

def bfs(board):
    queue = deque([(board, [])])
    while queue:
        current_board, moves = queue.popleft() # Queue for BFS

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "O")
            if is_win(new_board, "O"):
                return moves + [move]

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "X")
            if is_win(new_board, "X"):
                return moves + [move]

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "O")
            queue.append((new_board, moves + [move]))
    
    return None

def depth_limited_search(board, depth): # For Iterative deepening
    stack = [(board, [], 0)]
    while stack:
        current_board, moves, current_depth = stack.pop()

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "O")
            if is_win(new_board, "O"):
                return moves + [move]

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "X")
            if is_win(new_board, "X"):
                return moves + [move]

        if current_depth < depth:
            for move in get_moves(current_board):
                new_board = apply_move(current_board, move, "O")
                stack.append((new_board, moves + [move], current_depth + 1))
    
    return None

def ids(board, max_depth=10):
    for depth in range(1, max_depth + 1):
        result = depth_limited_search(board, depth)
        if result is not None:
            return result
    return None

def ucs(board):
    pq = PriorityQueue() # Priority Queue for UCS
    pq.put((0, board, []))
    while not pq.empty():
        cost, current_board, moves = pq.get()

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "O")
            if is_win(new_board, "O"):
                return moves + [move]

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "X")
            if is_win(new_board, "X"):
                return moves + [move]

        for move in get_moves(current_board):
            new_board = apply_move(current_board, move, "O")
            pq.put((cost + 1, new_board, moves + [move])) # Cost increases by 1 for each additional move.
    
    return None
