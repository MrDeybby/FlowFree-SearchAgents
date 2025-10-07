from game.flow_free import FlowFree
from game.player import HumanPlayer
from algorithms.astar import AStarPlayer
from algorithms.bfs import BFSPlayer
from algorithms.dfs import DFSPlayer

if __name__ == '__main__':
    
    game = FlowFree()
    #player = DFSPlayer()
    player = AStarPlayer()
    #player = BFSPlayer()
    #player = HumanPlayer()
    game.app(player)