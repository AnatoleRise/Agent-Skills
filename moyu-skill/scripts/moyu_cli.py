#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
摸鱼Skill - 文本游戏CLI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.moyu_games import MoyuGameManager

def main():
    game_manager = MoyuGameManager()
    
    print("欢迎使用摸鱼Skill！")
    print("支持的游戏：井字棋、五子棋、象棋")
    print("输入'玩 [游戏名称]'开始游戏，输入'退出'结束")
    
    while True:
        user_input = input("请输入指令: ")
        
        if user_input == '退出':
            print("再见！")
            break
        elif user_input.startswith('玩 '):
            game_name = user_input[2:].strip()
            if game_manager.start_game(game_name):
                game_manager.play_game()
            else:
                print(f"不支持的游戏: {game_name}")
                print("支持的游戏：井字棋、五子棋、象棋")
        else:
            print("无效指令，请输入'玩 [游戏名称]'或'退出'")

if __name__ == "__main__":
    main()