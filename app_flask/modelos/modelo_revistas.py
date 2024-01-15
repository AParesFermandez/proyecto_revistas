from app_flask.config.mysqlconnection import connectToMySQL
from flask import flash, request
from app_flask import BASE_DATOS

class Revista:
    def __init__(self, datos):
        self.id = datos['id']
        self.id_author = datos['id_author']
        self.titulo = datos['titulo']
        self.descripcion = datos['descripcion']
        self.fecha_creacion = datos['fecha_creacion']
        self.fecha_actualizacion = datos['fecha_actualizacion']

    @classmethod
    def crear_revista(cls, datos_revista):
        query = """
                INSERT INTO revista(id_author, titulo, descripcion)
                VALUES (%(id_author)s, %(titulo)s, %(descripcion)s);
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos_revista)

    @classmethod
    def obtener_por_id(cls, id_revista):
        query = """
                SELECT *
                FROM revista
                WHERE id = %(id_revista)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, {'id_revista': id_revista})
        if len(resultado) == 0:
            return None
        return cls(resultado[0])

    @classmethod
    def obtener_todos(cls):
        query = """
                SELECT r.*, u.nombre AS nombre_usuario
                FROM revista r
                JOIN usuario u ON r.id_author = u.id;
                """
        resultados = connectToMySQL(BASE_DATOS).query_db(query)
        revistas = []
        for resultado in resultados:
            revista = cls(resultado)
            revista.nombre_usuario = resultado['nombre_usuario']
            revistas.append(revista)
        return revistas

    @classmethod
    def obtener_todos_con_usuario(cls):
        query = """
                SELECT r.*, u.nombre AS nombre_usuario
                FROM revista r
                JOIN usuario u ON r.id_author = u.id;
                """
        resultados = connectToMySQL(BASE_DATOS).query_db(query)
        revistas = [cls(resultado) for resultado in resultados]
        return revistas
    
    @classmethod
    def obtener_uno_con_usuario(cls, datos_revista):
        query = """
                SELECT r.*, u.nombre AS nombre_usuario
                FROM revista r
                JOIN usuario u ON r.id_author = u.id
                WHERE r.id = %(id_revista)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, datos_revista)

        if not resultado or len(resultado) == 0:
            return None

        return cls(resultado[0])

    @classmethod
    def obtener_detalles_por_id_usuario(cls, id_usuario, id_revista):
        query = """
                SELECT r.*, u.nombre AS nombre_usuario
                FROM revista r
                JOIN usuario u ON r.id_author = u.id
                WHERE r.id = %(id_revista)s AND r.id_author = %(id_usuario)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, {'id_revista': id_revista, 'id_usuario': id_usuario})

        if not resultado or len(resultado) == 0:
            return None

        revista = cls(resultado[0])
        revista.nombre_usuario = resultado[0]['nombre_usuario']
        return revista

    @classmethod
    def obtener_revistas_por_usuario(cls, id_usuario):
        query = """
                SELECT *
                FROM revista
                WHERE id_author = %(id_usuario)s;
                """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, {'id_usuario': id_usuario})
        return [cls(revista) for revista in resultado]
    
    @classmethod
    def elimina_uno(cls, datos):
        query = """
                DELETE FROM revista
                WHERE id = %(id)s;
                """
        return connectToMySQL(BASE_DATOS).query_db(query, datos)

    @staticmethod
    def validar_revistas(datos_revista):
        es_valido = True

        if len(datos_revista['titulo']) < 2:
            es_valido = False
            flash('El título debe tener al menos 2 caracteres.', 'error_titulo')

        if len(datos_revista['descripcion']) < 10:
            es_valido = False
            flash('La descripción debe tener al menos 10 caracteres.', 'error_descripcion')

        return es_valido
