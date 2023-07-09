import pygame
import numpy as np
import colorsys

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)

# Set the width and height of the grid cells
CELL_SIZE = 8

# Set the number of rows and columns in the grid
ROWS = 100
COLS = 160

# Set the width and height of the game window
WINDOW_SIZE = (COLS * CELL_SIZE, ROWS * CELL_SIZE)

# Create the game window
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Conway's Game of Life")

# Create the initial grid
grid = np.zeros((ROWS, COLS), dtype=int)
initial_pattern = False

# Variable to show instructions
show_instructions = True

# Function to clear the grid
def clear_grid():
    global grid
    grid = np.zeros((ROWS, COLS), dtype=int)

# Function to display the instructions dialog box
def show_instructions_dialog():
    dialog_width = 400
    dialog_height = 300
    dialog_x = (WINDOW_SIZE[0] - dialog_width) // 2
    dialog_y = (WINDOW_SIZE[1] - dialog_height) // 2




    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if dialog_x <= event.pos[0] <= dialog_x + dialog_width and dialog_y <= event.pos[1] <= dialog_y + dialog_height:
                    return

        pygame.draw.rect(window, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(window, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        # Create font objects
        font_large = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

        # Display instructions
        text_title = font_large.render("Game of Life - Click Here to Start", True, BLACK)
        text_instructions1 = font_small.render("Press R to create a random initial pattern:", True, BLACK)
        text_instructions2 = font_small.render("- Left-click to create live cells", True, BLACK)
        text_instructions3 = font_small.render("- Right-click to create dead cells", True, BLACK)
        text_instructions4 = font_small.render("- Press Enter to start the simulation", True, BLACK)
        text_instructions5 = font_small.render("- Press Space to clear the grid and restart", True, BLACK)

        # Calculate the positions of the text
        title_position = text_title.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 50))
        instructions1_position = text_instructions1.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 100))
        instructions2_position = text_instructions2.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 140))
        instructions3_position = text_instructions3.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 180))
        instructions4_position = text_instructions4.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 220))
        instructions5_position = text_instructions5.get_rect(center=(dialog_x + dialog_width // 2, dialog_y + 260))

        # Draw the text on the screen
        window.blit(text_title, title_position)
        window.blit(text_instructions1, instructions1_position)
        window.blit(text_instructions2, instructions2_position)
        window.blit(text_instructions3, instructions3_position)
        window.blit(text_instructions4, instructions4_position)
        window.blit(text_instructions5, instructions5_position)

        pygame.display.flip()

# Function to hide the initial screen
def hide_initial_screen():
    window.fill(BLACK)

# Function to update the display
def update_display():
    pygame.display.flip()

def generate_random_pattern():
    global grid
    random_pattern = np.random.choice([0, 1], size=(ROWS, COLS), p=[0.9, 0.1])
    grid = random_pattern.astype(int)



# Game loop
running = True
initial_screen = True

while running:
    if initial_screen and show_instructions:
        show_instructions_dialog()
        hide_initial_screen()
        initial_screen = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and not initial_pattern:
            mouse_button_pressed = True  # Mouse button pressed

            # Get the mouse position
            pos = pygame.mouse.get_pos()

            # Calculate the cell position in the grid
            row = pos[1] // CELL_SIZE
            col = pos[0] // CELL_SIZE

            # Toggle the cell state based on the mouse button
            if event.button == 1:  # Left mouse button
                grid[row, col] = 1
            elif event.button == 3:  # Right mouse button
                grid[row, col] = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_button_pressed = False  # Mouse button released

        elif event.type == pygame.MOUSEMOTION and mouse_button_pressed and not initial_pattern:
            # Get the mouse position
            pos = pygame.mouse.get_pos()

            # Calculate the cell position in the grid
            row = pos[1] // CELL_SIZE
            col = pos[0] // CELL_SIZE

            # Toggle the cell state based on the mouse button
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                grid[row, col] = 1
            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                grid[row, col] = 0

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Start the simulation
                initial_pattern = True
                show_instructions = False
                hide_initial_screen()
            elif event.key == pygame.K_SPACE:
                # Clear the grid and restart
                initial_pattern = False
                show_instructions = True
                clear_grid()

                update_display()
            elif event.key == pygame.K_r:
                # Generate a random pattern
                if not initial_pattern:
                    generate_random_pattern()
                    update_display()

    if initial_pattern:
        # Create a copy of the grid to store the next generation
        new_grid = np.copy(grid)

        # Update each cell in the grid
        for i in range(ROWS):
            for j in range(COLS):
                # Get the indices of the neighboring cells
                neighbors = [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1),
                             (i, j - 1), (i, j + 1),
                             (i + 1, j - 1), (i + 1, j), (i + 1, j + 1)]

                # Count the number of live neighbors
                live_neighbors = 0
                for neighbor in neighbors:
                    if neighbor[0] in range(ROWS) and neighbor[1] in range(COLS):
                        if grid[neighbor[0], neighbor[1]] == 1:
                            live_neighbors += 1

                # Apply the rules of Conway's Game of LifeIt seems that there is an indentation error in the code I provided. Please make sure that the code inside the `if initial_pattern:` block is properly indented. Here's the corrected code:


                # Apply the rules of Conway's Game of Life
                if grid[i, j] == 1 and (live_neighbors < 2 or live_neighbors > 3):
                    new_grid[i, j] = 0
                elif grid[i, j] == 0 and live_neighbors == 3:
                    new_grid[i, j] = 1

        # Update the grid with the new generation
        grid = np.copy(new_grid)

    # Clear the game window
    window.fill(BLACK)

    # Draw the cells
    for i in range(ROWS):
        for j in range(COLS):
            if grid[i, j] == 1:
                # Calculate the cell position in the game window
                x = j * CELL_SIZE
                y = i * CELL_SIZE

                # Calculate the angle of the cell with respect to the center of the game canvas
                center_x = WINDOW_SIZE[0] // 2
                center_y = WINDOW_SIZE[1] // 2
                dx = x - center_x
                dy = y - center_y
                angle = np.arctan2(dy, dx)

                # Map the angle to a hue value in the range [0, 360]
                hue = (np.degrees(angle) + 180) % 360

                # Set the saturation and lightness values
                saturation = 100
                lightness = 50

                # Convert the HSL color values to RGB
                rgb = colorsys.hls_to_rgb(hue / 360, lightness / 100, saturation / 100)
                color = tuple(int(component * 255) for component in rgb)

                # Draw the cell with the calculated color
                pygame.draw.rect(window, color, (x, y, CELL_SIZE, CELL_SIZE))

    # Update the display
    update_display()

# Quit the game
pygame.quit()
