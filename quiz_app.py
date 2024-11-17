import csv

# Function to load words from a CSV file
def load_words_from_csv(file_name):
    words = []
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            words.append((row[0], row[1]))  # (Korean word, English word)
    return words

# Function to format the blanks based on the word length
def format_blanks(word):
    if len(word) <= 4:
        return "_" * len(word)
    else:
        return "_" * len(word) + " " + "_" * (len(word) - len(word)//2)

# Main function for the test
def phonics_test():
    words = load_words_from_csv('phonics_words.csv')  # Load from your CSV file
    score = 0
    total_questions = len(words)
    
    print("Phonics Test! Fill in the English word for the Korean color:")
    
    for i, (korean, english) in enumerate(words, 1):
        blank = format_blanks(english)  # Format the blanks based on word length
        answer = input(f"{i}. {korean} ({blank}) = ").strip().lower()
        
        if answer == english.lower():
            score += 1
            print("Correct!")
        else:
            print(f"Wrong! The correct answer is '{english}'.")

    # Calculate the score percentage
    score_percentage = (score / total_questions) * 100
    print(f"\nYour final score is: {score}/{total_questions} ({score_percentage:.2f}%)")

    if score_percentage >= 60:
        print("Great job!")
    else:
        print("숙제")

# Run the test
phonics_test()
