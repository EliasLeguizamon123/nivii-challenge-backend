import os, re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_sql_from_natural_language(message: str) -> str:
    """
    Use OpenIA API for generate SQL from message in natural language
    If in the message appears one day of the week translate it to English for generalized with `sales` table in database.
    
    Args:
        message (str): Textual message of type "user".
        
    Results:
        str: SQlite query obtained from `sales` table
        None: If the user message is not a valid SQlite query
    """
    prompt = f"""
    Eres un asistente experto en consultas SQLite para bases de datos SQLite. Tu tarea es analizar preguntas realizadas en lenguaje natural y convertirlas en una consulta SQLite válida **solo si** están relacionadas con el siguiente esquema de base de datos:

    Tabla: `sales`
    - id: int
    - date: datetime
    - week_day: string
    - hour: string
    - ticket_number: string
    - waiter: string
    - product_name: string
    - quantity: int
    - unitary_price: float
    - total: float

    ---

    ### ⚠️ Instrucciones importantes:

    1. SOLO generá una consulta SQL si la pregunta hace referencia explícita a **algún campo o concepto** del esquema, como productos, ventas, camareros, fechas, precios, cantidades, horas, días de la semana, etc.

    2. Si la pregunta **no está relacionada con datos de la tabla**, o no contiene información estructurada (como “hola”, “cómo estás”, “mostrame algo”, etc.), entonces respondé literalmente con:  
    **This is not a valid query**

    3. No generes SQL si el idioma no es comprensible para vos o la pregunta es ambigua. En ese caso, respondé también con:  
    **This is not a valid query**

    4. Podés recibir preguntas en distintos idiomas (español, inglés, chino, etc.). Tratá de detectar el idioma y procesar el mensaje igualmente si es posible.

    5. Si se menciona un día de la semana en **cualquier idioma**, traducilo al inglés y usalo como filtro sobre el campo `week_day`. Por ejemplo:
    - "domingo" → "Sunday"
    - "lunes" → "Monday"
    - "星期日" (chino para domingo) → "Sunday"

    Así, si alguien pregunta "ventas del domingo", deberás generar una condición como `WHERE week_day = 'Sunday'`.

    6. NO agregues filtros por fecha (como `MAX(date)`) a menos que la pregunta lo indique explícitamente con frases como “último domingo”, “fecha más reciente”, “última vez”, etc.

    7. Preferí consultas útiles para visualización gráfica, rankings o resúmenes. Si se pide “el más vendido” o “cuál fue el mayor total”, devolvé una lista ordenada (ej. con `ORDER BY total DESC`), y evitá `LIMIT 1` salvo que sea necesario.

    ---

    ###  Ejemplos de preguntas válidas (deben generar SQL):
    - ¿Qué productos se vendieron más el domingo?
    - Show me total sales per waiter
    - 最受欢迎的产品是什么？(¿Cuál es el producto más popular?)
    - Ventas por hora el sábado
    - 这个星期一的销售额是多少？(¿Cuál fue la facturación de este lunes?)

    ###  Ejemplos inválidos (deben responder “This is not a valid query”):
    - Hola
    - How are you?
    - Mostrame algo
    - Hi bot!
    - 今天的天气怎么样？(¿Cómo está el clima hoy?)
    - Cuéntame un chiste

    ---

    Convertí la siguiente pregunta en una consulta SQLite **solo si cumple con los criterios anteriores**. En caso contrario, respondé literalmente con:

    **This is not a valid query**

    ---

    Pregunta: {message}

    Consulta en SQLite:

    """
    
    response = client.responses.create(
        model="gpt-3.5-turbo",
        instructions=prompt,
        input=message
    )
    
    raw_sql = response.output[0].content[0].text
    
    cleaned_sql = re.sub(r"```sql|```", "", raw_sql).strip()
    
    if not cleaned_sql.lower().startswith("select"):
        return None
    
    return cleaned_sql