#Mason Corey, CS 165A Spring 2020

import sys
import copy
import string

board_size = 11
human_start = "b"
test = 1

class Tree(object):
    def __init__(self, board, node_type, color="n", v=0.0, move="", v_index=-1):
        #The current board configuration. For leaves, it is one of the permutations of the parent's board
        self.board = board
        #Node type is 'a' for max node, 'i' for min node, and 'l' for leaf node
        self.node_type = node_type
        #Only applicable for min/max nodes. Is "b" if current min/max node is the black player, while "l" if current min/max node is light player. "n" by default for leaf nodes
        self.color = color
        #v is the value of heuristics score for leaf nodes and best leaf node score for max/min nodes
        self.v = v
        #v_index is only applicable for min/max nodes, is the index of the leaf with best score
        self.v_index = v_index
        #Move, will always be an empty string when you initialize
        self.move = move
        #Children. Only applicable for min/max nodes
        self.children = []

#Build a minimax tree of all possibilities (with heuristics score) given board and player color, depth = 2
def build_tree(root, board, max_color, og_depth, depth):
    #Stop condition for recursive build_tree function
    if depth <= 0:
        return

    child_node_type = ''
    #Check what the child_node_type should be in advance when adding children to root
    #If depth == 1, the children of root will be leaf nodes
    if depth == 1:
        child_node_type = 'l'
    #Else depth is > 1. Assuming that root node should be max, we want 
    else:
        if og_depth%2 == 0:
            #Og_Depth is even, so if current depth is even, children nodes are min and if current depth is odd, children nodes are max
            if depth%2 == 0:
                #Depth is even, children nodes are min
                child_node_type = 'i'
            elif depth%2 == 1:
                #Depth is odd, children nodes are max
                child_node_type = 'a'
        elif og_depth%2 == 1:
            #Og_Depth is odd, so if current depth is even, children nodes are max and if current depth is odd, children nodes are min
            if depth%2 == 0:
                #Depth is even, children nodes are max
                child_node_type = 'a'
            elif depth%2 == 1:
                #Depth is odd, children nodes are min
                child_node_type = 'i'

    #Check what the child_color should be in advance when adding children to root. If max_color (i.e. max_color for max node) is 'b', max nodes are 'b' and min nodes are 'l'. If max_color is 'l', max nodes are 'l' and min nodes are 'b'.
    if(max_color == "b" and child_node_type == 'a'):
        child_color = "b"
    elif(max_color == "b" and child_node_type == 'i'):
        child_color = "l"
    elif(max_color == "l" and child_node_type == 'a'):
        child_color = "l"
    elif(max_color == "l" and child_node_type == 'i'):
        child_color = "b"
    #If child_node_type is leaf, child_color is max's color
    elif(max_color == "b" and child_node_type == 'l'):
        if og_depth%2 == 0:
            child_color = "b"
        elif og_depth%2 == 1:
            child_color = "l"
    elif(max_color == "l" and child_node_type == 'l'):
        if og_depth%2 == 0:
            child_color = "l"
        elif og_depth%2 == 1:
            child_color = "b"

    #Check what default value should be in advance when adding children to root. If child_node_type is min, default v should be +inf. If child_node_type is max, default v should be -inf. If leaf node, leave it as 0.
    if(child_node_type == 'i'):
        child_val = float('inf')
    elif(child_node_type == 'a'):
        child_val = float('-inf')
    elif(child_node_type == 'l'):
        child_val = 0.0
    
    #Build tree at each layer. Iterate through each EMPTY spot and check for adjacent stones. If adjacent stones exist, make create a new node and add it to the root's children
    for row in range(board_size):
        for column in range(board_size):
            #If the current spot is empty, check all adjacent spots to see if you should place a stone here as a possible move
            if(board[row][column] == 'x'):
                #If spot above current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                if(row-1 >= 0 and board[row-1][column] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

                #If spot below current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                elif(row+1 <= board_size-1 and board[row+1][column] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

                #If spot to the left of current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                elif(column-1 >= 0 and board[row][column-1] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

                #If spot to the right of current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                elif(column+1 <= board_size-1 and board[row][column+1] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

                #If spot to the top-right of current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                elif(((row-1 >= 0) and (column+1 <= board_size-1)) and board[row-1][column+1] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

                #If spot to the top-left of current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                elif(((row-1 >= 0) and (column-1 >= 0)) and board[row-1][column-1] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

                #If spot to the bottom-right of current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                elif(((row+1 <= board_size-1) and (column+1 <= board_size-1)) and board[row+1][column+1] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

                #If spot to the bottom-left of current place on board exists, check it for stones. If it contains a stone, make this a possible move and continue
                elif(((row+1 <= board_size-1) and (column-1 >= 0)) and board[row+1][column-1] != 'x'):
                    #Add stone at current spot and create a new node, adding to children of current root. Then change the board back and keep moving
                    new_board = copy.deepcopy(board)
                    if(child_color == "b"):
                        new_board[row][column] = 'l'
                    elif(child_color == "l"):
                        new_board[row][column] = 'b'
                    new_move = chr(97+column) + str(row+1)
                    new_node = Tree(new_board, child_node_type, child_color, child_val, new_move)
                    root.children.append(new_node)
                    continue

            #If current spot is not empty, ignore and continue
            else:
                continue

    #Repeat this process for all children with depth-1 until depth goes to 0
    for i in range(len(root.children)):
        build_tree(root.children[i], root.children[i].board, max_color, og_depth, depth-1)

    return root

#Run heuristics func for a max_player on a given board and max_color
def calc_score(board, max_color):
    #TODO: MAKE SURE TO CHANGE BLACK/LIGHT PATTERNS AT SOME POINT. THESE ARE PLACEHOLDERS. ALSO MIGHT HAVE TO IMPLEMENT THE "NO DOUBLE COUNTING A PATTERN AS A DIFFERENT PATTERN WHEN ALL THE STONES HAVE ALREADY BEEN USED" METHOD USING A DICTIONARY THAT TRACKS THE USAGE OF EACH STONE/SPOT
    black_patterns = [['b','b','b','b','b'], ['b','b','b','b','x'], ['b','b','b','x','x'], ['b','b','x','x','x'], ['b','x','x','x','x']]
    light_patterns = [['l','l','l','l','l'], ['l','l','l','l','x'], ['l','l','l','x','x'], ['l','l','x','x','x'], ['l','x','x','x','x']]

    #Every time a black_pattern at index 0 is scored, add 1 to index 0 of black scores, etc.
    black_scores = [0 for x in range(5)]
    light_scores = [0 for x in range(5)]

    #For each spot on the board, check if there is a pattern in one of the patterns lists up above. Check left, right, up, down, and diagonals. Don't check for item if the whole thing is not in range
    for row in range(board_size):
        for column in range(board_size):
            #If the current spot does not have a stone on it, that means it will never match any of the patterns. No point in checking. Onward to victory!
            if(board[row][column] == 'x'):
                continue

            test_score = []
            already_black = 0

            #Check the range to perform checks on up, down, left, right, diags. If range is valid, check each spot for potential win. Then move to next spot.
            if(row-4 >= 0):
                #Check up
                for i in range(5):
                    test_score.append(board[row-i][column])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []


            if(row+4 <= board_size-1):
                #Check down
                for i in range(5):
                    test_score.append(board[row+i][column])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []


            if(column-4 >= 0):
                #Check left
                for i in range(5):
                    test_score.append(board[row][column-i])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []


            if(column+4 <= board_size-1):
                #Check right
                for i in range(5):
                    test_score.append(board[row][column+i])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []


            if((row-4 >= 0) and (column+4 <= board_size-1)):
                #Check up-right diagonal
                for i in range(5):
                    test_score.append(board[row-i][column+i])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []


            if((row-4 >= 0) and (column-4 >= 0)):
                #Check up-left diagonal
                for i in range(5):
                    test_score.append(board[row-i][column-i])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []


            if((row+4 <= board_size-1) and (column+4 <= board_size-1)):
                #Check down-right diagonal
                for i in range(5):
                    test_score.append(board[row+i][column+i])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []


            if((row+4 <= board_size-1) and (column-4 >= 0)):
                #Check down-left diagonal
                for i in range(5):
                    test_score.append(board[row+i][column-i])

                #Check if test_score matches any of the black patterns. If so, mark this in black_scores and don't check the light patterns b/c it's definitely not a light pattern
                for i in range(len(black_patterns)):
                    if test_score == black_patterns[i]:
                        black_scores[i] += 1
                        already_black = 1
                        break
                
                #If test_score was already_black, just set it to 0 and move on. If not, check to see if test_score is any of the light_patterns
                if already_black == 0:
                    for i in range(len(light_patterns)):
                        if test_score == light_patterns[i]:
                            light_scores[i] += 1
                            break
                else:
                    already_black = 0

                test_score = []

    #Return the heuristics score based on if AI is black stones or light stones
    if max_color == "b":
        v_score = (50000*black_scores[0] + 1000*black_scores[1] + 6*black_scores[2] + 2*black_scores[3] + black_scores[4]) - (50000*light_scores[0] + 1000*light_scores[1] + 6*light_scores[2] + 2*light_scores[3] + light_scores[4])
    elif max_color == "l":
        v_score = (50000*light_scores[0] + 1000*light_scores[1] + 6*light_scores[2] + 2*light_scores[3] + light_scores[4]) - (50000*black_scores[0] + 1000*black_scores[1] + 6*black_scores[2] + 2*black_scores[3] + black_scores[4])

    return v_score

#Depth can only be 2 or 3 bc it's a shitty debug print. print_val is either 0 or 1, 1 if you want to print heuristic score of options and 0 if you don't want to
def debug_print_options(root, depth, print_val, print_index, print_move):
    temp_root = root

    if depth == 2:
        #Print options for debugging
        print("Root board: ", '\n')
        for item in temp_root.board:
            print(item)
        print('\n')

        for item in temp_root.children:
            print("Possible max option: ", '\n')
            if print_move == 1:
                print("This is the move for this option: ", item.move, '\n')
            if print_index == 1:
                print("This is the index for this option: ", item.v_index, '\n')
            for row in item.board:
                print(row)
            print('\n','\n')

            print("Possible min options: ", '\n')
            for item2 in item.children:
                #print("Possible min option: ", '\n')
                for row2 in item2.board:
                    print(row2)
                if print_val == 1:
                        print("This is the value of the current board: ", item2.v)
                print('\n')

                #print("Possible max2 options: ", '\n')
                #for item3 in item2.children:
                    #for row3 in item3.board:
                        #print(row3)
                    #print('\n')

            print('\n', '\n', '\n', '\n')

    elif depth == 3:
        #Print options for debugging
        print("Root board: ", '\n')
        for item in temp_root.board:
            print(item)
        print('\n')

        for item in temp_root.children:
            print("Possible max option: ", '\n')
            if print_move == 1:
                print("This is the move for this option: ", item.move, '\n')
            if print_index == 1:
                print("This is the index for this option: ", item.v_index, '\n')
            for row in item.board:
                print(row)
            #print('\n','\n')
            print('\n')

            #print("Possible min options: ", '\n')
            for item2 in item.children:
                print("Possible min option: ", '\n')
                for row2 in item2.board:
                    print(row2)
                print('\n')

                print("Possible max2 options: ", '\n')
                for item3 in item2.children:
                    if print_val == 1:
                        print("This is the value of the current board: ", item3.v)
                    for row3 in item3.board:
                        print(row3)
                    print('\n')

            print('\n', '\n', '\n', '\n')

#This is the old version, converting it to alpha/beta pruning
'''
def generate_heuristics(root, max_color):
    #If this is a leaf node, calculate the heuristics score and store it in the root
    if root.node_type == 'l':
        root.v = calc_score(root.board, max_color)
        return root

    for i in range(len(root.children)):
        if root.node_type == 'a':
            root.children[i] = generate_heuristics(root.children[i], max_color)
            if root.children[i].v > root.v:
                root.v = root.children[i].v
                root.v_index = i

        elif root.node_type == 'i':
            root.children[i] = generate_heuristics(root.children[i], max_color)
            if root.children[i].v < root.v:
                root.v = root.children[i].v
                root.v_index = i

    #Return root after all values have been propagated up to top
    return root
'''

#Alpha/beta pruned version of above code
def generate_heuristics(root, max_color, alpha, beta):
    #If this is a leaf node, calculate the heuristics score and store it in the root
    if root.node_type == 'l':
        root.v = calc_score(root.board, max_color)
        return root

    if root.node_type == 'a':
        for i in range(len(root.children)):
            root.children[i] = generate_heuristics(root.children[i], max_color, alpha, beta)
            if root.children[i].v > root.v:
                root.v = root.children[i].v
                root.v_index = i
            if root.v > alpha:
                alpha = root.v
            if beta <= alpha:
                break

    elif root.node_type == 'i':
        for i in range(len(root.children)):
            root.children[i] = generate_heuristics(root.children[i], max_color, alpha, beta)
            if root.children[i].v < root.v:
                root.v = root.children[i].v
                root.v_index = i
            if root.v < beta:
                beta = root.v
            if beta <= alpha:
                break

    #Return root after all values have been propagated up to top
    return root

#Decide the move you want to play. Build the decision tree, run the heuristics on it and alpha-beta prune. Currently in beta lol
def decide_move(board, color, first_move):
    if first_move:
        return chr(97+int(board_size/2)) + str(int(board_size/2)+1)
    else:
        #Create a minimax tree with all possible decisions, depth = 2.
        #Value of a max node is -inf to start, value of a min node is +inf to start
        root = Tree(board, 'a', color, float('-inf'))
        root = build_tree(root, board, color, 2, 2)

        #TODO: Run alpha/beta pruned search while filling in heuristics scores
        root = generate_heuristics(root, color, float('-inf'), float('inf'))

        #debug_print_options(root, 2, 0, 1, 1)

        #print("This is the best index of root: ", root.v_index, " And this is the best score of root: ", root.v, " And this is the move played: ", root.children[root.v_index].move)
        
        return root.children[root.v_index].move

#Play a move on the game board that the AI is keeping track of
def play_move(color, board, input):
    row, column = int(input[1:])-1, ord(input[0])-97
    #print(row, column)
    if(board[row][column] == 'x'):
        if color == "b":
            board[row][column] = 'b'
        elif color == "l":
            board[row][column] = 'l'
        return board

#Checking if a five-in-a-row has been made
def check_game_over(board, color):
    game_over = 0
    full = 1

    if color == "b":
        winning_condition = ['b','b','b','b','b']
    elif color == "l":
        winning_condition = ['l','l','l','l','l']

    #For each spot on the board, check if there is a five-in-a-row. Check left, right, up, down, and diagonals. Don't check for item if the whole thing is not in range
    for row in range(board_size):
        for column in range(board_size):
            test_win = []
            
            #Check if board is full
            if full == 1:
                if board[row][column] == 'x':
                    full = 0

            #Check the range to perform checks on up, down, left, right, diags. If range is valid, check each spot for potential win. Then move to next spot.
            if(row-4 >= 0):
                #Check up
                for i in range(5):
                    test_win.append(board[row-i][column])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

            if(row+4 <= board_size-1):
                #Check down
                for i in range(5):
                    test_win.append(board[row+i][column])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

            if(column-4 >= 0):
                #Check left
                for i in range(5):
                    test_win.append(board[row][column-i])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

            if(column+4 <= board_size-1):
                #Check right
                for i in range(5):
                    test_win.append(board[row][column+i])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

            if((row-4 >= 0) and (column+4 <= board_size-1)):
                #Check up-right diagonal
                for i in range(5):
                    test_win.append(board[row-i][column+i])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

            if((row-4 >= 0) and (column-4 >= 0)):
                #Check up-left diagonal
                for i in range(5):
                    test_win.append(board[row-i][column-i])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

            if((row+4 <= board_size-1) and (column+4 <= board_size-1)):
                #Check down-right diagonal
                for i in range(5):
                    test_win.append(board[row+i][column+i])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

            if((row+4 <= board_size-1) and (column-4 >= 0)):
                #Check down-left diagonal
                for i in range(5):
                    test_win.append(board[row+i][column-i])

                if test_win == winning_condition:
                    game_over = 1
                    return game_over, color
                else:
                    test_win = []

    #If game is still "full" by the end and no winning move has been played, the game is a tie.
    if full == 1:
        game_over = 1
        color = "n"
    return game_over, color

#PRINT_BOARD FUNCTION COPIED FROM REFEREE.PY FOR EASE OF USE DURING DEBUGGING. ALL CREDIT GOES TO KARL WANG AND ALL PREVIOUS WRITERS OF REFEREE.PY
def print_board(board):
    sys.stdout.write("  ")
    i = 0
    for c in string.ascii_lowercase:
      i += 1
      if i > board_size:
        break
      sys.stdout.write("   %s" % c)
    sys.stdout.write("\n   +")
    for i in range(0, board_size):
      sys.stdout.write("---+")
    sys.stdout.write("\n")

    for i in range(0, board_size):
      sys.stdout.write("%2d |" % (i + 1))
      for j in range(0, board_size):
        if board[i][j] == 'l':
          sys.stdout.write(" L |")
        elif board[i][j] == 'b':
          sys.stdout.write(" D |")
        else:
          sys.stdout.write("   |")
      sys.stdout.write("\n   +")
      for j in range(0, board_size):
        sys.stdout.write("---+")
      sys.stdout.write("\n")

def valid_input(board, input):
    if(not input[0].isalpha()):
        print("The first part of your move is not a letter.")
        return 0
    for i in range(1, len(input)-1):
        if(not input[i].isdigit()):
            print(input[i])
            print("The second part of your move is not all numbers.")
            return 0
    row, column = int(input[1:])-1, ord(input[0])-97
    if(row not in range(0, board_size) or column not in range(0, board_size)):
        print("Move out of bounds.")
        return 0
    elif(board[row][column] != 'x'):
        print("Spot already taken.")
        return 0
    return 1

if __name__ == "__main__":
    #Handle initial args
    if len(sys.argv) != 1:
        if sys.argv[1] == "-n":
            if int(sys.argv[2]) < 5 or int(sys.argv[2]) > 26:
                print("Board size must be 5-26! Pick again")
                exit(0)
            else:
                board_size = int(sys.argv[2])
            if len(sys.argv) != 3:
                if sys.argv[3] == "-l":
                    human_start = "l"
        elif sys.argv[1] == "-l":
            human_start = "l"
            if len(sys.argv) != 2:
                if sys.argv[2] == "-n":
                    if int(sys.argv[3]) < 5 or int(sys.argv[3]) > 26:
                        print("Board size must be 5-26! Pick again")
                        exit(0)
                    else:
                        board_size = int(sys.argv[3])

    #Initialize the game board
    board = [['x' for x in range(0, board_size)] for x in range(0, board_size)]
    #Set variable for first_move
    first_move = 1
    #repeat trading moves until game over
    print_board(board)
    while True:
        #Human starts if human_start == "b"
        if human_start == "b":
            #Human move
            print("Play your move, human!")
            human_input = sys.stdin.readline()
            while(not valid_input(board, human_input)):
                print("Input not valid! Please enter a letter and number within range: ")
                human_input = sys.stdin.readline()
            board = play_move("b", board, human_input)

            print_board(board)
            
            #Write move to referee.py
            sys.stdout.flush()
            sys.stdout.write("Move played: %s\n" % human_input)
            sys.stdout.flush()

            #Check game over condition after every move
            game_over, winner = check_game_over(board, "b")
            if game_over == 1:
                if winner == "b":
                    print("Game over! The winner is black player.")
                elif winner == "l":
                    print("Game over! The winner is light player.")
                elif winner == "n":
                    print("Game over! The board is full and the game is a tie.")
                exit(0)


            #AI Move
            move = decide_move(board, 'l', 0)
            board = play_move("l", board, move)

            print_board(board)

            #Write move to referee.py
            sys.stdout.flush()
            sys.stdout.write("Move played: %s\n" % move)
            sys.stdout.flush()

            #Check game over condition after every move
            game_over, winner = check_game_over(board, "l")
            if game_over == 1:
                if winner == "b":
                    print("Game over! The winner is black player.")
                elif winner == "l":
                    print("Game over! The winner is light player.")
                elif winner == "n":
                    print("Game over! The board is full and the game is a tie.")
                exit(0)


        #else, AI starts
        elif human_start == "l":
            #AI Move
            if first_move:
                first_move = 0
                move = decide_move(board, 'b', 1)
            else:
                move = decide_move(board, 'b', 0)
            test += 1
            board = play_move("b", board, move)

            print_board(board)

            #Write move to referee.py
            sys.stdout.flush()
            sys.stdout.write("Move played: %s\n" % move)
            sys.stdout.flush()

            #Check game over condition after every move
            game_over, winner = check_game_over(board, "b")
            if game_over == 1:
                if winner == "b":
                    print("Game over! The winner is black player.")
                elif winner == "l":
                    print("Game over! The winner is light player.")
                elif winner == "n":
                    print("Game over! The board is full and the game is a tie.")
                exit(0)


            #Human move
            print("Play your move, human!")
            human_input = sys.stdin.readline()
            while(not valid_input(board, human_input)):
                print("Input not valid! Please enter a letter and number within range: ")
                human_input = sys.stdin.readline()
            board = play_move("l", board, human_input)

            print_board(board)
            
            #Write move to referee.py
            sys.stdout.flush()
            sys.stdout.write("Move played: %s\n" % human_input)
            sys.stdout.flush()

            #Check game over condition after every move
            game_over, winner = check_game_over(board, "l")
            if game_over == 1:
                if winner == "b":
                    print("Game over! The winner is black player.")
                elif winner == "l":
                    print("Game over! The winner is light player.")
                elif winner == "n":
                    print("Game over! The board is full and the game is a tie.")
                exit(0)