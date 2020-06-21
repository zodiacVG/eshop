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
    sql2="select goods_id from fullsell group by goods_id having count(*)>=1"   #寻找最热
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    context['hits'] = data2
    sql3 = "select goods_id from fullsell group by goods_id having count(*)<=1"  #寻找最冷门
    cursor.execute(sql3)
    data3 = cursor.fetchall()
    context['nbcs'] = data3
    return render(request, 'sellhome.html', context)


def show_all_sell(request):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    if request.POST:
        start_time=request.POST['start_time']
        end_time=request.POST['end_time']
        sql = "select * from fullsell where sell_time between %s and %s"
        cursor.execute(sql, [start_time,end_time])
    else:
        sql = "select * from fullsell "
        cursor.execute(sql)
    data = cursor.fetchall()
    context = {}
    context['sells'] = data
    return render(request, 'allsell.html', context)
