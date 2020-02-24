"""This class methods are used in the main program to make the user
interactions easier"""


class ClientInterface:

    def __init__(self):
        pass

    def ask_safely(self, question, max):
        response = input(question)
        while True:
            try:
                response = int(response)
                assert response >= 1 and response <= max
                break
            except AssertionError:
                response = input(question)
            except ValueError:
                response = input(question)
        return response

    def display_correctly(self, iterable):
        choices = []
        for id, elt in enumerate(iterable):
            id += 1
            choices.append((id, elt))
            print(id, elt.name, sep=' | ')
        return choices

    def get_response(self, choices, response):
        for elt in choices:
            if elt[0] == response:
                chosen = elt[1]
        return chosen

    def quit_or_not(self):
        quit_or_not = self.ask_safely("\n1. Accueil"
                                      "\n2. Quitter\n"
                                      "\nRetour à l'accueil ou quitter ? ",
                                      2)
        if quit_or_not == 1:
            print("\nRetour à l'accueil\n")
            return False
        else:
            print("\nFermeture du programme")
            return True
