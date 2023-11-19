import pygame
from time import *
import os

start_time = os.stat('position').st_mtime


def display_image(center, image_path):
    # load the image
    image = pygame.image.load(image_path)
    # get the size of the image
    image_rect = image.get_rect()
    # get the center of the image
    image_rect.center = (square_size/2, square_size/2)
    # get the x and y coordinates of the center of the square
    x = center[0] - 50
    y = center[1] - 50
    # create a new surface with transparent background
    square = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
    # draw the image on the square surface
    square.blit(image, image_rect)
    # blit the square surface on the screen at the correct position
    screen.blit(square, (x, y))
    # update the display
    pygame.display.flip()

def what_piece(piece):
    if int(piece) == 0: return 0
    elif int(piece) > 0:
        piece_images = {
            1: 'WhitePawn.png',
            2: 'WhiteHorse.png',
            3: 'WhiteBishop.png',
            5: 'WhiteRook.png',
            9: 'WhiteQueen.png',
            10: 'WhiteKing.png'
        }

# Assuming piece is the key for the image you want
        return piece_images.get(int(piece))
    else:
        piece_images = {
            1: 'BlackPawn.png',
            2: 'BlackHorse.png',
            3: 'BlackBishop.png',
            5: 'BlackRook.png',
            9: 'BlackQueen.png',
            10: 'BlackKing.png'
        }

# Assuming piece is the key for the image you want
        return piece_images.get(abs(int(piece)))

def load_pices(png):
    for x in range(64):
        if what_piece(png[x]) != 0:
            display_image(square_centers[x], what_piece(png[x]))
        

def reset_board():
    screen = pygame.display.set_mode((800, 800))
    screen.fill((0, 0, 0))


def load_board():
    for row in range(8):
        for col in range(8):
            # calculate the x and y coordinates of the top left corner of the square
            x = col * square_size
            y = row * square_size
            if (row + col) % 2 == 0:
                color = (200, 200, 200)
            else:
                color = (70, 70, 70)
            pygame.draw.rect(screen, color, (x, y, square_size, square_size))

def load_PNG():
    global PNG
    with open('position', 'r') as file:
        PNG = file.read().split()
        PNG.reverse()

def check_update():
    global start_time
    global last_time
    last_time = os.stat('position').st_mtime
    if last_time != start_time:
        start_time = last_time
        return True
    else: return False


# initialize pygame
pygame.init()

# set the size of the window
size = (800, 800)
screen = pygame.display.set_mode(size)

# set the title of the window
pygame.display.set_caption("Chess Board")

# set the background color
screen.fill((255, 255, 255))

# set the size of each square
square_size = 100

#adding a position of a game


# create a 2D list to store the coordinates of the center of each square
square_centers = [[50, 50], [150, 50], [250, 50], [350, 50], [450, 50], [550, 50], [650, 50], [750, 50], [50, 150], [150, 150], [250, 150], [350, 150], [450, 150], [550, 150], [650, 150], [750, 150], [50, 250], [150, 250], [250, 250], [350, 250], [450, 250], [550, 250], [650, 250], [750, 250], [50, 350], [150, 350], [250, 350], [350, 350], [450, 350], [550, 350], [650, 350], [750, 350], [50, 450], [150, 450], [250, 450], [350, 450], [450, 450], [550, 450], [650, 450], [750, 450], [50, 550], [150, 550], [250, 550], [350, 550], [450, 550], [550, 550], [650, 550], [750, 550], [50, 650], [150, 650], [250, 650], [350, 650], [450, 650], [550, 650], [650, 650], [750, 650], [50, 750], [150, 750], [250, 750], [350, 750], [450, 750], [550, 750], [650, 750], [750, 750]]

# draw the chess board

        # calculate the x and y coordinates of the center of the square









load_PNG()
load_board()
load_pices(PNG)

while True:
    if check_update():
        reset_board()
        load_PNG()
        load_board()
        load_pices(PNG)
        pygame.display.flip()
    else: sleep(0.1)










# run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



# close pygame
pygame.quit()
