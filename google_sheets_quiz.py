import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# Define the scope of the access we need (Google Sheets and Google Drive)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

# Path to your service account JSON key file
SERVICE_ACCOUNT_FILE = '/path/to/your/service-account-file.json'  # Replace with your path

# Authenticate with Google API using the service account
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Authorize with gspread using the credentials
client = gspread.authorize(credentials)

# Open the Google Sheets by name
answer_sheet = client.open("Answer Sheet")  # The sheet with correct answers
response_sheet = client.open("Student Responses")  # The sheet where student answers will be written

# Select the worksheets
answer_worksheet = answer_sheet.get_worksheet(0)  # First sheet in the Answer Sheet
response_worksheet = response_sheet.get_worksheet(0)  # First sheet in the Student Responses

# Example student answers and score calculation
student_id = 1
student_name = "John Doe"
student_answers = ["yellow", "blue", "red", "green", "purple", "orange", "blue", "pink", "black", "white"]
correct_answers = [row[1] for row in answer_worksheet.get_all_values()[1:]]  # Fetching answers from Sheet 1

# Compare answers
correct_count = sum([1 for i, answer in enumerate(student_answers) if answer == correct_answers[i]])

# Calculate score
score = (correct_count / len(correct_answers)) * 100

# Determine result
result = "Passed" if score >= 70 else "Failed"

# Add the data to the Student Responses sheet
response_worksheet.append_row([student_id, student_name] + student_answers + [f"{score}%", result])

print("Student data added to the response sheet.")
