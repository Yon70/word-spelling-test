from flask import Flask, render_template, request
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Google Sheets API 인증 설정
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]
SERVICE_ACCOUNT_FILE = '/path/to/your/service-account-file.json'  # 서비스 계정 파일 경로
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(credentials)

# Google Sheets 열기
answer_sheet = client.open("Answer Sheet")  # 정답을 담고 있는 시트
response_sheet = client.open("Student Responses")  # 학생의 응답을 기록할 시트
answer_worksheet = answer_sheet.get_worksheet(0)  # 첫 번째 시트 (정답이 들어있는 시트)
response_worksheet = response_sheet.get_worksheet(0)  # 학생 응답 시트

# 정답을 Google Sheets에서 가져오기
correct_answers = [row[1] for row in answer_worksheet.get_all_values()[1:]]  # 첫 번째 열은 질문 번호, 두 번째 열은 정답

# 시험 단어 및 번역 (정답 배열을 기반으로)
words = [{"word": correct_answers[i], "meaning": f"번역 {i+1}"} for i in range(len(correct_answers))]

# 초기 상태 변수
current_question_index = 0
correct_answers_count = 0
test_complete = False

@app.route('/')
def index():
    global current_question_index, test_complete
    if test_complete:
        return "The test is complete. Thank you for participating!"
    
    question = words[current_question_index]
    question_text = f"Question {current_question_index + 1}: {question['meaning']}"
    
    return render_template("index.html", question_text=question_text, correct_word=question["word"], attempt=1, message="")

@app.route('/check_answer', methods=['POST'])
def check_answer():
    global current_question_index, correct_answers_count, test_complete
    user_answer = request.form['answer'].lower()
    correct_word = request.form['word']

    # 답이 맞으면 정답 카운트 증가
    if user_answer == correct_word:
        correct_answers_count += 1

    current_question_index += 1
    if current_question_index >= len(words):
        # 점수 계산
        score = (correct_answers_count / len(words)) * 100
        result = "Passed" if score >= 70 else "Failed"

        student_id = request.form.get('student_id', 'Unknown')
        student_name = request.form.get('student_name', 'Anonymous')
        
        # 학생 응답 기록을 Student Responses 시트에 추가
        response_worksheet.append_row([student_id, student_name] + request.form.getlist('answers[]') + [f"{score}%", result])

        if score < 70:
            # 점수가 70% 미만일 경우 숙제 상태로 전환
            homework_message = f"You scored below 70%. The test has been assigned to you as homework."
            # 숙제 상태로 Google Sheets에 기록
            response_worksheet.append_row([student_id, student_name, "Homework Assigned"])
            return homework_message

        test_complete = True
        return f"The test is now complete. Your score: {score:.2f}%. Thank you for participating!"

    # 다음 문제로 이동
    next_question = words[current_question_index]
    question_text = f"Question {current_question_index + 1}: {next_question['meaning']}"
    return render_template("index.html", question_text=question_text, correct_word=next_question["word"], attempt=1, message="")

if __name__ == '__main__':
    app.run(debug=True)
