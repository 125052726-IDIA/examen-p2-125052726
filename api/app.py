import os
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="DataMart API")

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "datamart")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

def get_db():
    return psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )

class ResultadoCreate(BaseModel):
    clave: str
    valor: float

@app.get("/")
def root():
    return {"status": "ok", "service": "DataMart API"}

@app.get("/resultados")
def obtener_todos():
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, clave, valor FROM resultados;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

@app.get("/resultados/{clave}")
def obtener_por_clave(clave: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, clave, valor FROM resultados WHERE clave = %s;", (clave,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if not rows:
        raise HTTPException(status_code=404, detail="Clave no encontrada")
    return rows

@app.post("/resultados", status_code=201)
def crear_resultado(item: ResultadoCreate):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO resultados (clave, valor)
        VALUES (%s, %s)
        ON CONFLICT (clave) DO UPDATE SET valor = EXCLUDED.valor
        RETURNING id, clave, valor;
    """, (item.clave, item.valor))
    nuevo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return nuevo

@app.delete("/resultados/{clave}")
def eliminar_resultado(clave: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM resultados WHERE clave = %s RETURNING id;", (clave,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": f"Clave '{clave}' eliminada correctamente"}
