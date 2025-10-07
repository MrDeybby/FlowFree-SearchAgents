from game.flow_free import FlowFree, FlowFreeBoard
from game.player import HumanPlayer
if __name__ == '__main__':
    
    game = FlowFree()
    # player = HumanPlayer()
    # # player = BFSPlayer(show_steps=True)
    # board = FlowFreeBoard("levels/5x5_4C_1.txt")
    # game.board = board
    # game.play(player=player)
    game.app()