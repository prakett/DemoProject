import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Step 1: Load and Prepare the Data

# Sample data representing the DASS-42 questionnaire
data = [
    "1 I found myself getting upset by quite trivial things 0 1 2 3",
    "2 I was aware of dryness of my mouth 0 1 2 3",
    "3 I couldn't seem to experience any positive feeling at all 0 1 2 3",
    "4 I experienced breathing difficulty (eg, excessively rapid breathing, breathlessness in the absence of physical exertion) 0 1 2 3",
    "5 I just couldn't seem to get going 0 1 2 3",
    "6 I tended to over-react to situations 0 1 2 3",
    "7 I had a feeling of shakiness (eg, legs going to give way) 0 1 2 3",
    "8 I found it difficult to relax 0 1 2 3",
    "9 I found myself in situations that made me so anxious I was most relieved when they ended 0 1 2 3",
    "10 I felt that I had nothing to look forward to 0 1 2 3",
    "11 I found myself getting upset rather easily 0 1 2 3",
    "12 I felt that I was using a lot of nervous energy 0 1 2 3",
    "13 I felt sad and depressed 0 1 2 3",
    "14 I found myself getting impatient when I was delayed in any way (eg, elevators, traffic lights, being kept waiting) 0 1 2 3",
    "15 I had a feeling of faintness 0 1 2 3",
    "16 I felt that I had lost interest in just about everything 0 1 2 3",
    "17 I felt I wasn't worth much as a person 0 1 2 3",
    "18 I felt that I was rather touchy 0 1 2 3",
    "19 I perspired noticeably (eg, hands sweaty) in the absence of high temperatures or physical exertion 0 1 2 3",
    "20 I felt scared without any good reason 0 1 2 3",
    "21 I felt that life wasn't worthwhile 0 1 2 3",
    "22 I found it hard to wind down 0 1 2 3",
    "23 I had difficulty in swallowing 0 1 2 3",
    "24 I couldn't seem to get any enjoyment out of the things I did 0 1 2 3",
    "25 I was aware of the action of my heart in the absence of physical exertion (eg, sense of heart rate increase, heart missing a beat) 0 1 2 3",
    "26 I felt down-hearted and blue 0 1 2 3",
    "27 I found that I was very irritable 0 1 2 3",
    "28 I felt I was close to panic 0 1 2 3",
    "29 I found it hard to calm down after something upset me 0 1 2 3",
    "30 I feared that I would be 'thrown' by some trivial but unfamiliar task 0 1 2 3",
    "31 I was unable to become enthusiastic about anything 0 1 2 3",
    "32 I found it difficult to tolerate interruptions to what I was doing 0 1 2 3",
    "33 I was in a state of nervous tension 0 1 2 3",
    "34 I felt I was pretty worthless 0 1 2 3",
    "35 I was intolerant of anything that kept me from getting on with what I was doing 0 1 2 3",
    "36 I felt terrified 0 1 2 3",
    "37 I could see nothing in the future to be hopeful about 0 1 2 3",
    "38 I felt that life was meaningless 0 1 2 3",
    "39 I found myself getting agitated 0 1 2 3",
    "40 I was worried about situations in which I might panic and make a fool of myself 0 1 2 3",
    "41 I experienced trembling (eg, in the hands) 0 1 2 3",
    "42 I found it difficult to work up the initiative to do things 0 1 2 3"
]

# Extract questions and options
questions = []
options = []

for line in data:
    parts = line.rsplit(' ', 4)
    if len(parts) == 5:
        question = parts[1].strip()
        response_options = ' '.join(parts[3:]).strip()
        questions.append(question)
        options.append(response_options)

# Create DataFrame
df = pd.DataFrame({
    "Question": questions,
    "Options": options
})

# Map categories (based on an assumed order)
categories = ['D', 'A', 'S', 'A', 'D', 'S', 'A', 'S', 'A', 'D', 'S', 'A', 'D', 'S', 'A', 'D',
              'D', 'S', 'A', 'D', 'S', 'A', 'D', 'A', 'D', 'S', 'A', 'S', 'A', 'A', 'D', 'S',
              'S', 'D', 'S', 'A', 'D', 'D', 'S', 'A', 'A', 'D']

df['Category'] = categories

# Simulate synthetic response data for 1000 participants
np.random.seed(42)
responses = np.random.randint(0, 4, size=(1000, len(df)))

# Convert responses to DataFrame
response_df = pd.DataFrame(responses, columns=[f'Q{i+1}' for i in range(len(df))])

# Calculate category scores
df_responses = pd.concat([df, response_df.T.reset_index(drop=True)], axis=1)
category_scores = df_responses.groupby('Category').sum().T

# Prepare data for training
X = responses
y = category_scores[['D', 'A', 'S']].values

# Step 2: Define and Train the Model
model = models.Sequential([
    layers.Dense(64, input_dim=len(df), activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(3, activation='linear')  # Output: Depression, Anxiety, Stress scores
])

model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)

# Save the trained model
model.save('dass_model.h5')

# Step 3: Generate Report
def generate_report(model, responses):
    scores = model.predict(np.array(responses).reshape(1, -1))
    depression, anxiety, stress = scores[0]

    report = f"""
    DASS-42 Report:
    --------------------
    Depression Score: {depression:.2f}
    Anxiety Score: {anxiety:.2f}
    Stress Score: {stress:.2f}
    --------------------
    Interpretation:
    - Depression: {'Severe' if depression > 21 else 'Mild/Moderate' if depression > 14 else 'Normal'}
    - Anxiety: {'Severe' if anxiety > 19 else 'Mild/Moderate' if anxiety > 10 else 'Normal'}
    - Stress: {'Severe' if stress > 26 else 'Mild/Moderate' if stress > 18 else 'Normal'}
    """
    return report

# Example usage with a new participant's responses
new_responses = np.random.randint(0, 4, size=(len(df),))
report = generate_report(model, new_responses)
print(report)
