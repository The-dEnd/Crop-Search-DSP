EN/FR [version française en fin de document]
FOREWORD/INTRODUCTION

This page aims at describing the output formatting of ML algorithms recognized by the front end interface. It is recommended mainly for power-users that intend to work on the ML part. For generic instructions on the use of application, please refer to "HowToUse.txt". For details on the front-end, please refer to "README_frontend.md". For details on the currently implemented ML algorithms, please refer to "README_ML.md"


Cette page décrit le format de sortie attendu pour l'algorithme de reconnaissance de motif par l'application GUI. Elle est majoritairement destinée à des utilisateurs IT techniques cherchant à développer la partie Machine Learning. Pour les instructions génériques sur l'utilisation par un utilisateur final, merci de se référer au document "HowToUse.txt". Pour la documentation technique sur l'implémentation du GUI, merci de se référer à "README_frontend.md". Pour la documentation technique sur l'implémentation du Machine Learning, merci de se référer à "README_ML.md".


===============================================================================
EN

The sherd recognition algorithm is expected to output a CSV document (semicolon-separated), of 36 columns, with following content and formatting:
NumTesson - Int - Reference number of the sherd that contains the die
NumDecor - Int - Reference number of the die
NumPhoto - Int - Reference number of the picture
NamePhoto - Str - Path of the picture and its name (e.g. "/home/user/Desktop/sherd/picture_2.jpg")
Choice1Id - Int - Id of the choice of die with the highest probability according to ML algorithms*
Choice1Pretty - Str - Pretty name of the die with highest probability (e.g. "Rouelle 3")
Proba1 - Float - Probability (between 0 and 1) of die with the highest probaility
Choice2Id - Int - Id of the choice of die with the second highest probability, according to ML algorithms*
Choice2Pretty - Str -Pretty name of die with second highest probability
Proba2 - Float - Probability of die with second highest probability
Choice3Id - Int*
Choice3Pretty -Str
Proba3 - Float
Choice4Id - Int*
Choice4Pretty -Str
Proba4 - Float
Choice5Id - Int*
Choice5Pretty -Str
Proba5 - Float
Choice6Id - Int*
Choice6Pretty -Str
Proba6 - Float
Choice7Id - Int*
Choice7Pretty -Str
Proba7 -Float
Comment - Str - A free form string column for any comments; these comments are displayed on the GUI on top of the picture
Aux1 - Field used for rollbacks on searches; to be left blank by ML algorithm
Aux2 - Field left blank and available in case new features are required in the future
Aux3 - Field left blank and available in case new features are required in the future
Aux4 - Field left blank and available in case new features are required in the future
Aux5 - Field left blank and available in case new features are required in the future
Aux6 - Field left blank and available in case new features are required in the future
Aux7 - Field left blank and available in case new features are required in the future
Aux8 - Field left blank and available in case new features are required in the future
Aux9 - Field left blank and available in case new features are required in the future
Aux10 - Field left blank and available in case new features are required in the future
xLeft - Int - Coordinates of left of detected die (in px)
yBottom - Int - Coordinates of bottom of detected die (in px)
xRight - Int - Coordinates of right of detected die (in px)
yTop - Int - Coordinates of top of detected die (in px)

Note: the formatting assumes that ML algorithms will not output more than 7 different possibilities of die for a specific picture. If more than 7 choices are offered (unlikely), the ML algorithzm should cut the numbers to 7. If less are offered, the unused fields can be left blank. The GUI will only display the top 4 options (up to "choice4" columns).

*The ID is following the formatting: X0YY, with X being the name of the die family, and YY being the number of the die among its family. X can be:
1-wheel
2-leaf
3-column
4-geometric
5-reticulate
6-arch
7-S
8-figure
The "0" separator is used as a safety in case a specific dies family reaches more than 100 shapes.
Example: A "rouelle 14" is labelled 1014; a "colonette 2" is labelled 3002




In addition to this CSV interfacing, the machine learning algorithm is called within "display.py", in the class "Init_Window", function "loadML", as well as in the module imports at the top of the "display.py" page. Should the ML algorithm change, it is recommended to change these two sections of "display.py" accordingly.
You can search for the string "HereChangeMLAlgo" in the code comments to know where to bring changes.

===============================================================================


FR

Le format attendu de la sortie des algorithmes de Machine Learning est un CSV (séparé par des point-virgules) de 36 colonnes, forrmattées comme suit:
NumTesson - Int - Numéro du tesson
NumDecor - Int - Numéro du motif
NumPhoto - Int - Numéro de référence de la photographie utilisée comme base pour l'algorithme de Machine Learning
NamePhoto - Str - Chemin et nom de la photographie (ex: "/home/user/Desktop/sherd/picture_2.jpg")
Choice1Id - Int - Identifiant du type de motif considéré comme le plus probable*
Choice1Pretty - Str - Nom du type de motif consiféré comme le plus probbale (ex: "Rouelle 3")
Proba1 - Float - Probabilité (comprise entre 0 et 1) du motif numéro 1
Choice2Id - Int - Idem pour le deuxième choix le plus probable*
Choice2Pretty - Str -Idem pour le deuxième choix le plus probable
Proba2 - Float - Idem pour le deuxième choix le plus probable
Choice3Id - Int*
Choice3Pretty -Str
Proba3 - Float
Choice4Id - Int*
Choice4Pretty -Str
Proba4 - Float
Choice5Id - Int*
Choice5Pretty -Str
Proba5 - Float
Choice6Id - Int*
Choice6Pretty -Str
Proba6 - Float
Choice7Id - Int*
Choice7Pretty -Str
Proba7 -Float
Comment - Str - Champ pouvant contenir des commentaires, affichés sur le GUI au dessus de la photo du tesson
Aux1 - Champ utilisé pour contenir le contenu en cas de retour arrière sur un poinçon déja traité (avec Ctrl+F); l'algorithme de ML doit le laisse vierge
Aux2 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux3 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux4 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux5 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux6 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux7 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux8 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux9 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
Aux10 - Champ laissé vide pour le moment, utilisable si des fonctionnalités imprévues sont à ajouter dans le futur
xLeft - Int - Pixel le plus à gauche du motif de cette entrée
yBottom - Int - Pixel le plus en bas du motif de cette entrée
xRight - Int - Pixel le plus à droite du motif de cette entrée
yTop - Int - Pixel le plus en haut du motif de cette entrée

Note: Le CSV ne contient de l'espace que pour 7 "options" de motifs détectés par photographie. Si plus de 7 choix sont présents (peu probable), il est nécessaire de réduire la sortie de l'algorithme de Machine Learning aux 7 résultats les plus probables. Si moins de 7 options sont proposées par l'algorithme, les colonnes inutilisées peuvent être laissées vides. Pour des raisons de lisibilité, le GUI affichera uniquement les 4 premières options (1-4).


*L'identifiant des motifs de poinçons suit la structure de formattage suivante: X0YY avec X le numéro de la famille de poinçon, et YY le numéro du motif au sein de la famille. X est choisi comme suit:
1-rouelle
2-palmete
3-colonette
4-géo
5-réticulé
6-arceau
7-S
8-figuratif
Le "0" est utilisé comme un champ de secours, si une famille de poinçons venait à contenir plus de 100 motifs différents.
Exemple: La "rouelle 14" possède l'identifiant 1014; la "colonette 2" possède l'identifiant 3002


En plus de l'interfaçage par CSV, la fonction principale de ML est appelée (avec ses arguments) au sein du fichier "display.py", classe "Init_Window", fonction "loadML", ainsi que dans les imports initiaux de la page py. si l'algorithme de ML venait à être modifié, ces deux portions de code de "display.py" devraient être modifiées en conséquence. Vous pouvez chercher la chaîne de caractère "HereChangeMLAlgo" dans le document pour savoir où apporter les modifications.
