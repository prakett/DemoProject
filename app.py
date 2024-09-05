from flask import Flask, request, render_template
import numpy as np
import random

from pandas.io.formats.format import return_docstring

from data import questions, psychiatrists, QUOTES  # Import from data.py

app = Flask(__name__)

def calculate_score(responses, start_index, end_index):
    """
    Calculate the cumulative score for a specific range of responses.
    """
    scores = responses[start_index:end_index]
    return sum(scores)

def generate_report(responses):
    try:
        # Calculate cumulative scores
        depression_score = calculate_score(responses, 0, 14)
        anxiety_score = calculate_score(responses, 14, 28)
        stress_score = calculate_score(responses, 28, 42)

        # Interpret scores based on thresholds
        report = {
            "Depression Score": depression_score,
            "Anxiety Score": anxiety_score,
            "Stress Score": stress_score,
            "Depression Interpretation": (
                'Extremely Severe' if depression_score >= 28 else
                'Severe' if depression_score >= 21 else
                'Moderate' if depression_score >= 14 else
                'Mild' if depression_score >= 10 else
                'Normal'
            ),
            "Anxiety Interpretation": (
                'Extremely Severe' if anxiety_score >= 20 else
                'Severe' if anxiety_score >= 15 else
                'Moderate' if anxiety_score >= 10 else
                'Mild' if anxiety_score >= 8 else
                'Normal'
            ),
            "Stress Interpretation": (
                'Extremely Severe' if stress_score >= 34 else
                'Severe' if stress_score >= 27 else
                'Moderate' if stress_score >= 19 else
                'Mild' if stress_score >= 11 else
                'Normal'
            )
        }

        # Add qualitative feedback
        report["Depression Feedback"] = (
            "It is highly recommended to seek professional help." if report["Depression Interpretation"] in ["Severe", "Extremely Severe"] else
            "Consider discussing with a mental health professional if symptoms persist." if report["Depression Interpretation"] == "Moderate" else
            "Your results are within the normal range, but staying mindful of your mental health is always important."
        )

        report["Anxiety Feedback"] = (
            "It is highly recommended to seek professional help." if report["Anxiety Interpretation"] in ["Severe", "Extremely Severe"] else
            "Consider discussing with a mental health professional if symptoms persist." if report["Anxiety Interpretation"] == "Moderate" else
            "Your results are within the normal range, but staying mindful of your mental health is always important."
        )

        report["Stress Feedback"] = (
            "It is highly recommended to seek professional help." if report["Stress Interpretation"] in ["Severe", "Extremely Severe"] else
            "Consider discussing with a mental health professional if symptoms persist." if report["Stress Interpretation"] == "Moderate" else
            "Your results are within the normal range, but staying mindful of your mental health is always important."
        )

        # Example follow-up question based on high stress
        if stress_score >= 19:
            report["Follow-up Question"] = "Have you been experiencing major life changes or stressors recently? It might help to talk about these with someone you trust."

        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return {"Error": str(e)}


@app.route('/index')
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

        # Generate report using the updated cumulative scoring
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

@app.route('/')
def first():
    return render_template('first.html')

@app.route('/second')
def second():
    return render_template('second.html')

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)
