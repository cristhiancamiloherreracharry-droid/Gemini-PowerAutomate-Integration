import os
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Configuración inicial
load_dotenv()
PA_URL = os.getenv("POWER_AUTOMATE_URL")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

# Validamos que las llaves existan
if not PA_URL or not GEMINI_KEY:
    print("❌ Error: Faltan variables en el archivo .env (URL o API Key)")
    exit()

genai.configure(api_key=GEMINI_KEY)

def procesar_con_ia(mensaje_usuario):
    """
    Usa Gemini para transformar lenguaje natural en un JSON estructurado.
    """
    # Usamos la ruta completa del modelo para evitar el error 404
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    
    prompt = f"""
    Eres un orquestador de infraestructura TI. Tu tarea es analizar el requerimiento del usuario y devolver un JSON.
    
    Entrada del usuario: "{mensaje_usuario}"
    
    Esquema del JSON a retornar:
    {{
        "accion": "Nombre_Accion (ej: Crear_Ticket, Reiniciar_Servicio, Escalar_Incidencia)",
        "resumen_ticket": "Resumen técnico de máximo 10 palabras",
        "prioridad": "Alta, Media o Baja"
    }}
    
    IMPORTANTE: Responde ÚNICAMENTE el objeto JSON. No agregues saludos ni explicaciones.
    """
    
    response = model.generate_content(prompt)
    
    # Limpieza de la respuesta (por si la IA devuelve ```json ... ```)
    texto_sucio = response.text.strip()
    texto_limpio = texto_sucio.replace('```json', '').replace('```', '').strip()
    
    return json.loads(texto_limpio)

def disparar_webhook(datos):
    """
    Envía el JSON procesado al Webhook de Power Automate.
    """
    headers = {'Content-Type': 'application/json'}
    # Enviamos los datos directamente como JSON
    response = requests.post(PA_URL, json=datos, headers=headers)
    return response.status_code

# --- Flujo Principal ---
if __name__ == "__main__":
    print("\n==============================================")
    print("🚀 ENTERPRISE AI ORCHESTRATOR - INICIADO")
    print("==============================================\n")
    
    consulta = input("¿Qué acción técnica deseas ejecutar?: ")
    
    try:
        print("\n🧠 Consultando a Gemini...")
        resultado_json = procesar_con_ia(consulta)
        
        print(f"📦 Payload generado: {json.dumps(resultado_json, indent=4, ensure_ascii=False)}")
        
        print("\n🔗 Conectando con Microsoft Power Automate...")
        status = disparar_webhook(resultado_json)
        
        if status in [200, 202]:
            print("\n✅ ¡ÉXITO! El flujo se disparó correctamente en la nube.")
        else:
            print(f"\n⚠️ Error en Power Automate. Status Code: {status}")
            
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")

    print("\n==============================================\n")