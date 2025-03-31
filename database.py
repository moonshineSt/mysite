import pandas as pd
import pymysql

class MyDB:
    # 변수 : 서버의 주소, 포트번호, 유저명, 비밀번호, 데이터베이스명
    # 변수들의 기본값을 설정(로컬 피씨)
    def __init__(self,
                 host = "127.0.0.1",
                 port = 3306,
                 user = 'root',
                 pwd = '1234',
                 db = 'ubion'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db


    # 서버와 연결하고 커서를 생성하는 함수
    def connect_sql(self):
        self.server = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.user,
            password=self.pwd,
            db = self.db  
        )
        self.cursor = self.server.cursor(pymysql.cursors.DictCursor)

    def close_sql(self):
        self.server.close()

    def execute_query(self, sql_query, *values, inplace = False):
        self.connect_sql()
        self.cursor.execute(sql_query, values)
        #if sql_query.upper().lstrip().startswith('SELECT'):
        if sql_query.upper().split()[0] == 'SELECT':
            sql_data = self.cursor.fetchall()
            result = pd.DataFrame(sql_data)
        else:
            # insert, update, delete인 경우
            # inplace True인 경우
            if inplace:
                self.server.commit()
            result = "Query Ok"

        self.close_sql()

        return result