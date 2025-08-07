import os
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

# Carregar API key do .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classificar_comentario(texto):
    prompt = f"""
Classifique o seguinte comentário como 'Promotor', 'Detrator' ou 'Neutro'.

Comentário:
\"\"\"{texto}\"\"\"

Resposta apenas com uma das palavras: Promotor, Detrator ou Neutro.
    """.strip()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # ou "gpt-4o-mini", "gpt-3.5-turbo"
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Erro na requisição:", e)
        return "erro"

def calcular_nps(df, verbose=True):

    try: p = df["classificacao"].value_counts()['Promotor']
    except KeyError: p = 0
    try: d = df["classificacao"].value_counts()['Detrator']
    except KeyError: d = 0  
    try: n = df["classificacao"].value_counts()['Neutro']
    except KeyError: n = 0
    if p+d+n == 0: nps = 0
    
    nps  = round((p/(p+d+n) - d/(p+d+n))*100, 2)

    if verbose:
        print(f"Promotores: {p}")
        print(f"Detratores: {d}")
        print(f"Neutros: {n}")
        print(f"NPS: {nps}")

    return nps