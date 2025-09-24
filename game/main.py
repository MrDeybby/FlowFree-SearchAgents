from flow_free import FlowFree, FlowFreeBoard
from player import HumanPlayer

if __name__ == '__main__':
    
    board = FlowFreeBoard("levels/5_x_5_4C_1.txt")
    game = FlowFree(board)
    player = HumanPlayer()
    game.play(player=player)