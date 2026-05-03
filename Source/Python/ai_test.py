import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def check_connection():
    # Usamos el modelo 2.5-flash que es el estándar de eficiencia para 2026
    selected_model = 'models/gemini-2.5-flash'
    
    print(f"--- Probando conexión con {selected_model} ---")
    try:
        model = genai.GenerativeModel(selected_model)
        # Una petición orientada a tu perfil profesional
        prompt = "Como experto en Business Analysis, dime en una frase por qué la IA es clave en la optimización de procesos."
        
        response = model.generate_content(prompt)
        
        print("\nRespuesta de la IA:")
        print(response.text)
        print("\n--- ¡Conexión Exitosa, Mateo! ---")
        
    except Exception as e:
        print(f"Error detectado: {e}")

if __name__ == "__main__":
    check_connection()