import pygame

# Pygame'i başlat
pygame.init()

# Ekran boyutları
tile_size = 80  # Her bir karenin boyutu
board_size = tile_size * 8
screen = pygame.display.set_mode((board_size, board_size))
pygame.display.set_caption("Chess Board")

# Renkler
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)

def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (col * tile_size, row * tile_size, tile_size, tile_size))

# Oyun döngüsü
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_board()
    pygame.display.flip()

pygame.quit()