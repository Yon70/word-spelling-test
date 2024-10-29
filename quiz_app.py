import csv
import random

def load_words(file_name):
    words = {}
    with open(file_name, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            words[row['word']] = row['meaning']
    return words

def generate_quiz(words):
    quiz_words = random.sample(list(words.items()), len(words))
    score = 0
    
    for word, meaning in quiz_words:
        # Determine the number of blanks
        if len(word) <= 4:
            blanks = '_ ' * len(word)
        else:
            blanks = '_ ' * (len(word) - 1)  # For longer words, keep one letter visible

        print(f"Meaning: {meaning}")
        print(f"Spell the word: {blanks.strip()}")

        answer = input("Your answer: ")
        if answer.lower() == word.lower():
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {word}")
        print()

    print(f"Your final score is: {score}/{len(words)}")

if __name__ == "__main__":
    words = load_words('words.csv')
    generate_quiz(words)
