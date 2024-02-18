import nltk
import re
from nltk.stem import PorterStemmer


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
    #real = []
    #Lowercase
    text = text.lower()

    #Removing special characters
    text = text.strip() #Removes /n
    text = "".join([char for char in text if char.isalpha() or char.isnumeric() or char == ' ']) #Removes non-letters & non-numbers

    #Removing stop words
    text_words = text.split() #Converts text to list of words
    text = " ".join([word for word in text_words if word not in stop_words])

    #Stemming words
    text_words = text.split()
    stemmer = PorterStemmer()
    words = []
    for word in text_words:
        word = stemmer.stem(word)
        words.append(word)
        if word in symptoms:
            real.append(word)
    # for i in range(len(words) - 1):
    #     if word[i] + " " + words[i+1] in symptoms: 
    #         real.append(word[i] + " " + word[i+1])
    return real

def findDisease():
    match = []
    count = 0
    for i in diseases:
        for j in diseases.get(i):
            if j in real and count >= 2: 
                match.append(i)
                break
            elif j in real: count += 1
    return match

def treatment():
    diseases = findDisease()
    for i in diseases:
        if i == "Common Cold":
            print("to drink plenty of fluids and get plenty of rest.")
        elif i == "Allergic Rhinitis (Hay Fever)":
            print("to avoid allergens and take antihistamines.")
        elif i == "Asthma":
            print("to avoid allergens and take a puff of your inhaler.")
        elif i == "Rash or Hives (Urticaria)":
            print("to take antihistamines and apply calamine lotion.")
        elif i == "Migraine":
            print("to take a painkiller and rest in a dark room.")
        elif i == "Influenza (Flu)":
            print("to drink plenty of fluids and take flu killers such as theraflu.")
        elif i == "Gastroesophageal Reflux Disease (GERD)":
            print("to avoid acidic foods and take antacids.")
        elif i == "Dehydration":
            print("to drink plenty of water over a 24 hour period.")
        elif i == "Heart Disease (Angina)":
            print("to take nitroglycerin and rest.")
        elif i == "Joint Pain (Arthritis)":
            print("to alternate between hot and cold packs and take painkillers.")
        else:
            print("You should see a doctor immediately.")

while True:
    text = input("Hello I understand you're not doing well today, what seems to be the problem?\n")
    if text == 'quit': 
        real = []
        break
    data = clean_text(text)
    print("Your symptoms appear to be: ", data)
    disease = findDisease()
    print("You may have these illnesses: ", disease)
    print("The recommended treatment is: ")
    treatment()