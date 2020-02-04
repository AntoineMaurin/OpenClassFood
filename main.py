"""User Interface"""
import datetime

from database.database_interaction import DatabaseInteraction

#Database connexion
interact = DatabaseInteraction()

print("\nBonjour ! Bienvenue sur OpenFoodRooms !\n")

# Display informations
print("Attention, certains produits sont incomplets")
print("Leurs données ne sont donc pas fiables.\n")
print("Choisissez une option en entrant le nombre associé à celle-ci\n")

# Display options
print(" 1. Choisir une catégorie d'aliment que vous souhaitez remplacer\n",
      "2. Retrouver mes aliments substitués\n")

# This function makes sure the input is convertible to an int and
# between the min and max
def ask_safely(question, min, max):
    response = input(question)
    while True:
        try:
            response = int(response)
            assert response >= min and response <= max
            break
        except:
            response = input(question)
    return response

# Asking safely the first question
response = ask_safely("Quelle option choisissez-vous ? ", 1, 2)

# Option 1
if response == 1:
    category_choices = []
    # display categories
    for id, category in enumerate(interact.get_categories()):
        category_choices.append((id, category[0]))
        print(id, "-", category)
    response = ask_safely("\nQuelle catégorie choisissez-vous ? ", 0, 9)
    for elt in category_choices:
        if elt[0] == response :
            chosen_category = elt[1]
            print('\nCatégorie choisie  : ', chosen_category, "\n")

    products_choices = []
    # display products inside category
    for id, product in enumerate(interact.get_products_from_category(chosen_category)):
        products_choices.append((id, product[0], product[1], product[2]))
        if id > 10:
            break
        print(id, "-", product[1:])
    response = ask_safely("\nChoisissez un aliment ", 0, 10)

    for elt in products_choices:
        if elt[0] == response :
            chosen_product_id = elt[1]
            chosen_product_name = elt[2]
            chosen_product_nutriscore = elt[3]

    # Ask database better product and display result of actual research
    substitute = interact.get_substitute(chosen_product_name)
    print("\n", substitute)
    substitute_id = substitute[0]

#Storage product and substitute in 'favoris'
    interact.add_research(chosen_product_id, substitute_id)

#Choice 2 : display ancient researches and result
else:
    interact.display_researches()
