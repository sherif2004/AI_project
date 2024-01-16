import numpy as np
import random
import pygame
import sys
import math
from button1 import Button

# Colors
BLACK = (0,0,0)
BLUE = (15,82,186)
YELLOW = (210,181,91)
RED = (184,15,10)

# Background image
BG = pygame.image.load("pics/Background.png")

ROWS = 6
COLS = 7

HUMAN = 0
AI = 1

EMPTY = 0
HUMAN_PIECE = 1
AI_PIECE = 2

GAME_OVER = False

WINDOW_LENGTH = 4

#بيعمل الماتريكس و يصفرها
def create_board():
    board = np.zeros((ROWS,COLS))
    return board

# بيحط القطعه في الماتريكس
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# بيشوف هل الصف متاح او لا
def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

#  بيعدي علي كل الصفوف بالنسبه لعمود معين و بيشوف هل هو متاح او لا ولو متاح بيرجع رقم الصف
def get_next_open_row(board, col):
    for row in range(ROWS):
        if board[row][col] == 0:
            return row
# بيطبع الماتريكس
def print_board(board):
    print(np.flip(board, 0))

# بيشوف الحركه الفائزه بجميع الجهات
def winning_move(board, piece):
    #  horizontal 
    for col in range(COLS-3):
        for row in range(ROWS):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    #  vertical 
    for col in range(COLS):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    #  positive diaganols
    for col in range(COLS-3):
        for row in range(ROWS-3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    #  negative diaganols
    for col in range(COLS-3):
        for row in range(3, ROWS):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True


#  بيشوف مين اللاعب الفائز او التعادل
def is_terminal_node(board):
    return winning_move(board, HUMAN_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

#
def minimax_without_Alpha_Beta(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)  # Positive score for winning move
            elif winning_move(board, HUMAN_PIECE):
                return (None, -10000000000000)  # Negative score for losing move
            else:  # Game over, no more moves
                return (None, 0)  # Zero score for a draw
        else:  # Depth = 0
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax_without_Alpha_Beta(b_copy, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else:  # Minimizing
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, HUMAN_PIECE)
            new_score = minimax_without_Alpha_Beta(b_copy, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value
def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    #the function returns a tuple containing the column and a score for that position.
    #The score is usually positive for a winning move, negative for a losing move, and zero for a draw
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, HUMAN_PIECE):
                return (None, -10000000000000)
            else: # Game over, no more moves
                return (None, 0)
        else: # Depth = 0
            return (None, score_position(board, AI_PIECE))
    # If it's the turn of the maximizing player, it selects the move with the maximum score,
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1] # \\0 ريكرجن عشان لما يعدي عليها يبعتها لل ميني \\ بتخلص لما نوصل للديبس ب
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    # and if it's the turn of the minimizing player,it selects the move with the minimum score.
    else: # Minimizing
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, HUMAN_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1] # ريكرجن عشان لما يعدي عليها يبعتها لل ماكس
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value
    #The alpha-beta pruning is applied to optimize the search by eliminating branches
    # that can't possibly affect the final decision.

# بيعمل اراي بيضع فيها الاماكن المتاحه
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLS):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Heuristic بتاع ال score بيشوف ال
def evaluate_window(window, piece):
    score = 0
    opp_piece = HUMAN_PIECE
    if piece == HUMAN_PIECE:
        opp_piece = AI_PIECE
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 10

    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 4

    if window.count(opp_piece) == 4:
        score -= 100
    elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 20
    return score

# the function returns the total score for the given position.
# The score_position function could be used as part of a heuristic evaluation function to assess the desirability of different moves during the search process, such as in a minimax algorithm with alpha-beta pruning.

# score عشان يعرف يختار احسن لعبه ب ال  Heuristic دي بيستخدها ال
def score_position(board, piece):
    score = 0
    ##  Center
    center_array = [int(i) for i in list(board[:, COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ##  Horizontal
    for row in range(ROWS):
        row_array = [int(i) for i in list(board[row,:])]
        for col in range(COLS-3):
            window = row_array[col:col+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ##  Vertical
    for col in range(COLS):
        col_array = [int(i) for i in list(board[:,col])]
        for row in range(ROWS-3):
            window = col_array[row:row+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ##  Diagonal
    for row in range(ROWS-3):
        for col in range(COLS-3):
            window = [board[row+i][col+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for row in range(ROWS-3):
        for col in range(COLS-3):
            window = [board[row+3-i][col+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Heuristic دي تبع ال
def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        #score = score_position(temp_board, piece)
        score = score_position_with_symmetry(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def score_position_with_symmetry(board, piece):
    # Create a copy of the board to work with
    symmetrical_board = np.rot90(board, k=2)  # Rotate the board 180 degrees

    # Evaluate the position on the original and symmetrical boards
    score_original = score_position(board, piece)
    score_symmetrical = score_position(symmetrical_board, piece)

    # Take the maximum score from the original and symmetrical positions
    max_score = max(score_original, score_symmetrical)

    return max_score

# gui of board of the game
def draw_board(board,human_colour,ai_colour):
    for col in range(COLS):
        for row in range(ROWS):
            pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for col in range(COLS):
        for row in range(ROWS):     
            if board[row][col] == HUMAN_PIECE:
                pygame.draw.circle(screen, human_colour, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[row][col] == AI_PIECE: 
                pygame.draw.circle(screen, ai_colour, (int(col*SQUARESIZE+SQUARESIZE/2), height-int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

pygame.init()
# for pygame
SQUARESIZE = 100
width = COLS * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
size = (width,height)
RADIUS = int(SQUARESIZE/2 - 10)
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("courier", 75)

def get_font(size): 
    return pygame.font.Font("pics/font.ttf", size)

# first page to be continued  
def main_menu():
    pygame.display.set_caption("MAIN Menu")
    condition = True
    try:
        while condition:
            screen.blit(BG,(0,0))# used to draw one image onto another

            MENU_MOUSE_POS = pygame.mouse.get_pos()

            MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(350,100))

            PLAY_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250),
                                text_input="PLAY MINIMAX", font=get_font(25), base_color="#d7fcd4", hovering_color="Yellow")

            PLAY_LOCAL_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 400),
                                text_input="PLAY Heuristic", font=get_font(25), base_color="#d7fcd4", hovering_color="Yellow")

            QUIT_BUTTON = Button(image=pygame.image.load("pics/Quit Rect.png"), pos=(350, 550),
                                text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="Yellow")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, PLAY_LOCAL_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):

                        choose_minimax()
                    if PLAY_LOCAL_BUTTON.checkForInput(MENU_MOUSE_POS):

                        choose_color_for_Heuristic()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        condition = False
            pygame.display.update()
        exit()
    except SystemExit:
        pygame.quit()

def choose_minimax():
    pygame.display.set_caption("CHOOSE MINIMAX")
    condition = True
    try:
        while condition:
            screen.blit(BG,(0,0))# used to draw one image onto another
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            MENU_TEXT = get_font(50).render("MINIMAX", True, "#b68f40")
            MENU_RECT = MENU_TEXT.get_rect(center=(350,100))

            PLAY_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250),
                                text_input="with ALPHA-BETA", font=get_font(20), base_color="#d7fcd4", hovering_color="Yellow")

            PLAY_LOCAL_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 400),
                                text_input="without ALPHA-BETA", font=get_font(20), base_color="#d7fcd4", hovering_color="Yellow")

            BACK = Button(image=None, pos=(350,650),text_input="BACK",font=get_font(40), base_color="Yellow", hovering_color="Green")

            screen.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, PLAY_LOCAL_BUTTON, BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):

                        choose_color_with_Alpha_Beta()
                    if PLAY_LOCAL_BUTTON.checkForInput(MENU_MOUSE_POS):

                        choose_color_without_Alpha_Beta()
                    if BACK.checkForInput(MENU_MOUSE_POS):
                        main_menu()
            pygame.display.update()
    except SystemExit:
        pygame.quit()
# الصفحه الي بختار فيها لون اللاعب
def choose_color_with_Alpha_Beta():
    pygame.display.set_caption("CHOOSE COLOUR with Alpha_Beta")
    try:
        while True:
            screen.blit(BG,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(50).render("CHOOSE COLOUR", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350,100))

            RED_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250),
                            text_input="RED", font=get_font(40), base_color=RED, hovering_color="Red")
            BLUE_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 450),
                            text_input="YELLOW", font=get_font(40), base_color=YELLOW, hovering_color="Yellow")

            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350,650),text_input="BACK",font=get_font(40), base_color="Yellow", hovering_color="Green")

            for button in [RED_BUTTON, BLUE_BUTTON,BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if RED_BUTTON.checkForInput(MENU_MOUSE_POS):
                        human_colour = RED
                        ai_colour = YELLOW
                        choose_difficulty_with_Alpha_Beta(human_colour,ai_colour)
                    if BLUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        human_colour = YELLOW
                        ai_colour = RED
                        choose_difficulty_with_Alpha_Beta(human_colour,ai_colour)
                    if BACK.checkForInput(MENU_MOUSE_POS):
                        choose_minimax()
            pygame.display.update()
    except SystemExit:
        pygame.quit()


def choose_color_without_Alpha_Beta():
    pygame.display.set_caption("CHOOSE COLOUR without Alpha_Beta")
    try:
        while True:
            screen.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(50).render("CHOOSE COLOUR", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350, 100))

            RED_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250),
                                text_input="RED", font=get_font(40), base_color=RED, hovering_color="Red")
            BLUE_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 450),
                                 text_input="YELLOW", font=get_font(40), base_color=YELLOW, hovering_color="Yellow")

            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350, 650), text_input="BACK", font=get_font(40), base_color="Yellow",
                          hovering_color="Green")

            for button in [RED_BUTTON, BLUE_BUTTON, BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if RED_BUTTON.checkForInput(MENU_MOUSE_POS):
                        human_colour = RED
                        ai_colour = YELLOW
                        choose_difficulty_without_Alpha_Beta(human_colour, ai_colour)
                    if BLUE_BUTTON.checkForInput(MENU_MOUSE_POS):
                        human_colour = YELLOW
                        ai_colour = RED
                        choose_difficulty_without_Alpha_Beta(human_colour, ai_colour)
                    if BACK.checkForInput(MENU_MOUSE_POS):
                        choose_minimax()
            pygame.display.update()
    except SystemExit:
        pygame.quit()
# الصفحه الي بختار فيها لون اللاعب
def choose_color_for_Heuristic():
    pygame.display.set_caption("CHOOSE COLOUR for heuristic")
    try:
        while True:
            screen.blit(BG,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(45).render("PLAYER 1 COLOUR", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350,100))

            RED_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 250),
                            text_input="RED", font=get_font(40), base_color=RED, hovering_color="Red")
            BLUE_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 450),
                            text_input="YELLOW", font=get_font(40), base_color=YELLOW, hovering_color="Yellow")

            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350,650),text_input="BACK",font=get_font(40), base_color="Yellow", hovering_color="Green")

            for button in [RED_BUTTON, BLUE_BUTTON,BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if RED_BUTTON.checkForInput(MENU_MOUSE_POS):

                        human_colour = RED
                        ai_colour = YELLOW
                        Heuristic_Ai(human_colour,ai_colour)
                    if BLUE_BUTTON.checkForInput(MENU_MOUSE_POS):

                        human_colour = YELLOW
                        ai_colour = RED
                        Heuristic_Ai(human_colour,ai_colour)

                    if BACK.checkForInput(MENU_MOUSE_POS):
                        main_menu()

            pygame.display.update()
    except SystemExit:
        pygame.quit()

# بيختار فيها صعوبه االلعبه
def choose_difficulty_with_Alpha_Beta(human_colour,ai_colour):
    pygame.display.set_caption("CHOOSE LEVEL with Alpha Beta")
    try:
        while True:
            screen.blit(BG,(0,0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(50).render("CHOOSE LEVEL", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350,100))

            EASY_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 230),
                                text_input="EASY", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")
            MEDIUM_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 380),
                                text_input="MEDIUM", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")
            HARD_BUTTON = Button(image=pygame.image.load("pics/Quit Rect.png"), pos=(350, 530),
                                text_input="HARD", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")

            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350,650),text_input="BACK",font=get_font(40), base_color="Yellow", hovering_color="Green")

            for button in [EASY_BUTTON, MEDIUM_BUTTON,HARD_BUTTON,BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level = 1
                        minimax_with_Alpha_Beta(level,human_colour,ai_colour)
                    if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level = 3
                        minimax_with_Alpha_Beta(level,human_colour,ai_colour)
                    if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level = 5
                        minimax_with_Alpha_Beta(level,human_colour,ai_colour)
                    if BACK.checkForInput(MENU_MOUSE_POS):
                        choose_color_with_Alpha_Beta()
            pygame.display.update()
    except SystemExit:
        pygame.quit()



def choose_difficulty_without_Alpha_Beta(human_colour, ai_colour):
    pygame.display.set_caption("CHOOSE LEVEL without Alpha Beta")
    try:
        while True:
            screen.blit(BG, (0, 0))
            MENU_MOUSE_POS = pygame.mouse.get_pos()

            CHOOSE = get_font(50).render("CHOOSE LEVEL", True, "#b68f40")
            CHOOSE_RECT = CHOOSE.get_rect(center=(350, 100))

            EASY_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 230),
                                 text_input="EASY", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")
            MEDIUM_BUTTON = Button(image=pygame.image.load("pics/Play Rect.png"), pos=(350, 380),
                                   text_input="MEDIUM", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")
            HARD_BUTTON = Button(image=pygame.image.load("pics/Quit Rect.png"), pos=(350, 530),
                                 text_input="HARD", font=get_font(40), base_color="#d7fcd4", hovering_color="Green")

            screen.blit(CHOOSE, CHOOSE_RECT)

            BACK = Button(image=None, pos=(350, 650), text_input="BACK", font=get_font(40), base_color="Yellow",
                          hovering_color="Green")

            for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON, BACK]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level = 1
                        Minimax_without_Alpha_Beta(level, human_colour, ai_colour)
                    if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level = 3
                        Minimax_without_Alpha_Beta(level, human_colour, ai_colour)
                    if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                        level = 5
                        Minimax_without_Alpha_Beta(level, human_colour, ai_colour)
                    if BACK.checkForInput(MENU_MOUSE_POS):
                        choose_color_without_Alpha_Beta()
            pygame.display.update()
    except SystemExit:
        pygame.quit()
# Heuristic لاعب ضد ذكاء ب ال
def Heuristic_Ai(human_colour,ai_colour):
    pygame.display.set_caption("Heuristic Game")
    board = create_board()
    print_board(board)
    turn = random.randint(HUMAN, AI)
    GAME_OVER = False
    WINNER = -1

    while not GAME_OVER:

        draw_board(board, human_colour, ai_colour)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                x = event.pos[0]
                if turn == HUMAN:
                    pygame.draw.circle(screen, human_colour, (x, int(SQUARESIZE / 2)), RADIUS)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # Player 1
                if turn == HUMAN:
                    x = event.pos[0]
                    col = int(math.floor(x / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, HUMAN_PIECE)

                        if winning_move(board, HUMAN_PIECE):
                            label = font.render("You Win!", 1, human_colour)
                            screen.blit(label, (40, 10))
                            WINNER = HUMAN
                            GAME_OVER = True

                        turn += 1
                        turn = turn % 2

                        print_board(board)
                        draw_board(board,human_colour,ai_colour)
                    if GAME_OVER:
                        if WINNER == -1:
                            label = font.render("Draw!", 1, ai_colour)
                            screen.blit(label, (40, 10))
                            print_board(board)
                            draw_board(board, human_colour, ai_colour)
                            pygame.display.update()
                        pygame.time.wait(3000)
                        main_menu()

        # Player 2
        if turn == AI and not GAME_OVER:
            # function Heuristic دي هي
            col = pick_best_move(board, AI_PIECE)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = font.render("AI Wins!", 1, ai_colour)
                    screen.blit(label, (40, 10))
                    WINNER = AI
                    GAME_OVER = True

                print_board(board)
                draw_board(board,human_colour,ai_colour)

                turn += 1
                turn = turn % 2

                if get_valid_locations(board) == []:
                    GAME_OVER = True

                if GAME_OVER:
                    if WINNER == -1:
                        label = font.render("Draw!", 1, ai_colour)
                        screen.blit(label, (40, 10))
                        print_board(board)
                        draw_board(board, human_colour, ai_colour)
                        pygame.display.update()
                    pygame.time.wait(3000)
                    main_menu()
    pygame.quit()
    sys.exit()

# minimaxلاعب ضد ذكاء ب ال
def minimax_with_Alpha_Beta(level,human_colour,ai_colour):
    print(level)
    pygame.display.set_caption("MINIMAX with Alpha Beta Game")
    board = create_board()
    print_board(board)
    turn = random.randint(HUMAN, AI)
    GAME_OVER = False
    WINNER = -1
    draw_board(board,human_colour,ai_colour)

    while not GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                x = event.pos[0]
                if turn == HUMAN:
                    pygame.draw.circle(screen, human_colour, (x, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

                # Player 1 
                if turn == HUMAN:
                    x = event.pos[0]
                    col = int(math.floor(x/SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, HUMAN_PIECE)
                        
                        if winning_move(board, HUMAN_PIECE):
                            label = font.render("You Win!", 1, human_colour)
                            screen.blit(label, (40,10))
                            WINNER = HUMAN
                            GAME_OVER = True
                        turn += 1  # علشان ينقل لل لاعب التاني
                        turn = turn % 2
                    
                        print_board(board)
                        draw_board(board,human_colour,ai_colour)
                    if GAME_OVER:
                        if WINNER == -1:
                            label = font.render("Draw!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            print_board(board)
                            draw_board(board, human_colour, ai_colour)
                            pygame.display.update()
                        pygame.time.wait(5000)
                        main_menu()

        # Player 2 
        if turn == AI and not GAME_OVER:

            col, minimax_score = minimax(board, level, -math.inf, math.inf, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                  
                    label = font.render("AI Wins!", 1, ai_colour)
                    screen.blit(label, (40,10))
                    WINNER = AI
                    GAME_OVER = True

                print_board(board)
                draw_board(board,human_colour,ai_colour)

                turn += 1  # علشان ينقل لل لاعب التاني
                turn = turn % 2

                if get_valid_locations(board) == []: # في حله التعادل اي لا يوجد اماكن فارغه لل لعب
                    GAME_OVER = True

                if GAME_OVER:
                    if WINNER == -1:

                        label = font.render("Draw!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        print_board(board)
                        draw_board(board,human_colour,ai_colour)
                        pygame.display.update()
                    pygame.time.wait(5000)
                    main_menu()
    pygame.quit()
    sys.exit()


def Minimax_without_Alpha_Beta(level, human_colour, ai_colour):
    print(level)
    pygame.display.set_caption("MINIMAX without AlphaBeta Game")
    board = create_board()
    print_board(board)
    turn = random.randint(HUMAN, AI)
    GAME_OVER = False
    WINNER = -1
    draw_board(board, human_colour, ai_colour)

    while not GAME_OVER:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                x = event.pos[0]
                if turn == HUMAN:
                    pygame.draw.circle(screen, human_colour, (x, int(SQUARESIZE / 2)), RADIUS)
            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # Player 1 
                if turn == HUMAN:
                    x = event.pos[0]
                    col = int(math.floor(x / SQUARESIZE))

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, HUMAN_PIECE)

                        if winning_move(board, HUMAN_PIECE):
                            label = font.render("You Win!", 1, human_colour)
                            screen.blit(label, (40, 10))
                            WINNER = HUMAN
                            GAME_OVER = True
                        turn += 1  # علشان ينقل لل لاعب التاني
                        turn = turn % 2

                        print_board(board)
                        draw_board(board, human_colour, ai_colour)
                    if GAME_OVER:
                        if WINNER == -1:
                            label = font.render("Draw!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            print_board(board)
                            draw_board(board, human_colour, ai_colour)
                            pygame.display.update()
                        pygame.time.wait(5000)
                        main_menu()

        # Player 2 
        if turn == AI and not GAME_OVER:

            col, minimax_score = minimax_without_Alpha_Beta(board, level, True)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                if winning_move(board, AI_PIECE):
                    label = font.render("AI Wins!", 1, ai_colour)
                    screen.blit(label, (40, 10))
                    WINNER = AI
                    GAME_OVER = True

                print_board(board)
                draw_board(board, human_colour, ai_colour)

                turn += 1  # علشان ينقل لل لاعب التاني
                turn = turn % 2

                if get_valid_locations(board) == []:  # في حله التعادل اي لا يوجد اماكن فارغه لل لعب
                    GAME_OVER = True

                if GAME_OVER:
                    if WINNER == -1:
                        label = font.render("Draw!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        print_board(board)
                        draw_board(board, human_colour, ai_colour)
                        pygame.display.update()
                    pygame.time.wait(5000)
                    main_menu()
    pygame.quit()
    sys.exit()

try:
    # هنا بيعرض صفخه الاساسيه
    main_menu()
except SystemExit:
    pygame.quit()