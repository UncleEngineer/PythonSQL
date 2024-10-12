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

# insert_expense('ค่าแท็กซี่',100,'ไปโรงเรียน')

print('#########โปรแกรมค่าใช้จ่ายประจำวัน########')
for i in range(3):
    print('#########{}#########'.format(i+1))
    title = input('รายการ: ')
    price = float(input('ราคา: ')) # float() คือการแปลงเป็นค่าทศนิยม
    others = input('หมายเหตุ: ')
    insert_expense(title,price,others)


