from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.chat import get_chain, roles
import random

# ===============================
# Inicialización de la app
# ===============================
app = FastAPI(
    title="GLYNNE Framework API",
    description="API para interactuar con el agente de diagnóstico empresarial",
    version="1.0.0"
)

# ===============================
# Configuración de CORS
# ===============================
origins = [
    "http://localhost:3000",   # 🧠 para desarrollo local con Next.js
    "http://127.0.0.1:3000",
    "https://tu-dominio-en-vercel.vercel.app",  # 🌍 dominio de producción
    "*"  # ⚠️ (opcional) permite todo — ideal solo en pruebas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],            # permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],            # permite todos los encabezados
)

# ===============================
# Modelos de datos
# ===============================
class Query(BaseModel):
    user_id: str | None = None
    mensaje: str
    rol: str | None = "auditor"


# ===============================
# Endpoints
# ===============================
@app.get("/")
def home():
    return {
        "message": "🚀 API del agente GLYNNE en funcionamiento.",
        "endpoints": ["/gpt", "/roles"]
    }


@app.get("/roles")
def listar_roles():
    """Lista los roles disponibles del agente."""
    return {"roles_disponibles": list(roles.keys())}


@app.post("/gpt")
def procesar_mensaje(data: Query):
    """Procesa un mensaje del usuario y devuelve la respuesta del agente."""

    # Si no hay user_id, se genera uno nuevo
    if not data.user_id:
        data.user_id = str(random.randint(10000, 90000))

    # Validar rol
    rol = data.rol.lower()
    if rol not in roles:
        rol = "auditor"

    # Obtener cadena (memoria + modelo)
    chain = get_chain(data.user_id)

    # Generar respuesta
    try:
        respuesta = chain.run(rol=rol, mensaje=data.mensaje)
        return {
            "user_id": data.user_id,
            "rol": rol,
            "respuesta": respuesta,
            "memoria": chain.memory.load_memory_variables({})
        }
    except Exception as e:
        return {"error": str(e)}


# ===============================
# Servidor local
# ===============================
# Ejecutar con: uvicorn server:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
