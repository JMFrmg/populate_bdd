import os
import csv
import time
import sqlite3

from sql_tables import CREATE_TABLES


CSV_PATH = "./csv_data/orders.csv"  # Path du fichier CSV

# Contrôle de l'existence du dossier database
if not os.path.exists("./database"):  
    os.makedirs("./database")

# Suppression de la base de données si elle existe    
if os.path.exists("./database/data.db"):  
    os.remove("./database/data.db")

# Création des objects connexion et cursor de sqlite
connexion = sqlite3.connect("./database/data.db")
cursor = connexion.cursor()

# Création des tables dans la base de données
for sql_command in CREATE_TABLES.values():
    cursor.execute(sql_command)


tables_data = {
        "customer": {},
        "product": {},
        "customer_order": {},
        "order_detail": {}
    }

with open(CSV_PATH, newline='') as f:
    print(f"\nExtraction des données...")
    reader = csv.reader(f, delimiter=';')
    reader.__next__()  # Permet de zapper la première ligne du CSV (celle avec les colonnes)
    for row in reader:
        # A chaque itération, row contient les données d'une ligne du fichier CSV sous forme de liste
        if row[3] not in tables_data["customer"]:
            tables_data["customer"][row[3]] = [row[3], row[4]]
        if row[7] not in tables_data["product"]:
            description = row[8].replace("'", " ").replace('"', '')  # Les "," dans la colonne description posaient problème dans les requêtes SQL. Elles sont supprimées.
            tables_data["product"][row[7]] = [row[7], description, row[9]]
        if row[0] not in tables_data["customer_order"]:
            tables_data["customer_order"][row[0]] = [row[0], row[1], row[2], row[3]]
        if row[5] not in tables_data["order_detail"]:
            tables_data["order_detail"][row[5]] = [row[5], row[6], row[0], row[7]]

for table_name, data in tables_data.items():
    # table_name : nom de la table
    # data : lignes de cette table
    print(f"{table_name} : {len(data)} lignes.")  # On affiche le nombre de ligne par table

# Dictionnaire avec en clé chaque table, et en valeur la liste des colonnes de cette table
# Permet de retrouver les noms des colonnes de chaque table dans la boucle d'insertion des données ci-dessous
TABLE_COLUMNS = {
    "customer": ["id", "country"],
    "product": ["id", "description", "price"],
    "customer_order": ["id", "invoice_nb", "invoice_date", "customer_id"],
    "order_detail": ["id", "quantity", "order_id", "product_id"]
}

errors = 0
inserted = 0

# Insertion des données dans la base de données SQL
for table_name, data in tables_data.items(): # On boucle sur les tables
    for row_id, row_data in data.items():  # On boucle sur les lignes
        # A chaque itération :
            # row_id : id de la ligne
            # row_data : données de la ligne (type list)
        # Création de la requête SQL sous forme de chaîne de caractères
        sql_command = f"""INSERT INTO {table_name} ('{"', '".join(TABLE_COLUMNS[table_name])}') VALUES ('{"', '".join(row_data)}')"""
        try:
            cursor.execute(sql_command)
            inserted += 1
        except Exception as e:
            print(sql_command)
            print(e)
            errors += 1
    connexion.commit()

connexion.close()

print(f"{inserted} lignes insérées dans la base de données sql avec {errors} erreurs.")  # Affichage des résultats
