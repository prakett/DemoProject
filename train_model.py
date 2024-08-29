import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

# Data Preparation
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
questions = [line.split(' ', 1)[1].rsplit(' ', 4)[0] for line in data]
options = [list(map(int, line.split()[-4:])) for line in data]

# Create DataFrame
df = pd.DataFrame({
    "Question": questions,
    "Options": options
})

# Generate synthetic response data for 1000 participants
np.random.seed(42)
responses = np.random.randint(0, 4, size=(1000, len(df)))

# Create DataFrame for responses
response_df = pd.DataFrame(responses, columns=[f'Q{i+1}' for i in range(len(df))])

# Simulate category scoring based on responses
categories = ['D'] * 14 + ['A'] * 14 + ['S'] * 14  # Adjust according to actual mapping
category_scores = pd.DataFrame(np.random.randint(0, 40, size=(1000, 3)), columns=['D', 'A', 'S'])

# Prepare data for training
X = responses.astype(np.float32)
y = category_scores[['D', 'A', 'S']].values.astype(np.float32)

# Define and Train the Model
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

print("Model training complete and saved as 'dass_model.h5'")
