from database.DB_connect import DBConnect
from modell.team import Team


class DAO:
    @staticmethod
    def get_years_from_1980():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT a.year 
                    FROM appearance a
                     WHERE a.year >= 1980
                     GROUP BY a.year 
                     ORDER BY a.year ASC"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_teams_for_year(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT id, team_code, name
                    FROM team
                    WHERE year = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(row["id"], row["team_code"], row["name"]))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def read_peso(anno):
        conn = DBConnect.get_connection()

        result = {}

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT s.team_id as team_id, SUM(s.salary) AS salary
                    FROM salary s
                    WHERE year = %s
                    GROUP BY s.team_id """

        cursor.execute(query, (anno,))

        for row in cursor:
            result[row['team_id']] = row["salary"]

        cursor.close()
        conn.close()
        return result

