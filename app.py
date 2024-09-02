from flask import Flask, request, render_template
import numpy as np
import random
from data import questions, psychiatrists, QUOTES  # Import from data.py

app = Flask(__name__)

def calculate_score(responses, start_index, end_index):
    """
    Calculate the average score for a specific range of responses.
    """
    scores = responses[start_index:end_index]
    return np.mean(scores)

def generate_report(responses):
    try:
        # Calculate cumulative scores
        depression_score = sum(responses[0:14])
        anxiety_score = sum(responses[14:28])
        stress_score = sum(responses[28:42])

        # Interpret scores based on cumulative thresholds
        report = {
            "Depression Score": depression_score,
            "Anxiety Score": anxiety_score,
            "Stress Score": stress_score,
            "Depression Interpretation": 'Severe' if depression_score > 28 else 'Mild/Moderate' if depression_score > 20 else 'Normal',
            "Anxiety Interpretation": 'Severe' if anxiety_score > 28 else 'Mild/Moderate' if anxiety_score > 20 else 'Normal',
            "Stress Interpretation": 'Severe' if stress_score > 28 else 'Mild/Moderate' if stress_score > 20 else 'Normal'
        }
        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return {"Error": str(e)}

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Collect form data
        responses = [int(request.form.get(f'question_{i+1}', 0)) for i in range(42)]
        print(f"Responses received: {responses}")  # Debugging line

        # Check if all responses are captured
        if len(responses) != 42:
            return "Error: Not all questions were answered."

        # Generate report using simple calculations
        report = generate_report(responses)
        print(f"Report generated: {report}")  # Debugging line

        # Generate 3 random quotes
        random_quotes = random.sample(QUOTES, 3)

        # Render report.html with psychiatrist data and quotes
        return render_template('report.html', report=report, psychiatrists=psychiatrists, quotes=random_quotes)
    except ValueError as e:
        print(f"ValueError: {e}")  # Debugging line
        return f"Error: {e}"
    except Exception as e:
        print(f"Exception: {e}")  # Debugging line
        return f"Error: {e}"

@app.route('/recommendation')
def recommendation():
    return render_template('recommendation.html', psychiatrists=psychiatrists)

if __name__ == '__main__':
    app.run(debug=True)
