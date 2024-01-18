from app.common.sql import ApiSql

def query_order(orderid):
    sql = """SELECT order.id, order.generatetime, order.status,order.payment_method,address.receiver,goods.goodsname,address.phone,address.addressname 
            FROM `order`
            JOIN address on order.address_id = address.id
            join goods on order.goods_id = goods.id 
            where order.id='%s'""" % (orderid)
    print(sql)
    with ApiSql() as s:
        data = s.read_sql(sql)
    return data