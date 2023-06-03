## We need to implement a game with offensive and defensive heuristics. There are six matchups we need to consider:
    Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)
    Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
    Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
    Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)
    Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)
    Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)

For bonus points, we can implement extended rules and report on matchups 2 and 3. 

We need to write a report describing our implementation, our choice of heuristics, and our findings. The report should include pseudocode or figures if they help clarify our approach. If we submit any work for bonus points, we should make sure it's clearly indicated in our report.

Additional bonus points can be earned by:

    Designing an interface for the game that allows us to play against the computer and discussing how well we do compared to the AI.
    Implementing advanced techniques from class lectures or our own reading to try to improve efficiency or quality of gameplay.
    Implementing a 1-depth greedy heuristic bot and describing the differences between the gameplays of the greedy bot and the minimax bot.

We need to submit our report in PDF format and our well-commented source code, along with any necessary executables or supporting files. We should include a Readme.txt file with instructions on how to compile and run our program.

Step 1
Define the Game State: In your Python program, you'll need a way to represent the state of the game. This might be a class or a data structure that includes information about the current configuration of the game board, whose turn it is, and any other relevant information.

Step 2
Implement the Heuristics: You'll need to implement at least two heuristics: an offensive one and a defensive one. A heuristic is a function that estimates the value of a game state. An offensive heuristic might prioritize states where you have a lot of pieces near the opponent's base, while a defensive heuristic might prioritize states where your pieces are safe from capture.

Step 3
Implement the AI: You'll need to implement AI players that use the Minimax and Alpha-beta pruning algorithms. These algorithms should use your heuristics to decide which move to make.