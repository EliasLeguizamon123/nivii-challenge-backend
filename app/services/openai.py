import os, re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_sql_from_natural_language(message: str) -> str:
    """
    Use OpenIA API for generate SQL from message in natural language
    """
    schema_description = """
    Tabla: sales
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
    """
    
    prompt = f"""
    Eres un asistente experto en SQLite. Convertí la siguiente pregunta en una consulta SQLite válida para una base de datos con el siguiente esquema:

    {schema_description}

    Instrucciones importantes:
    - Si la pregunta menciona un día de la semana (como "domingo", "lunes", etc.), traducilo al inglés ("Sunday", "Monday", etc.) y usalo como filtro: week_day = 'Sunday'.
    - NO apliques filtros adicionales por fecha (como date = MAX(date)) salvo que el usuario lo indique de forma explícita con frases como "último domingo", "el domingo más reciente", "última vez", etc.
    - Si no se menciona ningún día ni ninguna fecha, no agregues condiciones de tiempo.
    - La consulta debe ser útil para mostrar comparativas en gráficos. Si la pregunta incluye superlativos como "el más vendido", "el mayor total", etc., devolvé una lista ordenada (por ejemplo, los 5 productos más vendidos), evitando usar LIMIT 1 salvo que sea absolutamente necesario.
    - Siempre devolvé el resultado ordenado por la métrica relevante (por ejemplo, cantidad o total vendido), de mayor a menor.

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
    
    return cleaned_sql