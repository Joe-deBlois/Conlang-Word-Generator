from itertools import chain
from collections import Counter, defaultdict
import tempfile

#-----------------------------------------------------------
#Code for option 2; generated sentences from input strings 
#-----------------------------------------------------------

#add all sounds to the dictionary
#agglutinative morpheme segmentator
#make it output words
#make it output sentences

print("Text input rules: \n "
"-Text must be inputted as one string\n "
"-Text must be in the IPA, with periods as syllable markers and spaces as word boundaries. Seperate sentences with a tab-space\n "
"-Affricates and diphthongs must have a tie-bar above them\n "
"-This version does not support diacritics or tones\n "
"-The model will learn best with >___ words as input\n "
"-At this stage, the program will only use phonemes found in your string (it will not extrapolate and use likely novel phonemes)")

input_string = input("Please input your text here: \n")
print(input_string)

input_max_word_length = input("Please input the maximum number of syllables a word can have: \n")
input_max_word_length = int(input_max_word_length)

input_number_words = input("Please input how many words you want: \n")
input_number_words = int(input_number_words)



#  PART 1: PHONOTACTIC SYLLABIFIER--------------------------------------------------------------------------------------

#region ==PREPARE INPUT STRING ==

#for flattening lists later
def flatten_list(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten_list(item))
        else:
            flat_list.append(item)
    return flat_list

#map complex symbols so they can be read as characters
affricate_and_diphthong_mapping = {
    "d͡ʒ": "0",
    "t͡ʃ": "1", 
    "t͡s": "2",
    "d͡z": "3", 
    "p͡f" : "4", 
    "k͡x": "5", 
    "a͡ɪ":"6", 
    "e͡ɪ":"7", 
    "a͡ʊ": "8", 
    "o͡ʊ" :"9", 
    "ɔ͡ɪ": "@",
    "e͡ə": "#", 
    "ʊ͡ə": "$", 
    "u͡ɪ" : "%", 
    "i͡ʊ" : "^", 
    "ə͡ɪ" : "&", 
    "ɪ͡ə" : "*", 
    "œ͡ɪ" : "(", 
    "ʏ͡ə" : ")", 
    "œ͡ʊ" : "-", 
    "i͡ə": "+", 
    "u͡ə" : "=", 
    "y͡ə" : "`", 
    "e͡i": "[", 
    "ø͡i" :"]", 
    "ɛ͡ɪ": "<", 
    "a͡ɛ": ">", 
    "ɔ͡ə": "?"
}

def map_affricates_and_diphthongs(text):
    for aff_or_diph, replacement in affricate_and_diphthong_mapping.items():
        text = text.replace(aff_or_diph, replacement)
    return text

#map input data
input_string = map_affricates_and_diphthongs(input_string)
#endregion

#region ==DATA COLLECTION ITEMS==

words = input_string.split(" ")
word_counts = Counter(words)
raw_phonemes = list(input_string)
raw_phonemes = [p for p in raw_phonemes if p not in [" ", ".", "\t"]]
syllables = []
for word in words:
    word = word.split(".")
    syllables.append(word)
syllables = flatten_list(syllables)
syllable_structures = syllables.copy()

unique_syllables = list(set(syllables))

consonant_counts = dict()
vowel_counts = dict()
syllable_counts = dict() 
#syllable_counts ends up looking something like {'ka':3, 'pi', 2}
syllable_structure_counts = dict()
#ends up looking something like {'CV': 4, 'CVC' : 1}

#region ==DETERMINE ALL GIVEN PHONEMES==

#determine all phonemes in the input string
# Phoneme feature dictionary
# (You can easily extend this as needed — this covers most of the common IPA set.)
PHONEME_FEATURES = {
    # STOPS
    "p": {"place": "bilabial",   "manner": "stop",     "voicing": "voiceless"},
    "b": {"place": "bilabial",   "manner": "stop",     "voicing": "voiced"},
    "t": {"place": "alveolar",   "manner": "stop",     "voicing": "voiceless"},
    "d": {"place": "alveolar",   "manner": "stop",     "voicing": "voiced"},
    "ʈ": {"place": "retroflex",  "manner": "stop",     "voicing": "voiceless"},
    "ɖ": {"place": "retroflex",  "manner": "stop",     "voicing": "voiced"},
    "k": {"place": "velar",      "manner": "stop",     "voicing": "voiceless"},
    "g": {"place": "velar",      "manner": "stop",     "voicing": "voiced"},
    "q": {"place": "uvular",     "manner": "stop",     "voicing": "voiceless"},
    "ɢ": {"place": "uvular",     "manner": "stop",     "voicing": "voiced"},
    "ʔ": {"place": "glottal",    "manner": "stop",     "voicing": "voiceless"},

    # NASALS
    "m":   {"place": "bilabial",   "manner": "nasal",    "voicing": "voiced"},
    "ɱ":   {"place": "labiodental","manner": "nasal",    "voicing": "voiced"},
    "n":   {"place": "alveolar",   "manner": "nasal",    "voicing": "voiced"},
    "ɳ":   {"place": "retroflex",  "manner": "nasal",    "voicing": "voiced"},
    "ŋ":   {"place": "velar",      "manner": "nasal",    "voicing": "voiced"},
    "ɲ":   {"place": "palatal",    "manner": "nasal",    "voicing": "voiced"},
    "ɴ":   {"place": "uvular",     "manner": "nasal",    "voicing": "voiced"},

    # FRICATIVES
    "ɸ":  {"place": "bilabial",     "manner": "fricative", "voicing": "voiceless"},
    "β":  {"place": "bilabial",     "manner": "fricative", "voicing": "voiced"},
    "f":  {"place": "labiodental",  "manner": "fricative", "voicing": "voiceless"},
    "v":  {"place": "labiodental",  "manner": "fricative", "voicing": "voiced"},
    "θ":  {"place": "dental",       "manner": "fricative", "voicing": "voiceless"},
    "ð":  {"place": "dental",       "manner": "fricative", "voicing": "voiced"},
    "s":  {"place": "alveolar",     "manner": "fricative", "voicing": "voiceless"},
    "z":  {"place": "alveolar",     "manner": "fricative", "voicing": "voiced"},
    "ʂ":  {"place": "retroflex",    "manner": "fricative", "voicing": "voiceless"},
    "ʐ":  {"place": "retroflex",    "manner": "fricative", "voicing": "voiced"},
    "ʃ":  {"place": "postalveolar", "manner": "fricative", "voicing": "voiceless"},
    "ʒ":  {"place": "postalveolar", "manner": "fricative", "voicing": "voiced"},
    "x":  {"place": "velar",        "manner": "fricative", "voicing": "voiceless"},
    "ɣ":  {"place": "velar",        "manner": "fricative", "voicing": "voiced"},
    "χ":  {"place": "uvular",       "manner": "fricative", "voicing": "voiceless"},
    "ʁ":  {"place": "uvular",       "manner": "fricative", "voicing": "voiced"},
    "ħ":  {"place": "pharyngeal",   "manner": "fricative", "voicing": "voiceless"},
    "ʕ":  {"place": "pharyngeal",   "manner": "fricative", "voicing": "voiced"},
    "h":  {"place": "glottal",      "manner": "fricative", "voicing": "voiceless"},
    "ɦ":  {"place": "glottal",      "manner": "fricative", "voicing": "voiced"},

    # APPROXIMANTS
    "j":  {"place": "palatal",        "manner": "approximant", "voicing": "voiced"},
    "ɹ":  {"place": "alveolar",       "manner": "approximant", "voicing": "voiced"},
    "ɻ":  {"place": "retroflex",      "manner": "approximant", "voicing": "voiced"},
    "w":  {"place": "labio-velar",    "manner": "approximant", "voicing": "voiced"},
    "ɥ":  {"place": "labio-palatal",  "manner": "approximant", "voicing": "voiced"},
    "ʍ":  {"place": "labio-velar",    "manner": "approximant", "voicing": "voiceless"},

    # LATERAL APPROXIMANTS
    "l":  {"place": "alveolar",      "manner": "lateral-approximant", "voicing": "voiced"},
    "ɭ":  {"place": "retroflex",     "manner": "lateral-approximant", "voicing": "voiced"},
    "ʎ":  {"place": "palatal",       "manner": "lateral-approximant", "voicing": "voiced"},
    "ʟ":  {"place": "velar",         "manner": "lateral-approximant", "voicing": "voiced"},

    # TRILLS AND FLAPS
    "r":   {"place": "alveolar",     "manner": "trill",         "voicing": "voiced"},
    "ʙ":   {"place": "bilabial",     "manner": "trill",         "voicing": "voiced"},
    "ʀ":   {"place": "uvular",       "manner": "trill",         "voicing": "voiced"},
    "ɾ":   {"place": "alveolar",     "manner": "flap",          "voicing": "voiced"},
    "ɽ":   {"place": "retroflex",    "manner": "flap",          "voicing": "voiced"},

    # AFFRICATES (mapped versions)
    "0": {"place": "postalveolar", "manner": "affricate", "voicing": "voiced"},    # d͡ʒ
    "1": {"place": "postalveolar", "manner": "affricate", "voicing": "voiceless"}, # t͡ʃ
    "2": {"place": "alveolar",     "manner": "affricate", "voicing": "voiceless"}, # t͡s
    "3": {"place": "alveolar",     "manner": "affricate", "voicing": "voiced"},    # d͡z

    # VOWELS
        # FRONT VOWELS
    "i":  {"height": "close",       "backness": "front",   "rounded": False},
    "y":  {"height": "close",       "backness": "front",   "rounded": True},
    "ɪ":  {"height": "near-close",  "backness": "front",   "rounded": False},
    "ʏ":  {"height": "near-close",  "backness": "front",   "rounded": True},
    "e":  {"height": "close-mid",   "backness": "front",   "rounded": False},
    "ø":  {"height": "close-mid",   "backness": "front",   "rounded": True},
    "ɛ":  {"height": "open-mid",    "backness": "front",   "rounded": False},
    "œ":  {"height": "open-mid",    "backness": "front",   "rounded": True},
    "æ":  {"height": "near-open",   "backness": "front",   "rounded": False},

    # CENTRAL VOWELS
    "ɨ":  {"height": "close",       "backness": "central", "rounded": False},
    "ʉ":  {"height": "close",       "backness": "central", "rounded": True},
    "ɘ":  {"height": "close-mid",   "backness": "central", "rounded": False},
    "ɵ":  {"height": "close-mid",   "backness": "central", "rounded": True},
    "ə":  {"height": "mid",         "backness": "central", "rounded": False},
    "ɜ":  {"height": "open-mid",    "backness": "central", "rounded": False},
    "ɞ":  {"height": "open-mid",    "backness": "central", "rounded": True},
    "ɐ":  {"height": "near-open",   "backness": "central", "rounded": False},
    "a":  {"height": "open",        "backness": "front",   "rounded": False},
    "ɶ":  {"height": "open",        "backness": "front",   "rounded": True},

    # BACK VOWELS
    "ɯ":  {"height": "close",       "backness": "back",    "rounded": False},
    "u":  {"height": "close",       "backness": "back",    "rounded": True},
    "ɤ":  {"height": "close-mid",   "backness": "back",    "rounded": False},
    "o":  {"height": "close-mid",   "backness": "back",    "rounded": True},
    "ʌ":  {"height": "open-mid",    "backness": "back",    "rounded": False},
    "ɔ":  {"height": "open-mid",    "backness": "back",    "rounded": True},
    "ɑ":  {"height": "open",        "backness": "back",    "rounded": False},
    "ɒ":  {"height": "open",        "backness": "back",    "rounded": True},

    

    # CLICKS 
    "ʘ": {"place": "bilabial",      "manner": "click",    "voicing": "voiceless"},
    "ǀ": {"place": "dental",        "manner": "click",    "voicing": "voiceless"},
    "ǃ": {"place": "post-alveolar","manner": "click",    "voicing": "voiceless"},
    "ǂ": {"place": "palato-alveolar","manner":"click",   "voicing": "voiceless"},
    "ǁ": {"place": "alveolar lateral","manner":"click", "voicing": "voiceless"},
}

# Initialize classification containers
stops, nasals, trills, flaps, fricatives = [], [], [], [], []
approximants, lateral_approximants = [], []
affricates, voiced, voiceless = [], [], []
consonants, vowels = [], []
bilabials, alveolars, velars, palatals, glottals, uvulars = [], [], [], [], [], []
front, central, back, high, mid, low, rounded, unrounded = [], [], [], [], [], [], [], []
diphthongs = []  
clicks = []

# Classify each phoneme
for char in set(raw_phonemes):
    if char not in PHONEME_FEATURES:
        continue
    feats = PHONEME_FEATURES[char]

    # Consonant handling
    if "manner" in feats:
        consonants.append(char)
        manner = feats["manner"]
        place = feats["place"]
        voice = feats["voicing"]

        if manner == "stop": stops.append(char)
        elif manner == "nasal": nasals.append(char)
        elif manner == "fricative": fricatives.append(char)
        elif manner == "trill": trills.append(char)
        elif manner == "flap": flaps.append(char)
        elif manner == "approximant": approximants.append(char)
        elif manner == "lateral-approximant": lateral_approximants.append(char)
        elif manner == "affricate": affricates.append(char)
        elif manner == "click": clicks.append(char)

        if voice == "voiced": voiced.append(char)
        else: voiceless.append(char)

        # Places of articulation
        if place == "bilabial": bilabials.append(char)
        elif place == "alveolar": alveolars.append(char)
        elif place == "palatal": palatals.append(char)
        elif place == "velar": velars.append(char)
        elif place == "uvular": uvulars.append(char)
        elif place == "glottal": glottals.append(char)

    # Vowel handling
    elif "height" in feats:
        vowels.append(char)
        height = feats["height"]
        backness = feats["backness"]
        roundness = feats["rounded"]

        if height == "high": high.append(char)
        elif height == "mid": mid.append(char)
        elif height == "low": low.append(char)

        if backness == "front": front.append(char)
        elif backness == "central": central.append(char)
        elif backness == "back": back.append(char)

        if roundness: rounded.append(char)
        else: unrounded.append(char)
    elif char not in PHONEME_FEATURES: 
        continue

# Finalize full phoneme inventory
phoneme_inventory = list(set(consonants + vowels))
#endregion


#Map number of vowels and consonants to those consonants
for char in input_string:
    if char in vowels:
        if char not in vowel_counts:
            vowel_counts[char] = 1
        else:
            vowel_counts[char]+= 1
    if char in consonants:
        if char not in consonant_counts:
            consonant_counts[char] = 1
        else:
            consonant_counts[char]+= 1

#endregion 

#region ==DETERMINE ALL GIVEN SYLLABLES==

#Determine all syllables in C/V form
for i, syllable in enumerate(syllable_structures):
    structure = ""
    for char in syllable:
        if char in consonants:
            structure += "C"
        else:
            structure += "V"
    syllable_structures[i] = structure

#Map syllables to their counts
for syllable in syllables:
    if syllable not in syllable_counts:
        syllable_counts[syllable] = 1
    else:
        syllable_counts[syllable]+= 1

#Map syllable structures (i.e. C/V form syllables) to their counts
for structure in syllable_structures:
    if structure not in syllable_structure_counts:
        syllable_structure_counts[structure] = 1
    else:
        syllable_structure_counts[structure] +=1
    
#endregion

#PART 2: MORPHEME SEGMENTOR-------------------------------------------------------------------------------------

#region == MORPHOLOGICAL SEGMENTATION ==

#look for repeated syllables
#are they at the start, end, or middle?
#repeated ones in the middle are probably nouns, start/end are probably affixes
#given these, do the saved segments appear anywhere else in any other words?
#for each word add the first syllable to "prefixes", last syllable to , etc..
#different section for different types of language? Start with agglutinating 
#look for repeated syllables across words and classify based on distribution patterns. 








































































#assuming it segments based on syllables
syllable_segmentation = []
for word in words:
    syllable_segmentation.append(word.split("."))



morphological_typology = input("Is your language Isolating (1), Agglutinative (2), Fusional (3), or Polysynthetic(4)? \n")


if morphological_typology == "2":
    prefix_candidates = defaultdict(int)
    suffix_candidates = defaultdict(int)
    root_candidates = defaultdict(int)
    prefix_or_suffix_candidates = defaultdict(int)
    prefix_or_root_candidates = defaultdict(int)
    root_or_suffix_candidates = defaultdict(int)
    anywhere_candidates = defaultdict(int)
    stand_alone = defaultdict(int)


    for word in syllable_segmentation:
        if len(word) == 1: 
            stand_alone[word[0]] += 1
            continue
        prefix = word[0]
        suffix = word[-1]

        prefix_candidates[prefix] += 1
        suffix_candidates[suffix] += 1
        #root(s): anything between prefix and suffix
        if len(word) > 2:
            roots = word[1:-1]
        else:
            roots = word[1:-1]  # Will be empty if only 2 morphemes

        for root in roots:
            root_candidates[root] += 1

    # Make a list to avoid RuntimeError due to dict size change during iteration
    for key in list(prefix_candidates):
    
        if key in suffix_candidates and root_candidates:
            anywhere_candidates[key] = prefix_candidates[key] + suffix_candidates[key] + root_candidates[key]
            del prefix_candidates[key]
            del suffix_candidates[key]
            del root_candidates[key]
    
        if key in suffix_candidates:
            prefix_or_suffix_candidates[key] = prefix_candidates[key] + suffix_candidates[key]
            del prefix_candidates[key]
            del suffix_candidates[key]
    
        elif key in root_candidates:
            prefix_or_root_candidates[key] = prefix_candidates[key] + root_candidates[key]
            del prefix_candidates[key]
            del root_candidates[key]

    # Now check root vs suffix
    for key in list(root_candidates):
    
        if key in suffix_candidates:
            root_or_suffix_candidates[key] = root_candidates[key] + suffix_candidates[key]
            del root_candidates[key]
            del suffix_candidates[key]
#endregion


#region ==MORPHEME RULES ===

# r = root, p = prefix, s = suffix, rs = root/suffix, pr = prefix/root, ps = prefix/suffix, sa = stand alone, aw = anywhere

if morphological_typology == "1": #isolating
    word_structures = ["sa", "aw", "r"]
elif morphological_typology =="2":    #agglutinative
    word_structures = ["p+r", "r+s", "p+r+s", "r+rs", "p+rs", "rs+s","p+aw", "aw+s", "p+aw+s"]
elif morphological_typology =="3": #fusional
    word_structures = ["sa", "r", "aw","p+r", "r+s", "p+r+s","p+rs", "r+rs", "rs+s","p+pr", "pr+s","r+ps", "ps", "pr", "rs"]
elif morphological_typology == "4": #polysynthetic
    word_structures = ["sa", "r", "aw","p+r", "r+s", "p+r+s","p+aw", "aw+s", "p+aw+s", "aw+aw","p+pr", "pr+s", "p+rs", "rs+s", "p+p+r", "r+r","p+r+r","p+r+s+s","p+p+r+s","p+r+s+s+s", "p+aw+r+aw+s","p+r+aw+aw+s","p+pr+r+s","p+r+rs+s","p+n+r+s", "p+n+v+s","p+aw+n+v+s+s","aw+p+r+s+aw"]
        

#endregion

#PART 3: WORD GENERATOR--------------------------------------------------------------------------------------------
#What do we have to consider?
#User specs: max word length in input_max_word_length, words required in input_number_words
#Phonology data: all consonants/vowels, their frequency, 
#Syllable data: all valid syllable structures in unique_syllables
#Morphology: morphological_typology, as well as what morphemes can fit into that structure. 
#Extrapolations: valid syllables based on phoneme frequency and unique_syllables, valid morphemes based on valid syllables. Use a mix of pre-defined and generated sounds for new words? Weights for more probable sounds/syllables



#Add stress patterns and phonotactics design later



#all variables: 


