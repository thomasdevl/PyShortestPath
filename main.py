import pygame
import sys
from bfs import bfs

def create_grid(rows, columns, tile_size, gap_size, x, y):
    grid = []
    for row in range(rows):
        grid.append([])
        for column in range(columns):
            if column == 0 and row == 0:
                grid[row].append((x + column * (tile_size + gap_size), y + row * (tile_size + gap_size), 4))
            else:
                grid[row].append((x + column * (tile_size + gap_size), y + row * (tile_size + gap_size), 0))
    return grid

def clear_grid(grid):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            x, y, value = grid[row][column]
            if column == 0 and row == 0:
                continue
            grid[row][column] = (x, y, 0)
    return grid


def handle_events(grid, tile_size, gap_size, screen):
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in range(len(grid)):
                for column in range(len(grid[0])):
                    x, y, value = grid[row][column]
                    if x <= pos[0] <= x + tile_size and y <= pos[1] <= y + tile_size:
                        if column == 0 and row == 0:
                            continue
                        elif event.button == 1:
                            grid[row][column] = (x, y, 1)
                        elif event.button == 3:
                            grid[row][column] = (x, y, 2)
                        draw_grid(grid, tile_size, gap_size, screen)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                for row in range(len(grid)):
                    for column in range(len(grid[0])):
                        x, y, value = grid[row][column]
                        if column == 0 and row == 0:
                            continue
                        elif x <= pos[0] <= x + tile_size and y <= pos[1] <= y + tile_size:
                            grid[row][column] = (x, y, 3)
                            draw_grid(grid, tile_size, gap_size, screen)
    return True


def draw_grid(grid, tile_size, gap_size, screen):
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            x, y, value = grid[row][column]
            color = (255, 255, 255)
            if value == 1: # left click blue
                color = (0, 0, 255)
            elif value == 2: # right click white
                color = (255, 255, 255)
            elif value == 3: # end red
                color = (255, 0, 0)
            elif value == 4: # start purple can't be moved 
                color = (196, 48, 226)
            elif value == 5: # path green
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, [x, y, tile_size, tile_size])




def breath_first_search(grid):
    pygame.time.wait(100)
    
    value_map = {1: "#", 2: " ", 0: " ", 3: "X", 4: "O", 5: " "}
    print("-----")
    test = []
    for row in grid:
        # print([value_map[val] for _, _, val in row])
        test.append([value_map[val] for _, _, val in row])

    # remove all the Green
    for row in range(len(grid)):
        for column in range(len(grid[0])):
            x, y, value = grid[row][column]
            if value == 5:
                grid[row][column] = (x, y, 0)

    # W = " "
    # B = "#"
    # P = "O"
    # R = "X"
    for row in test:
        print(row)

    # solves the maze and returns an array with the path
    # check bfs.py for more details
    result = bfs(test)

    for row in result:
        print(row)

    for row in range(len(grid)):
        for column in range(len(grid[0])):
            x, y, value = grid[row][column]
            if result[row][column] == "+":
                grid[row][column] = (x, y, 5)

    return grid




def create_button(text, x, y, width, height, inactive_color, active_color, screen, grid):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            if text == "CLEAR":
                clear_grid(grid)
            elif text == "BFS":
                breath_first_search(grid)
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    font = pygame.font.Font(None, 20)
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x + (width/2 - text.get_width()/2), y + (height/2 - text.get_height()/2)))



def main():
    # Initialize pygame and create a window
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Python Pathfinding")

    # Create a grid
    grid = create_grid(5, 5, 100, 5, 50, 70)

    
    # Create a loop to handle events
    running = True
    event_occurred = False
    while running:

        event_occurred = handle_events(grid, 100, 5, screen)
        if not event_occurred:
            running = False

        if event_occurred:
            # Clear the screen
            screen.fill((0, 0, 0))

            # Draw the grid
            draw_grid(grid, 100, 5, screen)

            #create buttons
            create_button("CLEAR", 50, 10, 100, 50, (255, 0, 0), (128, 21, 43), screen, grid)
            create_button("BFS", 160, 10, 100, 50, (0, 0, 255), (15, 27, 131), screen, grid)

            # Update the display
            pygame.display.flip()
            event_occurred = False
            

    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
