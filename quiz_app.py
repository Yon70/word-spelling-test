from flask import Flask, render_template, request

app = Flask(__name__)

words = [("노랑", "yellow"), ("파랑색", "blue"), ("빨강색", "red"), ("녹색", "green"),
         ("보라색", "purple"), ("주황색", "orange"), ("갈색", "brown"), ("분홍색", "pink"),
         ("검은색", "black"), ("흰색", "white")]

@app.route('/')
def index():
    question = words[0]  # Pick the first word for simplicity
    question_text = f"What is the English word for {question[0]}?"
    return render_template('test.html', question_text=question_text, correct_word=question[1], attempt=1, message="")

@app.route('/check_answer', methods=['POST'])
def check_answer():
    answer = request.form['answer']
    correct_word = request.form['word']
    attempt = int(request.form['attempt']) + 1  # Increment the attempt number
    
    if answer.lower() == correct_word.lower():
        message = "Correct!"
    else:
        message = f"Wrong! The correct answer is {correct_word}."
    
    if attempt <= len(words):  # Show next question if there are more
        question_text = f"What is the English word for {words[attempt-1][0]}?"
        return render_template('test.html', question_text=question_text, correct_word=words[attempt-1][1], attempt=attempt, message=message)
    else:
        # End of test - show final message or score
        score = 100 * (attempt - 1) / len(words)  # Example scoring logic
        message = f"Your final score is: {score}%"
        if score < 60:
            message += " 숙제"
        return render_template('test.html', question_text="", correct_word="", attempt=0, message=message)

if __name__ == '__main__':
    app.run(debug=True)
