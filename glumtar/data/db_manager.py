import sqlite3

"""Mi primera consulta para leer datos es SELECT Position, Name, Score FROM Glumtar_best_scores;"""


class DBManager:
    def __init__(self, db_route):
        self.db_route = db_route
        self.column_names = []

    def consultSQL(self, consult):
        # 1. Conectar a la base de datos
        connection = sqlite3.connect(self.db_route)

        # 2. Abrir cursor
        cursor = connection.cursor()

        # 3. Ejecutar la consulta
        cursor.execute(consult)

        # 4. Tratar los datos
        # 4.1 Obtener los datos
        # Da una lista. Hay un fetchone también.
        returned_data = cursor.fetchall()

        # 4.2 Los guardo localmente
        self.recorded_best_scores = []
        self.column_names = []
        # Esto me va a dar una tupla con los nombres de la columna de la base de datos.
        for column in cursor.description:
            self.column_names.append(column[0])

        for data_in_recorded_row in returned_data:  # Esto me va a venir en una tupla con todos los datos del record
            # Diccionario vacío que tendrá los nombres de las columnas como key y los datos de cada columna como value.
            record = {}
            value = 0
            for name in self.column_names:
                record[name] = data_in_recorded_row[value]
                value += 1
            self.recorded_best_scores.append(record)

        # 5. Cerrar la conexión
        connection.close()

        # 6. Devolver los resultados
        return self.recorded_best_scores

    def insertSQL(self, insert, values):
        # 1. Conectar a la base de datos
        connection = sqlite3.connect(self.db_route)

        # 2. Abrir cursor
        cursor = connection.cursor()

        # 3. Ejecutar la consulta
        cursor.execute(insert, values)

        # 4. Tratar los datos
        # 4.1 Obtener los datos
        # Da una lista. Hay un fetchone también.
        inserted_record = cursor.fetchall()

        # 4.2 Los guardo localmente
        # self.recorded_best_scores = []  # Creo que aquí debería hacer un append?

        # Esto me va a dar una tupla con los nombres de la columna de la base de datos.
        # for column in cursor.description:
        #    self.column_names.append(column[0])

        # 5. Cerrar la conexión
        connection.commit()
        print(f'Debería haber insertado el dato')

        connection.close()

        # 6. Devolver los resultados
        return inserted_record, f'He terminado de pasar por el insert'
