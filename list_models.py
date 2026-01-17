import google.generativeai as genai

genai.configure(api_key="AIzaSyD_dM5ja0CESUCPoDJyUN3jxxzfGEzVaHc")

models = genai.list_models()

print("📌 Modèles disponibles pour ta clé API :\n")
for m in models:
    print("-", m.name)
