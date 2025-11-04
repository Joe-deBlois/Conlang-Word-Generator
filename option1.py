#%%

import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
import random


#-------------------------------------------------------
#Code for option 1; generated words from selected sounds
#-------------------------------------------------------

#possible next steps; make look nicer? Make a popup window with an IPA-chart style image where users can select phonemes, or a textbox for them to insert their own.





#region === Phoneme Collection ===
# List of IPA characters (add more as needed)
ipa_cons = [["p", "b", "t", "d", "ʈ", "ɖ", "c", "ɟ", "k", "ɡ", "q", "ɢ", "ʔ"], ["m", "ɱ", "n", "ɳ", "ɲ", "ŋ", "ɴ"], ["ʙ", "r", "ʀ"], ["ⱱ", "ɾ", "ɽ"], ["ɸ", "β", "f", "v", "θ", "ð", "s", "z", "ʃ","ʒ", "ʂ", "ʐ", "ç", "ʝ", "x", "ɣ", "χ", "ʁ", "ħ", "ʕ", "h","ɦ"], ["ɬ", "ɮ"], ["ʋ", "ɹ", "ɻ", "j", "ɰ"], ["l", "ɭ", "ʎ", "ʟ"]]
ipa_vowels = ["i", "y", "ɨ", "ʉ", "ɯ", "u", "ɪ", "ʏ", "ʊ", "e", "ø","ɘ", "ɵ", "ɤ", "o", "ə", "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ", "æ", "ɐ", "a", "ɶ", "ɑ", "ɒ"]
ipa_clicks = ["ʘ", "ǀ", "ǃ", "ǂ", "ǁ"]
ipa_affricates = ["d͡ʒ", "t͡ʃ", "t͡s","d͡z", "p͡f", "k͡x"]
ipa_other = ["pʼ", "tʼ", "kʼ", "sʼ", "ɧ", "ɕ", "ʑ", "ʍ", "w", "ɥ", "ʜ", "ʢ", "ʡ"]

#p’,p,t’,t,ʈ’,ʈ,k’,k,hn̥,hm̥,hŋ̥,ɸ,f,θ,s,ʃ,ʂ,x,ɧ,ǀ,!,ǂ,‖,ḁ͡ɪ,i̥,ɪ̥,u̥,ʊ̥,o̥͡ɪ,ə̥,ḁ͡ɪ˥˩,i̥˥˩,ɪ̥˥˩,u̥˥˩,ʊ̥˥˩,o̥͡ɪ˥˩,ə̥˥˩,ḁ͡ɪ˩˥,i̥˩˥,ɪ̥˩˥,u̥˩˥,ʊ̥˩˥,o̥͡ɪ˩˥,ə̥˩˥

print("Text input rules: \n "
"-Text must be inputted as one string, commas seperating each phoneme, with no spaces\n "
"-This version does not support diacritics or tones\n "
"-At this stage, the program will only use phonemes found in your string (it will not extrapolate and use likely novel phonemes)")

selected_phonemes = input("Please input your phonemes here: \n")

selected_phonemes = selected_phonemes.split(",")
selected_cons = []
selected_vowels = []

for phoneme in selected_phonemes: 
    for vowel in ipa_vowels: 
        if vowel in phoneme: 
            selected_vowels.append(phoneme)
    if phoneme not in selected_vowels and phoneme not in ["", " ", ",", ".", "'"]: #in case there is 
        selected_cons.append(phoneme)









#region === Valid Syllables ===
# number of syllables per word
selected_syllable_structures_num = input("Please select valid syllables, formatting your answer as a comma-seperated list: \nV : 1, \nCV: 2, \nVC: 3, \nCVC: 4, \nCCV: 5, \nCCVC: 6, \nCCCV: 7, \nCCCVC: 8, \nCVCC: 9, \nCCVCC: 10, \nCCCVCC: 11, \nCVCCC: 12, \nCCCVCCC: 13, \nVCC: 14, \nCCCCVCCCC: 15")
selected_syllable_structures_num = selected_syllable_structures_num.split(",")

syllable_structure_mapping = {
    "1": "V",
    "2": "CV",
    "3": "VC",
    "4": "CVC",
    "5": "CCV",
    "6": "CCVC",
    "7": "CCCV",
    "8": "CCCV C",
    "9": "CVCC",
    "10": "CCVCC",
    "11": "CCCVCC",
    "12": "CVCCC",
    "13": "CCCVCCC",
    "14": "VCC",
    "15": "CCCCVCCCC"
}


#1,2,3,4,5,6,9,14
selected_syllable_structures = [] 

def map_nums_to_syllables(ls):
    for num in ls: 
        selected_syllable_structures.append(syllable_structure_mapping[num])

map_nums_to_syllables(selected_syllable_structures_num)




 #endregion




#frequencies
#assign a frequency to each phoneme (make bars later)
#https://kapernikov.com/ipywidgets-with-matplotlib/

frequency_of_cons = {con: 0 for con in selected_cons}
frequency_of_vowels = {vowel:0 for vowel in selected_vowels}
frequency_of_syllables = {syll: 0 for syll in selected_syllable_structures}

def determine_frequencies(frequency_dict, label = "Phonemes"): 
    """
    Provide the user with interactive frequency bars for each phoneme in the list
    Normalize when user clicks "finish"
    """
 
    local_phonemes = list(frequency_dict.keys())
    if not local_phonemes:
        print(f"No {label.lower()} selected.")
        return
    
    #initial frequency is equal for all phonemes
    average = 100/len(local_phonemes)

    #prepare a dictionary to store sliders
    #like {'b': FloatSlider(...), 'c': FloatSlider(...), etc.}
    sliders = {
        ph:widgets.FloatSlider(
            value = average, 
            min = 0, 
                max = 100, 
                step = 0.1, 
                description = ph, 
                continuous_update = False
        )
        for ph in local_phonemes
    }

    output = widgets.Output()

    # Button to finish editing
    finish_button = widgets.Button(description="✅ Finish", button_style="success")


    def normalize_and_plot(change = None):
        """ Normalize values once user clicks 'finish'"""

        #get current values
        values = [sl.value for sl in sliders.values()]
        total = sum(values)
        normalized = [(v / total) * 100 if total > 0 else 100/len(values) for v in values]

        for ph, val in zip(local_phonemes, normalized):
            frequency_dict[ph] = val

        with output:
            output.clear_output(wait=True)
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.bar(local_phonemes, normalized, color='cornflowerblue')
            ax.set_ylim(0, 100)
            ax.set_ylabel('Frequency (%)')
            ax.set_title(f'{label} Frequencies (Normalized)')
            plt.show()
        print(f"{label} frequencies saved and normalized.")

    finish_button.on_click(normalize_and_plot)

    box = widgets.VBox(list(sliders.values()) + [finish_button, output])
    display(box)

determine_frequencies(frequency_of_cons, label="Consonant")
determine_frequencies(frequency_of_vowels, label="Vowel")
determine_frequencies(frequency_of_syllables, label = "Syllables")


print("Please adjust sliders and click 'Finish' for all categories before generating words.")






#%%
#region === User Specifications and Output ===
max_length = int(input("What is the maximum possible length of a word, in syllables?\n"))

num_words = int(input("How many words do you want outputted?\n"))


words = []
for i in range(num_words):
    #randomly select number of syllables
    num_syllables = random.choice(range(1, max_length+1))
    print(num_syllables)

    #randomly select which syllables & place syllable markers
    word_structure = []
    for i in range(num_syllables):
        if i > 0 and i < num_syllables:
            word_structure.append(".")
            word_structure.append(random.choices(list(frequency_of_syllables.keys()), weights = list(frequency_of_syllables.values()), k = 1))
        else: 
            word_structure.append(random.choices(list(frequency_of_syllables.keys()), weights = list(frequency_of_syllables.values()), k = 1))
            
    print(word_structure)

    #randomly select which consonants take the place of C
    word_breakdown = []
    for syllablelist in word_structure: 
        if syllablelist == ".":
            word_breakdown.append(".")
        else: 
            for syllable in syllablelist: 
                for character in syllable:
                    if character == "C":
                        word_breakdown.append(random.choices(list(frequency_of_cons.keys()), weights = list(frequency_of_cons.values()), k = 1))
                    if character == "V":
                        word_breakdown.append(random.choices(list(frequency_of_vowels.keys()), weights = list(frequency_of_vowels.values()), k = 1))
    print(word_breakdown)

    def flatten_list(nested_list):
        flat_list = []
        for item in nested_list:
            if isinstance(item, list):
                flat_list.extend(flatten_list(item))
            else:
                flat_list.append(item)
        return flat_list
    flat_word_breakdown = flatten_list(word_breakdown)
    print(flat_word_breakdown)
    
    word = "".join(flat_word_breakdown)
    print(word)
    
    words.append(word)

#save "words" as a plaintext file
with open("words.txt", "w", encoding="utf-8") as f:
    for word in words:
        f.write(word + "\n")

