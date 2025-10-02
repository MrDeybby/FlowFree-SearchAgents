from control import Control
import os
from color import Color
class Menu:
    
    CONTROL_SELECTIONS = {'W':-1, 'S':1, 'ENTER':'ENTER'}
    
    def __init__(self, sections:list, menu_name='Menu') -> None:
        self.menu_sections = sections
        self.menu_name = menu_name
        self.control = Control().select
    
    def select(self) -> int:
        os.system('cls')
        
        position = 0
        
        while True:
            print('' + '='*5 + f' {self.menu_name} ' + '='*5)
            for i in range(len(self.menu_sections)):


                if i == position:
                    print(f'> {Color.RED}{self.menu_sections[i]}{Color.RESET} <')
                else:   
                    print(self.menu_sections[i])
            
            print('Presiona una tecla [W] [S] [ENTER])')
                
            selected = self.control(self.CONTROL_SELECTIONS)
            if selected == 'ENTER':
                return position
            else:
                position += selected
                if position < 0: position = 0
                if position >= len(self.menu_sections): position = len(self.menu_sections)-1
            os.system('cls')
            
if __name__ == '__main__':
    pass
    b = Menu(['Jugar', 'Opciones', 'Salir'], menu_name='Numari')
    b.select()