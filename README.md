## ETL & Data Science

Proyecto que combina un pipeline ETL (en construcción) y un ejericio de data science.

### Estructura
- `etl/`: Código del pipeline ETL. Actualmente en desarrollo activo (no finalizado).
- `data_science/`: Notebook con ejemplo de clustering y clasificación.

### Requisitos
Cada subproyecto define sus dependencias:
- `etl/requirements.txt`
- `data_science/requirements.txt`

Instalación recomendada (por entorno):
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r etl/requirements.txt
pip install -r data_science/requirements.txt
```

### Uso rápido
- Data Science: abrir `data_science/notebook/clustering_classification.ipynb` y ejecutar las celdas.
- ETL (WIP): el módulo no está finalizado. El punto de entrada previsto es `etl/src/main.py`. 

### Estado del ETL
El código en `etl/` está incompleto y sujeto a cambios. La interfaz y el comportamiento pueden variar.
