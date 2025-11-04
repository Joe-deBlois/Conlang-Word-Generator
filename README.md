This is a program for conlangers that randomly generates feasible words given some user input. 

app-initialization.py should be run first; it prompts the user to select between options 1 or 2. 

If option 1 is selected, option1.py will automatically run. This program has two "cells". 
* In the first cell, the user will insert the IPA characters they want in their words and possible syllable structures. Then they will play with sliders to choose the frequency of each phoneme and each syllable structure. These frequencies are initialized with equal allocation, and after the user has moved the sliders and clicked the "finish" button, the frequencies are normalized between 0-100. 
* In the second cell, the user will specify the number of words desired and the maximum length of any word. 
* Finally, the program will output a plaintext file of words chosen via weighted random selection 

If option 2 is selected, option2.py will automatically run. 
* All the user has to do for this program is input words or a sentence from their conlang, max word length, and the number of words they want. The program specifies some rules on how these words should be inputted. 
* The program begins by gathering data on the inputted string's phonemes (e.g. manner of articulation and counts) and syllables (in IPA form and C/V form). This is done in the Phonotactic Syllabifier section.
* Next the words are run though a Morphological Segmentor. This classifies each syllable as a prefix, suffix, root, floating morpheme, stand-alone morpheme (such as an article or determiner in English), or more flexible morphemes like prefix/root, prefix/suffix, or root/suffix. Given user input, it also assigns which combinations of these segments are valid based on the language's morphological typology. 
* Lastly, all of the collected information is run through the Word Generator. Using frequencies and weights, the program utilizes old morphemes and generates new ones to create novel words for your conlang!
