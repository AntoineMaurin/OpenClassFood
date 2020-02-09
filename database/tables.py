TABLES = {}

TABLES['categorie'] = (
    "CREATE TABLE IF NOT EXISTS `categorie` ("
    "  `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `nom` VARCHAR(50) UNIQUE,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['aliment'] = (
    "CREATE TABLE IF NOT EXISTS `aliment` ("
    "  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `nom` VARCHAR(250),"
    "  `nutriscore` CHAR(1),"
    "  `description` TEXT,"
    "  `magasin` TEXT,"
    "  `lien_openfoodfacts` TEXT,"
    "  `id_categorie` MEDIUMINT UNSIGNED NOT NULL DEFAULT 1,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['recherche'] = (
    "CREATE TABLE IF NOT EXISTS `recherche` ("
    "  `id` MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,"
    "  `date` DATETIME NOT NULL,"
    "  `id_aliment` INT UNSIGNED NOT NULL,"
    "  `id_substitut` INT UNSIGNED NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
