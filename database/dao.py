from database.DB_connect import DBConnect

class DAO:
    @staticmethod
    def query_esempio():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM esempio """

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_anni():

        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection")
            return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct YEAR(s_datetime) as anno FROM sighting """
        cursor.execute(query)

        for row in cursor:
            result.append(row["anno"])

        cursor.close()
        conn.close()
        return sorted(result)

    @staticmethod
    def read_forme():
        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection")
            return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct s.shape as forma FROM sighting s WHERE s.shape!=''"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["forma"])

        cursor.close()
        conn.close()
        return sorted(result)

    @staticmethod
    def read_vertici():
        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection")
            return None

        result = []
        map_coordinate = dict()

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT distinct id, lat, lng FROM state s"""
        cursor.execute(query)

        for row in cursor:
            result.append(row["id"])
            map_coordinate[row["id"]] = (row["lat"], row["lng"])

        cursor.close()
        conn.close()
        return sorted(result), map_coordinate

    @staticmethod
    def read_archi():
        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection")
            return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT state1, state2 FROM neighbor n"""
        cursor.execute(query)

        for row in cursor:
            arco ={row["state1"], row['state2']}
            if arco not in result:
                result.append((row["state1"], row["state2"]))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_vertici_validi(anno, forma):
        conn = DBConnect.get_connection()
        if not conn:
            print("No database connection")
            return None

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT s.state as Stato, count(*) as NumEventi
                    FROM sighting s 
                    WHERE YEAR(s.s_datetime)=%s and s.shape = %s
                    GROUP BY s.state """
        cursor.execute(query,(anno, forma,))

        for row in cursor:
            result.append((row["Stato"].upper(), row["NumEventi"]))

        cursor.close()
        conn.close()
        return result