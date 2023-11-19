import re
import copy

def display(a):#zapisuje pozycje w pliku position który jest potem wykorzystywany przez board.py
    fen = ''
    with open("position", 'w') as lines:
        for x in a:
            for y in x:
                fen= fen+(str(y)+' ')
        lines.write(fen)


#Here are all the rules of pieces how can they move
class other:#użyłem classy jak folderu dla funkcji aby je oddzielić
    def legal_moves(pos, tem, boardtype):
        #pos to pozycja figury której ruch sprawdzamyi gdzie ona sie chce ruszyć.
        #tem to pozycja wyjściowa figury
        #zwraca liste legalnych ruchów dla danej figury
        piece_functions = {
            1: pc.pawn,#wszystkie z tych to funkcje zamieszczone w clasie pc
            2: pc.horse,
            3: pc.bishop,
            5: pc.rook,
            9: pc.queen,
            10: pc.king
        }
        return piece_functions.get(abs(tem))(pos, tem, boardtype)
        

    #[[1, 4], [3, 4]]
    def move(a):#ta funckja porusza figury 
        global white_to_move, white_king, black_king, white_checked, black_checked, temp_board, king_castle_white, king_castle_black, white_left_rook, white_right_rook, black_left_rook, black_right_rook
        order = other.change_string(a)#zmienia input użytkownika na liste


        temp = board[order[0][0]][order[0][1]]
        if not(br.turn(temp)) or not(order[0]!=order[1]):#sprawdza czy ruch jest prawidłowy
            print('incorrect coordynates')
            return 0


#każda figura ma swoją wartośc 1 pion, 2 kon, 3goniec, 5 wieża, 9hetman, 10 krol
        br.under_attack(board)
        if abs(temp) == 1:#sprawdza ruch piona
            if not(order[1] in other.legal_moves(order, temp, board)[0] or order[1] in other.legal_moves(order, temp, board)[1]):
                print('incorrect piece move')
                return False
        else:#sprawdza legalne ruchy reszty figur
            if not(order[1] in other.legal_moves(order, temp, board)):
                print('incorrect piece move')
                return False
        
        if(white_to_move):#sprawdza czy dany ruch stawia twojego króla w szachu
            temp_board = copy.deepcopy(board)
            temp_board[order[0][0]][order[0][1]] = 0#zmienia wartośc na wartość figury
            temp_board[order[1][0]][order[1][1]] = temp# zmienia wartośc poprzedniego pola na 0- czyli puste
            br.under_attack(temp_board)
            for x in black_enemy_control:#to samo tylko że z białym królem
                for y in x:
                    if white_king == y:
                        print("your king is under attack. you need to protect him")
                        return False
        elif(not(white_to_move)):
            temp_board = copy.deepcopy(board)
            temp_board[order[0][0]][order[0][1]] = 0#zmienia wartośc na wartość figury
            temp_board[order[1][0]][order[1][1]] = temp# zmienia wartośc poprzedniego pola na 0- czyli puste
            br.under_attack(temp_board)
            for x in white_enemy_control:#to samo tylko że z białym królem
                for y in x:
                    if black_king == y:
                        print("your king is under attack. you need to protect him")
                        return False
                    

        if(white_to_move):
            white_checked = False
        else: black_checked = False
        #if order = [[0,][]]

        board[order[0][0]][order[0][1]] = 0#zmienia wartośc na wartość figury
        board[order[1][0]][order[1][1]] = temp# zmienia wartośc poprzedniego pola na 0- czyli puste


###################################################################################
        if order[0] == black_king:
            black_king = order[1]
            king_castle_black = False#sprawdza prawo do roszady obydwu króli
            # print('black king false')
        elif order[0] == white_king:
            white_king = order[1]
            king_castle_white = False
            # print('white king false')
            
        if white_left_rook and board[0][0] != 5:
            white_left_rook = False
            # print('w right false')
        elif white_right_rook and board[0][7] != 5:#sprawdza czy roszada jest mozliwa
            white_right_rook = False
            # print('w left false')

        if black_left_rook and board[7][0] != -5:
            black_left_rook = False
            # print('b right false')
        elif black_right_rook and board[7][7] != -5:
            black_right_rook = False
            # print('b left false')
###################################################################################
        
        br.under_attack(board)
        if white_to_move:#jesli biały ma ruch
            for x in white_enemy_control:#to samo tylko że z białym królem
                if black_checked: break
                for y in x:
                    if black_king == y:
                        black_checked = True
                        break
                    else: black_checked = False

        else:
            for x in black_enemy_control:#to samo tylko że z białym królem
                if white_checked: break
                for y in x:
                    if white_king == y:
                        white_checked = True
                        break
                    else: white_checked = False
                

        
        if board[order[1][0]][order[1][1]] == 1 and order[1][0] == 7:
            x = int(input('9, 5, 3, 2: '))#wybierz na jaką figure chcesz zmienić pionka
            board[order[1][0]][order[1][1]] = x#zmienia pionka jeśli dojdzie do końca

        elif board[order[1][0]][order[1][1]] == -1 and order[1][0] == 0:
            x = int(input('9, 5, 3, 2: '))
            board[order[1][0]][order[1][1]] = -x#zmienia czarnego pionka ponieważ czarne figury oznaczone są liczbami ujemnymi dlatego -x


        white_to_move = not(white_to_move)#zmienia sie tura gracza na przemian biały i czarny mają ruch
        display(board)# zmienia plik position aby zaktualizować pozycje na planszy
        


    def change_string(string):
        return [[int(i) for i in item] for item in string.split()]# zmienia input użytkownika na liste np.: a2 a4 [[0,1][0,3]]

    def letters_to_numbers(coordinates):#zmienia abcd na pozycje na szachownicy która jest dwoma listami
        letters = 'hgfedcba'
        l1 = letters.index(coordinates[0])
        l2 = letters.index(coordinates[3])
        other.move(str(int(coordinates[1])-1)+str(l1)+' '+str(int(coordinates[4])-1)+str(l2))


class br:
    def under_attack(boardd):#sprawdza pola atakowane przez przeciwne figury
        global white_enemy_control
        global black_enemy_control
        black_enemy_control = []
        white_enemy_control = []

        for i in range(8):#sprawdza każde pole po kolej
            for j in range(8):
                if boardd[i][j] > 0:#jeśli wartośc pola jest większa niz 0 czyli jesli stoi tam biała figura to:
                    if boardd[i][j] == 1:#jeśli stoi tam pionek
                        white_enemy_control.append(other.legal_moves([[i, j]], boardd[i][j], boardd)[1])#nie wiem czemu pionek ma ruchy sprawdzane odzielnie <- to dlatego że pion zwraca [legal_pawn_moves, pawn_attack] wiec musimy znac pola przez niego atakowane
                    else:
                        white_enemy_control.append(other.legal_moves([[i, j]], boardd[i][j], boardd))#to sprawdza jakie pola atakuje ta figura
                        #dodaje pola atakowane przez figury do listy

        for i in range(8):
            for j in range(8):
                if boardd[i][j] < 0:#sprawdza czy figura na danym polu jest czarna
                    if boardd[i][j] == -1:
                        black_enemy_control.append(other.legal_moves([[i, j]], boardd[i][j], boardd)[1])
                    else:
                        black_enemy_control.append(other.legal_moves([[i, j]], boardd[i][j], boardd))#nastepnei sprawdza jej ruchy i dodaje do listy
        



    def turn(a):#check whose turn it is now black or white
        if (a>0 and white_to_move) or (a<0 and not(white_to_move)):
            return True
        else: return False

class pc:#pc to prawdopodomnie skrót od piece - po angielksu figura
    
    def pawn(pos, tem, boardtype):#pos to order czyli np.:[[1,2][3,2]] lista ruchów,,, #tem nie mam pojęcia
        sp=pos[0]#sp pierwszy element listy[1,2]^
        pawn_attack = []#lista pól atakowanych przez piona
        legal_pawn_moves = []#lista pól na które pion może sie ruszyć bez ataku
        if (sp[0]+1*tem) >= 0 and (sp[0]+1*tem) <= 7:#sprawdza warunki do ruchu o 2 pola na pierwszym ruchu
            if boardtype[sp[0]+1*tem][sp[1]]==0:
                    legal_pawn_moves.append([sp[0]+1*tem, sp[1]])#dodaje je do listy
        if (sp[0]+2*tem) >= 0 and (sp[0]+2*tem) <= 7:#sprawdza ruchy i dodaje do listy
            if sp[0] in [1, 6] and boardtype[sp[0]+2*tem][sp[1]]==0:
                legal_pawn_moves.append([sp[0]+2*tem, sp[1]])
    

        
        if tem == 1:
            if sp[0]+1<=7 and sp[0]+1>=0 and sp[1]+1<=7 and sp[1]+1>=0:    
                if boardtype[sp[0]+1*tem][sp[1]+1] < 0:
                    pawn_attack.append([sp[0]+1*tem, sp[1]+1])#huh?
            if sp[0]+1<=7 and sp[0]+1>=0 and sp[1]-1<=7 and sp[1]-1>=0:#zwraca pola atakowane przez piona ale nie wiem jak sie to dzieje
                if boardtype[sp[0]+1*tem][sp[1]-1] < 0:
                    pawn_attack.append([sp[0]+1*tem, sp[1]-1])
        else: 
            if sp[0]+1<=7 and sp[0]+1>=0 and sp[1]+1<=7 and sp[1]+1>=0:
                if boardtype[sp[0]-1*tem][sp[1]+1] < 0:
                    pawn_attack.append([sp[0]+1*tem, sp[1]+1])
            if sp[0]+1<=7 and sp[0]+1>=0 and sp[1]-1<=7 and sp[1]-1>=0:
                if boardtype[sp[0]-1*tem][sp[1]-1] < 0:
                    pawn_attack.append([sp[0]+1*tem, sp[1]-1])
        return [legal_pawn_moves, pawn_attack]
        
        

    #[1, 4]
    def horse(a, tem,boardtype):
        legal_horse_moves = []
        if tem > 0:
            if (0 <= a[0][0]-2 <= 7) and (0 <= a[0][1]+1 <= 7) and (boardtype[a[0][0]-2][a[0][1]+1] <= 0):#sprawdza po kolei każde pole na jakie może iść kon i czy jest dozwolone
                legal_horse_moves.append([a[0][0]-2, a[0][1]+1])
            if (0 <= a[0][0]-1 <= 7) and (0 <= a[0][1]+2 <= 7) and (boardtype[a[0][0]-1][a[0][1]+2] <= 0):
                legal_horse_moves.append([a[0][0]-1, a[0][1]+2])
            if (0 <= a[0][0]+1 <= 7) and (0 <= a[0][1]+2 <= 7) and (boardtype[a[0][0]+1][a[0][1]+2] <= 0):
                legal_horse_moves.append([a[0][0]+1, a[0][1]+2])
            if (0 <= a[0][0]+2 <= 7) and (0 <= a[0][1]+1 <= 7) and (boardtype[a[0][0]+2][a[0][1]+1] <= 0):
                legal_horse_moves.append([a[0][0]+2, a[0][1]+1])
            if (0 <= a[0][0]+2 <= 7) and (0 <= a[0][1]-1 <= 7) and (boardtype[a[0][0]+2][a[0][1]-1] <= 0):
                legal_horse_moves.append([a[0][0]+2, a[0][1]-1])
            if (0 <= a[0][0]+1 <= 7) and (0 <= a[0][1]-2 <= 7) and (boardtype[a[0][0]+1][a[0][1]-2] <= 0):
                legal_horse_moves.append([a[0][0]+1, a[0][1]-2])
            if (0 <= a[0][0]-1 <= 7) and (0 <= a[0][1]-2 <= 7) and (boardtype[a[0][0]-1][a[0][1]-2] <= 0):
                legal_horse_moves.append([a[0][0]-1, a[0][1]-2])
            if (0 <= a[0][0]-2 <= 7) and (0 <= a[0][1]-1 <= 7) and (boardtype[a[0][0]-2][a[0][1]-1] <= 0):
                legal_horse_moves.append([a[0][0]-2, a[0][1]-1])
        else:
            if (0 <= a[0][0]-2 <= 7) and (0 <= a[0][1]+1 <= 7) and (boardtype[a[0][0]-2][a[0][1]+1] >= 0):#nie wiem czemu ten cały blok if' ów powtarza sie drógi raz <- to dlatego że odnielnie sprawdza dla białego i czarnego
                legal_horse_moves.append([a[0][0]-2, a[0][1]+1])
            if (0 <= a[0][0]-1 <= 7) and (0 <= a[0][1]+2 <= 7) and (boardtype[a[0][0]-1][a[0][1]+2] >= 0):
                legal_horse_moves.append([a[0][0]-1, a[0][1]+2])
            if (0 <= a[0][0]+1 <= 7) and (0 <= a[0][1]+2 <= 7) and (boardtype[a[0][0]+1][a[0][1]+2] >= 0):
                legal_horse_moves.append([a[0][0]+1, a[0][1]+2])
            if (0 <= a[0][0]+2 <= 7) and (0 <= a[0][1]+1 <= 7) and (boardtype[a[0][0]+2][a[0][1]+1] >= 0):
                legal_horse_moves.append([a[0][0]+2, a[0][1]+1])
            if (0 <= a[0][0]+2 <= 7) and (0 <= a[0][1]-1 <= 7) and (boardtype[a[0][0]+2][a[0][1]-1] >= 0):
                legal_horse_moves.append([a[0][0]+2, a[0][1]-1])
            if (0 <= a[0][0]+1 <= 7) and (0 <= a[0][1]-2 <= 7) and (boardtype[a[0][0]+1][a[0][1]-2] >= 0):
                legal_horse_moves.append([a[0][0]+1, a[0][1]-2])
            if (0 <= a[0][0]-1 <= 7) and (0 <= a[0][1]-2 <= 7) and (boardtype[a[0][0]-1][a[0][1]-2] >= 0):
                legal_horse_moves.append([a[0][0]-1, a[0][1]-2])
            if (0 <= a[0][0]-2 <= 7) and (0 <= a[0][1]-1 <= 7) and (boardtype[a[0][0]-2][a[0][1]-1] >= 0):
                legal_horse_moves.append([a[0][0]-2, a[0][1]-1])
        return legal_horse_moves

    

    def bishop(pos, tem, boardtype):#sprawdza ruchy gońców
        cond = [1, 1, 1, 1]#huh? <- sprawdza w lini pole po kolej a gdy trafi na jakąś figure lub koniec planszy przestaje sprawdzać pola w tym kierunku, elementy to 4 kierunki
        legal_bishop_moves = []
        sp = pos[0]
        if tem > 0:
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[0]:#sprawdza po kolei
                    if boardtype[sp[0]+x][sp[1]+x] <= 0:
                        legal_bishop_moves.append([sp[0]+x, sp[1]+x])
                        if boardtype[sp[0]+x][sp[1]+x] < 0:
                            cond[0]=0#jesli natrafi na figure zmienia cond tego na zery tym samym nie doda pól za figura
                    else: cond[0]=0

                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[1]:
                    if boardtype[sp[0]+x][sp[1]-x] <= 0:
                        legal_bishop_moves.append([sp[0]+x, sp[1]-x])
                        if boardtype[sp[0]+x][sp[1]-x] < 0:
                            cond[1]=0
                    else: cond[1]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[2]:
                    if boardtype[sp[0]-x][sp[1]-x] <= 0:
                        legal_bishop_moves.append([sp[0]-x, sp[1]-x])
                        if boardtype[sp[0]-x][sp[1]-x] < 0:
                            cond[2]=0
                    else: cond[2]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[3]:
                    if boardtype[sp[0]-x][sp[1]+x] <= 0:
                        legal_bishop_moves.append([sp[0]-x, sp[1]+x])
                        if boardtype[sp[0]-x][sp[1]+x] < 0:
                            cond[3]=0
                    else: cond[3]=0
        else:#sprawdza dla czarnych
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[0]:
                    if boardtype[sp[0]+x][sp[1]+x] >= 0:
                        legal_bishop_moves.append([sp[0]+x, sp[1]+x])
                        if boardtype[sp[0]+x][sp[1]+x] > 0:
                            cond[0]=0
                    else: cond[0]=0

                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[1]:
                    if boardtype[sp[0]+x][sp[1]-x] >= 0:
                        legal_bishop_moves.append([sp[0]+x, sp[1]-x])
                        if boardtype[sp[0]+x][sp[1]-x] > 0:
                            cond[1]=0
                    else: cond[1]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[2]:
                    if boardtype[sp[0]-x][sp[1]-x] >= 0:
                        legal_bishop_moves.append([sp[0]-x, sp[1]-x])
                        if boardtype[sp[0]-x][sp[1]-x] > 0:
                            cond[2]=0
                    else: cond[2]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[3]:
                    if boardtype[sp[0]-x][sp[1]+x] >= 0:
                        legal_bishop_moves.append([sp[0]-x, sp[1]+x])
                        if boardtype[sp[0]-x][sp[1]+x] > 0:
                            cond[3]=0
                    else: cond[3]=0

        return legal_bishop_moves#zwraca liste mozliwych ruchów


    def rook(pos, tem, boardtype):
        cond = [1, 1, 1, 1]#tak samo jak w gońcu 
        legal_rook_moves = []#to samo jak goniec ale pionowo i poziomo a nie na ukos
        sp = pos[0]
        if tem > 0 :
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]<=7 and sp[1]>=0 and cond[0]:
                    if boardtype[sp[0]+x][sp[1]] <= 0:
                        legal_rook_moves.append([sp[0]+x, sp[1]])
                        if boardtype[sp[0]+x][sp[1]] < 0:
                            cond[0]=0
                    else: cond[0]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]<=7 and sp[1]>=0 and cond[1]:
                    if boardtype[sp[0]-x][sp[1]] <= 0:
                        legal_rook_moves.append([sp[0]-x, sp[1]])
                        if boardtype[sp[0]-x][sp[1]] < 0:
                            cond[1]=0
                    else: cond[1]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[2]:
                    if boardtype[sp[0]][sp[1]+x] <= 0:
                        legal_rook_moves.append([sp[0], sp[1]+x])
                        if boardtype[sp[0]][sp[1]+x] < 0:
                            cond[2]=0
                    else: cond[2]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[3]:
                    if boardtype[sp[0]][sp[1]-x] <= 0:
                        legal_rook_moves.append([sp[0], sp[1]-x])
                        if boardtype[sp[0]][sp[1]-x] < 0:
                            cond[3]=0
                    else: cond[3]=0
        else: 
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]<=7 and sp[1]>=0 and cond[0]:
                    if boardtype[sp[0]+x][sp[1]] >= 0:
                        legal_rook_moves.append([sp[0]+x, sp[1]])
                        if boardtype[sp[0]+x][sp[1]] > 0:
                            cond[0]=0
                    else: cond[0]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]<=7 and sp[1]>=0 and cond[1]:
                    if boardtype[sp[0]-x][sp[1]] >= 0:
                        legal_rook_moves.append([sp[0]-x, sp[1]])
                        if boardtype[sp[0]-x][sp[1]] > 0:
                            cond[1]=0
                    else: cond[1]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[2]:
                    if boardtype[sp[0]][sp[1]+x] >= 0:
                        legal_rook_moves.append([sp[0], sp[1]+x])
                        if boardtype[sp[0]][sp[1]+x] > 0:
                            cond[2]=0
                    else: cond[2]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[3]:
                    if boardtype[sp[0]][sp[1]-x] >= 0:
                        legal_rook_moves.append([sp[0], sp[1]-x])
                        if boardtype[sp[0]][sp[1]-x] > 0:
                            cond[3]=0
                    else: cond[3]=0

        return legal_rook_moves
    



        
    def queen(pos, tem, boardtype):#skopiowałem kod dla wierzy i gonca drógi raz tutaj
        cond = [1, 1, 1, 1]#nie wiem czemu nei zrobiłem return bishop() + rook() ale robiłem to rok temu
        legal_queen_moves = []
        sp = pos[0]
        if tem > 0 :
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]<=7 and sp[1]>=0 and cond[0]:
                    if boardtype[sp[0]+x][sp[1]] <= 0:
                        legal_queen_moves.append([sp[0]+x, sp[1]])
                        if boardtype[sp[0]+x][sp[1]] < 0:
                            cond[0]=0
                    else: cond[0]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]<=7 and sp[1]>=0 and cond[1]:
                    if boardtype[sp[0]-x][sp[1]] <= 0:
                        legal_queen_moves.append([sp[0]-x, sp[1]])
                        if boardtype[sp[0]-x][sp[1]] < 0:
                            cond[1]=0
                    else: cond[1]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[2]:
                    if boardtype[sp[0]][sp[1]+x] <= 0:
                        legal_queen_moves.append([sp[0], sp[1]+x])
                        if boardtype[sp[0]][sp[1]+x] < 0:
                            cond[2]=0
                    else: cond[2]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[3]:
                    if boardtype[sp[0]][sp[1]-x] <= 0:
                        legal_queen_moves.append([sp[0], sp[1]-x])
                        if boardtype[sp[0]][sp[1]-x] < 0:
                            cond[3]=0
                    else: cond[3]=0
            cond = [1, 1, 1, 1]
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[0]:
                    if boardtype[sp[0]+x][sp[1]+x] <= 0:
                        legal_queen_moves.append([sp[0]+x, sp[1]+x])
                        if boardtype[sp[0]+x][sp[1]+x] < 0:
                            cond[0]=0
                    else: cond[0]=0

                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[1]:
                    if boardtype[sp[0]+x][sp[1]-x] <= 0:
                        legal_queen_moves.append([sp[0]+x, sp[1]-x])
                        if boardtype[sp[0]+x][sp[1]-x] < 0:
                            cond[1]=0
                    else: cond[1]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[2]:
                    if boardtype[sp[0]-x][sp[1]-x] <= 0:
                        legal_queen_moves.append([sp[0]-x, sp[1]-x])
                        if boardtype[sp[0]-x][sp[1]-x] < 0:
                            cond[2]=0
                    else: cond[2]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[3]:
                    if boardtype[sp[0]-x][sp[1]+x] <= 0:
                        legal_queen_moves.append([sp[0]-x, sp[1]+x])
                        if boardtype[sp[0]-x][sp[1]+x] < 0:
                            cond[3]=0
                    else: cond[3]=0
        else:
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]<=7 and sp[1]>=0 and cond[0]:
                    if boardtype[sp[0]+x][sp[1]] >= 0:
                        legal_queen_moves.append([sp[0]+x, sp[1]])
                        if boardtype[sp[0]+x][sp[1]] > 0:
                            cond[0]=0
                    else: cond[0]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]<=7 and sp[1]>=0 and cond[1]:
                    if boardtype[sp[0]-x][sp[1]] >= 0:
                        legal_queen_moves.append([sp[0]-x, sp[1]])
                        if boardtype[sp[0]-x][sp[1]] > 0:
                            cond[1]=0
                    else: cond[1]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[2]:
                    if boardtype[sp[0]][sp[1]+x] >= 0:
                        legal_queen_moves.append([sp[0], sp[1]+x])
                        if boardtype[sp[0]][sp[1]+x] > 0:
                            cond[2]=0
                    else: cond[2]=0

                if sp[0]<=7 and sp[0]>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[3]:
                    if boardtype[sp[0]][sp[1]-x] >= 0:
                        legal_queen_moves.append([sp[0], sp[1]-x])
                        if boardtype[sp[0]][sp[1]-x] > 0:
                            cond[3]=0
                    else: cond[3]=0
            cond = [1, 1, 1, 1]
            for x in range(1, 8):
                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[0]:
                    if boardtype[sp[0]+x][sp[1]+x] >= 0:
                        legal_queen_moves.append([sp[0]+x, sp[1]+x])
                        if boardtype[sp[0]+x][sp[1]+x] > 0:
                            cond[0]=0
                    else: cond[0]=0

                if sp[0]+x<=7 and sp[0]+x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[1]:
                    if boardtype[sp[0]+x][sp[1]-x] >= 0:
                        legal_queen_moves.append([sp[0]+x, sp[1]-x])
                        if boardtype[sp[0]+x][sp[1]-x] > 0:
                            cond[1]=0
                    else: cond[1]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]-x<=7 and sp[1]-x>=0 and cond[2]:
                    if boardtype[sp[0]-x][sp[1]-x] >= 0:
                        legal_queen_moves.append([sp[0]-x, sp[1]-x])
                        if boardtype[sp[0]-x][sp[1]-x] > 0:
                            cond[2]=0
                    else: cond[2]=0
                
                if sp[0]-x<=7 and sp[0]-x>=0 and sp[1]+x<=7 and sp[1]+x>=0 and cond[3]:
                    if boardtype[sp[0]-x][sp[1]+x] >= 0:
                        legal_queen_moves.append([sp[0]-x, sp[1]+x])
                        if boardtype[sp[0]-x][sp[1]+x] > 0:
                            cond[3]=0
                    else: cond[3]=0
        return legal_queen_moves

    def king(pos, tem, boardtype):#ah król jest rudny ponieważ nie może chodzić jeśli pole jest atakowane
        sp = pos[0]  # starting position
        legal_king_moves = []
        if tem == 10:
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if (0 <= sp[0]+x <= 7) and (0 <= sp[1]+y <= 7):
                        if boardtype[sp[0]+x][sp[1]+y] <= 0:
                            legal_king_moves.append([sp[0]+x, sp[1]+y])#na początku dodaje o jedno pole wokół niego
            for x in black_enemy_control:
                legal_king_moves = [item for item in legal_king_moves if item not in x] 

            for x in black_enemy_control:#huh?
               for y in x:
                   if boardtype[0][1] == y or boardtype[0][2] == y:
                       break
            else:
               if not(white_checked) and white_left_rook and king_castle_white and boardtype[0][1] == 0 and boardtype[0][2] == 0:
                   legal_king_moves.append([0, 1])
            
            for x in black_enemy_control:
               for y in x:
                   if boardtype[0][4] == x or boardtype[0][5] == x:
                       break
            else:
               if not(white_checked) and white_left_rook and king_castle_white and boardtype[0][4] == 0 and boardtype[0][5] == 0 and boardtype[0][6] == 0:
                   legal_king_moves.append([0, 5])       


        else: #i dla czarnego
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if (0 <= sp[0]+x <= 7) and (0 <= sp[1]+y <= 7):
                        if boardtype[sp[0]+x][sp[1]+y] >= 0:
                            legal_king_moves.append([sp[0]+x, sp[1]+y])

            for x in white_enemy_control:
                legal_king_moves = [item for item in legal_king_moves if item not in x] 
            
            for x in white_enemy_control:#huh?
               for y in x:
                   if boardtype[0][1] == y or boardtype[0][2] == y:
                       break
            else:
               if not(white_checked) and white_left_rook and king_castle_white and boardtype[0][1] == 0 and boardtype[0][2] == 0:
                   legal_king_moves.append([0, 1])
            
            for x in white_enemy_control:
               for y in x:
                   if boardtype[0][4] == x or boardtype[0][5] == x:
                       break
            else:
               if not(white_checked) and white_left_rook and king_castle_white and boardtype[0][4] == 0 and boardtype[0][5] == 0 and boardtype[0][6] == 0:
                   legal_king_moves.append([0, 5])
        # print(legal_king_moves)
        return legal_king_moves

        

#move function whcich later uses the class to check is the move available

global white_to_move, white_king, black_king, white_checked, black_checked, temp_board, king_castle_white, king_castle_black, white_left_rook, white_right_rook, black_left_rook, black_right_rook
enemy_control = []
white_to_move = True #check whose turn it is now
white_king = [0, 3]
black_king = [7, 3]
black_checked = False
white_checked = False
king_castle_white = True
king_castle_black = True
white_left_rook = True
white_right_rook = True
black_left_rook = True
black_right_rook = True
list_of_attacks = []

board = [
    [5, 2, 3, 10, 9, 3, 2, 5],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1],
    [-5, -2, -3, -10, -9, -3, -2, -5]
]
temp_board = []


while True:
    
    user_input = input('Enter move (ex: a2 a4): ')
    match = re.fullmatch(r'([a-hA-H])([1-9])\s([a-hA-H])([1-9])', user_input)
    if match:
        other.letters_to_numbers(user_input.lower())
    else:
        print('Invalid input format. Please enter a valid move.')





    