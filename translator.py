#This file is a large dictionnary that manages translation of PyQt messages. It also contains a translation function.
import time
from datetime import datetime

try:
    with open("resources/data/language.conf", "r") as f: #retrieve languages
        for line in f:
            line = line.strip()
            if "=" in line:
                var, value = line.split("=", 1)
                var = var.strip()
                value = value.split("#")[0].strip().replace('"','')
                if var == "current_language":
                    current_language = value
                if var == "default_language":
                    default_language = value
except: #it seems that sometims there are access rights issues on the language.conf file (unknozn reason); hence, this failsafe loop defaults languages to English if this happens
    current_language = "en"
    default_language = "en"
    pass


# Dictionary of messages per language
translations = { #WARNING: the UI layout has been designed for the fr version; it is strongly recommended that your translation does not exceed fr message length
    "lMotifs": {
        "en": {1:"Wheel",2:"Leaf",3:"Column",4:"Geometric",5:"Reticulate",6:"Arch",7:"S-shape",8:"Figure",0:"Select a die type"},
        "fr": {1:"Rouelle",2:"Palmette",3:"Colonette",4:"Géométrique",5:"Réticulé",6:"Arceau",7:"S-serpentin",8:"Figuratif",0:"Sélectionner un motif",4:"Geometrique",4:"Geo."}, #accentuated characters are duplicated to ease up understanding of reverse dictionnary
    },
    "loca": {
        "en": "Location",
        "fr": "Localisation",
    },
    "forceLocation": {
        "en": "Force a new default\nlocation?",
        "fr": "Forcer nouvelle localisation\npar défaut?",
    },
    "photoNr": {
        "en": "picture #",
        "fr": "photo n°",
    },
    "sherdNr": {
        "en": "sherd #",
        "fr": "tesson n°",
    },
    "dieNr": {
        "en": "die #",
        "fr": "poinçon n°",
    },
    "algoComm": {
        "en": "Comments: ",
        "fr": "Commentaires: ",
    },
    "country": {
        "en": "Country",
        "fr": "Pays",
    },
    "region": {
        "en": "Region",
        "fr": "Région",
    },
    "dpt": {
        "en": "District/County",
        "fr": "Département",
    },
    "city": {
        "en": "City",
        "fr": "Commune",
    },
    "place": {
        "en": "Exact location",
        "fr": "Lieu-dit",
    },
    "featureNr": {
        "en": "Feat. #",
        "fr": "Fait n°",
    },
    "featurePrompt": {
        "en": "Type feature #",
        "fr": "Taper n° de fait",
    },
    "contextNr": {
        "en": "Context #",
        "fr": "US N°",
    },
    "contextPrompt": {
        "en": "Type context #",
        "fr": "Taper n° d'US",
    },
    "ceramData": {
        "en": "Caramological data",
        "fr": "Données céramologiques",
    },
    "category": {
        "en": "Category",
        "fr": "Catégorie",
    },
    "cratype": {
        "en": "CRA mode",
        "fr": "CRA de mode",
    },
    "sherdLoc": {
        "en": "Sherd location",
        "fr": "Emplacement du fragment",
    },
    "edge": {
        "en": "Edge",
        "fr": "Bord",
    },
    "belly": {
        "en": "Belly",
        "fr": "Panse",
    },
    "bottom": {
        "en": "Bottom",
        "fr": "Fond",
    },
    "shape": {
        "en": "Shape",
        "fr": "Forme",
    },
    "otherType": {
        "en": "Other/New",
        "fr": "Autre/Inédit",
    },
    "displayTypes": {
        "en": "Display all types",
        "fr": "Afficher les types",
    },
    "displayLicense": {
        "en": "Show licences",
        "fr": "Afficher licenses",
    },
    "typeComment": {
        "en": "Type your comments here",
        "fr": "Taper commentaires ici",
    },
    "selectPattern": {
        "en": "Select a die type",
        "fr": "Sélectionner un motif",
    },
    "noSelect": {
        "en": "WARNING: you did not select a die type/number.",
        "fr": "ATTENTION: veuillez sélectionner un motif et n°.",
    },
    "force": {
        "en": "Force",
        "fr": "Forcer",
    },
    "undet": {
        "en": "Undetermined",
        "fr": "Indéterminé",
    },
    "falsePos": {
        "en": "Not a die",
        "fr": "Pas un motif",
    },
    "falseNeg": {
        "en": "Undetected pattern/die?",
        "fr": "Un motif n'est pas détecté?",
    },
    "or": {
        "en": "or",
        "fr": "ou",
    },
    "author": {
        "en": "Identification author",
        "fr": "Auteur des identifications",
    },
    "themeSelector": {
        "en": "Choose your preferred theme",
        "fr": "Choisissez votre thème",
    },
    "pickRIG": {
        "en": "Pick a RIG Type",
        "fr": "Sélectionnez un type de CRAV ",
    },
    "next": {
        "en": "Next",
        "fr": "Suivant",
    },
    "noRadio": {
        "en": "Warning, no radio button selected; please select one option.",
        "fr": "Attention: aucun choix de motif effectué; merci d'en sélectionner",
    },
    "errorNoFold": {
        "en": "No selected folder, the application will now exit...",
        "fr": "Aucun dossier sélectionné; l'application va se fermer...",
    },
    "errorNoPic": {
        "en": "Selected folder does not contain JPG/PNG, application will now exit...",
        "fr": "Le dossier sélectionné ne contient pas d'images (JPG, PNG); l'application va se fermer...",
    },
    "startup1": {
        "en": "Information: ",
        "fr": "Information: Il reste ",
    },
    "startup2": {
        "en": " dies were found from a previous session (dated ",
        "fr": " poinçons issues d'une session précédente (",
    },
    "startup3": {
        "en": "); do you want to reopen this session instead of startin a new session?",
        "fr": "); voulez-vous rouvrir cette session au lieu d'en charger une nouvelle?",
    },
    "folderSelector": {
        "en": "Please select the folder that contains you pictures",
        "fr": "Sélectionnez le dossier contenant les photos de poinçons",
    },
    "noFalseNegTwoPoints": {
        "en": "WARNING: you did not provide 2 points to frame the die pattern.",
        "fr": "ATTENTION: vous devez fournir 2  points pour encadrer le motif.",
    },
    "mainTitle": {
        "en": "Die pattern classifying assistance",
        "fr": "Classement motif poinçons",
    },
    "typeNr": {
        "en": "Type # here",
        "fr": "Taper n° ici",
    },
    "exit": {
        "en": "Exit",
        "fr": "Quitter",
    },
    "skip": {
        "en": "Skip",
        "fr": "Passer",
    },
    "new": {
        "en": "New",
        "fr": "Inédit",
    },
    "falseNegIntro": {
        "en": "Click on both corners of the pattern; if you misclicked, keep clicking: only the latest 2 clicks will be kept.\nLocation data will be copied from main window; if they are incorrect, please change them in main window first before returning here.",
        "fr": "Cliquez aux deux coins opposés du motif; en cas d\'erreur, continuez à cliquer aux bons endroits: seuls les deux derniers points seront conservés en mémoire\nLes coordonées, n° de faits et autre seront reprises de la denêtre principale; changez les là bas puis revenez ici au besoin",
    },
    "typeNrHere": {
        "en": "Type Number here",
        "fr": "Taper numéro ici",
    },
    "typeNum": {
        "en": "Type #",
        "fr": "Type n°",
    },
    "okMsg": {
        "en": "OK",
        "fr": "Klar",
    },
    "cancel": {
        "en": "Cancel",
        "fr": "Annuler",
    },
    "validate": {
        "en": "Validate",
        "fr": "Valider",
    },
    "recent": {
        "en": "Recent",
        "fr": "Récents",
    },
    "searchTitle": {
        "en": "Search a previous sherd",
        "fr": "Chercher un motif précédent",
    },
    "searchPlaceholder": {
        "en": "Type shred number",
        "fr": "Tapez n° de motif",
    },
    "searchNotFound": {
        "en": "WARNING: die number unrecognized, please try again...",
        "fr": "ATTENTION: le n° de motif saisi n'a pas été retrouvé; veuillez réessayer...",
    },
    "rollbackMsg": {
        "en": "This die was manually set and rolled back.",
        "fr": "Ce motif a été revu et a été recherché.",
    },
    "setScale": {
        "en": "Set scale",
        "fr": "Donner l'échelle",
    },
    "measureLength": {
        "en": "Measure length",
        "fr": "Mesurer longueur",
    },
    "typeLength": {
        "en": "Type here the length you know",
        "fr": "Tapez ici la longueur connue",
    },
    "pleaseWait": {
        "en": "Please wait, detection ongoing...",
        "fr": "Patientez, détection en cours...",
    },
    "warnNoDetec": {
        "en": "WARNING: no dies detected on this picture",
        "fr": "ATTENTION: aucun motif détecté sur cette image",
    },
    "numDecoRegTitle": {
        "en": "# Decorative Registers",
        "fr": "Nombre de registres déco.",
    },
    "numDecoReg": {
        "en": "This die is present multiple times on the sherd: $ How many decorative registers do contain it? (lines, circles, ...)",
        "fr": "Le poinçon $ est présent plusieurs fois sur le tesson; sur combien de regsitres décoratifs différents (lignes, cercles, ...) est-il présent?",
    },
    "decoRegMsg": {
        "en": "The die £ is present on $ decorative registries on this sherd",
        "fr": "Le poinçon £ est présent sur $ registres décoratifs sur ce tesson",
    },
    "okMsg": {
        "en": "OK",
        "fr": "Klar",
    },
    "okMsg": {
        "en": "OK",
        "fr": "Klar",
    },
    "okMsg": {
        "en": "OK",
        "fr": "Klar",
    },
    "okMsg": {
        "en": "OK",
        "fr": "Klar",
    },
}


def tr(key): #returns the value associated to the key, for current_language
    msg = translations.get(key)
    if not msg: #if the key does not exist, just display the key
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    Translation key "+key+"not found\n")
        return f"[{key}]"
    if current_language in msg: #if current_language has a translation, return current_language
        return msg[current_language]
    else: #if current_language translation is unavailable, return default_language instead
        with open("logs.txt", "a") as logFile:
            logFile.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")+"    Translation key "+key+"not found for language "+current_language+"; defaulting to "+default_language+"\n")
        return msg[default_language]
    return f"[{key}]"