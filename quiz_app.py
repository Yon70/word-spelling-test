from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 시험 단어와 한국어 뜻
words = [
    {"word": "yellow", "meaning": "노랑"},
    {"word": "blue", "meaning": "파랑색"},
    {"word": "red", "meaning": "빨강색"},
    {"word": "green", "meaning": "녹색"},
    {"word": "purple", "meaning": "보라색"},
    {"word": "orange", "meaning": "주황색"},
    {"word": "brown", "meaning": "갈색"},
    {"word": "pink", "meaning": "분홍색"},
    {"word": "black", "meaning": "검은색"},
    {"word": "white", "meaning": "흰색"}
]

# 빈칸 포함된 단어 생성 함수
def create_blank(word):
    if len(word) <= 3:
        return word[0] + "_" + word[2:]
    else:
        return word[0] + "_" * (len(word) - 2) + word[-1]

# 현재 진행 중인 시험 문제
current_question_index = 0

@app.route('/')
def index():
    global current_question_index
    question = words[current_question_index]
    question_text = f"{create_blank(question['word'])}: {question['meaning']}"
    return render_template("index.html", question_text=question_text, correct_word=question["word"], attempt=1, message="")

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global current_question_index
    user_answer = request.form['answer'].lower()
    correct_word = request.form['word']
    attempt = int(request.form['attempt'])

    if user_answer == correct_word:
        message = "Correct!"
        current_question_index = (current_question_index + 1) % len(words)
    else:
        if attempt < 2:
            message = "Incorrect. Try again!"
            return render_template("index.html", question_text=f"{create_blank(correct_word)}: {words[current_question_index]['meaning']}", correct_word=correct_word, attempt=attempt + 1, message=message)
        else:
            message = f"Incorrect. The correct answer was '{correct_word}'. Moving to the next word."
            current_question_index = (current_question_index + 1) % len(words)

    # 다음 문제로 이동
    next_question = words[current_question_index]
    question_text = f"{create_blank(next_question['word'])}: {next_question['meaning']}"
    return render_template("index.html", question_text=question_text, correct_word=next_question["word"], attempt=1, message=message)

if __name__ == '__main__':
    app.run(debug=True)
