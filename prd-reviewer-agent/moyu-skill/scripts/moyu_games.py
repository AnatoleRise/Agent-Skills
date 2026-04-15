import os
import time

class BoardGame:
    def __init__(self):
        self.board = []
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        pass
    
    def make_move(self, move):
        pass
    
    def check_winner(self):
        pass
    
    def reset(self):
        pass

class TicTacToe(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("井字棋")
        print("---------")
        for i in range(3):
            print(f"| {self.board[i*3]} | {self.board[i*3+1]} | {self.board[i*3+2]} |")
            print("---------")
    
    def make_move(self, move):
        try:
            move = int(move) - 1
            if 0 <= move < 9 and self.board[move] == ' ':
                self.board[move] = self.current_player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                return True
            else:
                return False
        except:
            return False
    
    def check_winner(self):
        # 检查行
        for i in range(0, 9, 3):
            if self.board[i] == self.board[i+1] == self.board[i+2] != ' ':
                self.winner = self.board[i]
                self.game_over = True
                return True
        # 检查列
        for i in range(3):
            if self.board[i] == self.board[i+3] == self.board[i+6] != ' ':
                self.winner = self.board[i]
                self.game_over = True
                return True
        # 检查对角线
        if self.board[0] == self.board[4] == self.board[8] != ' ':
            self.winner = self.board[0]
            self.game_over = True
            return True
        if self.board[2] == self.board[4] == self.board[6] != ' ':
            self.winner = self.board[2]
            self.game_over = True
            return True
        # 检查平局
        if ' ' not in self.board:
            self.game_over = True
            return True
        return False

class Gomoku(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        self.board = [['.' for _ in range(15)] for _ in range(15)]
        self.current_player = 'X'  # X 代表黑棋，O 代表白棋
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("五子棋")
        print("  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4")
        for i in range(15):
            row = f"{i%10} "
            for j in range(15):
                row += f"{self.board[i][j]} "
            print(row)
    
    def make_move(self, move):
        try:
            x, y = map(int, move.split())
            if 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == '.':
                self.board[x][y] = self.current_player
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                return True
            else:
                return False
        except:
            return False
    
    def check_winner(self):
        # 检查横、竖、斜四个方向
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for i in range(15):
            for j in range(15):
                if self.board[i][j] != '.':
                    for dx, dy in directions:
                        count = 1
                        # 检查正方向
                        x, y = i, j
                        while True:
                            x += dx
                            y += dy
                            if 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == self.board[i][j]:
                                count += 1
                            else:
                                break
                        # 检查反方向
                        x, y = i, j
                        while True:
                            x -= dx
                            y -= dy
                            if 0 <= x < 15 and 0 <= y < 15 and self.board[x][y] == self.board[i][j]:
                                count += 1
                            else:
                                break
                        if count >= 5:
                            self.winner = self.board[i][j]
                            self.game_over = True
                            return True
        return False

class ChineseChess(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        # 初始化棋盘
        # 红棋用大写字母，黑棋用小写字母
        self.board = [
            ['r', 'h', 'e', 'a', 'k', 'a', 'e', 'h', 'r'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', 'c', '.', '.', '.', '.', '.', 'c', '.'],
            ['p', '.', 'p', '.', 'p', '.', 'p', '.', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', '.', 'P', '.', 'P', '.', 'P', '.', 'P'],
            ['.', 'C', '.', '.', '.', '.', '.', 'C', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
            ['R', 'H', 'E', 'A', 'K', 'A', 'E', 'H', 'R']
        ]
        self.current_player = 'R'  # R 代表红方，B 代表黑方
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("中国象棋")
        print("  0 1 2 3 4 5 6 7 8")
        for i in range(10):
            row = f"{i} "
            for j in range(9):
                row += f"{self.board[i][j]} "
            print(row)
        print("红方: R H E A K A E H R")
        print("黑方: r h e a k a e h r")
        print("P/p: 兵/卒, C/c: 炮, H/h: 马, E/e: 相/象, A/a: 士/仕, K/k: 将/帅, R/r: 车")
    
    def make_move(self, move):
        # 简单实现，只处理基本移动
        try:
            # 输入格式：起始位置和目标位置，如 "0,0 1,2"
            start, end = move.split()
            start_x, start_y = map(int, start.split(','))
            end_x, end_y = map(int, end.split(','))
            
            piece = self.board[start_x][start_y]
            if piece == '.':
                return False
            
            # 检查是否是当前玩家的棋子
            if (self.current_player == 'R' and piece.islower()) or (self.current_player == 'B' and piece.isupper()):
                return False
            
            # 简单移动规则（实际象棋规则更复杂）
            self.board[start_x][start_y] = '.'
            self.board[end_x][end_y] = piece
            self.current_player = 'B' if self.current_player == 'R' else 'R'
            return True
        except:
            return False
    
    def check_winner(self):
        # 简单实现，检查将帅是否存在
        red_king = False
        black_king = False
        for i in range(10):
            for j in range(9):
                if self.board[i][j] == 'K':
                    red_king = True
                elif self.board[i][j] == 'k':
                    black_king = True
        
        if not red_king:
            self.winner = 'B'
            self.game_over = True
            return True
        elif not black_king:
            self.winner = 'R'
            self.game_over = True
            return True
        return False

class Othello(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        # 初始布局
        self.board[3][3] = 'O'
        self.board[3][4] = 'X'
        self.board[4][3] = 'X'
        self.board[4][4] = 'O'
        self.current_player = 'X'  # X 代表黑棋，O 代表白棋
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("黑白棋（奥赛罗）")
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            row = f"{i} "
            for j in range(8):
                row += f"{self.board[i][j]} "
            print(row)
        print("黑棋: X, 白棋: O")
    
    def is_valid_move(self, x, y):
        if self.board[x][y] != '.':
            return False
        
        directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        valid = False
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] != '.' and self.board[nx][ny] != self.current_player:
                # 找到对方棋子，继续检查
                while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] != '.' and self.board[nx][ny] != self.current_player:
                    nx += dx
                    ny += dy
                if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == self.current_player:
                    valid = True
                    break
        
        return valid
    
    def make_move(self, move):
        try:
            x, y = map(int, move.split())
            if 0 <= x < 8 and 0 <= y < 8 and self.is_valid_move(x, y):
                # 落子
                self.board[x][y] = self.current_player
                
                # 翻转对方棋子
                directions = [(0, 1), (1, 0), (1, 1), (1, -1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] != '.' and self.board[nx][ny] != self.current_player:
                        # 找到对方棋子，继续检查
                        temp = []
                        while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] != '.' and self.board[nx][ny] != self.current_player:
                            temp.append((nx, ny))
                            nx += dx
                            ny += dy
                        if 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx][ny] == self.current_player:
                            # 翻转棋子
                            for px, py in temp:
                                self.board[px][py] = self.current_player
                
                # 切换玩家
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                return True
            else:
                return False
        except:
            return False
    
    def check_winner(self):
        # 检查是否有空格
        has_empty = False
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == '.':
                    has_empty = True
                    break
            if has_empty:
                break
        
        if not has_empty:
            # 计算双方棋子数
            x_count = 0
            o_count = 0
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] == 'X':
                        x_count += 1
                    elif self.board[i][j] == 'O':
                        o_count += 1
            
            if x_count > o_count:
                self.winner = 'X'
            elif o_count > x_count:
                self.winner = 'O'
            # 平局
            self.game_over = True
            return True
        
        # 检查当前玩家是否有合法移动
        has_valid_move = False
        for i in range(8):
            for j in range(8):
                if self.is_valid_move(i, j):
                    has_valid_move = True
                    break
            if has_valid_move:
                break
        
        if not has_valid_move:
            # 切换玩家
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            # 检查新玩家是否有合法移动
            has_valid_move = False
            for i in range(8):
                for j in range(8):
                    if self.is_valid_move(i, j):
                        has_valid_move = True
                        break
                if has_valid_move:
                    break
            
            if not has_valid_move:
                # 游戏结束，计算棋子数
                x_count = 0
                o_count = 0
                for i in range(8):
                    for j in range(8):
                        if self.board[i][j] == 'X':
                            x_count += 1
                        elif self.board[i][j] == 'O':
                            o_count += 1
                
                if x_count > o_count:
                    self.winner = 'X'
                elif o_count > x_count:
                    self.winner = 'O'
                # 平局
                self.game_over = True
                return True
        
        return False

class Checkers(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        self.board = [['.' for _ in range(8)] for _ in range(8)]
        # 初始布局
        for i in range(3):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'X'  # X 代表黑棋
        for i in range(5, 8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    self.board[i][j] = 'O'  # O 代表白棋
        self.current_player = 'O'  # 白棋先行
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("跳棋")
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            row = f"{i} "
            for j in range(8):
                row += f"{self.board[i][j]} "
            print(row)
        print("黑棋: X, 白棋: O")
    
    def make_move(self, move):
        try:
            # 输入格式：起始位置和目标位置，如 "7,1 5,3"
            start, end = move.split()
            start_x, start_y = map(int, start.split(','))
            end_x, end_y = map(int, end.split(','))
            
            piece = self.board[start_x][start_y]
            if piece == '.' or (self.current_player == 'O' and piece != 'O') or (self.current_player == 'X' and piece != 'X'):
                return False
            
            # 检查移动是否合法
            dx = end_x - start_x
            dy = end_y - start_y
            
            # 普通移动
            if abs(dx) == 1 and abs(dy) == 1:
                if self.board[end_x][end_y] == '.':
                    # 检查是否是王棋
                    if (self.current_player == 'O' and end_x == 0) or (self.current_player == 'X' and end_x == 7):
                        self.board[end_x][end_y] = piece.upper()
                    else:
                        self.board[end_x][end_y] = piece
                    self.board[start_x][start_y] = '.'
                    self.current_player = 'X' if self.current_player == 'O' else 'O'
                    return True
            # 吃子移动
            elif abs(dx) == 2 and abs(dy) == 2:
                mid_x = (start_x + end_x) // 2
                mid_y = (start_y + end_y) // 2
                if self.board[mid_x][mid_y] != '.' and self.board[mid_x][mid_y] != piece and self.board[end_x][end_y] == '.':
                    # 检查是否是王棋
                    if (self.current_player == 'O' and end_x == 0) or (self.current_player == 'X' and end_x == 7):
                        self.board[end_x][end_y] = piece.upper()
                    else:
                        self.board[end_x][end_y] = piece
                    self.board[start_x][start_y] = '.'
                    self.board[mid_x][mid_y] = '.'
                    self.current_player = 'X' if self.current_player == 'O' else 'O'
                    return True
            
            return False
        except:
            return False
    
    def check_winner(self):
        # 检查是否有一方没有棋子
        x_count = 0
        o_count = 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 'X' or self.board[i][j] == 'X':
                    x_count += 1
                elif self.board[i][j] == 'O' or self.board[i][j] == 'O':
                    o_count += 1
        
        if x_count == 0:
            self.winner = 'O'
            self.game_over = True
            return True
        elif o_count == 0:
            self.winner = 'X'
            self.game_over = True
            return True
        
        return False

class TextAdventure(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        self.current_room = 'start'
        self.inventory = []
        self.game_over = False
        self.winner = None
        self.story = {
            'start': {
                'description': '你站在一个黑暗的房间里，面前有三个门：左、中、右。',
                'options': ['左', '中', '右']
            },
            'left': {
                'description': '你进入了一个书房，里面有一本书和一把钥匙。',
                'options': ['拿书', '拿钥匙', '返回']
            },
            'middle': {
                'description': '你进入了一个厨房，里面有食物和水。',
                'options': ['拿食物', '拿水', '返回']
            },
            'right': {
                'description': '你进入了一个卧室，里面有一张床和一个宝箱。',
                'options': ['打开宝箱', '睡觉', '返回']
            },
            'end': {
                'description': '恭喜你找到了宝藏！游戏结束。',
                'options': []
            }
        }
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("文字冒险游戏")
        print("=" * 50)
        print(self.story[self.current_room]['description'])
        print("\n物品栏:", self.inventory if self.inventory else "空")
        print("\n可用选项:")
        for i, option in enumerate(self.story[self.current_room]['options'], 1):
            print(f"{i}. {option}")
        print("=" * 50)
    
    def make_move(self, move):
        try:
            option_index = int(move) - 1
            options = self.story[self.current_room]['options']
            if 0 <= option_index < len(options):
                option = options[option_index]
                
                # 处理选项
                if self.current_room == 'start':
                    if option == '左':
                        self.current_room = 'left'
                    elif option == '中':
                        self.current_room = 'middle'
                    elif option == '右':
                        self.current_room = 'right'
                elif self.current_room == 'left':
                    if option == '拿书':
                        if '书' not in self.inventory:
                            self.inventory.append('书')
                            print("你拿起了书。")
                            time.sleep(1)
                    elif option == '拿钥匙':
                        if '钥匙' not in self.inventory:
                            self.inventory.append('钥匙')
                            print("你拿起了钥匙。")
                            time.sleep(1)
                    elif option == '返回':
                        self.current_room = 'start'
                elif self.current_room == 'middle':
                    if option == '拿食物':
                        if '食物' not in self.inventory:
                            self.inventory.append('食物')
                            print("你拿起了食物。")
                            time.sleep(1)
                    elif option == '拿水':
                        if '水' not in self.inventory:
                            self.inventory.append('水')
                            print("你拿起了水。")
                            time.sleep(1)
                    elif option == '返回':
                        self.current_room = 'start'
                elif self.current_room == 'right':
                    if option == '打开宝箱':
                        if '钥匙' in self.inventory:
                            self.current_room = 'end'
                            self.game_over = True
                            self.winner = '玩家'
                        else:
                            print("宝箱需要钥匙才能打开。")
                            time.sleep(1)
                    elif option == '睡觉':
                        print("你睡了一觉，恢复了体力。")
                        time.sleep(1)
                    elif option == '返回':
                        self.current_room = 'start'
                
                return True
            else:
                return False
        except:
            return False
    
    def check_winner(self):
        return self.game_over

class TextRPG(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        self.player = {
            'name': '冒险者',
            'hp': 100,
            'attack': 20,
            'defense': 10,
            'level': 1,
            'exp': 0
        }
        self.current_location = '村庄'
        self.monsters = {
            '哥布林': {'hp': 50, 'attack': 15, 'defense': 5, 'exp': 20},
            '狼人': {'hp': 80, 'attack': 25, 'defense': 10, 'exp': 40},
            '巨龙': {'hp': 200, 'attack': 50, 'defense': 20, 'exp': 100}
        }
        self.game_over = False
        self.winner = None
        self.locations = {
            '村庄': {
                'description': '这是一个宁静的村庄，有一个酒馆和一个商店。',
                'options': ['去酒馆', '去商店', '前往森林', '前往山洞']
            },
            '酒馆': {
                'description': '酒馆里有一些冒险者在喝酒聊天。',
                'options': ['休息', '打听消息', '返回村庄']
            },
            '商店': {
                'description': '商店里有各种装备和道具。',
                'options': ['购买装备', '出售物品', '返回村庄']
            },
            '森林': {
                'description': '森林里充满了危险，你遇到了一只哥布林！',
                'options': ['战斗', '逃跑', '返回村庄']
            },
            '山洞': {
                'description': '山洞里黑暗潮湿，你遇到了一只巨龙！',
                'options': ['战斗', '逃跑', '返回村庄']
            }
        }
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("文字角色扮演游戏")
        print("=" * 50)
        print(f"玩家: {self.player['name']}")
        print(f"等级: {self.player['level']}")
        print(f"生命值: {self.player['hp']}")
        print(f"攻击力: {self.player['attack']}")
        print(f"防御力: {self.player['defense']}")
        print(f"经验值: {self.player['exp']}")
        print(f"\n当前位置: {self.current_location}")
        print(self.locations[self.current_location]['description'])
        print("\n可用选项:")
        for i, option in enumerate(self.locations[self.current_location]['options'], 1):
            print(f"{i}. {option}")
        print("=" * 50)
    
    def make_move(self, move):
        try:
            option_index = int(move) - 1
            options = self.locations[self.current_location]['options']
            if 0 <= option_index < len(options):
                option = options[option_index]
                
                # 处理选项
                if self.current_location == '村庄':
                    if option == '去酒馆':
                        self.current_location = '酒馆'
                    elif option == '去商店':
                        self.current_location = '商店'
                    elif option == '前往森林':
                        self.current_location = '森林'
                    elif option == '前往山洞':
                        self.current_location = '山洞'
                elif self.current_location == '酒馆':
                    if option == '休息':
                        self.player['hp'] = 100
                        print("你休息了一下，恢复了生命值。")
                        time.sleep(1)
                    elif option == '打听消息':
                        print("你听到了一些关于附近怪物的消息。")
                        time.sleep(1)
                    elif option == '返回村庄':
                        self.current_location = '村庄'
                elif self.current_location == '商店':
                    if option == '购买装备':
                        self.player['attack'] += 5
                        self.player['defense'] += 5
                        print("你购买了一些装备，攻击力和防御力都提高了。")
                        time.sleep(1)
                    elif option == '出售物品':
                        print("你出售了一些物品，获得了金币。")
                        time.sleep(1)
                    elif option == '返回村庄':
                        self.current_location = '村庄'
                elif self.current_location == '森林':
                    if option == '战斗':
                        # 与哥布林战斗
                        monster = self.monsters['哥布林'].copy()
                        print("战斗开始！")
                        while monster['hp'] > 0 and self.player['hp'] > 0:
                            # 玩家攻击
                            damage = max(1, self.player['attack'] - monster['defense'])
                            monster['hp'] -= damage
                            print(f"你对哥布林造成了 {damage} 点伤害！")
                            time.sleep(0.5)
                            
                            if monster['hp'] <= 0:
                                print("你击败了哥布林！")
                                self.player['exp'] += monster['exp']
                                if self.player['exp'] >= 100:
                                    self.player['level'] += 1
                                    self.player['exp'] -= 100
                                    self.player['attack'] += 10
                                    self.player['defense'] += 5
                                    self.player['hp'] = 100
                                    print("你升级了！")
                                time.sleep(1)
                                break
                            
                            # 怪物攻击
                            damage = max(1, monster['attack'] - self.player['defense'])
                            self.player['hp'] -= damage
                            print(f"哥布林对你造成了 {damage} 点伤害！")
                            time.sleep(0.5)
                            
                            if self.player['hp'] <= 0:
                                print("你被击败了！")
                                self.game_over = True
                                time.sleep(1)
                                break
                    elif option == '逃跑':
                        print("你成功逃跑了！")
                        time.sleep(1)
                        self.current_location = '村庄'
                    elif option == '返回村庄':
                        self.current_location = '村庄'
                elif self.current_location == '山洞':
                    if option == '战斗':
                        # 与巨龙战斗
                        monster = self.monsters['巨龙'].copy()
                        print("战斗开始！")
                        while monster['hp'] > 0 and self.player['hp'] > 0:
                            # 玩家攻击
                            damage = max(1, self.player['attack'] - monster['defense'])
                            monster['hp'] -= damage
                            print(f"你对巨龙造成了 {damage} 点伤害！")
                            time.sleep(0.5)
                            
                            if monster['hp'] <= 0:
                                print("你击败了巨龙！")
                                print("你成为了传说中的英雄！")
                                self.game_over = True
                                self.winner = '玩家'
                                time.sleep(1)
                                break
                            
                            # 怪物攻击
                            damage = max(1, monster['attack'] - self.player['defense'])
                            self.player['hp'] -= damage
                            print(f"巨龙对你造成了 {damage} 点伤害！")
                            time.sleep(0.5)
                            
                            if self.player['hp'] <= 0:
                                print("你被击败了！")
                                self.game_over = True
                                time.sleep(1)
                                break
                    elif option == '逃跑':
                        print("你成功逃跑了！")
                        time.sleep(1)
                        self.current_location = '村庄'
                    elif option == '返回村庄':
                        self.current_location = '村庄'
                
                return True
            else:
                return False
        except:
            return False
    
    def check_winner(self):
        return self.game_over

class LinkGame(BoardGame):
    def __init__(self):
        super().__init__()
        self.reset()
    
    def reset(self):
        # 创建一个8x8的棋盘，使用字母A-P代表不同的图案
        import random
        patterns = list('ABCDEFGHIJKLMNOP') * 4
        random.shuffle(patterns)
        self.board = []
        for i in range(8):
            row = []
            for j in range(8):
                row.append(patterns[i*8 + j])
            self.board.append(row)
        self.selected = None
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("连连看")
        print("  0 1 2 3 4 5 6 7")
        for i in range(8):
            row = f"{i} "
            for j in range(8):
                row += f"{self.board[i][j]} "
            print(row)
        if self.selected:
            print(f"已选择: ({self.selected[0]}, {self.selected[1]}) - {self.board[self.selected[0]][self.selected[1]]}")
        print("输入坐标选择图案，如 '0 0'")
    
    def can_connect(self, x1, y1, x2, y2):
        # 检查两个点是否相同
        if self.board[x1][y1] != self.board[x2][y2]:
            return False
        if (x1, y1) == (x2, y2):
            return False
        
        # 检查是否可以直接连接（没有障碍物）
        if x1 == x2:
            # 同一行
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            for y in range(min_y + 1, max_y):
                if self.board[x1][y] != '.':
                    break
            else:
                return True
        elif y1 == y2:
            # 同一列
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            for x in range(min_x + 1, max_x):
                if self.board[x][y1] != '.':
                    break
            else:
                return True
        
        # 检查是否可以通过一个转折点连接
        # 第一个转折点
        if self.board[x1][y2] == '.':
            # 检查x1,y1到x1,y2是否畅通
            min_y = min(y1, y2)
            max_y = max(y1, y2)
            for y in range(min_y + 1, max_y):
                if self.board[x1][y] != '.':
                    break
            else:
                # 检查x1,y2到x2,y2是否畅通
                min_x = min(x1, x2)
                max_x = max(x1, x2)
                for x in range(min_x + 1, max_x):
                    if self.board[x][y2] != '.':
                        break
                else:
                    return True
        # 第二个转折点
        if self.board[x2][y1] == '.':
            # 检查x1,y1到x2,y1是否畅通
            min_x = min(x1, x2)
            max_x = max(x1, x2)
            for x in range(min_x + 1, max_x):
                if self.board[x][y1] != '.':
                    break
            else:
                # 检查x2,y1到x2,y2是否畅通
                min_y = min(y1, y2)
                max_y = max(y1, y2)
                for y in range(min_y + 1, max_y):
                    if self.board[x2][y] != '.':
                        break
                else:
                    return True
        
        return False
    
    def make_move(self, move):
        try:
            x, y = map(int, move.split())
            if 0 <= x < 8 and 0 <= y < 8 and self.board[x][y] != '.':
                if not self.selected:
                    # 第一次选择
                    self.selected = (x, y)
                    return True
                else:
                    # 第二次选择
                    x1, y1 = self.selected
                    if self.can_connect(x1, y1, x, y):
                        # 连接成功，移除两个图案
                        self.board[x1][y1] = '.'
                        self.board[x][y] = '.'
                        self.selected = None
                        return True
                    else:
                        # 连接失败，重新选择
                        self.selected = (x, y)
                        return True
            else:
                return False
        except:
            return False
    
    def check_winner(self):
        # 检查是否所有图案都被消除
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != '.':
                    return False
        
        self.game_over = True
        self.winner = '玩家'
        return True

class MoyuGameManager:
    def __init__(self):
        self.games = {
            '井字棋': TicTacToe(),
            '五子棋': Gomoku(),
            '象棋': ChineseChess(),
            '黑白棋': Othello(),
            '跳棋': Checkers(),
            '文字冒险游戏': TextAdventure(),
            '文字角色扮演游戏': TextRPG(),
            '连连看': LinkGame()
        }
        self.current_game = None
    
    def start_game(self, game_name):
        if game_name in self.games:
            self.current_game = self.games[game_name]
            self.current_game.reset()
            return True
        return False
    
    def play_game(self):
        if not self.current_game:
            return False
        
        while not self.current_game.game_over:
            self.current_game.display_board()
            if hasattr(self.current_game, 'current_player'):
                print(f"当前玩家: {self.current_game.current_player}")
            
            move = input("请输入移动 (输入'退出'结束游戏): ")
            if move == '退出':
                break
            
            if self.current_game.make_move(move):
                self.current_game.check_winner()
            else:
                print("无效的移动，请重试")
                time.sleep(1)
        
        if self.current_game.game_over:
            self.current_game.display_board()
            if self.current_game.winner:
                print(f"游戏结束，获胜者: {self.current_game.winner}")
            else:
                print("游戏结束，平局")
            time.sleep(2)
        
        self.current_game = None
        return True