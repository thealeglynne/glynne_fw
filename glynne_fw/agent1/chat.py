import os
from dotenv import load_dotenv
import random
from langchain_groq import ChatGroq 
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain 

# =========================
# Cargar API Key
# =========================
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError('en el .env no hay una api valida')

# =========================
# Inicializar LLM con límite de tokens
# =========================
llm = ChatGroq(
    model='llama3-70b-8192',
    api_key=api_key,
    temperature=0.4,
    max_output_tokens=80  # respuesta corta para ahorrar créditos
)

# =========================
# Prompt simplificado
# =========================
Prompt_estruccture  =  """
[META] Analiza el negocio y genera un diagnóstico breve sobre cómo la IA puede mejorar el crecimiento empresarial.
Sé {rol}, profesional, conciso y directo. No inventes datos.

[MEMORIA] Contexto previo: {historial}

[ENTRADA DEL USUARIO]
consulta: {mensaje}

respuesta:
"""

# =========================
# Diccionario de usuarios y cadenas
# =========================
usuario = {}

def get_chain(user_id):
    if user_id not in usuario:
        memory = ConversationBufferMemory(
            memory_key='historial',
            input_key='mensaje',
            k=3 # solo guarda la última interacción para ahorrar tokens
        )
        prompt = PromptTemplate(
            input_variables=['rol','mensaje','historial'],
            template=Prompt_estruccture.strip()
        )
        chain = LLMChain(
            llm=llm,
            prompt=prompt,
            memory=memory,
            verbose=True
        )
        usuario[user_id] = chain 
    return usuario[user_id]

# =========================
# Roles disponibles
# =========================
roles = {
    'auditor': 'actúa como auditor empresarial y determina estrategias que se pueden implementar con IA',
    'dessarrollador': 'explica todo de forma técnica, describiendo estrategias de integración a departamentos empresariales',
    'vendedor': 'intenta vender un software de forma despectiva y mala técnica de venta'
}

# =========================
# Inicialización del usuario
# =========================
user_id = str(random.randint(10000,90000))
print(f"Tu user id es {user_id}")
rol = 'auditor'

# =========================
# Bucle principal
# =========================
"""while True:
    try:
        user_input = input('Tu: ')
        if user_input.lower() == 'salir':
            break
        
        if user_input.startswith('/rol '):
            nuevo_rol = user_input.split('/rol ', 1)[1].lower().strip()
            if nuevo_rol in roles:
                rol = nuevo_rol
                print(f"Tu nuevo rol es {nuevo_rol}")
            else:
                print('Rol no disponible')
            continue
        
        chain = get_chain(user_id)
        respuesta = chain.run(rol=rol, mensaje=user_input)
        print(respuesta)
        
        print('Memoria actual:')
        print(chain.memory.load_memory_variables({}))
        
    except Exception as e:
        print(f"Error: {e}")
        break
"""