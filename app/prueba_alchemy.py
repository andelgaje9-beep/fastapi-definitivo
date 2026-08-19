from sqlalchemy import text, create_engine



"""
Este módulo es una prueba de cómo establecer una conexión con SQLite3.
Recordemos que podemos trabajar de dos formas:

1. En memoria: la base de datos se crea temporalmente en RAM y se elimina al cerrar el programa.
   Ideal para pruebas rápidas, ya que no persiste en disco.

2. Con un archivo .db: la base de datos se guarda en un archivo binario (.db),
   lo que permite que los cambios se registren de manera persistente y podamos
   acceder a ellos directamente desde el archivo.

La conexión puede apuntar tanto a una base en memoria como a un archivo físico,
dependiendo de la cadena de conexión que definamos.
"""

engine = create_engine("sqlite+pysqlite:///sqlite.db", echo=True)

#with engine.connect() as conn:
 #   result = conn.execute(text("select 'hello world'"))
  #  print(result.all())
    

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()