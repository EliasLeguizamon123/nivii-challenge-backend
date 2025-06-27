from sqlalchemy.exc import OperationalError, ProgrammingError, SQLAlchemyError
from sqlalchemy import text
from typing import Tuple
from datetime import datetime

from app.entities.charts import Chart
from app.entities.chart_data import ChartData

def generate_assistant_content_and_chart_data(
    query: str,
    session,
    history,
    message
) -> Tuple[str, bool]:
    try:
        result = session.execute(text(query))
        rows = result.fetchall()

        print(f"Query result rows count: {len(rows)}")
        print(f"Rows: {rows}")

        valid_rows = [row for row in rows if row and len(row) == 2 and row[0] is not None and row[1] is not None]

        if not valid_rows:
            try:
                last_date_result = session.execute(text("SELECT MAX(DATE(date)) FROM sales")).scalar()
                if last_date_result:
                    formated_date = datetime.strptime(last_date_result, "%Y-%m-%d").strftime("%B %d, %Y")
                    assistant_content = (
                        f"No results were found for your query. "
                        f"The latest date registered in your database is {formated_date}. "
                        "Try rephrasing your question or adjusting the time period."
                    )
                else:
                    assistant_content = "No results were found and the sales table appears to be empty."
            except Exception as error:
                assistant_content = (
                    f"No results were found for your query. "
                    f"(Additionally, an error occurred while checking the latest date: {str(error)})"
                )
            return assistant_content, False

        # Si hay datos válidos, generar el chart
        assistant_content = "This is your generated chart of your query"

        chart = Chart(
            history_id=history.id,
            chart_type="bar",
            title=message.content[:30],
            x_axis="label",
            y_axis="value"
        )
        session.add(chart)
        session.commit()
        session.refresh(chart)

        for label, value in valid_rows:
            chart_data = ChartData(
                chart_id=chart.id,
                label=str(label),
                value=float(value)
            )
            session.add(chart_data)

        session.commit()

        return assistant_content, True

    except OperationalError as oe:
        return f"There was a problem executing your query. It might be a syntax error or invalid column.\nDetails: {str(oe.orig)}", False

    except ProgrammingError as pe:
        return f"The query could not be executed due to a database error. Please check your input.\nDetails: {str(pe.orig)}", False

    except SQLAlchemyError as se:
        return f"An unexpected error occurred while accessing the database.\nDetails: {str(se)}", False

    except Exception as e:
        return f"Unexpected error: {str(e)}", False