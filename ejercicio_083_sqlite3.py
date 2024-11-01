import sqlite3

# 1. Abrir la conexión (se abre con un nombre de fichero)
# 10. Cerrar la conexión
class Pelicula:
    def __init__(self, id, titulo, duracion):
        self.id = id
        self.titulo = titulo
        self.duracion = duracion

    def __str__(self):
        return f'ID:{self.id}. Título:{self.titulo}. Duración:{self.duracion}'
    
    def __repr__(self) -> str:
        return self.__str__()

class DBManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.connection = sqlite3.connect(file_name)
        self.__create_model()

    def __create_model(self):
        cursor = self.connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS peliculas 
                       (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       titulo TEXT NOT NULL, duracion INTEGER NOT NULL)""")
        cursor.close()

    #CRUD(C)-CREATE
    def insert_movie(self, movie):
        cursor = self.connection.cursor()
        #cursor.execute(f"INSERT INTO peliculas (titulo, duracion) VALUES ('{movie.titulo}',{movie.duracion})")
        cursor.execute("INSERT INTO peliculas (titulo, duracion) VALUES (?,?)",(movie.titulo, movie.duracion))
        self.connection.commit()
        cursor.close()

    #CRUD(R)-READ
    def get_movie(self, id):
        cursor = self.connection.cursor()
        registro = cursor.execute("SELECT * FROM peliculas WHERE id=?",
                                  (id,)).fetchone()
        pelicula = Pelicula(id=registro[0], titulo=registro[1], duracion=registro[2])
        cursor.close()
        return pelicula
    
    #CRUD(R)-READ
    def get_movies(self):
        cursor = self.connection.cursor()
        registros = cursor.execute("SELECT * FROM peliculas").fetchall()
        peliculas = []
        for registro in registros:
            peliculas.append(Pelicula(id=registro[0],titulo=registro[1],
                                      duracion=registro[2]))
        cursor.close()
        return peliculas
    
    #CRUD(U)-UPDATE
    def update_movie(self, movie):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE peliculas SET titulo=?, duracion=? WHERE id=?"
                       ,(movie.titulo, movie.duracion, movie.id))
        self.connection.commit()
        cursor.close()

    #CRUD(D)-DELETE
    def delete_movie(self, id):
        cursor = self.connection.cursor()
        datos = cursor.execute("DELETE FROM peliculas WHERE id=?",(id,))
        self.connection.commit()
        cursor.close()
        if (datos.rowcount==0):
            raise IndexError("El identificador de la película")

    def __del__(self):
        self.connection.close()

DB_NAME = "movies.db"

#pelicula = Pelicula(0, 'Superman', 90)
db_manager = DBManager(DB_NAME)
pelicula = db_manager.get_movie(1)
pelicula.duracion = 1_000
db_manager.update_movie(pelicula)
db_manager.delete_movie(1)
