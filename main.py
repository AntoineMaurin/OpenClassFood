"""User Interface"""

from client_interaction.client_interface import ClientInterface
from database.database_populating import DatabasePopulating
from models.category import Category


def main():

    db_pop = DatabasePopulating()
    interact = ClientInterface()

    print("\nBonjour ! Bienvenue sur OpenFoodRooms !\n"
          "Attention, certains produits sont incomplets "
          "Leurs données ne sont donc pas fiables.\n"
          "\nChoisissez une option en entrant le nombre associé à celle-ci\n")

    while True:
        print("1. Choisir une catégorie d'aliment que je souhaite remplacer\n"
              "2. Voir mes aliments substitués\n")

        # Asking safely the first question
        response = interact.ask_safely("Quelle option choisissez-vous ? ", 2)

        # Option 1
        if response == 1:

            categories = Category.get_all()
            choices = interact.display_correctly(categories)

            response = interact.ask_safely(
                                "\nQuelle catégorie choisissez-vous ? ", 10)
            chosen_category = interact.get_response(choices, response)
            print('\nCatégorie choisie  : ', chosen_category.name, "\n")

            products = chosen_category.get_products()
            choices = interact.display_correctly(products)
            response = interact.ask_safely("\nChoisissez un aliment ", 12)
            chosen_product = interact.get_response(choices, response)
            # print('\nProduit choisi  : ', chosen_product.name, "\n")
            print("\nProduit choisi : \n", chosen_product.name,
                  chosen_product.nutriscore, chosen_product.description,
                  chosen_product.stores, chosen_product.url, sep=' | ')

            # Ask database better product and display result of actual research
            substitute = chosen_product.get_substitute()
            print("\nSubstitut : \n", substitute.name, substitute.nutriscore,
                  substitute.description, substitute.stores, substitute.url,
                  sep=' | ')

            # Storage product and substitute in 'favoris'
            final_choice = interact.ask_safely("\n1. Oui"
                                               "\n2. Non\n"
                                               "\nEnregistrer la recherche ? ",
                                               2)
            if final_choice == 1:
                db_pop.add_research(chosen_product.id, substitute.id)
            else:
                print("Recherche non enregistrée")

            if interact.quit_or_not():
                break

        else:
            db_pop.display_researches()
            if interact.quit_or_not():
                break


if __name__ == '__main__':
    main()
