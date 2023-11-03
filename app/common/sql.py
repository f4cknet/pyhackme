import pymysql

class ApiSql(object):

    def __enter__(self):
        self.conn = pymysql.connect(host="localhost",port=3306,user='hackme',passwd='admin123456',db='hackme')
        self.cur = self.conn.cursor()
        return self

    def write_sql(self,sql):
        self.cur.execute(sql)
        self.conn.commit()
        return

    def read_sql(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def __exit__(self,exc_type,exc_val,exc_tb):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    sql = "select password from user where phone = '13112345223' limit 0,1"
    with ApiSql() as s:
        data = s.read_sql(sql)

    print(data)