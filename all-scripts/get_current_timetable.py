import datetime
from datetime import datetime, date, timedelta
import openpyxl
import os
import pronotepy
import configparser
import getpass
import pandas as pd  # For export to Excel
from fpdf import FPDF  # For export to PDF
from tabulate import tabulate
from pronotepy.ent import (
    cas_arsene76,
    cas_ent27,
    cas_kosmos,
    ent_creuse,
    occitanie_montpellier,
    val_doise,
    val_de_marne,
    cas_cybercolleges42_edu,
    ecollege_haute_garonne_edu,
    ac_orleans_tours,
    ac_poitiers,
    ac_reunion,
    cas_agora06,
    cas_seinesaintdenis_edu,
    eclat_bfc,
    ent_auvergnerhonealpe,
    laclasse_educonnect,
    monbureaunumerique,
    ent77,
    ent_ecollege78,
    ent_essonne,
    ent_mayotte,
    ile_de_france,
    neoconnect_guadeloupe,
    paris_classe_numerique,
    lyceeconnecte_aquitaine,
    ent_94,
    ent_hdf,
    ent_var,
    l_normandie,
    lyceeconnecte_edu,
    ent_elyco,
    bordeaux,
    atrium_sud,
    laclasse_lyon,
    extranet_colleges_somme
)

# Mapping of ENT options with their names
ent_options = {
    "1": ("cas_arsene76", cas_arsene76),
    "2": ("cas_ent27", cas_ent27),
    "3": ("cas_kosmos", cas_kosmos),
    "4": ("ent_creuse", ent_creuse),
    "5": ("occitanie_montpellier", occitanie_montpellier),
    "6": ("val_doise", val_doise),
    "7": ("val_de_marne", val_de_marne),
    "8": ("cas_cybercolleges42_edu", cas_cybercolleges42_edu),
    "9": ("ecollege_haute_garonne_edu", ecollege_haute_garonne_edu),
    "10": ("ac_orleans_tours", ac_orleans_tours),
    "11": ("ac_poitiers", ac_poitiers),
    "12": ("ac_reunion", ac_reunion),
    "13": ("cas_agora06", cas_agora06),
    "14": ("cas_seinesaintdenis_edu", cas_seinesaintdenis_edu),
    "15": ("eclat_bfc", eclat_bfc),
    "16": ("ent_auvergnerhonealpe", ent_auvergnerhonealpe),
    "17": ("laclasse_educonnect", laclasse_educonnect),
    "18": ("monbureaunumerique", monbureaunumerique),
    "19": ("ent77", ent77),
    "20": ("ent_ecollege78", ent_ecollege78),
    "21": ("ent_essonne", ent_essonne),
    "22": ("ent_mayotte", ent_mayotte),
    "23": ("ile_de_france", ile_de_france),
    "24": ("neoconnect_guadeloupe", neoconnect_guadeloupe),
    "25": ("paris_classe_numerique", paris_classe_numerique),
    "26": ("lyceeconnecte_aquitaine", lyceeconnecte_aquitaine),
    "27": ("ent_94", ent_94),
    "28": ("ent_hdf", ent_hdf),
    "29": ("ent_var", ent_var),
    "30": ("l_normandie", l_normandie),
    "31": ("lyceeconnecte_edu", lyceeconnecte_edu),
    "32": ("ent_elyco", ent_elyco),
    "33": ("bordeaux", bordeaux),
    "34": ("atrium_sud", atrium_sud),
    "35": ("laclasse_lyon", laclasse_lyon),
    "36": ("extranet_colleges_somme", extranet_colleges_somme)
}

config_file = 'config_tool.ini'
config = configparser.ConfigParser()

# If the config file exists, read it
if os.path.exists(config_file):
    config.read(config_file)
    USERNAME = config.get('login', 'username')
    PASSWORD = config.get('login', 'password')
    ENT_KEY = config.get('login', 'ent')

    # Check if the specified ENT_KEY is valid
    if ENT_KEY in ent_options:
        ENT = ent_options[ENT_KEY][1]  # Get the ENT function
    else:
        print(f"ENT clé '{ENT_KEY}' invalide, veuillez sélectionner à nouveau.")
        ENT = None  # Set ENT to None to indicate invalid selection
else:
    # Ask user for login information
    USERNAME = str(input("Quel est votre nom d'utilisateur : "))
    PASSWORD = getpass.getpass("Quel est votre mot de passe : ")

    # Display available ENT options in a table-like format
    ent_items = list(ent_options.items())
    table_data = []

    for i in range(0, len(ent_items), 4):
        row = ent_items[i:i+4]
        table_row = []
        for key, value in row:
            table_row.append(f"{key}: {value[0]}")
        table_data.append(table_row)

    print("Veuillez choisir votre ENT parmi les options suivantes :")
    print(tabulate(table_data, headers=[], tablefmt="grid"))

    # Prompt the user to enter the corresponding ENT number
    ENT_KEY = input("\nEntrez le numéro correspondant à votre ENT : ").strip()

    # Assign the selected ENT
    if ENT_KEY in ent_options:
        ENT = ent_options.get(ENT_KEY)[1]  # Get the ENT function
    else:
        print("Numéro de l'ENT invalide. Veuillez réessayer.")
        exit(1)  # Exit if the ENT is invalid
    
    # Save the information in the config file
    config['login'] = {
        'username': USERNAME,
        'password': PASSWORD,
        'ent': ENT_KEY
    }

    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Create the client using the selected ENT
if ENT is not None:  # Check if ENT is defined
    client = pronotepy.Client('https://0841093g.index-education.net/pronote/eleve.html',
        username=USERNAME,
        password=PASSWORD,
        ent=ENT)

# Verificate if connexion was etablished
if client.logged_in:
    today = date.today()
    days_ahead = 7 - today.weekday()
    next_monday = today + timedelta(days=days_ahead)
    next_sunday = next_monday + timedelta(days=6)
    timetable = client.lessons(next_monday, next_sunday)
    print("Emploi du temps récupéré !")

    # Ask user for output format
    output_format = input("Voulez-vous exporter l'emploi du temps en .txt (1), dans le terminal directement (2) ou dans un fichier excel (3) ? ").strip()

if output_format == "1":
    with open("all-scripts/emploi_du_temps.txt", "w") as file:
    # Browse and view the timetable in txt format
        for lesson in timetable:
            # Write the content
            file.write(f"Leçon: {lesson.subject.name}\n")
            file.write(f"De {lesson.start} à {lesson.end}\n\n")
    print("Emploi du temps exporté dans le fichier 'emploi_du_temps.txt'.")
elif output_format == "2":
        # Browse and view the timetable
    for lesson in timetable:
            print(f"Leçon: {lesson.subject.name}")
            print(f"De {lesson.start} à {lesson.end}")
elif output_format == "3":

    # Open existing Excel file
    wb = openpyxl.load_workbook('all-scripts/emploi_du_temps.xlsx')
    feuille = wb.active  # Select active sheet

    # Go through all cells and empty them
    for row in feuille.iter_rows():
        for cell in row:
            cell.value = None  # Clear cell contents

    # Save Excel file
    wb.save('all-scripts/emploi_du_temps.xlsx')
else:
    print("Ereur, vérifier la connexion ou le format sélectionné")