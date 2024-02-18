import nltk
import re
from nltk.stem import PorterStemmer
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["symptoms"]
        processed_input, diseases, treatment_info = process_input(user_input)
        return render_template("index.html", input=processed_input, diseases=diseases, treatment_info=treatment_info)

    return render_template("form.html")

def process_input(user_input):
    symptoms = [
    "sneez", "runni nose", "stuffi nose", "wateri eye", "itchi eye", "itchi throat", "itchi ear",
    "wheez", "rash", "hive", "swell", "throb", "pulsat pain", "sensit light", "sensit sound",
    "sensit smell", "nausea", "vomit", "blur vision", "lightheaded", "faint", "short breath",
    "chest tight", "cough", "chest pain", "angina", "weak", "dizzi", "thirst", "urin",
    "hunger", "weight loss", "fatigu", "heal", "sore", "infect",
    "heartburn", "regurgit food", "sour liquid", "difficulti swallow", "dri cough", "headach",
    "heartbeat", "blood urin", "ach", "fever", "chill", "joint pain", "joint swell",
    "stiff"
    ]

    diseases = {
    "Common Cold": ["sneez", "runni nose", "stuffi nose", "cough", "fever", "chill"],
    "Allergic Rhinitis (Hay Fever)": ["sneez", "runni nose", "stuffi nose", "wateri eye", "itchi eye", "itchi throat", "itchi ear"],
    "Asthma": ["wheez", "short breath", "cough", "chest tight"],
    "Rash or Hives (Urticaria)": ["rash", "hive"],
    "Migraine": ["headach", "nausea", "vomit", "sensit light", "sensit sound", "sensit smell"],
    "Influenza (Flu)": ["fever", "chill", "cough", "ach", "fatigu"],
    "Gastroesophageal Reflux Disease (GERD)": ["heartburn", "regurgit food", "sour liquid", "difficulti swallow"],
    "Dehydration": ["thirst", "frequent urin", "weak", "dizzi", "fatigu", "dry mouth"],
    "Heart Disease (Angina)": ["chest pain", "short breath", "lightheaded", "faint", "heartbeat"],
    "Joint Pain (Arthritis)": ["joint pain", "joint swell", "stiff", "bodi ach"]
    }

    nltk.download("stopwords")
    stop_words = nltk.corpus.stopwords.words("english")
    cleanHTML = re.compile('<.*?>')

    real = []

    def clean_text(text):
        # Lowercase
        text = text.lower()

        # Removing special characters
        text = text.strip()  # Removes /n
        text = re.sub(cleanHTML, "", text)  # Removes HTML tags
        text = "".join([char for char in text if char.isalpha() or char.isnumeric() or char == ' '])  # Removes non-letters & non-numbers

        # Removing stop words
        text_words = text.split()  # Converts text to a list of words
        text = " ".join([word for word in text_words if word not in stop_words])

        # Stemming words
        text_words = text.split()
        stemmer = PorterStemmer()
        text = []
        for word in text_words:
            if stemmer.stem(word) in symptoms:
                real.append(stemmer.stem(word))
                text.append(word)
        # " ".join([stemmer.stem(word) for word in text_words])

        return text

    def findDisease():
        match = []
        for i in diseases:
            count = 0
            for j in diseases.get(i):
                if j in real and count >= 2:
                    match.append(i)
                    break
                elif j in real: count += 1
        return match

    def treatment():
        diseases = findDisease()
        treatment_info = []
        for i in diseases:
            if i == "Common Cold":
                treatment_info.append("Drink plenty of fluids and get plenty of rest.")
            elif i == "Allergic Rhinitis (Hay Fever)":
                treatment_info.append("Avoid allergens and take antihistamines.")
            elif i == "Asthma":
                treatment_info.append("Avoid allergens and take a puff of your inhaler.")
            elif i == "Rash or Hives (Urticaria)":
                treatment_info.append("Take antihistamines and apply calamine lotion.")
            elif i == "Migraine":
                treatment_info.append("Take a painkiller and rest in a dark room.")
            elif i == "Influenza (Flu)":
                treatment_info.append("Drink plenty of fluids and take flu killers such as Theraflu.")
            elif i == "Gastroesophageal Reflux Disease (GERD)":
                treatment_info.append("Avoid acidic foods and take antacids.")
            elif i == "Dehydration":
                treatment_info.append("Drink plenty of water over a 24-hour period.")
            elif i == "Heart Disease (Angina)":
                treatment_info.append("Take nitroglycerin and rest.")
            elif i == "Joint Pain (Arthritis)":
                treatment_info.append("Alternate between hot and cold packs and take painkillers.")
            else:
                treatment_info.append("You should see a doctor immediately.")
        return treatment_info

    # Process user input
    user_input = clean_text(user_input)
    diseases = findDisease()
    treatment_info = treatment()

    processed_input = " ".join(real)

    return processed_input, diseases, treatment_info

if __name__ == "__main__":
    app.run(debug=True)

