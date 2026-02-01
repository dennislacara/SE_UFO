from database.DB_connect import DBConnect
from model.sighting import Sighting
from model.state import State
from model.neighbor import Neighbor

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
    def read_sightings():
        conn = DBConnect.get_connection()
        if not conn:
            print('no DB connection, read_sightings()')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                select *
                from sighting s 
                """

        try:
            cursor.execute(query)

            for row in cursor:
                sighting = Sighting(**row)
                result.append(sighting)
        except Exception:
            print('Errore nella query')
            result = None
        finally:
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def read_states():
        conn = DBConnect.get_connection()
        if not conn:
            print('no DB connection, read_states()')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                select *
                from state s
                """
        try:
            cursor.execute(query)

            for row in cursor:
                state = State(**row)
                result.append(state)
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()
        return result

    @staticmethod
    def read_archi(anno, forma):
        conn = DBConnect.get_connection()
        if not conn:
            print('no DB connection, read_states()')
            return
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                with tab as(
                SELECT s.state, s.shape , COUNT(*) as avvistamenti
                FROM sighting s
                WHERE YEAR(s.s_datetime) = %s and s.shape = %s
                GROUP BY s.state 
                ),
                tab2 as(
                SELECT n.state1 , n.state2 , tA.avvistamenti avvA, tB.avvistamenti avvB
                FROM neighbor n LEFT OUTER JOIN tab tA on n.state1 = tA.state LEFT OUTER JOIN tab tB on n.state2 = tB.state
                )
                SELECT
                    state1,
                    state2,
                    COALESCE(avvA, 0) +
                    COALESCE(avvB, 0) AS total_sightings
                FROM tab2
                """
        try:
            cursor.execute(query, (anno, forma, ))

            for row in cursor:
                neighbor = Neighbor(**row)
                result.append(neighbor)
        except Exception as e:
            print(e)
            result = None
        finally:
            cursor.close()
            conn.close()
        return result