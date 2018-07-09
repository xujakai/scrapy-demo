
import mysql.connector

class LoadIpUtils:

    @staticmethod
    def loadIp():
        conn = mysql.connector.connect(user='root', password='123456', database='crawler', )
        cursor = conn.cursor()
        query_sql = """
                select type,ip,port from ip_proxy where is_valid=1;
                """
        cursor.execute(query_sql)
        list = []
        for type, ip, port in cursor:
            list.append('{}://{}:{}'.format(type, ip, port))
        cursor.close()
        conn.close()
        # print(list)
        return list