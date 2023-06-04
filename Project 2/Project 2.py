from copy import deepcopy
import pygame
import pygame_gui
import random
import sys
class Game:
    def __init__(self, state, black_player, white_player):
        self.state = state
        self.player1 = white_player
        self.player2 = black_player
        self.current_player = self.player1

    def play_game(self):
        while not self.is_game_over():
            move = self.current_player.choose_move(self.state)
            self.state = self.apply_move(self.state, move)
            self.current_player = self.player2 if self.current_player == self.player1 else self.player1

    def is_game_over(self):
        # The game is over if one player has no pieces left
        return not any(piece.color == 'black' for row in self.state for piece in row) or \
               not any(piece.color == 'white' for row in self.state for piece in row)
    
    def play_turn(state, move):
        # Apply the move to the state
        new_state = game.apply_move(state, move)

        # Switch turns
        turn = 'black' if turn == 'white' else 'white'

        return new_state    
    def apply_move(self, state, move):
        # Update the game state based on the move
        # This is a very basic implementation and you would need to add more logic to handle the specific rules of your game
        old_row, old_col, new_row, new_col = move
        state[new_row][new_col] = state[old_row][old_col]
        state[old_row][old_col] = None
        return state
  
class Heuristic:
    def __init__(self, color):
        self.color = color

    def evaluate(self, state):
        raise NotImplementedError
    
    def search_algorithm(self):
        raise NotImplementedError

class DefensiveHeuristic1(Heuristic):
    def evaluate(self, state):
        
        # Determine the opponent's color
        opponent_color = 'black' if self.color == 'white' else 'white'
        # Count the number of own pieces remaining
        num_own_pieces = sum(1 for row in state for piece in row if piece is not None and piece.color == opponent_color)
        
        # Compute the value
        value = 2 * num_own_pieces + random.random()
        
        return value

    def search_algorithm(self):
        return "minimax"
    
class OffensiveHeuristic1(Heuristic):
    def evaluate(self, state):
        # Determine the opponent's color
        opponent_color = 'black' if self.color == 'white' else 'white'
        # Count the number of opponent's pieces remaining
        num_opponent_pieces = sum(1 for row in state for piece in row if piece is not None and piece.color != opponent_color)
        # Compute the value
        value = 2 * (30 - num_opponent_pieces) + random.random()
        return value

    def search_algorithm(self):
        return "alpha-beta"

class DefensiveHeuristic2(Heuristic):
    def evaluate(self, state):
        # Implement the evaluation for Defensive Heuristic 2
        # might prioritize blocking the opponent's pieces
        pass

class OffensiveHeuristic2(Heuristic):
    def evaluate(self, state):
        # Implement the evaluation for Offensive Heuristic 2
        # might prioritize advancing its own pieces towards the opponent's side of the board.
        pass

class AIPlayer:
    def __init__(self, heuristic, color):
        self.heuristic = heuristic(color)
        self.color = color

    def has_won(self, state, color):
        # If the color is white, check the last row
        if color == 'white':
            return any(piece is not None and piece.color == 'white' for piece in state[7])
        # If the color is black, check the first row
        else:  # color == 'black'
            return any(piece is not None and piece.color == 'black' for piece in state[0])

    
    # choose the move based 
    def choose_move(self, state):
        if self.heuristic.search_algorithm() == "minimax":
            _, move = self.max_value_minimax(state, 3)  # Depth of 3 for minimax
        else:  # Assume alpha-beta if not minimax
            _, move = self.max_value_alpha_beta(state, -float('inf'), float('inf'), 4)  # Depth of 4 for alpha-beta
        return move
    
    # implementation from the project manual
    def max_value_minimax(self, state):
        if self.is_terminal(state):
            return self.utility(state), None
        v = -float('inf')
        best_move = None
        for a in self.actions(state):
            v2, _ = self.min_value_minimax(self.result(state, a))
            if v2 > v:
                v, best_move = v2, a
        return v, best_move

    # implementation from the project manual
    def max_value_minimax(self, state, depth):
        if self.is_terminal(state) or depth == 0:
            return self.heuristic.evaluate(state), None
        v = -float('inf')
        best_move = None
        for a in self.actions(state):
            v2, _ = self.min_value_minimax(self.result(state, a), depth - 1)
            if v2 > v:
                v, best_move = v2, a
        return v, best_move

    # implementation from the project manual
    def min_value_minimax(self, state, depth):
        if self.is_terminal(state) or depth == 0:
            return self.heuristic.evaluate(state), None
        v = float('inf')
        best_move = None
        for a in self.actions(state):
            v2, _ = self.max_value_minimax(self.result(state, a), depth - 1)
            if v2 < v:
                v, best_move = v2, a
        return v, best_move

    # implementation from the project manual
    def max_value_alpha_beta(self, state, alpha, beta, depth):
        if self.is_terminal(state) or depth == 0:
            return self.heuristic.evaluate(state), None
        v = -float('inf')
        best_move = None
        for a in self.actions(state):
            v2, _ = self.min_value_alpha_beta(self.result(state, a), alpha, beta, depth - 1)
            if v2 > v:
                v, best_move = v2, a
            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)
        return v, best_move

    # implementation from the project manual
    def min_value_alpha_beta(self, state, alpha, beta, depth):
        if self.is_terminal(state) or depth == 0:
            return self.heuristic.evaluate(state), None
        v = float('inf')
        best_move = None
        for a in self.actions(state):
            v2, _ = self.max_value_alpha_beta(self.result(state, a), alpha, beta, depth - 1)
            if v2 < v:
                v, best_move = v2, a
            if v <= alpha:
                return v, best_move
            beta = min(beta, v)
        return v, best_move


    def is_terminal(self, state):
        # Check if a player has won or if there are no more legal moves
        if self.has_won(state, 'white') or self.has_won(state, 'black') or not self.actions(state):
            return True
        return False


    def utility(self, state):
        # Calculate the utility of the state
        # This is just a placeholder and should be replaced with your own logic
        return self.heuristic.evaluate(state)


    def actions(self, state):
        # Generate all possible actions
        actions = []
        for row in range(len(state)):
            for col in range(len(state[row])):
                if state[row][col] is not None and state[row][col].color == self.color:
                    actions.extend(self.generate_moves(state, (row, col)))
        return actions

    def result(self, state, action):
        # Apply the action to the state
        new_state = deepcopy(state)
        move_from, move_to = action
        new_state[move_to[0]][move_to[1]] = new_state[move_from[0]][move_from[1]]
        new_state[move_from[0]][move_from[1]] = None
        return new_state


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
    'Player' : None,
}

white_heuristic = None
white_player = None
black_player = None
def setup_game():
    # Display the popup panel for the user to set the heuristics selections
    popup_panel.show()

    # Wait for the user to press the submit button
    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            manager.process_events(event)  # Add this line

            # Handle QUIT events
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle USEREVENT events
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == submit_button:
                        # Hide the popup panel
                        popup_panel.hide()
                        # Set the options
                        black_heuristic = heuristic_classes[black_heuristic_dropdown.selected_option]
                        white_heuristic = heuristic_classes[white_heuristic_dropdown.selected_option]
                        black_player = AIPlayer(black_heuristic, 'black')
                        white_player = AIPlayer(white_heuristic, 'white')
                        return black_player, white_player

        manager.update(time_delta)  # Update the UI
        manager.draw_ui(screen)  # Draw the UI

        # Update the display
        pygame.display.update()

class Piece:
    def __init__(self, image, color):
        self.image = image
        self.color = color
        


# Initialize the game state
game_state = [[Piece(piece_black, 'black') if i < 2 else Piece(piece_white, 'white') if i >= 6 else None for j in range(8)] for i in range(8)]



# Draw the board
for row in range(8):
    for col in range(8):
        color = LIGHT_SQUARE if (row + col) % 2 == 0 else DARK_SQUARE
        pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        piece = game_state[row][col]
        if piece is not None:
            screen.blit(piece.image, ((col * SQUARE_SIZE) + 15, (row * SQUARE_SIZE) + 5))
            
# Call the setup function before starting the game loop
black_player, white_player = setup_game()
if white_player.heuristic == 'Player':
    game = Game(game_state, black_player, None)
else:
    game = Game(game_state, black_player, white_player)

print(white_player, black_player)

game.play_game()

# Game loop
running = True
dragging = False
dragged_piece = None
turn = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Initialize the original position
            original_pos = None
                               
        ## Logic for manually moving game pieces, can be used for a move piece function or for the player vs ai
            # In the MOUSEBUTTONDOWN event handler, save the original position
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if white_heuristic == 'Player':  # Only allow manual movement if white_heuristic is None
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
            if white_heuristic == 'Player':  # Only allow manual movement if white_heuristic is Player
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

        
               # Let the AI choose a move
        
        manager.process_events(event)
    
    if turn == 'white':
        if white_player is not None:
            move = white_player.choose_move(game_state)
        else:
            print("White player is not defined yet.")
    else:
        if black_player is not None:
            move = black_player.choose_move(game_state)
        else:
            print("Black player is not defined yet.")

    if move:
        # Apply the move to the game state
        game_state = game.play_turn(game_state, move)
    

    manager.update(pygame.time.get_ticks())
    clock.tick(60)
    manager.draw_ui(screen)

    # Draw the dragged piece
    if dragging:
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(dragged_piece.image, (mouse_pos[0] - SQUARE_SIZE // 2, mouse_pos[1] - SQUARE_SIZE // 2))


    pygame.display.update()


# Quit Pygame
pygame.quit()



