def check_winner(board):
    # Check horizontal locations for a win
    for row in range(len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row][col + 1] == board[row][col + 2] == board[row][col + 3] != 0:
                return board[row][col]

    # Check vertical locations for a win
    for row in range(len(board) - 3):
        for col in range(len(board[row])):
            if board[row][col] == board[row + 1][col] == board[row + 2][col] == board[row + 3][col] != 0:
                return board[row][col]

    # Check positively sloped diagonals
    for row in range(len(board) - 3):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row + 1][col + 1] == board[row + 2][col + 2] == board[row + 3][col + 3] != 0:
                return board[row][col]

    # Check negatively sloped diagonals
    for row in range(3, len(board)):
        for col in range(len(board[row]) - 3):
            if board[row][col] == board[row - 1][col + 1] == board[row - 2][col + 2] == board[row - 3][col + 3] != 0:
                return board[row][col]

    return None
