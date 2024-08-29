from flask import Flask, request, render_template
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('model/dass_model.h5')

# List of DASS-42 questions
questions = [
    "I found myself getting upset by quite trivial things",
    "I was aware of dryness of my mouth",
    "I couldn't seem to experience any positive feeling at all",
    "I experienced breathing difficulty (eg, excessively rapid breathing, breathlessness in the absence of physical exertion)",
    "I just couldn't seem to get going",
    "I tended to over-react to situations",
    "I had a feeling of shakiness (eg, legs going to give way)",
    "I found it difficult to relax",
    "I found myself in situations that made me so anxious I was most relieved when they ended",
    "I felt that I had nothing to look forward to",
    "I found myself getting upset rather easily",
    "I felt that I was using a lot of nervous energy",
    "I felt sad and depressed",
    "I found myself getting impatient when I was delayed in any way (eg, elevators, traffic lights, being kept waiting)",
    "I had a feeling of faintness",
    "I felt that I had lost interest in just about everything",
    "I felt I wasn't worth much as a person",
    "I felt that I was rather touchy",
    "I perspired noticeably (eg, hands sweaty) in the absence of high temperatures or physical exertion",
    "I felt scared without any good reason",
    "I felt that life wasn't worthwhile",
    "I found it hard to wind down",
    "I had difficulty in swallowing",
    "I couldn't seem to get any enjoyment out of the things I did",
    "I was aware of the action of my heart in the absence of physical exertion (eg, sense of heart rate increase, heart missing a beat)",
    "I felt down-hearted and blue",
    "I found that I was very irritable",
    "I felt I was close to panic",
    "I found it hard to calm down after something upset me",
    "I feared that I would be 'thrown' by some trivial but unfamiliar task",
    "I was unable to become enthusiastic about anything",
    "I found it difficult to tolerate interruptions to what I was doing",
    "I was in a state of nervous tension",
    "I felt I was pretty worthless",
    "I was intolerant of anything that kept me from getting on with what I was doing",
    "I felt terrified",
    "I could see nothing in the future to be hopeful about",
    "I felt that life was meaningless",
    "I found myself getting agitated",
    "I was worried about situations in which I might panic and make a fool of myself",
    "I experienced trembling (eg, in the hands)",
    "I found it difficult to work up the initiative to do things"
]

def transform_responses_to_features(responses):
    responses = np.array(responses).reshape(-1, 1)
    feature1 = np.mean(responses[0:14])
    feature2 = np.mean(responses[14:28])
    feature3 = np.mean(responses[28:42])
    return np.array([feature1, feature2, feature3]).reshape(1, -1)

def generate_report(model, responses):
    try:
        responses = transform_responses_to_features(responses)
        if np.all(responses == 0):
            return {
                "Depression Score": 0,
                "Anxiety Score": 0,
                "Stress Score": 0,
                "Depression Interpretation": 'Normal',
                "Anxiety Interpretation": 'Normal',
                "Stress Interpretation": 'Normal'
            }
        scores = model.predict(responses)
        depression, anxiety, stress = scores[0]

        report = {
            "Depression Score": round(depression, 2),
            "Anxiety Score": round(anxiety, 2),
            "Stress Score": round(stress, 2),
            "Depression Interpretation": 'Severe' if depression > 21 else 'Mild/Moderate' if depression > 14 else 'Normal',
            "Anxiety Interpretation": 'Severe' if anxiety > 19 else 'Mild/Moderate' if anxiety > 10 else 'Normal',
            "Stress Interpretation": 'Severe' if stress > 26 else 'Mild/Moderate' if stress > 18 else 'Normal'
        }
        return report
    except Exception as e:
        return {"Error": str(e)}

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        responses = [int(request.form[f'question_{i+1}']) for i in range(42)]
        report = generate_report(model, responses)
        return render_template('report.html', report=report)
    except ValueError as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
