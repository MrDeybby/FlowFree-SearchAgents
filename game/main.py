from flow_free import FlowFree, FlowFreeBoard
from player import HumanPlayer

if __name__ == '__main__':
    
    # board = FlowFreeBoard("levels/7x7_4C_1.txt")
    # game = FlowFree(board)
    # player = HumanPlayer()
    # game.play(player=player)
    
    game = FlowFree()
    
    player = HumanPlayer()
    game.app(player)