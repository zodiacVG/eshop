from django.shortcuts import render,redirect
import pymysql


def show_sells(request):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    if request.POST:
        goods_id = request.POST['goods_id']
        sql = "select * from fullsell where goods_id= %s"
        cursor.execute(sql, goods_id)
    else:
        sql = "select * from fullsell "
        cursor.execute(sql)
    data = cursor.fetchall()
    context = {}
    context['sells'] = data
    sql2="select goods_id,goods_name,count(*) as total_num from fullsell join goods using(goods_id) group by goods_id having count(*)>=1"   #寻找最热
    cursor.execute(sql2)
    data2 = cursor.fetchall()
    context['hits'] = data2
    sql3 = "select goods_id,goods_name,count(*) as total_num  from fullsell join goods using(goods_id) group by goods_id having count(*)<=1"  #寻找最冷门
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


def allgoods(request):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    if request.POST:
        goods_id=request.POST['goods_id']
        sql = "select * from fullgoods where goods_id=%s"
        cursor.execute(sql,goods_id)
    else:
        sql = "select * from fullgoods "
        cursor.execute(sql)
    data = cursor.fetchall()
    context = {}
    context['goods'] = data
    return render(request, 'showgoods.html', context)



def show_goods_sell(request,goods_id):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    context = {}
    if request.POST:
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        sql = "select * from fullsell where goods_id=%s and sell_time between %s and %s"
        cursor.execute(sql,[goods_id,start_time,end_time])
        data = cursor.fetchall()
        context['sells']=data

        sql2="select sum(sell_num) as num from fullsell where goods_id=%s group by goods_id"
        cursor.execute(sql2, goods_id)
        data2 = cursor.fetchall()
        context['num'] = data2
    else:
        sql3 = "select * from fullsell where goods_id=%s"
        cursor.execute(sql3,goods_id)
        data3 = cursor.fetchall()
        context['sells'] = data3

        sql4 = "select sum(sell_num) as num from fullsell where goods_id=%s group by goods_id"
        cursor.execute(sql4, goods_id)
        data4 = cursor.fetchall()
        context['num'] = data4

    return render(request, 'showgoodssell.html', context)


def returngoods(request):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    context = {}
    if request.POST:
        return_id=request.POST['return_id']
        goods_id = request.POST['goods_id']
        return_num = request.POST['return_num']
        return_reason = request.POST['return_reason']
        return_time = request.POST['return_time']
        sell_id = request.POST['sell_id']
        sql = "insert into returngoods values (%s,%s,%s,%s,%s,%s,0.00)"
        cursor.execute(sql, [return_id,goods_id,return_num,return_reason,return_time,sell_id])
        db.commit()
        context['result']="成功提交退货"
        context['box']={'return_id':''}
    else:
        context['result'] = "请输入退货单数据"
        context['box'] = {'return_id':''}
    return render(request, 'returngoods.html', context)


def modifysell(request,sell_id):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    context = {}
    if request.POST:
        sell_id=request.POST['sell_id']
        goods_id=request.POST['goods_id']
        sell_price=request.POST['sell_price']
        sell_num=request.POST['sell_num']
        customer_id=request.POST['customer_id']
        seller_id=request.POST['selller_id']
        sql = " update sell_detail set sell_price=%s,sell_num=%s,customer_id=%s,seller_id=%s where sell_id=%s and goods_id=%s"
        cursor.execute(sql, [sell_price,sell_num,customer_id,seller_id,sell_id,goods_id])
        sql2="select * from sell_detail where sell_id=%s"
        cursor.execute(sql2, sell_id)
        data = cursor.fetchall()
        db.commit()
        context['result']="成功修改"
        context['sells']=data
    else:
        context['result'] = "请谨慎修改"
        sql3 = "select * from sell_detail where sell_id=%s"
        cursor.execute(sql3,sell_id)
        data2=cursor.fetchall()
        context['sells']=data2

    return render(request, 'modifysell.html', context)

def deletesell(request,sell_id):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    context = {}
    sql="delete from sell_detail where sell_id=%s"
    cursor.execute(sql,sell_id)
    db.commit()

    return redirect('/show_all_sell')


def addsell(request):
    db = pymysql.connect("localhost", "testuser", "PlayStation5", "eshop", port=3306,
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    context = {}
    if request.POST:
        sell_id = request.POST['sell_id']
        goods_id = request.POST['goods_id']
        sell_price = request.POST['sell_price']
        sell_num = request.POST['sell_num']
        customer_id = request.POST['customer_id']
        sell_time= request.POST['sell_time']
        seller_id = request.POST['seller_id']
        sell_statement= request.POST['sell_statement']
        sql = "insert into sell values (%s,%s,%s)"
        cursor.execute(sql, [sell_id,sell_time,sell_statement])
        sql2="insert into sell_detail values(%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql2,[sell_id,goods_id,sell_price,sell_num,customer_id,seller_id])
        db.commit()
        context['result']="成功提交销售单"
        context['box'] = {'return_id': ''}
    else:
        context['result'] = "请输入销售单信息"
        context['box'] = {'return_id':''}
    return render(request, 'addsell.html', context)