from game.flow_free import FlowFree
from game.player import HumanPlayer
from algorithms.astar import AStarPlayer

if __name__ == '__main__':
    
    game = FlowFree()
    player = HumanPlayer()
    player = AStarPlayer()
    game.app(player)