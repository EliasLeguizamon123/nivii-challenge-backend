# scripts/test_openai.py

from app.services.openai import generate_sql_from_natural_language

if __name__ == "__main__":

    # Pregunta que quieras testear
    question = "¿Cuál fue el producto más vendido del domingo?"

    # Llamar a la función
    sql_result = generate_sql_from_natural_language(question)

    # Mostrar resultado
    print("🔍 Pregunta:", question)
    print("🧠 SQL generado:")
    print(sql_result)
