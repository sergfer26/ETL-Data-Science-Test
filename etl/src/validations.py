import re
import pandas as pd
from datetime import datetime

def validar_columnas(data: pd.DataFrame, columns: list[str]) -> bool:
    return all(col in data.columns for col in columns)


def validar_email(email: str) -> bool:
    ## Regex pattern suggested by Deepseek
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validar_fecha(fecha_str: str) -> bool:
    try:
        datetime.strptime(fecha_str, '%d/%m/%Y %H:%M')
        return True
    except ValueError:
        return False