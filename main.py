import pygame
import sys
import heapq

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
    grid[0][0] = (grid[0][0][0], grid[0][0][1], 4)
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
            elif value == 6: # searching yellow
                color = (255, 255, 0)
            elif value == 7: # checked gray
                color = (128, 128, 128)
            pygame.draw.rect(screen, color, [x, y, tile_size, tile_size])



def breath_first_search(grid, tile_size, gap_size, screen):
    start_x, start_y = 0, 0 # find the start position 
    queue = [(start_x, start_y, None)]
    visited = set()
    path = []
    goal_reached = False
    while queue:
        x, y, parent = queue.pop(0)
        if (x,y) in visited:
            continue
        visited.add((x,y))
        
        if grid[x][y][2] == 3:
            goal_reached = True
            path.append((x,y))
            break

        grid[x][y] = (grid[x][y][0], grid[x][y][1], 6)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()
        pygame.time.wait(100)

        #add the neighbors to the queue
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if 0 <= x+dx < len(grid) and 0 <= y+dy < len(grid[0]):
                if grid[x+dx][y+dy][2] != 1:
                    queue.append((x+dx,y+dy,(x,y)))
        grid[x][y] = (grid[x][y][0], grid[x][y][1], 7)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()

    if goal_reached:
        for pos in path:
            x, y = pos
            grid[x][y] = (grid[x][y][0], grid[x][y][1], 5)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()
    return goal_reached


def depth_first_search(grid, tile_size, gap_size, screen):
    start_x, start_y = 0, 0 # find the start position
    stack = [(start_x, start_y, None)]
    visited = set()
    path = []
    goal_reached = False
    while stack:
        x, y, parent = stack.pop()
        if (x,y) in visited:
            continue
        visited.add((x,y))

        if grid[x][y][2] == 3:
            goal_reached = True
            path.append((x,y))
            break

        grid[x][y] = (grid[x][y][0], grid[x][y][1], 6)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()
        pygame.time.wait(100)

        #add the neighbors to the stack
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if 0 <= x+dx < len(grid) and 0 <= y+dy < len(grid[0]):
                if grid[x+dx][y+dy][2] != 1:
                    stack.append((x+dx,y+dy,(x,y)))
        grid[x][y] = (grid[x][y][0], grid[x][y][1], 7)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()

    if goal_reached:
        for pos in path:
            x, y = pos
            grid[x][y] = (grid[x][y][0], grid[x][y][1], 5)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()
    return goal_reached



def heuristic(a, b):
    # Manhattan distance as the heuristic function
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(grid, tile_size, gap_size, screen):
    start_x, start_y = 0, 0 # find the start position
    goal_x, goal_y = len(grid) - 1, len(grid[0]) - 1 # find the goal position
    heap = [(0, (start_x, start_y))]
    visited = set()
    parent = {}
    g_score = {(start_x, start_y): 0}
    f_score = {(start_x, start_y): heuristic((start_x, start_y), (goal_x, goal_y))}
    path = []
    goal_reached = False
    while heap:
        current = heapq.heappop(heap)[1]
        if current in visited:
            continue
        visited.add(current)
        x, y = current

        if current == (goal_x, goal_y):
            goal_reached = True
            break

        grid[x][y] = (grid[x][y][0], grid[x][y][1], 6)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()
        pygame.time.wait(100)

        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if 0 <= x+dx < len(grid) and 0 <= y+dy < len(grid[0]):
                if grid[x+dx][y+dy][2] != 1:
                    neighbor = (x+dx, y+dy)
                    if neighbor in visited:
                        continue
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        parent[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, (goal_x, goal_y))
                        heapq.heappush(heap, (f_score[neighbor], neighbor))
        grid[x][y] = (grid[x][y][0], grid[x][y][1], 7)
        draw_grid(grid, tile_size, gap_size, screen)
        pygame.display.update()

    if goal_reached:
        current = (goal_x, goal_y)
        while current != (start_x, start_y):
            path.append(current)
            current = parent[current]
        path.append((start_x, start_y))
        for pos in path[::-1]:
            x, y = pos
            grid[x][y] = (grid[x][y][0], grid[x][y][1], 5)
        draw_grid(grid,tile_size, gap_size, screen)
        pygame.display.update()
    return goal_reached




def create_button(text, x, y, width, height, inactive_color, active_color, screen, grid, tile_size, gap_size):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            if text == "CLEAR":
                clear_grid(grid)
            elif text == "BFS":
                breath_first_search(grid, tile_size, gap_size, screen )
            elif text == "DFS":
                depth_first_search(grid, tile_size, gap_size, screen )
            elif text == "A*":
                a_star(grid, tile_size, gap_size, screen )
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    font = pygame.font.Font(None, 20)
    text = font.render(text, True, (255, 255, 255))
    screen.blit(text, (x + (width/2 - text.get_width()/2), y + (height/2 - text.get_height()/2)))



def main():
    # Initialize pygame and create a window
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Python Pathfinding")
    clock = pygame.time.Clock()
    
    # Create a grid
    grid = create_grid(6, 8, 100, 5, 50, 70)

    
    # Create a loop to handle events
    running = True
    event_occurred = False
    while running:

        clock.tick(30)
        event_occurred = handle_events(grid, 100, 5, screen)
        if not event_occurred:
            running = False

        if event_occurred:
            # Clear the screen
            screen.fill((0, 0, 0))

            # Draw the grid
            draw_grid(grid, 100, 5, screen)

            #create buttons
            create_button("CLEAR", 50, 10, 100, 50, (255, 0, 0), (128, 21, 43), screen, grid, 100, 5)
            create_button("BFS", 160, 10, 100, 50, (0, 0, 255), (15, 27, 131), screen, grid, 100, 5)
            create_button("DFS", 270, 10, 100, 50, (0, 0, 255), (15, 27, 131), screen, grid, 100, 5)
            create_button("A*", 380, 10, 100, 50, (0, 0, 255), (15, 27, 131), screen, grid, 100, 5)

            # Update the display
            pygame.display.flip()
            event_occurred = False
            

    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
