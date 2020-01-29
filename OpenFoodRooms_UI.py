"""Database connexion"""

"""User Interface that using database data"""

"""Display options"""

print("\nBonjour ! Bienvenue sur OpenFoodRooms !\n")

print("Attention, certains produits sont incomplets")
print("Leurs données ne sont donc pas fiables.\n")
print("Choisissez une option en entrant le nombre associé à celle-ci\n")

"""Choice of one item"""

print(" 1. Quelle catégorie d'aliment souhaitez-vous remplacer ?\n",
      "2. Retrouver mes aliments substitués\n")

entry = input("Quelle option choisissez-vous ? ")
while True:
    try:
        entry = int(entry)
        assert entry > 0 and entry < 3
        break
    except ValueError:
        print(" 1. Quel aliment souhaitez-vous remplacer ?\n",
              "2. Retrouver mes aliments substitués\n")

        entry = input("Quelle option choisissez-vous ? ")
    except AssertionError:
        print(" 1. Quel aliment souhaitez-vous remplacer ?\n",
              "2. Retrouver mes aliments substitués\n")

        entry = input("Quelle option choisissez-vous ? ")
print("Vous avez choisi l'option ", entry)


"""Choice 1 : display food"""
if entry == 1:
    for i in range(10):
        print(i, " : ")

"""Ask database better product"""

"""Storage product and substitute in 'favoris'"""

"""Display result of actual research"""

"""Choice 2 : display ancient researches and result"""

"""Ask database to show ancient researches"""
# elif:
#     print("champs de la table recherche et noms des aliments via les id")
