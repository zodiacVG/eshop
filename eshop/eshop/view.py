from django.shortcuts import render
import pymysql


def show_sells(request):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    if request.POST:
        goods_id = request.POST['goods_id']
        # sell_id=request.POST['sell_id']
        # customer_id=request.POST['customer_id']
        # seller_id=request.POST['seller_id']
        sql = "select * from fullsell where goods_id= %s"
        cursor.execute(sql, goods_id)
    else:
        sql = "select * from fullsell "
        cursor.execute(sql)
    data = cursor.fetchall()
    context = {}
    context['sells'] = data
    return render(request, 'sellhome.html', context)

