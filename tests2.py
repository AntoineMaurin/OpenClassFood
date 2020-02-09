"""User Interface"""
import datetime

from database.ui_interaction import UiInteraction
from database.database_populating import DatabasePopulating

#Database connexion
interact = UiInteraction()
db_pop = DatabasePopulating()
# Display informations and options choice
print("\nBonjour ! Bienvenue sur OpenFoodRooms !\n"
      "Attention, certains produits sont incomplets "
      "Leurs données ne sont donc pas fiables.\n"
      "\nChoisissez une option en entrant le nombre associé à celle-ci\n"
      "\n0. Choisir une catégorie d'aliment que vous souhaitez remplacer\n"
      "1. Voir mes aliments substitués\n")

# This function makes sure the input is convertible to an int and
# between the min and max
def ask_safely(question, max):
    response = input(question)
    while True:
        try:
            response = int(response)
            assert response >= 0 and response <= max
            break
        except:
            response = input(question)
    return response

def display_correctly(iterable):
    choices = []
    for id, elt in enumerate(iterable):
        choices.append((id, elt))
        print(id, elt.name, sep=' | ')
        if id > 10:
            break
    return choices

def get_response(choices, response):
    for elt in choices:
        if elt[0] == response :
            chosen = elt[1]
    return chosen

# Asking safely the first question
response = ask_safely("Quelle option choisissez-vous ? ", 1)

# Option 1
if response == 0:
    # display categories
    choices = display_correctly(interact.get_categories())
    # ask for the category choice
    response = ask_safely("\nQuelle catégorie choisissez-vous ? ", 9)
    chosen_category = get_response(choices, response)
    print('\nCatégorie choisie  : ', chosen_category.name, "\n")

    # display products inside category
    choices = display_correctly(interact.get_products(chosen_category))
    response = ask_safely("\nChoisissez un aliment ", 11)
    chosen_product = get_response(choices, response)
    # print('\nProduit choisi  : ', chosen_product.name, "\n")
    print("\nProduit choisi : \n", chosen_product.name, chosen_product.nutriscore,
          chosen_product.stores, chosen_product.url, sep=' | ')

    # Ask database better product and display result of actual research
    substitute = interact.get_substitute(chosen_product)
    print("\nSubstitut : \n", substitute.name, substitute.nutriscore,
          substitute.stores, substitute.url, sep=' | ')

    # Storage product and substitute in 'favoris'
    db_pop.add_research(chosen_product.id, substitute.id)

    #Choice 2 : display ancient researches and result
else:
    db_pop.display_researches()
