# game/base_player.py

from abc import ABC, abstractmethod

class Player(ABC):
    
    @abstractmethod
    def play(self):
        pass