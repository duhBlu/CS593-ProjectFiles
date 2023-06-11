import pygame
# from pygame.locals import *
import sys, os, math
from minimax_agent import *
from model import *
from alpha_beta_agent import *
import time
import threading
import queue
class BreakthroughGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1000, 700
        self.sizeofcell = int(700/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
        # chessboard and workers
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0
        self.computer = None

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
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece = 0
        # Caption
        pygame.display.set_caption("Breakthrough!")

        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initgraphics()
        self.ai_queue = queue.Queue()
        self.ai_thread = threading.Thread(target=self.ai_loop)
        self.ai_thread.start()
        

            
    def run(self, matchup):
        # Clear the AI queue
        self.clear_ai_queue()
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
                self.ai_move(*matchup[0])
                self.total_time_1 += (time.process_time() - start)
                self.total_step_1 += 1
                print('WHITE: total_step_1 = ', self.total_step_1,
                    'total_nodes_1 = ', self.total_nodes_1,
                    'node_per_move_1 = ', self.total_nodes_1 / self.total_step_1,
                    'time_per_move_1 = ', self.total_time_1 / self.total_step_1,
                    'have_eaten = ', self.eat_piece)
                
                
            elif self.turn == 2:
                start = time.process_time()
                self.ai_move(*matchup[1])
                self.total_time_2 += (time.process_time() - start)
                self.total_step_2 += 1
                print('BLACK: total_step_2 = ', self.total_step_2,
                    'total_nodes_2 = ', self.total_nodes_2,
                    'node_per_move_2 = ', self.total_nodes_2 / self.total_step_2,
                    'time_per_move_2 = ', self.total_time_2 / self.total_step_2,
                    'have_eaten: ', self.eat_piece)
                
        
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
        if self.isgoalstate():
            self.show_end_game_popup()
        
    def show_end_game_popup(self):
        # Create a font object.
        font = pygame.font.Font(None, 36)

        # Calculate statistics.
        node_per_move_1 = self.total_nodes_1 / self.total_step_1
        time_per_move_1 = self.total_time_1 / self.total_step_1
        node_per_move_2 = self.total_nodes_2 / self.total_step_2
        time_per_move_2 = self.total_time_2 / self.total_step_2

        # Create the text.
        winner_text = f"Winner: {'White' if self.turn == 2 else 'Black'}"
        white_stats = [
            "[White Statistics]",
            f"total_step = {self.total_step_1}",
            f"total_nodes = {self.total_nodes_1}",
            f"node_per_move = {node_per_move_1:.2f}",
            f"time_per_move = {time_per_move_1:.2f}",
            f"have_eaten = {self.eat_piece}"
        ]
        black_stats = [
            "[Black Statistics]",
            f"total_step = {self.total_step_2}",
            f"total_nodes = {self.total_nodes_2}",
            f"node_per_move = {node_per_move_2:.2f}",
            f"time_per_move = {time_per_move_2:.2f}",
            f"have_eaten = {self.eat_piece}"
        ]

        # Create a solid surface.
        s = pygame.Surface((self.width, self.height))  # the size of your rect
        s.fill((0, 0, 0))  # this fills the entire surface

        # Render the winner text and blit it to the surface.
        winner_render = font.render(winner_text, True, (255, 255, 255))
        s.blit(winner_render, (self.width // 2 - winner_render.get_width() // 2, 20))

        # Render the statistics and blit them to the surface.
        for i, (white_line, black_line) in enumerate(zip(white_stats, black_stats)):
            white_render = font.render(white_line, True, (255, 255, 255))
            black_render = font.render(black_line, True, (255, 255, 255))
            s.blit(white_render, (20, 80 + i * 40))
            s.blit(black_render, (self.width // 2 + 20, 80 + i * 40))

        # Blit the surface to the screen and update the display.
        self.screen.blit(s, (0, 0))
        pygame.display.flip()

        # Wait for the user to click.
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False




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
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.board, (0, 0))
        self.screen.blit(self.reset, (700, 50))
        self.screen.blit(self.computer, (790, 50))
        self.screen.blit(self.auto, (880, 50))
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

        # Create the text.
        white_stats = [
            "White player statistics:",
            f"total_step_1:    {self.total_step_1}",
            f"total_nodes_1:   {self.total_nodes_1}",
            f"node_per_move_1: {round((self.total_nodes_1 / self.total_step_1 if self.total_step_1 else 0), 2)}",
            f"time_per_move_1: {self.total_time_1 / self.total_step_1 if self.total_step_1 else 0}",
            f"have_eaten:      {self.eat_piece}"
        ]
        black_stats = [
            "Black player statistics:",
            f"total_step_2:    {self.total_step_2}",
            f"total_nodes_2:   {self.total_nodes_2}",
            f"node_per_move_2: {round((self.total_nodes_2 / self.total_step_2 if self.total_step_2 else 0), 2)}",
            f"time_per_move_2: {self.total_time_2 / self.total_step_2 if self.total_step_2 else 0}",
            f"have_eaten:      {self.eat_piece}"
        ]

        # Render the statistics and blit them to the screen.
        for i, (white_line, black_line) in enumerate(zip(white_stats, black_stats)):
            white_render = font.render(white_line, True, (0, 0, 0))
            black_render = font.render(black_line, True, (0, 0, 0))
            self.screen.blit(white_render, (725, 125 + i * 30))
            self.screen.blit(black_render, (725, 325 + i * 30))

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
    
    # Updated ai move functions to implement a threaded queue to execute the moves
    def clear_ai_queue(self):
        while not self.ai_queue.empty():
            try:
                self.ai_queue.get(False)
            except queue.Empty:
                continue
            self.ai_queue.task_done()
    
    def ai_loop(self):
        while True:
            task = self.ai_queue.get()
            if task is None:
                break  # Exit the loop if None is added to the queue

            searchtype, evaluation = task
            if searchtype == 1:
                self.ai_move_minimax(evaluation)
            elif searchtype == 2:
                self.ai_move_alphabeta(evaluation)

            self.ai_queue.task_done()
            
    def ai_move(self, searchtype, evaluation):
        self.ai_queue.put((searchtype, evaluation))
        
    # def ai_move(self, searchtype, evaluation):
    #     if searchtype == 1:
    #         return self.ai_move_minimax(evaluation)
    #     elif searchtype == 2:
    #         return self.ai_move_alphabeta(evaluation)

    def ai_move_minimax(self, function_type):
        board, nodes, piece = MinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3
            #print(self.boardmatrix)x

    def ai_move_alphabeta(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.boardmatrix, self.turn, 5, function_type).alpha_beta_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3

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

def main():
    matchups = [
        ((1, 1), (2, 1)),  # Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)
        ((2, 2), (2, 1)),  # Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
        ((2, 1), (2, 2)),  # Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
        ((2, 2), (2, 1)),  # Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
        ((2, 1), (2, 1)),  # Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
        ((2, 2), (2, 2))   # Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)
    ]
    i = 1
    for matchup in matchups:
        print("Starting matchup " + str(i))
        game = BreakthroughGame()
        game.run(matchup)
        i += 1
    game.ai_queue.put(None)
    game.ai_thread.join()
    pygame.quit()


if __name__ == '__main__':
    main()

