# Examen Parcial 2 - Pipeline DataMart Containerizado

**Estudiante:** Matrícula `125052726` (Último dígito: 6)  
**Lógica de Negocio:** Top 10 productos por ingreso total en el año.

---

##  Arquitectura del Sistema
- **Hadoop (debian:bookworm-slim):** Procesamiento distribuido MapReduce Streaming.
- **PostgreSQL 15:** Almacenamiento relacional del DataMart.
- **FastAPI / Uvicorn:** API REST para consultar y gestionar los resultados.
- **Docker Compose:** Orquestación de los tres servicios en red compartida.

---



1. **Levantar el entorno containerizado:**
   ```bash
   docker compose up --build -d
python3 generar_dataset.py
docker exec -it hadoop bash -c "
  rm -rf /app/mapreduce_output && \
  hadoop jar \$HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -D mapreduce.task.io.sort.mb=256 \
    -input /data/input/ventas_125052726.csv \
    -output /app/mapreduce_output \
    -mapper /app/mapreduce/mapper.py \
    -reducer /app/mapreduce/reducer.py \
    -file /app/mapreduce/mapper.py \
    -file /app/mapreduce/reducer.py
"
docker exec -it api python3 /app/scripts/cargar_resultados.py
curl http://localhost:8000/resultados
EXIT
