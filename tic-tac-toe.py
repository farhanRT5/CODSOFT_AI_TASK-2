import numpy as np
import math
import random

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_moves())

    def is_terminal(self):
        return self.state.is_terminal()

    def get_best_child(self, exploration_weight=1.41):
        children_with_scores = [
            (child, child.wins / (child.visits + 1e-6) +
             exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6)))
            for child in self.children
        ]
        return max(children_with_scores, key=lambda x: x[1])[0]

    def add_child(self, child_state):
        child_node = Node(child_state, parent=self)
        self.children.append(child_node)
        return child_node

class TicTacToe:
    def __init__(self):
        self.board = np.array([' ' for _ in range(9)]).reshape(3, 3)
        self.current_player = 'X'

    def get_legal_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']

    def is_terminal(self):
        return self.get_winner() is not None or ' ' not in self.board

    def get_winner(self):
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
        for line in lines:
            symbols = self.board.flatten()[list(line)]
            if symbols[0] == symbols[1] == symbols[2] != ' ':
                return symbols[0]
        return None

    def make_move(self, move):
        self.board[move] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def perform_random_move(self):
        legal_moves = self.get_legal_moves()
        if not legal_moves:
            return None
        return random.choice(legal_moves)

def print_board(board):
    print("  0 | 1 | 2 ")
    print(" ---+---+---")
    print("  3 | 4 | 5 ")
    print(" ---+---+---")
    print("  6 | 7 | 8 ")
    print()
    print("Current board:")
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print(" ---+---+---")

def monte_carlo_tree_search(initial_state, iterations=1000):
    root = Node(initial_state)

    for _ in range(iterations):
        node = root
        while not node.is_terminal():
            if not node.is_fully_expanded():
                child_state = node.state.perform_random_move()
                node = node.add_child(child_state)
            else:
                node = node.get_best_child()

        # Simulate a random game from this node
        winner = node.state.get_winner()
        if winner == 'X':
            result = 1
        elif winner == 'O':
            result = -1
        else:
            result = 0

        # Backpropagate the result
        while node is not None:
            node.visits += 1
            node.wins += result if node.state.current_player == 'X' else -result
            node = node.parent

    return root.get_best_child(exploration_weight=0).state

if __name__ == "__main__":
    game = TicTacToe()

    while not game.is_terminal():
        if game.current_player == 'X':
            print_board(game.board)
            move_number = int(input("Enter your move (0-8): "))
            if move_number not in range(9):
                print("Invalid move. Try again.")
                continue
            move = divmod(move_number, 3)  # Convert move number to (row, col)
            if move not in game.get_legal_moves():
                print("Cell already taken. Try again.")
                continue
        else:
            print("Current board:")
            print_board(game.board)
            move = game.perform_random_move()
            print("AI's move (O):", move)

        game.make_move(move)

    print("Final board:")
    print_board(game.board)

    winner = game.get_winner()
    if winner == 'X':
        print("You win!")
    elif winner == 'O':
        print("AI wins!")
    else:
        print("It's a draw!")
