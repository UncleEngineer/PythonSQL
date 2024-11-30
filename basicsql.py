import sqlite3
from datetime import datetime # นำไปไว้บนสุด

# เชื่อมต่อกับฐานข้อมูล
conn = sqlite3.connect('expense.sqlite3')
# conn = sqlite3.connect('C:\\Users\\Uncle Engineer\\Desktop\\expense.sqlite3')
# ตัวดำเนินการ
c = conn.cursor()

# สร้างตารางชื่อ expense
c.execute("""CREATE TABLE IF NOT EXISTS expense (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                others TEXT,
                timestamp TEXT )""")


# ทดลอง insert ข้อมูล

def insert_expense(title,price,others):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn:
        command = 'INSERT INTO expense VALUES (?,?,?,?,?)' # SQL
        c.execute(command,(None,title,price,others,ts))
    conn.commit() # save to database
    print('saved')

def view_expense():
    with conn:
        command = 'SELECT * FROM expense'
        c.execute(command)
        result = c.fetchall()
    #print(result)
    return result

def update_expense(ID,field,newvalue):
    with conn:
        command = 'UPDATE expense SET {} = (?) WHERE ID = (?)'.format(field)
        c.execute(command,(newvalue,ID))
    conn.commit()

# update_expense(3,'price',150)

def delete_expense(ID):
    with conn:
        command = 'DELETE FROM expense WHERE ID=(?)'
        c.execute(command,([ID]))
    conn.commit()

############SEARCH############
def search_expense(keyword):
    with conn:
        command = 'SELECT * FROM expense WHERE ID=(?) OR title LIKE ? OR others LIKE ?'
        text_search = '%{}%'.format(keyword)
        c.execute(command,(keyword,text_search,text_search))
        result = c.fetchall()
    return result
    
# data = search_expense('บ้าน')
# print(data)
insert_expense('ค่าขนม',600,'กลับบ้านต่างจังหวัด')
print(view_expense())

with conn:
    c.execute('SELECT * FROM expense ORDER BY ID DESC LIMIT 1')
    last_record = c.fetchone()
    print(last_record)









# insert_expense('ค่าเดินทาง',600,'กลับบ้านต่างจังหวัด')

# print('#########โปรแกรมค่าใช้จ่ายประจำวัน########')
# for i in range(3):
#     print('#########{}#########'.format(i+1))
#     title = input('รายการ: ')
#     price = float(input('ราคา: ')) # float() คือการแปลงเป็นค่าทศนิยม
#     others = input('หมายเหตุ: ')
#     insert_expense(title,price,others)


# delete_expense(6)

# data = view_expense()
# for d in data:
#     print(d)