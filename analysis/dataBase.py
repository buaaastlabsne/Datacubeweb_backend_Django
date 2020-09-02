import pymysql


def connect(user, passwd, db):
    try:
        conn = pymysql.connect('localhost', user=user, passwd=passwd)
    except:
        print("数据库账号或密码输入错误")
        return 0
    try:
        database = db
        conn.select_db(database)
    except:
        print("数据库名输入错误")
        return 1
    return 2


def query_tables(user, passwd, db):
    # 查看表的数量，表的名称
    conn = pymysql.connect('localhost', user=user, passwd=passwd)
    cursor = conn.cursor()
    conn.select_db(db)
    sql = 'show tables from '+db
    rows = cursor.execute(sql)  # 返回执行成功的结果条数
    print(f'一共有 {rows} 张表')
    tables = []
    for d in cursor.fetchall():
        print(d)
        tables.append(d)
    return tables


# query_tables("root","root","sne")
def query_a_table(user, passwd, db, tb):
    conn = pymysql.connect('localhost', user=user, passwd=passwd)
    cursor = conn.cursor()
    conn.select_db(db)
    # 查看某个表的字段信息等
    sql = "select COLUMN_NAME,DATA_TYPE,COLUMN_COMMENT,NULL from information_schema.COLUMNS where table_name =" \
          " "+"'"+tb+"'"
    info = cursor.execute(sql)
    print(info)
    info = []
    for d in cursor.fetchall():
        print(d)
        info.append(d)
    return info

# query_a_table("root","root","sne","tpv2")