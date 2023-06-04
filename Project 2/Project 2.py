import pygame
import pygame_gui
class GameState:
    def __init__(self):
        # Initialize the game state
        pass
    
    # Add methods as needed to manipulate and evaluate the game state



class Heuristic:
    def evaluate(self, state):
        raise NotImplementedError

class DefensiveHeuristic1(Heuristic):
    def evaluate(self, state):
        # Implement the evaluation for Defensive Heuristic 1
        pass

class OffensiveHeuristic1(Heuristic):
    def evaluate(self, state):
        # Implement the evaluation for Offensive Heuristic 1
        pass

class DefensiveHeuristic2(Heuristic):
    def evaluate(self, state):
        # Implement the evaluation for Defensive Heuristic 2
        pass

class OffensiveHeuristic2(Heuristic):
    def evaluate(self, state):
        # Implement the evaluation for Offensive Heuristic 2
        pass

class AIPlayer:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def choose_move(self, state):
        _, move = self.max_value(state)
        return move

    def max_value(self, state):
        if self.is_terminal(state):
            return self.utility(state), None
        v = -float('inf')
        best_move = None
        for a in self.actions(state):
            v2, _ = self.min_value(self.result(state, a))
            if v2 > v:
                v, best_move = v2, a
        return v, best_move

    def min_value(self, state):
        if self.is_terminal(state):
            return self.utility(state), None
        v = float('inf')
        best_move = None
        for a in self.actions(state):
            v2, _ = self.max_value(self.result(state, a))
            if v2 < v:
                v, best_move = v2, a
        return v, best_move

    def is_terminal(self, state):
        # TODO: Implement this method to check if the game is over
        pass

    def utility(self, state):
        # TODO: Implement this method to calculate the utility of a state
        pass

    def actions(self, state):
        # TODO: Implement this method to generate all possible actions from a state
        pass

    def result(self, state, action):
        # TODO: Implement this method to calculate the result of an action
        pass


    def choose_move(self, state):
        # Use the Minimax or Alpha-beta pruning algorithm to choose a move
        pass

# More code goes here to set up the game, create players, and manage gameplay


# Matching the game board to visibly represent the board on wikipedia
# Define some constants
WINDOW_SIZE = [600, 600]
DARK_SQUARE = (255, 207, 159)
LIGHT_SQUARE = (210, 140, 69)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SQUARE_SIZE = 75  # Each square is 75x75 pixels

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

black_piece_png = pygame.image.load('Project 2\Black-Game-Piece.png')
White_piece_png = pygame.image.load('Project 2\White-Game-Piece.png')

# Resize the image
piece_black = pygame.transform.scale(black_piece_png, (SQUARE_SIZE - 30, SQUARE_SIZE - 10))
piece_white = pygame.transform.scale(White_piece_png, (SQUARE_SIZE - 30, SQUARE_SIZE - 10))

# Set up the display
screen = pygame.display.set_mode(WINDOW_SIZE)
manager = pygame_gui.UIManager(WINDOW_SIZE)

# Create a panel for the popup box
popup_panel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((150, 150), (300, 250)),
                                          starting_height=1,
                                          manager=manager)

# Create labels
black_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 10), (280, 30)),
                      text='Black Heuristic',
                      manager=manager,
                      container=popup_panel)
white_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((10, 70), (280, 30)),
                      text='White Heuristic',
                      manager=manager,
                      container=popup_panel)

# Create dropdowns
black_heuristic_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['Defensive Heuristic 1', 'Offensive Heuristic 1', 'Defensive Heuristic 2', 'Offensive Heuristic 2'],
    starting_option='Defensive Heuristic 1',
    relative_rect=pygame.Rect((10, 40), (280, 30)),
    manager=manager,
    container=popup_panel
)
white_heuristic_dropdown = pygame_gui.elements.UIDropDownMenu(
    options_list=['Player', 'Defensive Heuristic 1', 'Offensive Heuristic 1', 'Defensive Heuristic 2', 'Offensive Heuristic 2'],
    starting_option='Defensive Heuristic 1',
    relative_rect=pygame.Rect((10, 100), (280, 30)),
    manager=manager,
    container=popup_panel
)

# Create submit button
submit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((100, 150), (100, 30)),
    text='Submit',
    manager=manager,
    container=popup_panel)

heuristic_classes = {
    'Defensive Heuristic 1': DefensiveHeuristic1,
    'Offensive Heuristic 1': OffensiveHeuristic1,
    'Defensive Heuristic 2': DefensiveHeuristic2,
    'Offensive Heuristic 2': OffensiveHeuristic2,
}

black_heuristic = black_heuristic_dropdown.selected_option
white_heuristic = white_heuristic_dropdown.selected_option
black_player = AIPlayer(black_heuristic)
if white_heuristic_dropdown.selected_option != 'Player':
    white_player = AIPlayer(white_heuristic)

# Set up the clock for managing the frame rate

class Piece:
    def __init__(self, image, color):
        self.image = image
        self.color = color

# Initialize the game state
game_state = [[Piece(piece_black, 'black') if i < 2 else Piece(piece_white, 'white') if i >= 6 else None for j in range(8)] for i in range(8)]

# Game loop
running = True
dragging = False
dragged_piece = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Initialize the original position
            original_pos = None
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == submit_button:
                    # Hide the popup panel
                    popup_panel.hide()

                    # Set the options
                    black_heuristic = black_heuristic_dropdown.selected_option
                    white_heuristic = white_heuristic_dropdown.selected_option
                    black_player = AIPlayer(black_heuristic)
                    if white_heuristic_dropdown.selected_option != 'Player':
                        white_player = AIPlayer(white_heuristic)
                    else:
                        print("Not Implemented -- Player vs AI")
        ## Logic for manually moving game pieces, can be used for a move piece function or for the player vs ai
            # In the MOUSEBUTTONDOWN event handler, save the original position
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if white_heuristic is 'Player':  # Only allow manual movement if white_heuristic is None
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // SQUARE_SIZE
                row = mouse_pos[1] // SQUARE_SIZE
                if game_state[row][col] is not None and game_state[row][col].color == 'white':  # Check if there's a piece on the clicked square and it's white
                    original_pos = (row, col)
                    dragged_piece = game_state[row][col]
                    game_state[row][col] = None
                    dragging = True

        # In the MOUSEBUTTONUP event handler, check the color of the piece on the square
        elif event.type == pygame.MOUSEBUTTONUP:
            if white_heuristic is 'Player':  # Only allow manual movement if white_heuristic is None
                mouse_pos = pygame.mouse.get_pos()
                col = mouse_pos[0] // SQUARE_SIZE
                row = mouse_pos[1] // SQUARE_SIZE
                if 0 <= col < 8 and 0 <= row < 8:  # Check if the mouse is within the bounds of the board
                    if game_state[row][col] is None:  # If the square is empty
                        # Check if the move is one step straight or diagonally forward
                        if (original_pos[0] - row == 1) and (abs(original_pos[1] - col) <= 1):
                            game_state[row][col] = dragged_piece
                        else:
                            # If the move is not valid, return the piece to its original position
                            game_state[original_pos[0]][original_pos[1]] = dragged_piece
                    elif game_state[row][col].color == 'black':  # If the square contains a piece of the other color
                        # Check if the move is one step diagonally forward
                        if (original_pos[0] - row == 1) and (abs(original_pos[1] - col) == 1):
                            game_state[row][col] = dragged_piece
                        else:
                            # If the move is not valid, return the piece to its original position
                            game_state[original_pos[0]][original_pos[1]] = dragged_piece
                    else:
                        # If the square contains a piece of the same color, return the piece to its original position
                        game_state[original_pos[0]][original_pos[1]] = dragged_piece
                else:  # If the mouse is outside the board, return the piece to its original position
                    game_state[original_pos[0]][original_pos[1]] = dragged_piece
                dragged_piece = None
                dragging = False
        manager.process_events(event)
        
    # Draw the board
    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            piece = game_state[row][col]
            if piece is not None:
                screen.blit(piece.image, ((col * SQUARE_SIZE) + 15, (row * SQUARE_SIZE) + 5))

    manager.update(pygame.time.get_ticks())
    clock.tick(60)
    manager.draw_ui(screen)

    # Draw the dragged piece
    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(dragged_piece.image, (mouse_pos[0] - SQUARE_SIZE // 2, mouse_pos[1] - SQUARE_SIZE // 2))


    pygame.display.flip()
    pygame.display.update()


# Quit Pygame
pygame.quit()



