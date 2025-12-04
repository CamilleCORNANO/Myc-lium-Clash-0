def get_int_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            return int(user_input)    
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre entier.")

def get_float_input(prompt):
    while True:
        user_input = input(prompt)
        try:
            return float(user_input)    
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre décimal.")
            
