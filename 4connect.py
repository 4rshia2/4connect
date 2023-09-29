import numpy as np
import random
import pygame
import sys
import math
modes = int(input('Choose Mode : \n(1) Player vs AI \n(2) AI vs AI\n'))

PLAYER = 0
AI = 1
row_num = int(input('Enter the number of row : '))
col_num = int(input('Enter the number of columns : '))
ROW_COUNT = row_num
COLUMN_COUNT = col_num

EMPTY_BLOCK = 0
PLAYER_PIECE = 1
AI_PIECE = 2

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board
def to_playing_the_turn(board, row, col, piece):
	board[row][col] = piece

def canBePlaced(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_first_empty_row(board, col):
	for row in range(ROW_COUNT):
		if board[row][col] == 0:
			return row

def isWon(board, piece):
	# horizontal
	for col in range(COLUMN_COUNT-3):
		for row in range(ROW_COUNT):
			if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
				return True

	# vertical
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT-3):
			if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
				return True

	#diaganols
	for col in range(COLUMN_COUNT-3):
		for row in range(ROW_COUNT-3):
			if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
				return True

	#diaganols
	for col in range(COLUMN_COUNT-3):
		for row in range(3, ROW_COUNT):
			if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
				return True

def evaluate_area(area, piece):
	point = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if area.count(piece) == 4:
		point += 100
	elif area.count(piece) == 3 and area.count(EMPTY_BLOCK) == 1:
		point += 5
	elif area.count(piece) == 2 and area.count(EMPTY_BLOCK) == 2:
		point += 2

	if area.count(opp_piece) == 3 and area.count(EMPTY_BLOCK) == 1:
		point -= 4

	return point

def point_of_position(board, piece):
	point = 0

	## center of the board has bigger price
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	point += center_count * 3

	## point Horizontal
	for row in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[row,:])]
		for col in range(COLUMN_COUNT-3):
			area = row_array[col:col+4]
			point += evaluate_area(area, piece)

	## point Vertical
	for col in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,col])]
		for row in range(ROW_COUNT-3):
			area = col_array[row:row+4]
			point += evaluate_area(area, piece)

	## point diagonal
	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			area = [board[row+i][col+i] for i in range(4)]
			point += evaluate_area(area, piece)

	for row in range(ROW_COUNT-3):
		for col in range(COLUMN_COUNT-3):
			area = [board[row+3-i][col+i] for i in range(4)]
			point += evaluate_area(area, piece)

	return point

def isLeaf(board):
	return isWon(board, PLAYER_PIECE) or isWon(board, AI_PIECE) or len(get_possible_cols(board)) == 0

def minimax(board, depth, alpha, beta, maxTurn):
	possible_cols = get_possible_cols(board)
	leaf = isLeaf(board)
	if depth == 0 or leaf:
		if leaf:
			if isWon(board, AI_PIECE):
				return (None, 100000000000000)
			elif isWon(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else:
				return (None, 0)
		else:
			return (None, point_of_position(board, AI_PIECE))
	if maxTurn:
		value = -math.inf
		column = random.choice(possible_cols)
		for col in possible_cols:
			row = get_first_empty_row(board, col)
			board_copy = board.copy()
			to_playing_the_turn(board_copy, row, col, AI_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else:
		value = math.inf
		column = random.choice(possible_cols)
		for col in possible_cols:
			row = get_first_empty_row(board, col)
			board_copy = board.copy()
			to_playing_the_turn(board_copy, row, col, PLAYER_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_possible_cols(board):
	possible_cols = []
	for col in range(COLUMN_COUNT):
		if canBePlaced(board, col):
			possible_cols.append(col)
	return possible_cols

def make_board(board):
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):
			pygame.draw.rect(screen, '#653700', ((col)*GAME_SIZE, (row+1)*GAME_SIZE, GAME_SIZE, GAME_SIZE))
			pygame.draw.circle(screen, (255, 255, 255), (col*GAME_SIZE+GAME_SIZE//2, int(row*GAME_SIZE+GAME_SIZE+GAME_SIZE/2)), RADIUS)
	
	for col in range(COLUMN_COUNT):
		for row in range(ROW_COUNT):		
			if board[row][col] == PLAYER_PIECE:
				pygame.draw.circle(screen, (0 , 0 ,0), (int(col*GAME_SIZE+GAME_SIZE/2), HEIGHT-int(row*GAME_SIZE+GAME_SIZE/2)), RADIUS)
			elif board[row][col] == AI_PIECE: 
				pygame.draw.circle(screen, 'orange', (int(col*GAME_SIZE+GAME_SIZE/2), HEIGHT-int(row*GAME_SIZE+GAME_SIZE/2)), RADIUS)
	pygame.display.update()

board = create_board()

GAME_SIZE = 100
pygame.init()



WIDTH = (COLUMN_COUNT) * GAME_SIZE
HEIGHT = (ROW_COUNT+1) * GAME_SIZE

RADIUS = GAME_SIZE//2 - 5

screen = pygame.display.set_mode((WIDTH , HEIGHT))

make_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("Bold", 75)


def player_vs_AI(board , myfont , ):
    game_over = False
    turn = random.randint(PLAYER, AI)
    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, (0 ,0 , 0), (0,0, WIDTH, GAME_SIZE))
                if turn == PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx/GAME_SIZE))

                    if canBePlaced(board, col):
                        row = get_first_empty_row(board, col)
                        to_playing_the_turn(board, row, col, PLAYER_PIECE)

                        if isWon(board, PLAYER_PIECE):
                            label = myfont.render("YOU Won", 1, (255 , 0 , 0))
                            screen.blit(label, (40,10))
                            game_over = True
                        turn += 1
                        turn = turn % 2
                        make_board(board)
        if turn == AI and not game_over:				
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if canBePlaced(board, col):
                row = get_first_empty_row(board, col)
                to_playing_the_turn(board, row, col, AI_PIECE)
                if isWon(board, AI_PIECE):
                    label = myfont.render("AI Won", 1, (255, 255 ,255))
                    screen.blit(label, (40,10))
                    game_over = True

                make_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(2000)
def ai_vs_ai(board , myfont):
    game_over = False
    turn = random.randint(PLAYER, AI)
    while not game_over:

     for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        pygame.display.update()

        if turn == PLAYER and not game_over:				
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if canBePlaced(board, col):
                row = get_first_empty_row(board, col)
                to_playing_the_turn(board, row, col, PLAYER_PIECE)
                if isWon(board, PLAYER_PIECE):
                    label = myfont.render("AI1 Won", 1, (255, 255 ,255))
                    screen.blit(label, (40,10))
                    game_over = True

                make_board(board)

                turn += 1
                turn = turn % 2
        elif turn == AI and not game_over:				
            col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
            if canBePlaced(board, col):
                row = get_first_empty_row(board, col)
                to_playing_the_turn(board, row, col, AI_PIECE)
                if isWon(board, AI_PIECE):
                    label = myfont.render("AI2 Won", 1, (255, 255 ,255))
                    screen.blit(label, (40,10))
                    game_over = True

                make_board(board)

                turn += 1
                turn = turn % 2

        if game_over:
            pygame.time.wait(5000)
if modes == 1:
    player_vs_AI(board , myfont)
elif modes == 2:
    ai_vs_ai(board , myfont)