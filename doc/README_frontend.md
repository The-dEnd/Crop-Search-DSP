EN/FR [version française en fin de document]
FOREWORD/INTRODUCTION

This page aims a describing the structure of GUI scripts, and the general content of the folder for the die/sherd recognition tool. More generally, it aims at describing the full front-end interface. It is recommended mainly for power-users that intend to modify the GUI look. For generic instructions on the use of application, please refer to "HowToUse.txt". For details on the currently implemented ML algorithms, please refer to "README_ML.md". For details on interfacig the GUI with ML algorithms, please refer to "README_interface_ML.md".

Cette page décrit l'interface utilisateur GUI de l'application de reocnnaissance de motifs de tessons, ainsi que la structure générale de l'arborescence de fichiers de l'application. Elle est majoritairement destinée à des utilisateurs IT techniques cherchant à modifier le GUI. Pour les instructions génériques sur l'utilisation par un utilisateur final, merci de se référer au document "HowToUse.txt". Pour la documentation technique sur les algorithmes de reconnaissance de motifs utilisés, merci de se référer au document "README_ML.md". Pour la documentation technique sur l'interfacçage entre les algorithmes de rconnaissance et le GUI, merci de se référer au documente "README_interface_ML.md".


================================================================================
EN

GENERAL ARCHITECTURE
The GUI windows are divided in three main parts:
- the initialization windows, which request user to provide the path to files to be identified, and associated windows (loading screen, popups, ...).
- the main identification window, in which most of manual identfication will be performed (windos which displays die and sherd picture, localization, ...).
- the additional popups that can be displayed by specific requests from the user (type/shape of pottery -RIG-, undetected dies, force die type selector, licenses and legal mentions).

The production source code folder contains the following files and folders:
-resources/: folder that contains additional resources to be used for the assessment. It contains two folders, media (for the standard bictures to be used by the application, such as loading animations or die templates), and data (for static text, such as e.g. licensing, or the default localisation of archeological excavations).
-_Final_Output.csv: file that contains a CSV (semicollon separators) with output from manual assessment performed by reviewers. The following fields are present: Numero de tesson;Numero de decor;Numero de photo;Nom photo;Type de motif identifie;Numero de motif identifie;Commentaire;Pays;Region;Departement;Commune;Site/Lieu-dit;Lambert-X;Lambert-Y;Lambert-Z;Numero de fait;Numero d'US;Type de CRA;Numero de CRA;Position du tesson;Auteur de l'identification
-_START_APP.ps1: Powershell script that starts the application. It should only be used in a (Windows) environment with all expected packages and modules. For standalone deployment (for non-tech users), it is advised to use pyinstaller.
-_START_APP.sh: Bash version of _START_APP.ps1 It should only be used in a (Linux) environment with all expected packages and modules. For standalone deployment (for non-tech users), it is advised to use pyinstaller.
-ClickableQLabel.py: a Python class used for the popups where one should click somewhere to triger an action (e.g. RIG popup and force-type popup).
-crashlog.txt: supposed output of the terminal initiation scripts in case of a crash/error.
-display.py: main script; please refer to section "How to Edit files" for more details about its structure and functions
-display_types.py: handles the display of the popup that shows profile types (RIG, CRAV for Fanjeaux) if user clicks on "Afficher les types", in bottom-left of the main application window; the window is built automatically based on the content of resources/media/RIG_types/ folder (3 first chars of files are integer digits used as an index for display order, then the name to be displayed)
-doc/: folder that contains additional documentation on specific aspects of this file
-force_sherd.py: PyQt file that popups to set a die type automatically, and handles clicking on a die category; it is called by the buttons in other windows that use the "Magnifier" icon
-hooks/: folder managing compilation hooks for Pyinstaller; necessary at compilation time
-license_popup.ui and license_popup.py: Qt (.ui) file and it Python compatible export (.py) that handles the display of the popup that shows licenses and legal mentions of the application if user clicks on "Afficher license"
-loading_screen.ui and loading_screen.py: Qt (.ui) file and it Python compatible export (.py) that handles the display of the progress bar and loading screen while the application ML algorithms perform pattern recognition on die pictures
-logs.txt and logs.txt.*: (rather verbose) logs of current/last session, and the three previous sessions; these files are suposed to log the timestamp and almoste very action performe by the user (editing a field value, clicking a button, ...); only 4 latest logs (running session +3 last sessions) are kept, to prevent excessive disk storage
-main_layout.ui and main_layout.py: Qt (.ui) file and it Python compatible export (.py) that handles the display template of main identification window
-measure_state.py: a file that keeps track of some global variables that need to be called in both display and main_layout, to avoid a circular import
-numDecoRgister.py: a popup managing decorative registries is the same die is present multiple times on a sherd;
-Outil_Poincons.spec: .spec file, used to store the configuration of PyInstaller compiler
-output_ML.csv: file populated by ML algorithm, that contains the output of previous session of die recognition by Machine Learning. For more details on its content and structure, please refer to file "doc/README_interface_ML.md". To keep it simple, this file is the output of ML, and the input of all visual parts of the Application.
-run_ML.py: the (current) script running all the ML part
-tmp/: folder that is used to store resized pictures of sherds, with dies reframed on them; will be empty when the application is not running
-translator.py: Python file that handles the translation of all the application's text, vie a translating function and a dictionnary
-undetected_die.py: Python file that handles the display of the windows that allows users to manually select an area on the picture that contains an undetected die, and that frames this area with red crosses at its edge. The Python file required many manual adjustments from the raw export of .ui file, and a diff should be made and reviewed in case you want to modify the .ui file, before editing this file (1) edit the .ui 2) export the .ui to .py with another name 3) check and assess the differences between the original .py file and your export result 4) edit your export result accordingly 5) replace the original .py file with your modified export result)

The development source code folder contains the following additional files and folders (plus the ontent of production folder):

-tmp_pics/: folder that contains a sample of sherd pictures used as testing data
-output_ML.csv: file that appears after running machine learning scripts in theory. In development, it has been pre-populated for testing purpose
-backup/: folder that contains previous versions of source code
-TODO.txt: 1) checks to be made before each release and 2) potential improvements/bug report notes to the Application



Most of the application "main window" "live" code (e.g. non-static display) is present in file "display.py". Should functionnal modifications be performed in the application, it is most likely that this file should be the most/single affected file. Please refer to next sections "How to edit files" for more details on this file.


HOW TO EDIT FILES

To edit a window display layout:
	-if .ui file exists, use PyQtDesigner to modify the layout graphically. Save the .ui file in PyQtDesigner (Ctrl+S). Then, convert it to .py using the command "pyuic5 /path/to/window.ui -o /path/to/window.py". /!\ recheck in the py files: relative paths (e.g. resources/folder/img.jpg) tend to be replaced by absolute paths (e.g. /home/user/tool/resources/folder/img.jpg); Finally, compare the different version, and append the code sections addes in the original py file.
	-else, edit directly the .py file


Each Python function, and each difficultly-readable code section, are normally commented with explicit comments that explicit its purpose.

The file display.py contains the following functions and classes:
-class Selector_Main: manages the main window, and the user actions once the dies have been recognized by ML algorithm
	-__init__: class initiator
	-get_values: when a user validates his assessment, retrieves data from all fields filled by user, to provide a list of values corresponding to user assessment in each field
	-next_clicked: handles what happens when the user clicks next: calls get_values to retrieve values, calls output_application_files and output_application_csv, and checks if default location has changed; then loads new sherd picture by calling newPart
	-skip_clicked: handles whhat happens when the user clicks skip: do nothing and call newPart
	-exit_clicked: handles whhat happens when the user clicks exit: close the main window
	-newPart: initiates the windows with value from a sherd ML authentication
	-show_types: calls class Display_Types
	-force_RIG_types: used by class Force_Type_Class to change the RIG type following the user's clicks in Force_Type_Class UI
	-popup_license: calls class License_Popup
	-false_negative: if a die is not detected in the picture byt the ML algorithm, the user will click on a button that calls this function; calls class Undetected_Die
	-get_location: loads from the location config file (in resources>data) the location of the archeological site
	-set_location: overwrites the location config file (in resources>data) with current values filled by user in "location" section of screen (top left); NOTE: this does not affect Fait and US, which are the most volatile values (compared to the location of archeological excavations), and are thus not stored in a static config file
	-[all other functions in this class]: logs a specific action/click from the user, for debuggin/logging purposes.
-class Init_Window: handles the application startup and loading screen
	-__init__: class initiator; if the user wants to run a new ML set, prompts him to select a folder that contains pictures (by calling select_files), and runs the ML algorithm on the (jpg or png) content of this folder
	-resumeConfirm: calls outputML_CSV_exists to assess if a previous session was not finished; if such a session exists, prompts the user a choice to relaunch it or not; returns a boolean with the user output, and false if no older session was identified; the purpose is to avoid rerunning time-consuming ML algorithm is previous session is still applicable
	-setup_loading_window: displays a loading screen while the ML algorithm runs
	-select_files: prompts the user to pick a folder containing sherd pictures; called by __init__
	-loadML: calls ML algorithm on files within a path, to provide hypotheses on the die shape
-class Display_Types: handles the opening of display_types.py
	-__init__: class initiator
	-clicked: received the part of the windows that the user clicked on to set the RIG type, and changes the displayed RIG type value accordingly
-class Force_Type_Class: handles the opening of force_sherd.py
	-__init__: class initiator
	-clicked: received the part of the windows that the user clicked on to set the die type, and changes the displayed die type value accordingly
-class License_Popup: handles the opening of license_popup.ui
	-__init__: class initiator
-class Undetected_Die: handled the opening of undetected_die.py
	-__init__: class initiator
	-exit: gracefully shuts down the popup
	-accept: if the users sets an area of the photo that should contain a die and does not, retrieves data about the die and populates "_Final_Output.csv" accordingly
	-getParentAttributes: retrieves shred-related data from the main window (e.g. location, RIG type), but of course not the die-related data
-doSomething: this function is only used during testing, to emulate the bahavior of an actual ML algorithm that populates "output_ML.csv"; it is basically only a time.sleep.
-outputML_CSV_exists: checks if an output from a previous run of ML algorithm exists, and contains dies/sherds that were not manually attributed; used by Init_Window>resumeConfirm
-output_application_csv: manages the output of user's manual review to file "_Final_Output.csv"
-output_application_files: manages the output of user's manual review that regards the copying of sherd pictures in a subfolder named after the die shape that is represented on the sherd
-cleanLogs: manages the lifespan of log files for each session (creating a new log files, and pushing olders log files one step further in the "old>older>oldest" direction
-readDataCsvML: manages the CSV returned by ML algorithm "output_ML.csv", with the list of pictures, and the associated diagnostic on the die type and asociated probability
-prepareData: formats a line from ML algorithm output CSV into variables managable by the application
-setCurrent: takes the (already edited) picture from tmp folder, and highlights current die on the picture, to ease visual detection.
-properClosure: handles the exit signal, logs the events, and saves unclassified die list in "output_ML.csv", in prevision of next session
-basicWarning: a simple function that can display a basic warning popup with text to be provided, as an alternative for all the simplest message box popups.

HOW TO RUN/TEST FILES

The display can be run with Bash and Powershell terminal commands (_START_APP.ps1, _START_APP.sh), but their content is minimal and can be directly typed in Bash/Powershell to display debugging information properly.

In case of a crash, every user action should (normally) be logged in the file "log.txt" for the last session. Older sessions are logged in "log.txt.old", "log.txt.older", "log.txt.oldest". History for sessions older than the three last sessions is not retained, in order to limit the storage space taken by (mostly useless) logs.


HOW TO CHANGE THEME/UI
In resources/styles, a few .qss ("CSS for Qt") files are already defined. Feel free to edit them or add your own styles. It is recommended to ensure that the theme is running smoothly before compiling with Pyinstaller.
Note: the "accesibility" theme is designed to be accessible for color-blind people, as well as dyslexic people. It is recommended to edit it with caution.


HOW TO TRANSLATE TO A NEW LANGUAGE
The file "translator.py" contains a dictionnary. Set a new language (e.g. ISO3166-2 format), and add a new entry for this new language in each section of the dictionnary. Then in resources/data/language.conf, change the current_language variable to you new language.



FUTURE EVOLUTIONS

Comments labeled as "#TODO" in the Python code define additional steps to be performed. Comments labeled as "HereChangeMLAlgo" label the places where the ML picture recognition algorithms should be placed in the future. 

The algorithm can be called via a Python function (ideally), or via an OS command if necessary:
import subprocess, sys
command = sys.argv[1:]
subprocess.run(command[0], shell = True, executable="./ML_Algo")

Please refer to the file "README_interface_ML.md" for more details on the interfacing of an ML recognition program with the GUI.


================================================================================
FR (traduit par IA avec GPT4, peut contenir des erreurs/contresens; en cas de soucis merci de bien vouloir se référer au texte Anglais)

ARCHITECTURE D'ENSEMBLE

Les fenêtres GUI sont divisées en trois catégories principales :
- les fenêtres d'initialisation, qui demandent à l'utilisateur de fournir le chemin des fichiers à identifier, ainsi que les fenêtres associées (écran de chargement, pop-ups, ...).
- la fenêtre principale d'identification, dans laquelle la plupart des identifications manuelles seront effectuées (fenêtre affichant les photos de poinçons et de tessons, leur localisation, ...).
- les pop-ups supplémentaires qui peuvent être affichés à la demande de l'utilisateur (type/forme de poterie -RIG-, poinçons non détectés, sélection forcée du type de poinçon, licences et mentions légales).

Le dossier du code source de production contient les fichiers et dossiers suivants :
-resources/ : dossier contenant des ressources supplémentaires utilisées pour l'évaluation. Il contient deux sous-dossiers, media (pour les images standard utilisées par l'application, telles que les animations de chargement ou les modèles de poinçons) et data (pour les textes statiques, comme les licences ou la localisation par défaut des fouilles archéologiques).
-_Final_Output.csv : fichier contenant un CSV (séparateurs par point-virgule) avec les résultats de l'évaluation manuelle effectuée par les réviseurs. Les champs suivants sont présents : Numero de tesson;Numero de decor;Numero de photo;Nom photo;Type de motif identifie;Numero de motif identifie;Commentaire;Pays;Region;Departement;Commune;Site/Lieu-dit;Lambert-X;Lambert-Y;Lambert-Z;Numero de fait;Numero d'US;Type de CRA;Numero de CRA;Position du tesson;Auteur de l'identification.
-_START_APP.ps1 : script PowerShell qui lance l'application. Il ne doit être utilisé que dans un environnement (Windows) avec tous les modules et paquets requis. Pour une application toute packagée (pour un utilisateur non technique), il est recommandé d'utiliser Pyinstaller à la place.
-_START_APP.sh : version Bash de _START_APP.ps1. Il ne doit être utilisé que dans un environnement (Linux) avec tous les modules et paquets requis.  Pour une application toute packagée (pour un utilisateur non technique), il est recommandé d'utiliser Pyinstaller à la place.
-ClickableQLabel.py : une classe Python utilisée pour les pop-ups où l'on doit cliquer quelque part pour déclencher une action (par exemple, pop-up RIG et sélection forcée de type).
-crashlog.txt : sortie prévue des scripts d'initialisation du terminal en cas de crash/erreur.
-display.py : script principal ; veuillez vous référer à la section "Comment modifier les fichiers" pour plus de détails sur sa structure et ses fonctions.
-display_types.py: gère l'affichage du pop-up montrant les types de profils (RIG, appelé "CRAV" à Fanjeaux) lorsque l'utilisateur clique sur "Afficher les types", en bas à gauche de la fenêtre principale de l'application; la fenêtre est construite automatiquement en fonction du contenu du dossier resources/media/RIG_types/ (chaque image commence par l'indice souhaité de l'image dans l'affichage, sur 3 entiers, puis le nom que l'on souhaite afficher à coté de l'image)
-doc/ : dossier contenant une documentation supplémentaire sur certains aspects de l'Application.
-force_sherd.py : fichier PyQt qui fait apparaître un pop-up permettant de définir automatiquement un type de poinçon et gérant les clics sur une catégorie de poinçon ; il est appelé par les boutons d'autres fenêtres qui utilisent l'icône "Loupe".
-hooks/: dossier gérant les hooks de Pyinstaller, pour la compilation du code
-license_popup.ui et license_popup.py : fichier Qt (.ui) et son export compatible Python (.py) qui gère l'affichage du pop-up des licences et mentions légales de l'application lorsque l'utilisateur clique sur "Afficher license".
-loading_screen.ui et loading_screen.py : fichier Qt (.ui) et son export compatible Python (.py) qui gère l'affichage de la barre de progression et de l'écran de chargement pendant que les algorithmes de Machine Learning de l'application effectuent la reconnaissance des motifs sur les images de poinçons.
-logs.txt et logs.txt.* : journaux (plutôt détaillés) de la session actuelle ou de la dernière session, ainsi que des trois sessions précédentes. Ces fichiers enregistrent l'horodatage et presque toutes les actions effectuées par l'utilisateur (modification d'une valeur de champ, clic sur un bouton, ...). Seuls les quatre derniers journaux (session en cours + 3 dernières sessions) sont conservés afin d'éviter une consommation excessive d'espace disque.
-main_layout.ui et main_layout.py : fichier Qt (.ui) et son export compatible Python (.py) qui gère le modèle d'affichage de la fenêtre principale d'identification.
-measure_state.py: un fichier qui assure le suivi de variables globals nécessaires à la fois dans display et main_layout, pour éviter un import ciruclaire entre les deux fichiers
-numDecoRgister.py: une popup qui gère les registres décoratifs si un tesson a plusieurs fois le même motif.
-Outil_Poincons.spec : fichier .spec utilisé pour stocker la configuration du compilateur PyInstaller.
-output_ML.csv : fichier généré par l'algorithme de Machine Learning, contenant les résultats de la session précédente de reconnaissance de poinçons. Pour plus de détails sur son contenu et sa structure, veuillez vous référer au fichier "doc/README_interface_ML.md". En résumé, ce fichier est la sortie du Machine Learning et l'entrée de toutes les parties visuelles de l'application.
-run_ML.py: l'algorithme de reconnaissance Machine Learning (à l'heure actuelle)
-tmp/ : dossier utilisé pour stocker des images redimensionnées de tessons, avec les poinçons recadrés dessus ; il sera vide lorsque l'application ne sera pas en cours d'exécution.
-translator.py: fichier Python gérant la traduction de tout texte dans les langues disponibles via une fonction de traduction et un dictionnaire de messages
-undetected_die.py : fichier Python qui gère l'affichage de la fenêtre permettant aux utilisateurs de sélectionner manuellement une zone sur l'image contenant un poinçon non détecté, en l'encadrant avec des croix rouges sur ses bords. Le fichier Python a nécessité de nombreux ajustements manuels après l'export brut du fichier .ui, et une comparaison des différences devrait être effectuée avant de modifier ce fichier (1) modifier le .ui 2) exporter le .ui en .py sous un autre nom 3) vérifier et évaluer les différences entre le fichier .py original et votre export 4) ajuster votre export en conséquence 5) remplacer le fichier .py original par votre version modifiée).


Le dossier du code source de développement contient les fichiers et dossiers supplémentaires suivants (en plus du contenu du dossier de production) :

-tmp_pics/ : dossier contenant un échantillon d'images de tessons utilisées comme données de test.
-output_ML.csv : fichier qui apparaît après l'exécution des scripts de Machine Learning en théorie. En développement, il a été pré-rempli à des fins de test.
-backup/ : dossier contenant les versions précédentes du code source.
-TODO.txt : 1) vérifications à effectuer avant chaque version et 2) améliorations potentielles / rapports de bugs concernant l'application.

La majeure partie du code "dynamique" de la "fenêtre principale" de l'application (c'est-à-dire l'affichage non statique) se trouve dans le fichier "display.py". Si des modifications fonctionnelles doivent être apportées à l'application, il est fort probable que ce soit le fichier le plus impacté, voire le seul. Veuillez vous référer aux sections suivantes "Comment modifier les fichiers" pour plus de détails sur ce fichier.


COMMENT EDITER LE CODE

Pour modifier la disposition de l'affichage d'une fenêtre :
	-si un fichier .ui existe, utilisez PyQtDesigner pour modifier graphiquement la mise en page. Enregistrez le fichier .ui dans PyQtDesigner (Ctrl+S). Ensuite, convertissez-le en .py à l'aide de la commande "pyuic5 /path/to/window.ui -o /path/to/window.py". /!\ Vérifiez dans les fichiers .py : les chemins relatifs (ex. resources/folder/img.jpg) ont tendance à être remplacés par des chemins absolus (ex. /home/user/tool/resources/folder/img.jpg). Ensuite, recopiez les éléments de code Python qui ne sont pas générés automatiquement par PyQt depuis le fichier Py original.
	-sinon, modifiez directement le fichier .py.

Chaque fonction Python et chaque section de code difficilement lisible sont normalement commentées avec des explications explicites de leur objectif.

Le fichier display.py contient les fonctions et classes suivantes :

-classe Selector_Main : gère la fenêtre principale et les actions de l'utilisateur une fois que les poinçons ont été reconnus par l'algorithme de ML.
	-__init__ : initialisation de la classe.
	-get_values : lorsqu'un utilisateur valide son évaluation, récupère les données de tous les champs remplis pour fournir une liste de valeurs correspondant à l'évaluation de l'utilisateur.
	-next_clicked : gère ce qui se passe lorsque l'utilisateur clique sur "Suivant" : appelle get_values pour récupérer les valeurs, appelle output_application_files et output_application_csv, vérifie si la localisation par défaut a changé, puis charge une nouvelle image de tesson en appelant newPart.
	-skip_clicked : gère ce qui se passe lorsque l'utilisateur clique sur "Ignorer" : ne fait rien et appelle newPart.
	-exit_clicked : gère ce qui se passe lorsque l'utilisateur clique sur "Quitter" : ferme la fenêtre principale.
	-newPart : initialise la fenêtre avec la valeur issue d'une authentification de tesson par ML.
	-show_types : appelle la classe Display_Types.
	-force_RIG_types : utilisé par la classe Force_Type_Class pour modifier le type RIG selon les clics de l'utilisateur dans l'interface Force_Type_Class.
	-popup_license : appelle la classe License_Popup.
	-false_negative : si un poinçon n'est pas détecté sur l'image par l'algorithme de ML, l'utilisateur clique sur un bouton qui appelle cette fonction ; elle invoque la classe Undetected_Die.
	-get_location : charge depuis le fichier de configuration (dans resources>data) la localisation du site archéologique.
	-set_location : écrase le fichier de configuration avec les valeurs actuelles saisies par l'utilisateur dans la section "Localisation" (en haut à gauche) ; NOTE : cela n'affecte pas "Fait" et "US", qui sont les valeurs les plus volatiles (par rapport à la localisation des fouilles archéologiques), et ne sont donc pas stockées dans un fichier de configuration statique.
	-[toutes les autres fonctions de cette classe] : journalise une action/un clic spécifique de l'utilisateur, à des fins de débogage et de suivi.

-classe Init_Window : gère le démarrage de l'application et l'écran de chargement.
	-__init__ : initialisation de la classe ; si l'utilisateur veut exécuter un nouveau traitement ML, lui demande de sélectionner un dossier contenant des images (en appelant select_files) et exécute l'algorithme ML sur le contenu (jpg ou png) de ce dossier.
	-resumeConfirm : appelle outputML_CSV_exists pour évaluer si une session précédente n'a pas été terminée ; si une session existe, demande à l'utilisateur s'il souhaite la relancer ; retourne un booléen avec la réponse de l'utilisateur (false si aucune session antérieure n'est trouvée). L'objectif est d'éviter de relancer un algorithme ML long si la session précédente est toujours applicable.
	-setup_loading_window : affiche un écran de chargement pendant l'exécution de l'algorithme ML.
	-select_files : demande à l'utilisateur de sélectionner un dossier contenant des images de tessons ; appelé par __init__.
	-loadML : appelle l'algorithme ML sur les fichiers du chemin donné, pour fournir des hypothèses sur la forme du poinçon.

-classe Display_Types : gère l'ouverture de display_types.py.
	-__init__ : initialisation de la classe.
	-clicked : récupère la partie de la fenêtre sur laquelle l'utilisateur a cliqué pour définir le type RIG et modifie la valeur affichée du type RIG en conséquence.

-classe Force_Type_Class : gère l'ouverture de force_sherd.py.
	-__init__ : initialisation de la classe.
	-clicked : récupère la partie de la fenêtre sur laquelle l'utilisateur a cliqué pour définir le type de poinçon et modifie la valeur affichée du type de poinçon en conséquence.

-classe License_Popup : gère l'ouverture de license_popup.ui.
	-__init__ : initialisation de la classe.

-classe Undetected_Die : gère l'ouverture de undetected_die.py.
	-__init__ : initialisation de la classe.
	-exit : ferme proprement le pop-up.
	-accept : si l'utilisateur définit une zone de la photo qui devrait contenir un poinçon mais qui n'en contient pas, récupère les données du poinçon et remplit "_Final_Output.csv" en conséquence.
	-getParentAttributes : récupère les données liées au tesson depuis la fenêtre principale (ex. localisation, type RIG), mais pas les données liées au poinçon.

-doSomething : cette fonction est uniquement utilisée lors des tests, pour émuler le comportement d'un véritable algorithme ML qui remplit "output_ML.csv" ; elle utilise simplement un time.sleep.
-outputML_CSV_exists : vérifie si un résultat d'une exécution précédente de l'algorithme ML existe et contient des poinçons/tessons qui n'ont pas été attribués manuellement ; utilisé par Init_Window>resumeConfirm.
-output_application_csv : gère la sortie de l'examen manuel de l'utilisateur vers le fichier "_Final_Output.csv".
-output_application_files : gère la sortie de l'examen manuel de l'utilisateur concernant la copie des images de tessons dans un sous-dossier nommé d'après la forme du poinçon représenté sur le tesson.
-cleanLogs : gère la durée de vie des fichiers journaux de chaque session (création d'un nouveau fichier journal et déplacement des anciens fichiers dans la direction "ancien>plus ancien>plus ancien encore").
-readDataCsvML : gère le CSV retourné par l'algorithme ML "output_ML.csv", contenant la liste des images et le diagnostic associé sur le type de poinçon et sa probabilité associée.
-prepareData : formate une ligne du fichier CSV de sortie de l'algorithme ML en variables exploitables par l'application.
-setCurrent : prend l'image (déjà éditée) du dossier tmp et met en surbrillance le poinçon actuel sur l'image pour faciliter la détection visuelle.
-properClosure : gère le signal de sortie, journalise les événements et enregistre la liste des poinçons non classifiés dans "output_ML.csv" en prévision de la prochaine session.
-basicWarning : une fonction simple permettant d'afficher un pop-up d'avertissement basique avec un texte fourni, en alternative aux pop-ups de message les plus simples.

COMMENT EXÉCUTER/TESTER LES FICHIERS

L'affichage peut être exécuté à l'aide des commandes de terminal Bash et Powershell (_START_APP.ps1, _START_APP.sh), mais leur contenu est minimal et peut être directement saisi dans Bash/Powershell pour afficher correctement les informations de débogage.

En cas de crash, chaque action de l'utilisateur devrait (normalement) être enregistrée dans le fichier "log.txt" pour la dernière session. Les sessions plus anciennes sont enregistrées dans "log.txt.old", "log.txt.older", "log.txt.oldest". L'historique des sessions antérieures aux trois dernières n'est pas conservé afin de limiter l'espace de stockage occupé par des journaux (les logs étant généralement inutiles hors bug/crash).


COMMENT CHANGER LE THEME/L'INTERFACE VISUELLE
Dans resources/styles, une liste de fichiers QSS (des "CSS pour Qt") est déja présente. Vous pouvez les éditer ou ajouter de nouveaux fichiers qss pour adapter les styles. Il est recommandé de tester l'aspect graphique d'un thème avant de le compiler avec Pyinstaller.
Note: le thème "accessibility" est conçu pour être utilisable par des utilisateurs daltoniens et/ou dyslexiques. Modifiez-le avec précaution.


COMMENT TRADUIRE DANS UNE AUTRE LANGUE
Ajoutez des entrées pour une nouvelle langue dans le fichier "translator.py", et modifiez la variable "current_language" dans resources/data/language.conf en conséquence.


ÉVOLUTIONS FUTURES

Les commentaires marqués comme "#TODO" dans le code Python définissent les étapes supplémentaires à effectuer. Les commentaires marqués "HereChangeMLAlgo" indiquent les emplacements où les algorithmes de reconnaissance d'images ML devront être intégrés à l'avenir. L'algorithme peut être appelé via une fonction Python (idéalement) ou via une commande système si nécessaire :

python
import subprocess, sys
command = sys.argv[1:]
subprocess.run(command[0], shell=True, executable="./ML_Algo")

Veuillez vous référer au fichier "README_interface_ML.md" pour plus de détails sur l'interface entre un programme de reconnaissance ML et l'interface graphique.




