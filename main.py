from game.flow_free import FlowFree
from game.player import HumanPlayer

if __name__ == '__main__':
    
    game = FlowFree()
    player = HumanPlayer()
    game.app(player)