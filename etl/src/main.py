import pandas as pd

from loguru import logger

import db
import transform
import error_manager
from retrive import retrieve_txt_files
from validations import validar_email, validar_fecha, validar_columnas

COLUMNS =  [
    'email', 'jk', 'Badmail', 'Baja', 'Fecha envio', 'Fecha open', 
    'Opens', 'Opens virales', 'Fecha click', 'Clicks', 'Clicks virales', 
    'Links', 'IPs', 'Navegadores', 'Plataformas'
]


def _txt_to_df(file_path: str) -> pd.TextFileReader| pd.Unknown |pd.DataFrame:
    """
    Parsea las líneas de un archivo txt a una l
    """
    data = pd.read_csv(file_path, sep=",")
    return data


def process_txt_file(file_name: str) -> pd.DataFrame | None:
    """
    Process a text file into a pandas DataFrame and validate the data.
    
    :param file_name: Name/path of the file to process
    :return: pandas DataFrame with the data and a list of errors
    """
    data = _txt_to_df(file_name)
    
    if not isinstance(data, pd.DataFrame) or not validar_columnas(data, COLUMNS):
        logger.error(f"[!] Columns are not valid in {file_name}")
        return None
    errors = []
    descriptions = []
    valid_data = False
    for e, row in data.iterrows():
        description = []
        if pd.isna(row['email']) or not validar_email(row['email']):
            logger.error(f"[!] Invalid email: {row['email']}")
            description.append(f"Invalid email: {row['email']}")
            valid_data = False
        
        date_fields = ['Fecha envio', 'Fecha open', 'Fecha click']
        for field in date_fields:
            if pd.isna(row[field]) or not validar_fecha(row[field]):
                logger.error(f"[!] Invalid date in {field}: {row[field]}")
                description.append(f"Invalid date in {field}: {row[field]}")
                valid_data = False
        
        errors.append(valid_data)
        descriptions.append(description)
        
    data["error"] = errors
    data["error_description"] = descriptions
    return data


def etl_pipeline():
    """
    ETL pipeline to process txt files and load data into the database.
    
    :return: None
    """
    txt_files = retrieve_txt_files()
    for file_name in txt_files:
        try:
            data = process_txt_file(file_name)
        except Exception as e:
            logger.error(f"[!] Error processing {file_name}: {e}")
            error_manager.log_error(file_name, e)
            continue
        if data is None:
            logger.warning(f"[!] Error processing {file_name}")
            continue
        
        correct_data = data[data["error"]]
        incorrect_data = data[~data["error"]]
        try:
            for e, row in correct_data.iterrows():
                visitor_data = transform.visitor_table(row)
                stats_data = transform.stats_table(row)
                
                db.insert_visitor_data(visitor_data)
                db.insert_stats_data(stats_data)
        except Exception as e:
            logger.error(f"[!] Error processing correct data: {e}")
        
        try:
            for e, row in incorrect_data.iterrows():
                error_data = transform.error_table(row)
                db.insert_error_data(error_data)
        except Exception as e:
            logger.error(f"[!] Error processing incorrect data: {e}")
            error_manager.log_error(file_name, e)
            continue