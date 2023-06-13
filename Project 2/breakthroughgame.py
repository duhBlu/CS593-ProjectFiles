import pygame
# from pygame.locals import *
import sys, os, math
from minimax_agent import *
from model import *
from alpha_beta_agent import *
import time
import threading
from pprint import pprint
class BreakthroughGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1200, 700
        self.sizeofcell = int(700/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([31, 31, 31])
        # chessboard and workers
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0
        self.computer = None
        self.current_white_matchup = None
        self.current_black_matchup = None

        # status 0: origin;  1: ready to move; 2: end
        # turn 1: black 2: white
        self.status = 0
        self.turn = 1
        # Variable for moving
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        # matrix for position of chess, 0 - empty, 1 - black, 2 - white
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        self.total_nodes_1 = 0
        self.total_nodes_2 = 0
        self.total_time_1 = 0
        self.total_time_2 = 0
        self.prev_time_1 = 0
        self.prev_time_2 = 0
        self.prev_nodes_1 = 0
        self.prev_nodes_2 = 0
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece_1 = 0
        self.eat_piece_2 = 0
        
        # Caption
        pygame.display.set_caption("Breakthrough!")

        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initgraphics()
        #self.ai_queue = queue.Queue()
        #self.ai_thread = threading.Thread(target=self.ai_loop)
        #self.ai_thread.start()
        

            
    def run(self, matchup):
        # Clear the AI queue
        # self.clear_ai_queue()
        
        self.current_white_matchup = self.get_matchup_name(matchup[0])
        self.current_black_matchup = self.get_matchup_name(matchup[1])
        # Reset the game state
        self.boardmatrix = [
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2]
        ]
        self.turn = 1
        self.status = 5
        self.clock.tick(60)
        # clear the screen
        self.screen.fill([255, 255, 255])
        while not self.isgoalstate():
            # Black
            if self.turn == 1:
                    start = time.process_time()
                    nodes_searched = self.ai_move(*matchup[0])
                    self.prev_nodes_1 = nodes_searched  # store the nodes searched in the current turn
                    self.total_nodes_1 += nodes_searched
                    self.prev_time_1  = time.process_time() - start
                    self.total_time_1 += self.prev_time_1
                    self.total_step_1 += 1                
            else:
                    start = time.process_time()
                    nodes_searched = self.ai_move(*matchup[1])
                    self.prev_nodes_2 = nodes_searched  # store the nodes searched in the current turn
                    self.total_nodes_2 += nodes_searched
                    self.prev_time_2  = time.process_time() - start
                    self.total_time_2 += self.prev_time_2
                    self.total_step_2 += 1
            
            
        
            if self.isgoalstate():
                self.status = 3

            # Events accepting
            for event in pygame.event.get():
                # Quit if close the windows
                if event.type == pygame.QUIT:
                    exit()
                # reset button pressed
                elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):
                    self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                                        [1, 1, 1, 1, 1, 1, 1, 1],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0],
                                        [2, 2, 2, 2, 2, 2, 2, 2],
                                        [2, 2, 2, 2, 2, 2, 2, 2]]
                    self.turn = 1
                    self.status = 0
                # computer button pressed
                elif event.type == pygame.MOUSEBUTTONDOWN and self.iscomputer(event.pos):
                    self.ai_move_alphabeta(1)
                    # self.ai_move_minimax()

                elif event.type == pygame.MOUSEBUTTONDOWN and self.isauto(event.pos):
                    self.status = 5

                # ====================================================================================
                # select chess
                elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 0:
                    x, y = event.pos
                    coor_y = math.floor(x / self.sizeofcell)
                    coor_x = math.floor(y / self.sizeofcell)
                    if self.boardmatrix[coor_x][coor_y] == self.turn:
                        self.status = 1
                        self.ori_y = math.floor(x / self.sizeofcell)
                        self.ori_x = math.floor(y / self.sizeofcell)
                # check whether the selected chess can move, otherwise select other chess
                elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 1:
                    x, y = event.pos
                    self.new_y = math.floor(x / self.sizeofcell)
                    self.new_x = math.floor(y / self.sizeofcell)
                    if self.isabletomove():
                        self.movechess()
                        if (self.new_x == 7 and self.boardmatrix[self.new_x][self.new_y] == 1) \
                            or (self.new_x == 0 and self.boardmatrix[self.new_x][self.new_y] == 2):
                            self.status = 3
                    elif self.boardmatrix[self.new_x][self.new_y] == self.boardmatrix[self.ori_x][self.ori_y]:
                        self.ori_x = self.new_x
                        self.ori_y = self.new_y
                        # display the board and chess
            self.display()
            # update the screen
            pygame.display.flip()
            
            if self.turn == 1:
                game_dir = f"{self.current_white_matchup}_vs_{self.current_black_matchup}"
                os.makedirs(game_dir, exist_ok=True)
                screenshot_filename = f"{game_dir}/turn_{self.total_step_2}.png"
                pygame.image.save(self.screen, screenshot_filename)
            
        if self.isgoalstate():
            game_dir = f"{self.current_white_matchup}_vs_{self.current_black_matchup}"
            os.makedirs(game_dir, exist_ok=True)
            screenshot_filename = f"{game_dir}/turn_{self.total_step_2}.png"
            pygame.image.save(self.screen, screenshot_filename)
            return self.show_end_game_popup()
            
    def get_matchup_name(self, matchup):
        # Return a string describing the given matchup.
        search_method, heuristic = matchup
        search_method_name = "Minimax" if search_method == 1 else "Alpha-beta"
        if heuristic == 1:
            heuristic_name = "Offensive Heuristic 1"
        elif heuristic == 2:
            heuristic_name = "Defensive Heuristic 1"
        elif heuristic == 7:
            heuristic_name = "Offensive Heuristic 2"
        elif heuristic == 8:
            heuristic_name = "Defensive Heuristic 2"
        else:
            heuristic_name = "Unknown Heuristic"
        
        return f"{search_method_name} ({heuristic_name})"

      
    def show_end_game_popup(self):
        # Create a font object.
        font = pygame.font.Font(None, 36)

        # Calculate statistics.
        node_per_move_1 = self.total_nodes_1 / self.total_step_1
        time_per_move_1 = self.total_time_1 / self.total_step_1
        node_per_move_2 = self.total_nodes_2 / self.total_step_2
        time_per_move_2 = self.total_time_2 / self.total_step_2

        # Create the text.
        winner_text = f"Winner: {self.current_black_matchup if self.turn == 2 else self.current_white_matchup}"
        white_stats = [
            f"White: [{self.current_white_matchup} Statistics]",
            f"Total Steps = {self.total_step_2}",
            f"Total Nodes = {self.total_nodes_2}",
            f"Total Turn Duration = {self.total_time_2:.4f}",
            f"Average Nodes Searched per Turn = {node_per_move_2:.4f}",
            f"Average Time per Turn = {time_per_move_2:.4f}",
            f"Opponents Defeated = {self.eat_piece_2}"
        ]
        black_stats = [
            f"Black: [{self.current_black_matchup} Statistics]",
            f"Total Steps = {self.total_step_1}",
            f"Total nodes = {self.total_nodes_1}",
            f"Total Turn Duration = {self.total_time_1:.4f}",
            f"Average Nodes Searched per Turn = {node_per_move_1:.4f}",
            f"Average Time per Turn = {time_per_move_1:.4f}",
            f"Opponent Pieces Defeated = {self.eat_piece_1}"
        ]
        
        # Create a solid surface.
        s_game = pygame.Surface((self.height, self.height))  # the size of your rect
        s_game.fill((0, 0, 0)) 
        s_game.set_alpha(200)

        # Create a solid surface for the statistics pane.
        s_stats = pygame.Surface((self.width - self.height, self.height))  # the size of your rect
        s_stats.fill((0, 0, 0)) 
        s_stats.set_alpha(255)

        # Create a transparent surface for the text.
        s_text = pygame.Surface((self.width, self.height), pygame.SRCALPHA) 
        
       # Render the winner text and blit it to the text surface.
        winner_render = font.render(winner_text, True, (255, 255, 255))
        s_text.blit(winner_render, (self.width // 2 - winner_render.get_width() // 2, 20))

        # Render the statistics and blit them to the text surface.
        for i, (white_line, black_line) in enumerate(zip(white_stats, black_stats)):
            white_render = font.render(white_line, True, (255, 255, 255))
            black_render = font.render(black_line, True, (255, 255, 255))
            s_text.blit(white_render, (20, 80 + i * 40))
            s_text.blit(black_render, (self.width // 2 + 20, 80 + i * 40))

        # Blit the surfaces to the screen and update the display.
        self.screen.blit(s_game, (0, 0))
        self.screen.blit(s_stats, (self.height, 0))
        self.screen.blit(s_text, (0, 0))
        pygame.display.flip()

        # Wait for the user to click.
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    return winner_text, white_stats, black_stats




    # load the graphics and rescale them
    def initgraphics(self):
        self.board = pygame.image.load_extended(os.path.join('Project 2\src', 'chessboard.jpg'))
        self.board = pygame.transform.scale(self.board, (700, 700))
        self.blackchess = pygame.image.load_extended(os.path.join('Project 2\src', 'blackchess.png'))
        self.blackchess = pygame.transform.scale(self.blackchess, (self.sizeofcell- 20, self.sizeofcell - 20))
        self.whitechess = pygame.image.load_extended(os.path.join('Project 2\src', 'whitechess.png'))
        self.whitechess = pygame.transform.scale(self.whitechess, (self.sizeofcell - 20, self.sizeofcell - 20))
        self.outline = pygame.image.load_extended(os.path.join('Project 2\src', 'square-outline.png'))
        self.outline = pygame.transform.scale(self.outline, (self.sizeofcell, self.sizeofcell))
        self.reset = pygame.image.load_extended(os.path.join('Project 2\src', 'reset.jpg'))
        self.reset = pygame.transform.scale(self.reset, (50, 50))
        self.winner = pygame.image.load_extended(os.path.join('Project 2\src', 'winner.png'))
        self.winner = pygame.transform.scale(self.winner, (250, 250))
        self.computer = pygame.image.load_extended(os.path.join('Project 2\src', 'computer.png'))
        self.computer = pygame.transform.scale(self.computer, (50, 50))
        self.auto = pygame.image.load_extended(os.path.join('Project 2\src', 'auto.png'))
        self.auto = pygame.transform.scale(self.auto, (50, 50))

    # display the graphics in the window
    def display(self):
        self.screen.fill((31, 31, 31))
        self.screen.blit(self.board, (0, 0))
        self.screen.blit(self.reset, (780, 20))
        self.screen.blit(self.computer, (870, 20))
        self.screen.blit(self.auto, (960, 20))
        for i in range(8):
            for j in range(8):
                if self.boardmatrix[i][j] == 1:
                    self.screen.blit(self.blackchess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
                elif self.boardmatrix[i][j] == 2:
                    self.screen.blit(self.whitechess, (self.sizeofcell * j + 10, self.sizeofcell * i + 10))
        if self.status == 1:
            # only downward is acceptable
            if self.boardmatrix[self.ori_x][self.ori_y] == 1:
                x1 = self.ori_x + 1
                y1 = self.ori_y - 1
                x2 = self.ori_x + 1
                y2 = self.ori_y + 1
                x3 = self.ori_x + 1
                y3 = self.ori_y
                # left down
                if y1 >= 0 and self.boardmatrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                    (self.sizeofcell * y1, self.sizeofcell * x1))
                # right down
                if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                    (self.sizeofcell * y2, self.sizeofcell * x2))
                # down
                if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                    (self.sizeofcell * y3, self.sizeofcell * x3))

            if self.boardmatrix[self.ori_x][self.ori_y] == 2:
                x1 = self.ori_x - 1
                y1 = self.ori_y - 1
                x2 = self.ori_x - 1
                y2 = self.ori_y + 1
                x3 = self.ori_x - 1
                y3 = self.ori_y
                # left up
                if y1 >= 0 and self.boardmatrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                    (self.sizeofcell * y1, self.sizeofcell * x1))
                # right up
                if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                    (self.sizeofcell * y2, self.sizeofcell * x2))
            # up
                if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                    (self.sizeofcell * y3, self.sizeofcell * x3))
        if self.status == 3:
            self.screen.blit(self.winner, (100, 100))
            
        font = pygame.font.Font(None, 24)
        
        
        # Create the text for current player's turn.
        current_player_text = "Black" if self.turn == 1 else "White"

        if current_player_text == "Black":
            current_player_render = font.render(current_player_text, True, (100, 100, 100))
            self.screen.blit(current_player_render, (770, 110))
        else:
            current_player_render = font.render(current_player_text, True, (255, 255, 255))
            self.screen.blit(current_player_render, (830, 110))
        # Render the text and blit it to the screen.
        self.screen.blit(font.render("Turn:", True, (255,255,255)), (725, 110))
        
        white_stats = [
            f"White: {self.current_white_matchup}",
            f"Total Steps: {self.total_step_2}",
            f"Nodes searched last Turn: {self.prev_nodes_2}",
            f"Average Nodes per Turn: {round((self.total_nodes_2 / self.total_step_2 if self.total_step_2 else 0), 4)}",
            f"Time for previous Turn: {self.prev_time_2:.4f}s",
            f"Average time per Turn: {round((self.total_time_2 / self.total_step_2 if self.total_step_2 else 0),4)}s",
            f"Opponents Defeated: {self.eat_piece_2}"
        ]
        black_stats = [
            f"Black: {self.current_black_matchup}",
            f"Total Steps: {self.total_step_1}",
            f"Nodes searched last Turn: {self.prev_nodes_1}",
            f"Average Nodes per Turn: {round((self.total_nodes_1 / self.total_step_1 if self.total_step_1 else 0), 4)}",
            f"Time for previous Turn: {self.prev_time_1:.4f}s",
            f"Average time per Turn: {round((self.total_time_1 / self.total_step_1 if self.total_step_1 else 0), 4)}s",
            f"Opponents Defeated: {self.eat_piece_1}"
        ]


        
        # Render the statistics and blit them to the screen.
        for i, (white_line, black_line) in enumerate(zip(white_stats, black_stats)):
            white_render = font.render(white_line, True, (255, 255, 255))
            black_render = font.render(black_line, True, (255, 255, 255))
            self.screen.blit(white_render, (725, 430 + i * 30))
            self.screen.blit(black_render, (725, 150 + i * 30))

    def movechess(self):
        self.boardmatrix[self.new_x][self.new_y] = self.boardmatrix[self.ori_x][self.ori_y]
        self.boardmatrix[self.ori_x][self.ori_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0

    def isreset(self, pos):
        x, y = pos
        if 670 >= x >= 590 and 50 <= y <= 130:
            return True
        return False

    def iscomputer(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 200 <= y <= 280:
            return True
        return False

    def isauto(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 340 <= y <= 420:
            return True
        return False

    def isabletomove(self):
        if (self.boardmatrix[self.ori_x][self.ori_y] == 1
            and self.boardmatrix[self.new_x][self.new_y] != 1
            and self.new_x - self.ori_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 2)) \
            or (self.boardmatrix[self.ori_x][self.ori_y] == 2
                and self.boardmatrix[self.new_x][self.new_y] != 2
                and self.ori_x - self.new_x == 1
                and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
                and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 1)):
            return 1
        return 0
    

        
    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.ai_move_minimax(evaluation)
        elif searchtype == 2:
            return self.ai_move_alphabeta(evaluation)

    def ai_move_minimax(self, function_type):
        board, nodes, piece = MinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_decision()
        if board is None:
            return 0 
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.eat_piece_1 = 16 - piece
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.eat_piece_2 = 16 - piece
            self.turn = 1
        if self.isgoalstate():
            self.status = 3
            #print(self.boardmatrix)x
        return nodes

    def ai_move_alphabeta(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 5, function_type).alpha_beta_decision()
        if board is None:
            return 0 
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.eat_piece_1 = 16 - piece
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.eat_piece_2 = 16 - piece
            self.turn = 1
        
        if self.isgoalstate():
            self.status = 3
        return nodes

    def isgoalstate(self, base=0):
        if base == 0:
            if 2 in self.boardmatrix[0] or 1 in self.boardmatrix[7]:
                return True
            else:
                for line in self.boardmatrix:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.boardmatrix[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.boardmatrix[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.boardmatrix:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False

# Minimax (Offensive Heuristic 1) = (1, 1)
# Alpha-beta (Offensive Heuristic 1) = (2, 1)
# Alpha-beta (Defensive Heuristic 1) = (2, 2)
# Alpha-beta (Offensive Heuristic 2) = (2, 7)
# Alpha-beta (Defensive Heuristic 2) = (2, 8)

def main():
    matchups = [
        ((1, 1), (2, 1)),  # Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)
        #((2, 7), (2, 2)),  # Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
        #((2, 8), (2, 1)),  # Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
        #((2, 7), (2, 1)),  # Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
        #((2, 8), (2, 2)),  # Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
        #((2, 7), (2, 8))   # Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)
    ]
    i = 1
    game_stats = []
    for matchup in matchups:
        print("Starting matchup " + str(i))
        game = BreakthroughGame()
        stats = game.run(matchup)
        i += 1
        game_stats.append(stats)
    #game.ai_queue.put(None)
    #game.ai_thread.join()
    pygame.quit()

    for game_statistics in game_stats:
        pprint(game_statistics)
if __name__ == '__main__':
    main()

