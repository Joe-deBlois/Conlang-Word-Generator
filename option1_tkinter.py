import tkinter as tk

#to do: 
#formatting the tkinter interface (change size when window size changes, scroll bar? )
#figure out the probability formula for creating words.


#-------------------------------------------------------
#Code for option 1; generated words from selected sounds
#-------------------------------------------------------


#region === IPA Characters ===
# List of IPA characters (add more as needed)
ipa_cons = [["p", "b", "t", "d", "ʈ", "ɖ", "c", "ɟ", "k", "ɡ", "q", "ɢ", "ʔ"], ["m", "ɱ", "n", "ɳ", "ɲ", "ŋ", "ɴ"], ["ʙ", "r", "ʀ"], ["ⱱ", "ɾ", "ɽ"], ["ɸ", "β", "f", "v", "θ", "ð", "s", "z", "ʃ","ʒ", "ʂ", "ʐ", "ç", "ʝ", "x", "ɣ", "χ", "ʁ", "ħ", "ʕ", "h","ɦ"], ["ɬ", "ɮ"], ["ʋ", "ɹ", "ɻ", "j", "ɰ"], ["l", "ɭ", "ʎ", "ʟ"]]
ipa_vowels = [["i", "y", "ɨ", "ʉ", "ɯ", "u"], ["ɪ", "ʏ", "ʊ"], ["e", "ø","ɘ", "ɵ", "ɤ", "o"], ["ə"], ["ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ"], ["æ", "ɐ"], ["a", "ɶ", "ɑ", "ɒ"]]
ipa_clicks = ["ʘ", "ǀ", "ǃ", "ǂ", "ǁ"]
ipa_affricates = ["d͡ʒ", "t͡ʃ", "t͡s","d͡z", "p͡f", "k͡x"]
ipa_other = ["pʼ", "tʼ", "kʼ", "sʼ", "ɧ", "ɕ", "ʑ", "ʍ", "w", "ɥ", "ʜ", "ʢ", "ʡ"]

#endregion

#region === State Management () ===
# List to hold clicked characters
selected_chars = []

#probabilities
probabilities = {}
bars = {}
updating_bars = False 
#endregion

#region === Select/Click IPA symbol Method ===
def selection_click(char):
    if char in selected_chars:
        selected_chars.remove(char)
        probabilities.pop(char, None)
    else:
        selected_chars.append(char)
    probabilities[char] = 100/len(selected_chars)
    update_bars()
    display_label.config(text='Sounds in the language: ' + ''.join(selected_chars))
    # Save
    with open("selected_ipa.txt", "w", encoding="utf-8") as f:
        for c in selected_chars:
            f.write(f"{c}: {probabilities[c]:.2f}%\n")
#endregion

#region === IPA Selection and Frequency Bars ===
# Create main window and title for window
window = tk.Tk()
window.title("Interactive IPA Chart")

# Display label
display_label = tk.Label(window, text= "Select the sounds in your conlang.")
display_label = tk.Label(window, text="Selected: ")
display_label.pack(pady=10)

#endregion

#region === Buttons and Associated Labels ===
# Create buttons for each IPA character
#"command = ..." tells the button what to do when clicked
#"lambda c=char: selection_click(c)" freezes the current character in the loop so it gets passed to the function correctly
button_frame = tk.Frame(window)
button_frame.pack()


def show_buttons(char_list, start_row):
    """shows the buttons of all components for the IPA chart"""
    if char_list == ipa_cons:
        title = "Consonants"
    if char_list == ipa_vowels:
        title = "Vowels"
    if char_list == ipa_clicks:
        title = "Clicks"
    if char_list == ipa_affricates:
        title = "Affricates"
    if char_list == ipa_other:
        title = "Other Phonemes"

        
    # Add section title label
    section_label = tk.Label(button_frame, text=title, font=("Arial", 12, "bold"))
    section_label.grid(row=start_row, column=0, columnspan=10, pady=(10, 0), sticky="w")
    start_row += 1  # Move down to start placing buttons
    
    if not char_list:
        return start_row

    for row_index, row in enumerate(char_list):
        for col_index, char in enumerate(row):
            btn = tk.Button(button_frame, text=char, width=4, height=2, font = (16),
                            command=lambda c=char: selection_click(c))
            btn.grid(row=start_row + row_index, column=col_index, padx=2, pady=2)

    return start_row + len(char_list)  # move down by number of rows added

next_row = 0
next_row = show_buttons(ipa_cons, next_row)
next_row = show_buttons(ipa_vowels, next_row)
next_row = show_buttons(ipa_clicks, next_row)
#endregion 

#region === Bars and Associated Methods and Labels === 
def update_bars():
    # Clear old bars
    for widget in bars_frame.winfo_children():
        widget.destroy()
    bars.clear()
    
    for i, char in enumerate(selected_chars):
        scale = tk.Scale(bars_frame, from_=100, to=0, orient='vertical', length=150, label=char,
                         command=lambda val, c=char: on_bar_change(c, float(val)))
        scale.set(probabilities.get(char, 0))
        scale.grid(row=0, column=i, padx=0)
        bars[char] = scale

#Display bars using Tkinter scale vertically
bars_frame = tk.Frame(window)
bars_frame.pack(pady = 10)

#Handle scale changes by user and keep total = 100
def on_bar_change(char, new_val):
    #this little segment ensures that editing any probability bar will redistribute the values of ALL OTHERS
    global updating_bars
    if updating_bars:
        return
    
    old_val = probabilities[char]
    diff = new_val - old_val
    probabilities[char] = new_val
    
    others = [c for c in probabilities if c != char]
    total_others = sum(probabilities[c] for c in others)
    
    # Prevent negative or > 100 total
    if total_others - diff <= 0:
        # Set others to zero, char to 100
        for c in others:
            probabilities[c] = 0
        probabilities[char] = 100
    else:
        # Adjust others proportionally to keep sum 100
        for c in others:
            # reduce/increase others by ratio
            probabilities[c] = probabilities[c] - (diff * (probabilities[c] / total_others))
    
    # Normalize: make sure total == 100
    total = sum(probabilities.values())
    if total != 100:
        correction = 100 - total
        # Spread correction proportionally over all bars (including the one changed)
        for c in probabilities:
            probabilities[c] += correction * (probabilities[c] / total)
    
    # Update the scales to reflect new values
    for c in probabilities:
        if c != char:
            bars[c].set(round(probabilities[c], 2))
    updating_bars = False
#endregion




#region === Valid Syllables ===
# number of syllables per word
 #have user select from structures = ["V", "CV", "VC", "CVC", "CCV", "CCVC", "CCCV", "CCCVC", "CVCC", "CCVCC", "CCCVCC", "CVCCC", "CCCVCCC", "VCC", "CCCCVCCCC"] and their frequencies

 #endregion


#region === User Specifications and Output ===

#User specifies number of words, max/min length of any word
#Program outputs plaintext file of randomly generated words seperated by \n

#endregion



# Start app
window.mainloop()
