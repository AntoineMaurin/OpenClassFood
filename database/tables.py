TABLES = {}

TABLES['recherche'] = (
    "CREATE TABLE IF NOT EXISTS `recherche` ("
    "  `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `date` DATETIME NOT NULL,"
    "  `id_produit` INT UNSIGNED NOT NULL,"
    "  `id_substitut` INT UNSIGNED NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['produit'] = (
    "CREATE TABLE IF NOT EXISTS `produit` ("
    "  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `nom` VARCHAR(250),"
    "  `nutriscore` CHAR(1),"
    "  `description` TEXT,"
    "  `magasin` TEXT,"
    "  `lien_openfoodfacts` TEXT,"
    "  `id_categorie` MEDIUMINT UNSIGNED NOT NULL DEFAULT 0,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['categorie'] = (
    "CREATE TABLE IF NOT EXISTS `categorie` ("
    "  `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `nom` VARCHAR(50) UNIQUE,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
