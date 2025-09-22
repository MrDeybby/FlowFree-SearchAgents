import keyboard
import time
class Control:
    
    @staticmethod
    def select(selections:dict) -> any:
        if not selections:
            raise ValueError("El diccionario 'selections' no puede estar vacío")
        
        buttons = [k.upper() for k in selections.keys()] # When we push a key the program read it as a upper key
        
        while True:
            key = keyboard.read_key(suppress=True).upper()
            time.sleep(0.2)
            
            if key in buttons:
                return selections[key]
        

if __name__ == '__main__':
   if Control.select({'W':'UP', 'S':'DOWN', 'A':'LEFT', 'ESC':'SALIR'}) == 'SALIR':
        print('Salir')
   else:
        print('Continuar')

 