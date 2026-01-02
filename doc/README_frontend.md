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

To edit a window display layout, edit directly the corresonding .py file.


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
The file "resources/data/translations.yaml" contains a dictionnary. Set a new language (e.g. ISO3166-2 format), and add a new entry for this new language in each section of the yaml. Then in resources/data/language.conf, change the current_language variable to you new language.



FUTURE EVOLUTIONS

Comments labeled as "#TODO" in the Python code define additional steps to be performed. Comments labeled as "HereChangeMLAlgo" label the places where the ML picture recognition algorithms should be placed in the future. 

The algorithm can be called via a Python function (ideally), or via an OS command if necessary:
import subprocess, sys
command = sys.argv[1:]
subprocess.run(command[0], shell = True, executable="./ML_Algo")

Please refer to the file "README_interface_ML.md" for more details on the interfacing of an ML recognition program with the GUI.
