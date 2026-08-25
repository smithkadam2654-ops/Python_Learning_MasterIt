def main():
    print("Welcome to Mad Libs Generator!")
    print("Please provide the following words:\n")
    
    adjective1 = input("Adjective: ")
    noun1 = input("Noun: ")
    verb_past_tense = input("Verb (past tense): ")
    adverb = input("Adverb: ")
    adjective2 = input("Adjective: ")
    noun2 = input("Noun: ")
    
    story = f"""
    Once upon a time, there was a {adjective1} {noun1}.
    It {verb_past_tense} {adverb} through the forest.
    Suddenly, it saw a {adjective2} {noun2}!
    What a strange day indeed.
    """
    
    print("\nHere is your Mad Libs story:")
    print(story)

if __name__ == "__main__":
    main()
