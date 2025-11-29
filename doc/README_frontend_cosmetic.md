This documentation describes the process to change the tool's graphic chart, and translate it.
Note: Changing graphic chart can be done without recompiling the code, while translating requires recompilation. Feel free to contact us if you need help and advice.

TRANSLATION
The default tool suports English and French, but it is quite easy to adapt it to other languages.
If you want a language that is already supported, you can change the file /resources/data/language.conf, mostly current_language (we recommend to keep the default_language to "en" as a fallback in case there are translation issues in your language).

If you develop a translation in a language, we would strongly apppreciate that you share it with us. The language will be added in the list of supported languages, updates will be compiled with your language supported, and other users may benefit from it.

All translation is performed in the translator.py file. It contains a Python dictionnary with all classes in use. For each entry, you can add your own translation, with a prefix (e.g. ISO3166-2) that is the same for each entry. Then, recompile the code and update the /resources/data/language.conf.

Please note that UI size has been set to fit French wording. Hence, it is suggested to keep a size of message shorter or equivalent to the French version as much as possible.
Newline characters can be added with \n.




GRAPHIC CHART UPDATE
The graphic options are defined using .qss files (quite similar to CSS files) that define the style of buttons. These files are available in resources/styles/

To change the graphical style, it is recommended to copy an existing qss file, and adapt it.
Once you will have restarted the application, the new theme should be visible with a preview, under its file name, when clicking on the sun button ☀.

To change the color of the bounding boxes (squares around the die patterns) or of the ruler (used to measure picture scale), change:
-for bounding boxes, in file display.py, the global variables normalColor and highlightColor (RGB values)
-for ruler, in file main_layout.py, the global variables setLineColor and getLineColor (RGB values).

Please note that these colors have been picked to be easily distinguishable by people with various color-blindness disabilities. We strongly recommend that you pick colors patterns as recommended in https://www.nceas.ucsb.edu/sites/default/files/2022-06/Colorblind%20Safe%20Color%20Schemes.pdf
You can also take a screenshot of your layout, and paste it in websites such as https://www.color-blindness.com/coblis-color-blindness-simulator/ to ensure they are distinguishable.


To add a new font, you can download it in .otf format (of course ensure that you have the correct license rights to do so), and paste the .otf in resources/styles/fonts/. You can then load them using the syntax:
@font-face {
    font-family: "FontName";
    src: url("fonts/fontFileName.otf");
}

If your font is not properly loaded, you can check the logs.txt file for the entries:
-"Font file xxx did not load correctly."
-"Font file xxx loaded."