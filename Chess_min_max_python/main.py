import pygame
import random

# Pygame'i başlat
pygame.init()

tile_size = 80  # size of every square
board_size = tile_size * 8
screen = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption("Chess Board")

WHITE = (240, 217, 181)
BLACK = (181, 136, 99)

piece_images = {}
pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
colors = ["white", "black"]
for color in colors:
    for piece in pieces:
        image = pygame.image.load(f"images/{color}_{piece}.png")
        image = pygame.transform.scale(image, (tile_size, tile_size))
        piece_images[f"{color}_{piece}"] = image

class Piece:
    def __init__(self, name, color, row, col):
        self.name = name
        self.color = color
        self.row = row
        self.col = col
        self.image = piece_images[f"{color}_{name}"]

    def draw(self, screen):
        screen.blit(self.image, (self.col * tile_size, self.row * tile_size))
    
    def get_valid_moves(self, board):
        moves = []
        if self.name == "pawn":
            direction = -1 if self.color == "white" else 1
            if 0 <= self.row + direction < 8:
                moves.append((self.row + direction, self.col))
        elif self.name == "rook":
            for i in range(8):
                if i != self.row:
                    moves.append((i, self.col))
                if i != self.col:
                    moves.append((self.row, i))
        elif self.name == "knight":
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                            (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                new_row, new_col = self.row + dr, self.col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    moves.append((new_row, new_col))
        elif self.name == "bishop":
            for i in range(1, 8):
                for dr, dc in [(i, i), (i, -i), (-i, i), (-i, -i)]:
                    new_row, new_col = self.row + dr, self.col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        moves.append((new_row, new_col))
        elif self.name == "queen":
            for i in range(8):
                if i != self.row:
                    moves.append((i, self.col))
                if i != self.col:
                    moves.append((self.row, i))
            for i in range(1, 8):
                for dr, dc in [(i, i), (i, -i), (-i, i), (-i, -i)]:
                    new_row, new_col = self.row + dr, self.col + dc
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        moves.append((new_row, new_col))
        elif self.name == "king":
            for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                new_row, new_col = self.row + dr, self.col + dc
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    moves.append((new_row, new_col))
        return moves

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * tile_size, row * tile_size, tile_size, tile_size))

def setup_pieces():
    pieces = []
    for col in range(8):
        pieces.append(Piece("pawn", "white", 6, col))
        pieces.append(Piece("pawn", "black", 1, col))
    piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
    for col in range(8):
        pieces.append(Piece(piece_order[col], "white", 7, col))
        pieces.append(Piece(piece_order[col], "black", 0, col))
    return pieces

def evaluate_board(pieces):
    score = 0
    values = {"pawn": 1, "knight": 3, "bishop": 3, "rook": 5, "queen": 9, "king": 1000}
    for piece in pieces:
        score += values[piece.name] if piece.color == "white" else -values[piece.name]
    return score

def minmax(pieces, depth, maximizing):
    if depth == 0:
        return evaluate_board(pieces)
    
    if maximizing:
        max_eval = float('-inf')
        for piece in pieces:
            if piece.color == "white":
                for move in piece.get_valid_moves(pieces):
                    original_row, original_col = piece.row, piece.col
                    piece.row, piece.col = move
                    eval = minmax(pieces, depth-1, False)
                    piece.row, piece.col = original_row, original_col
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for piece in pieces:
            if piece.color == "black":
                for move in piece.get_valid_moves(pieces):
                    original_row, original_col = piece.row, piece.col
                    piece.row, piece.col = move
                    eval = minmax(pieces, depth-1, True)
                    piece.row, piece.col = original_row, original_col
                    min_eval = min(min_eval, eval)
        return min_eval

game_pieces = setup_pieces()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_board()
    for piece in game_pieces:
        piece.draw(screen)
    
    pygame.display.flip()

pygame.quit()
