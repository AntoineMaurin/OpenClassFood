"""User Interface"""


from database.ui_interaction import UiInteraction
from database.database_populating import DatabasePopulating


# This function makes sure the input is convertible to an int and
# between 0 and the max set
def ask_safely(question, max):
    response = input(question)
    while True:
        try:
            response = int(response)
            assert response >= 1 and response <= max
            break
        except ValueError:
            response = input(question)
    return response


# This function displays the name each element of an iterable separated
# with a | symbol
def display_correctly(iterable):
    choices = []
    for id, elt in enumerate(iterable):
        id += 1
        choices.append((id, elt))
        print(id, elt.name, sep=' | ')
        if id > 11:
            break
    return choices


# This function returns the element bound to the number entered by user
def get_response(choices, response):
    for elt in choices:
        if elt[0] == response:
            chosen = elt[1]
    return chosen


def main():
    # Database and models connexion
    interact = UiInteraction()
    db_pop = DatabasePopulating()
    # Display informations and options choice
    print("\nBonjour ! Bienvenue sur OpenFoodRooms !\n"
          "Attention, certains produits sont incomplets "
          "Leurs données ne sont donc pas fiables.\n"
          "\nChoisissez une option en entrant le nombre associé à celle-ci\n"
          "\n1. Choisir une catégorie d'aliment que vous souhaitez remplacer\n"
          "2. Voir mes aliments substitués\n")

    # Asking safely the first question
    response = ask_safely("Quelle option choisissez-vous ? ", 2)

    # Option 1
    if response == 1:
        # display categories
        choices = display_correctly(interact.get_categories())
        # ask for the category choice
        response = ask_safely("\nQuelle catégorie choisissez-vous ? ", 10)
        chosen_category = get_response(choices, response)
        print('\nCatégorie choisie  : ', chosen_category.name, "\n")

        # display products inside category
        choices = display_correctly(interact.get_products(chosen_category))
        response = ask_safely("\nChoisissez un aliment ", 12)
        chosen_product = get_response(choices, response)
        # print('\nProduit choisi  : ', chosen_product.name, "\n")
        print("\nProduit choisi : \n", chosen_product.name,
              chosen_product.nutriscore, chosen_product.description,
              chosen_product.stores, chosen_product.url, sep=' | ')

        # Ask database better product and display result of actual research
        substitute = interact.get_substitute(chosen_product)
        print("\nSubstitut : \n", substitute.name, substitute.nutriscore,
              substitute.description, substitute.stores, substitute.url,
              sep=' | ')

        # Storage product and substitute in 'favoris'
        db_pop.add_research(chosen_product.id, substitute.id)

        # Choice 2 : display ancient researches and result
    else:
        db_pop.display_researches()


if __name__ == '__main__':
    main()
