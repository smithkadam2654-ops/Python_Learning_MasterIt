MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', ' ': '/'
}

def text_to_morse(text):
    text = text.upper()
    morse_code = []
    
    for char in text:
        if char in MORSE_DICT:
            morse_code.append(MORSE_DICT[char])
        else:
            # Use a question mark for characters not in our dictionary (like punctuation)
            morse_code.append('?') 
            
    return ' '.join(morse_code)

if __name__ == "__main__":
    print("--- 📡 Morse Code Translator ---")
    user_input = input("Enter text to translate to Morse Code: ")
    morse = text_to_morse(user_input)
    print("\nResult:")
    print(morse)
