import connect_db as conn


def test():
    username = '07885'
    password = '.7885'
    sql = "select * from mappingdatatest where lotid = 'D1908150CED' "
    print(sql)

    res = conn.OracleConn.query(sql)
    if not res:
        print('查询不到数据')

    for row in res:
        a = row[0]
        b = row[1]
        c = row[6]
        print("a:", type(a), a)
        print("b:", type(str(b)), str(b))
        print("c:", type(c), c)

    print(res)


if __name__ == "__main__":
    test()
