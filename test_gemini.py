import google.generativeai as genai

# Mets ta clé API Gemini ici
genai.configure(api_key="AIzaSyB1bN3L6hCpHGdry_0Ub4iRfdJ1kKbhqE4")

# Modèle recommandé pour tests gratuits
model = genai.GenerativeModel("gemini-2.5-flash")
try:
    response = model.generate_content("Bonjour ! Test de la clé API Gemini.")
    print("Réponse de Gemini :")
    print(response.text)
except Exception as e:
    print("Erreur :", e)
