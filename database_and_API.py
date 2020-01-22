import requests
import json

#List des urls sur lesquelles je vais chercher les données
urls = ['https://fr.openfoodfacts.org/categorie/citronnades.json',
        'https://fr.openfoodfacts.org/categorie/chocolats-noirs-aux-feves-de-cacao.json',]
        # 'https://fr.openfoodfacts.org/categorie/pizzas-a-la-bolognaise.json',
        # 'https://fr.openfoodfacts.org/categorie/liegeois.json']


headers = {'User-Agent' : 'OpenFoodRooms - windows/mac - Version 1.0'}

biglist = []

i = 0
while True:
    i += 1
    #looping on multiple pages
    for url in urls:
        url = (url[:-5] + '/' + str(i))
        incremented_url = url + '.json'
        print('url : ', incremented_url)

        try:
            response = requests.get(incremented_url, headers=headers)
            print(response.status_code)
            assert response.status_code < 400
        except AssertionError:
            print("An error has occured")
            break
        else:
            pass

        json_response = json.loads(response.text)
        data = json_response["products"]
        for elt in data:
            try :

                print('product_name_fr : ', elt["product_name_fr"])
                print('description : ', elt["generic_name_fr"])
                print('nutrition_score : ', elt["nutrition_grade_fr"])
                print('stores : ', elt["stores"])
                print('url : ', elt["url"])

                biglist.append(list((elt["product_name_fr"],
                           elt["generic_name_fr"],
                           elt["nutrition_grade_fr"],
                           elt["stores"],
                           elt["url"])))

            except KeyError:
                print('product_name_fr : ', '')
                print('description : ', '')
                print('nutrition_score : ', '')
                print('stores : ', '')
                print('url : ', '')
                biglist.append("")
                
    if json_response["products"] == []:
        print(json_response["products"])
        break

for elt in biglist:
    print(elt)

print('finished !')
