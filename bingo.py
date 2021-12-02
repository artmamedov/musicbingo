import numpy as np
class Bingo:
    def __init__(self,boards):
        #Make boards
        self.boards = boards

    def find_line_bingo(self,played, board, num_bingos = 1):
        bingo_count = 0
        board = np.array(board)
        board_sides = len(board)
        for i,row in enumerate(board):
            bingo = all(song in played for song in row)
            if bingo:
                bingo_count+=1
        for i, col in enumerate(board.T):
            bingo = all(song in played for song in col)
            if bingo:
                bingo_count+=1
        top_left_diag = [board[i][i] for i in range(board_sides)]
        bingo = all(song in played for song in top_left_diag)
        if bingo:
            bingo_count+=1
        top_right_diag = [board[i][board_sides-1-i] for i in range(board_sides)]
        bingo = all(song in played for song in top_right_diag)
        if bingo:
            bingo_count+=1
        return bingo_count >= num_bingos

    def full_bingo(self,played,board):
        row_counts = 0
        for row in board:
            bingo = all(song in played for song in row)
            if bingo:
              row_counts += 1
        if row_counts == len(board):
            return True
        else:
            return False

    def find_bingo(self,played,queue,find_bingo_count=5):
        to_be_played = played.copy()
        queue_copy = queue.copy()
        found_bingo = False
        round_count = 0
        full_bingo_count = 0
        single_bingo_count = 0
        double_bingo_count = 0
        triple_bingo_count = 0
        #Insert play next button
        full_winning_boards = []
        single_winning_boards = []
        double_winning_boards = []
        triple_winning_boards = []

        full_winning_boards_i = []
        single_winning_boards_i = []
        double_winning_boards_i = []
        triple_winning_boards_i = []

        while full_bingo_count < find_bingo_count and len(queue_copy)>0:
            round_count += 1
            to_be_played.append(queue_copy[0])
            queue_copy = queue_copy[1:]
            for i, board in enumerate(self.boards):
                single_bingo = self.find_line_bingo(to_be_played,board,1)
                double_bingo = self.find_line_bingo(to_be_played,board,2)
                triple_bingo = self.find_line_bingo(to_be_played,board,3)
                full_bingo = self.full_bingo(to_be_played,board)
                if single_bingo and len(single_winning_boards) < find_bingo_count and i not in single_winning_boards_i:
                    single_bingo_count +=1
                    single_winning_boards.append((i,round_count,len(played)+round_count))
                    single_winning_boards_i.append(i)
                    #print(f"Board #{i} found a single bingo in {round_count} rounds on round {len(played)+round_count}")
                if double_bingo and len(double_winning_boards) < find_bingo_count and i not in double_winning_boards_i:
                    double_bingo_count +=1
                    double_winning_boards.append((i,round_count,len(played)+round_count))
                    double_winning_boards_i.append(i)
                    #print(f"Board #{i} found a double bingo in {round_count} rounds on round {len(played)+round_count}")
                if triple_bingo and len(triple_winning_boards) < find_bingo_count and i not in triple_winning_boards_i:
                    triple_bingo_count +=1
                    triple_winning_boards.append((i,round_count,len(played)+round_count))
                    triple_winning_boards_i.append(i)

                    #print(f"Board #{i} found a triple bingo in {round_count} rounds on round {len(played)+round_count}")
                if full_bingo and i not in full_winning_boards_i:
                    full_bingo_count +=1
                    full_winning_boards.append((i,round_count,len(played)+round_count))
                    full_winning_boards_i.append(i)

                    #print(f"Board #{i} found a full bingo in {round_count} rounds on round {len(played)+round_count}")
        print("Single Line Winners:")
        for single in single_winning_boards:
            print(f"Board #{single[0]} in {single[1]} on round {single[2]}")
        print("")
        print("Double Line Winners:")
        for double in double_winning_boards:
            print(f"Board #{double[0]} in {double[1]} on round {double[2]}")
        print("")
        print("Triple Line Winners:")
        for triple in triple_winning_boards:
            print(f"Board #{triple[0]} in {triple[1]} on round {triple[2]}")
        print("")
        print("Full Board Winners:")
        for full in full_winning_boards:
            print(f"Board #{full[0]} in {full[1]} on round {full[2]}")
        print("")
