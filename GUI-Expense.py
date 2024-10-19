from tkinter import *
from tkinter import ttk
from tkinter import messagebox


##########SQL##########
import sqlite3
from datetime import datetime # นำไปไว้บนสุด
conn = sqlite3.connect('expense.sqlite3')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS expense (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                price REAL,
                others TEXT,
                timestamp TEXT )""")
def insert_expense(title,price,others):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn:
        command = 'INSERT INTO expense VALUES (?,?,?,?,?)' # SQL
        c.execute(command,(None,title,price,others,ts))
    conn.commit() # save to database
    print('saved')



#######################
GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by ลุง')
GUI.geometry('700x600')

FONT1 = ('Angsana New',20)

#############
L = Label(GUI,text='โปรแกรมบันทึกค่าใช้จ่าย',font=('Angsana New',30,'bold'))
L.pack(pady=10)
#############
L = Label(GUI,text='รายการ',font=FONT1)
L.pack()

v_title = StringVar()
E1 = ttk.Entry(GUI,textvariable=v_title ,font=FONT1,width=50)
E1.pack()

#############
L = Label(GUI,text='ราคา',font=FONT1)
L.pack()

v_price = StringVar()
E2 = ttk.Entry(GUI,textvariable=v_price ,font=FONT1,width=50)
E2.pack()

#############
L = Label(GUI,text='หมายเหตุ',font=FONT1)
L.pack()

v_others = StringVar()
E3 = ttk.Entry(GUI,textvariable=v_others ,font=FONT1,width=50)
E3.pack()


def Save(event=None):

    if v_price.get() == '':
        E2.focus()
        messagebox.showinfo('ข้อมูลไม่ครบ','กรุณากรอกตัวเลขราคาด้วย')
    else:
        title = v_title.get() # ดึงค่ามาจาก v_title
        price = float(v_price.get())
        others = v_others.get()

        print(title, price, others)
        insert_expense(title,price,others)

        v_title.set('')
        v_price.set('')
        v_others.set('')
        E1.focus()
        # messagebox.showinfo('Message',title)

E3.bind('<Return>',Save) # ใส่ event=None ในฟังชั่น

B1 = ttk.Button(GUI,text='Save',command=Save)
B1.pack(ipadx=20,ipady=10,pady=20)


GUI.mainloop()