import os
import psycopg2

DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "datamart")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

def cargar():
    conn = psycopg2.connect(
        host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS resultados (
            id SERIAL PRIMARY KEY,
            clave VARCHAR(255) UNIQUE NOT NULL,
            valor NUMERIC(15, 2) NOT NULL
        );
    """)

    filepath = "/app/mapreduce_output/part-00000"
    if not os.path.exists(filepath):
        filepath = "mapreduce_output/part-00000"

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) == 2:
                clave, valor = parts[0], float(parts[1])
                cur.execute("""
                    INSERT INTO resultados (clave, valor)
                    VALUES (%s, %s)
                    ON CONFLICT (clave) DO UPDATE SET valor = EXCLUDED.valor;
                """, (clave, valor))

    conn.commit()
    cur.close()
    conn.close()
    print("Resultados cargados exitosamente en PostgreSQL.")

if __name__ == "__main__":
    cargar()
