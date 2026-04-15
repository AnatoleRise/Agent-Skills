#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摸鱼Skill测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.moyu_games import TicTacToe, Gomoku, ChineseChess, Othello, Checkers, TextAdventure, TextRPG, LinkGame

def test_tic_tac_toe():
    """测试井字棋游戏"""
    print("测试井字棋游戏...")
    game = TicTacToe()
    
    # 测试横向获胜
    print("测试横向获胜...")
    game.board = ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
    assert game.check_winner() == True
    assert game.winner == 'X'
    print("✓ 横向获胜测试通过")
    
    # 测试纵向获胜
    print("测试纵向获胜...")
    game.reset()
    game.board = ['X', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ']
    assert game.check_winner() == True
    assert game.winner == 'X'
    print("✓ 纵向获胜测试通过")
    
    # 测试斜向获胜
    print("测试斜向获胜...")
    game.reset()
    game.board = ['X', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X']
    assert game.check_winner() == True
    assert game.winner == 'X'
    print("✓ 斜向获胜测试通过")
    
    # 测试平局
    print("测试平局...")
    game.reset()
    game.board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
    assert game.check_winner() == True
    assert game.winner is None
    print("✓ 平局测试通过")
    
    # 测试落子
    print("测试落子...")
    game.reset()
    assert game.make_move('1') == True
    assert game.board[0] == 'X'
    assert game.current_player == 'O'
    print("✓ 落子测试通过")
    
    print("井字棋测试完成！\n")

def test_gomoku():
    """测试五子棋游戏"""
    print("测试五子棋游戏...")
    game = Gomoku()
    
    # 测试横向获胜
    print("测试横向获胜...")
    for i in range(5):
        game.board[7][5+i] = 'X'
    assert game.check_winner() == True
    assert game.winner == 'X'
    print("✓ 横向获胜测试通过")
    
    # 测试纵向获胜
    print("测试纵向获胜...")
    game.reset()
    for i in range(5):
        game.board[5+i][7] = 'X'
    assert game.check_winner() == True
    assert game.winner == 'X'
    print("✓ 纵向获胜测试通过")
    
    # 测试正斜线获胜
    print("测试正斜线获胜...")
    game.reset()
    for i in range(5):
        game.board[5+i][5+i] = 'X'
    assert game.check_winner() == True
    assert game.winner == 'X'
    print("✓ 正斜线获胜测试通过")
    
    # 测试反斜线获胜
    print("测试反斜线获胜...")
    game.reset()
    for i in range(5):
        game.board[5+i][9-i] = 'X'
    assert game.check_winner() == True
    assert game.winner == 'X'
    print("✓ 反斜线获胜测试通过")
    
    # 测试落子
    print("测试落子...")
    game.reset()
    assert game.make_move('7 7') == True
    assert game.board[7][7] == 'X'
    assert game.current_player == 'O'
    print("✓ 落子测试通过")
    
    print("五子棋测试完成！\n")

def test_chinese_chess():
    """测试象棋游戏"""
    print("测试象棋游戏...")
    game = ChineseChess()
    
    # 测试落子
    print("测试落子...")
    assert game.make_move('9,4 8,4') == True
    assert game.board[9][4] == '.'
    assert game.board[8][4] == 'K'
    assert game.current_player == 'B'
    print("✓ 落子测试通过")
    
    # 测试获胜检测
    print("测试获胜检测...")
    game.reset()
    game.board[9][4] = '.'  # 移除红方将帅
    assert game.check_winner() == True
    assert game.winner == 'B'
    print("✓ 获胜检测测试通过")
    
    print("象棋测试完成！\n")

def test_othello():
    """测试黑白棋游戏"""
    print("测试黑白棋游戏...")
    game = Othello()
    
    # 测试初始布局
    assert game.board[3][3] == 'O'
    assert game.board[3][4] == 'X'
    assert game.board[4][3] == 'X'
    assert game.board[4][4] == 'O'
    print("✓ 初始布局测试通过")
    
    # 测试落子
    print("测试落子...")
    # 测试合法落子
    assert game.make_move('2 3') == True
    print("✓ 落子测试通过")
    
    print("黑白棋测试完成！\n")

def test_checkers():
    """测试跳棋游戏"""
    print("测试跳棋游戏...")
    game = Checkers()
    
    # 测试初始布局
    assert game.board[5][0] == 'O'  # (5+0)%2=1，符合条件
    assert game.board[0][1] == 'X'  # (0+1)%2=1，符合条件
    print("✓ 初始布局测试通过")
    
    # 测试落子
    print("测试落子...")
    # 测试合法移动 - 从第5行移动到第4行（空白行）
    assert game.make_move('5,0 4,1') == True  # 从(5,0)移动到(4,1)
    print("✓ 落子测试通过")
    
    print("跳棋测试完成！\n")

def test_text_adventure():
    """测试文字冒险游戏"""
    print("测试文字冒险游戏...")
    game = TextAdventure()
    
    # 测试初始状态
    assert game.current_room == 'start'
    assert len(game.inventory) == 0
    print("✓ 初始状态测试通过")
    
    # 测试选择选项
    print("测试选择选项...")
    assert game.make_move('1') == True  # 选择左门
    assert game.current_room == 'left'
    print("✓ 选择选项测试通过")
    
    print("文字冒险游戏测试完成！\n")

def test_text_rpg():
    """测试文字角色扮演游戏"""
    print("测试文字角色扮演游戏...")
    game = TextRPG()
    
    # 测试初始状态
    assert game.player['name'] == '冒险者'
    assert game.current_location == '村庄'
    print("✓ 初始状态测试通过")
    
    # 测试选择选项
    print("测试选择选项...")
    assert game.make_move('1') == True  # 去酒馆
    assert game.current_location == '酒馆'
    print("✓ 选择选项测试通过")
    
    print("文字角色扮演游戏测试完成！\n")

def test_link_game():
    """测试连连看游戏"""
    print("测试连连看游戏...")
    game = LinkGame()
    
    # 测试初始状态
    assert len(game.board) == 8
    assert len(game.board[0]) == 8
    print("✓ 初始状态测试通过")
    
    # 测试选择图案
    print("测试选择图案...")
    assert game.make_move('0 0') == True  # 选择第一个图案
    assert game.selected == (0, 0)
    print("✓ 选择图案测试通过")
    
    print("连连看测试完成！\n")

def main():
    print("开始测试摸鱼Skill...\n")
    
    try:
        test_tic_tac_toe()
        test_gomoku()
        test_chinese_chess()
        test_othello()
        test_checkers()
        test_text_adventure()
        test_text_rpg()
        test_link_game()
        print("所有测试通过！摸鱼Skill功能正常。")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()