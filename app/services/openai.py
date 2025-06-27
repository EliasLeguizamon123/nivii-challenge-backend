import os
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
    
    Ask: {message}
    
    SQLite: 
    """
    
    response = client.responses.create(
        model="gpt-3.5-turbo",
        instructions=prompt,
        input=message
    )
    
    sql = response.output[0].content[0].text
    
    return sql