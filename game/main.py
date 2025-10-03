from flow_free import FlowFree, FlowFreeBoard
from player import HumanPlayer

if __name__ == '__main__':
    
    game = FlowFree()
    player = HumanPlayer()
    game.app(player)