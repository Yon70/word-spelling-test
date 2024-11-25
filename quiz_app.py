from flask import Flask, render_template, request, redirect, url_for
import json
import random

app = Flask(__name__)

# Load words from JSON
def load_words_from_json():
    with open('phonics_words.json', 'r', encoding='utf-8') as jsonfile:
        return json.load(jsonfile)

questions = load_words_from_json()

# Function to create blanks in words
def blank_word(word):
    if len(word) <= 5:
        # For words with 5 or fewer letters, create a single blank in the middle
        blank_pos = len(word) // 2
        return word[:blank_pos] + "_" + word[blank_pos + 1:]
    else:
        # For words with more than 5 letters, create two blanks, not consecutive
        blank_pos1 = len(word) // 3
        blank_pos2 = len(word) * 2 // 3
        return word[:blank_pos1] + "_" + word[blank_pos1 + 1:blank_pos2] + "_" + word[blank_pos2 + 1:]

@app.route('/')
def index():
    return redirect(url_for('quiz', question_index=0, correct_count=0, total_attempts=0))

@app.route('/quiz/<int:question_index>/<int:correct_count>/<int:total_attempts>', methods=['GET', 'POST'])
def quiz(question_index, correct_count, total_attempts):
    if request.method == 'POST':
        answer = request.form['answer'].strip().lower()
        correct_word = request.form['correct_word']
        attempt = int(request.form['attempt'])

        # Check if the answer is correct
        if answer == correct_word.lower():
            return redirect(url_for('quiz', question_index=question_index + 1, correct_count=correct_count + 1, total_attempts=total_attempts + 1))

        # If incorrect, handle second attempt or reveal answer
        if attempt == 1:
            # Show second attempt
            return render_template('quiz.html', question=questions[question_index], blanks=blank_word(questions[question_index]['word']),
                                   attempt=2, message="Try again!", correct_word=correct_word, question_index=question_index,
                                   correct_count=correct_count, total_attempts=total_attempts)
        else:
            # Show correct answer and move to next question
            return render_template('quiz.html', question=questions[question_index], blanks=blank_word(questions[question_index]['word']),
                                   attempt=0, message=f"The correct answer was '{correct_word}'. Moving to next question.",
                                   correct_word=correct_word, question_index=question_index + 1, correct_count=correct_count,
                                   total_attempts=total_attempts + 1)

    # End of questions, show results
    if question_index >= len(questions):
        correct_rate = (correct_count / total_attempts) * 100 if total_attempts > 0 else 0
        
        # Determine the message based on the score
        message = "Good job!" if correct_rate >= 70 else "숙제"
        show_retry_button = correct_rate < 70

        return render_template('result.html', correct_count=correct_count, total_attempts=total_attempts, 
                               correct_rate=int(correct_rate), message=message, show_retry_button=show_retry_button)

    # First attempt for current question
    question = questions[question_index]
    return render_template('quiz.html', question=question, blanks=blank_word(question['word']), attempt=1, message="",
                           correct_word=question['word'], question_index=question_index, correct_count=correct_count,
                           total_attempts=total_attempts)

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
