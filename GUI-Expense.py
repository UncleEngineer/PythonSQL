from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os


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

######TAB#######
PATH = os.getcwd() # check current folder
Tab = ttk.Notebook(GUI)
Tab.pack(fill=BOTH,expand=1)

T1 = Frame(Tab)
T2 = Frame(Tab)

icon_t1 = os.path.join(PATH,'form.png')
icon_t2 = os.path.join(PATH,'history.png')
iconimage_t1 = PhotoImage(file=icon_t1)
iconimage_t2 = PhotoImage(file=icon_t2)


Tab.add(T1,text='บันทึกค่าใช้จ่าย',image=iconimage_t1,compound='left')
Tab.add(T2,text='ประวัติค่าใช้จ่าย',image=iconimage_t2,compound='left')


#############


icon = os.path.join(PATH,'wallet.png')
iconimage = PhotoImage(file=icon)

L = Label(T1,image=iconimage)
L.pack()

L = Label(T1,text='โปรแกรมบันทึกค่าใช้จ่าย',font=('Angsana New',30,'bold'))
L.pack(pady=10)
#############
L = Label(T1,text='รายการ',font=FONT1)
L.pack()

v_title = StringVar()
E1 = ttk.Entry(T1,textvariable=v_title ,font=FONT1,width=50)
E1.pack()

#############
L = Label(T1,text='ราคา',font=FONT1)
L.pack()

v_price = StringVar()
E2 = ttk.Entry(T1,textvariable=v_price ,font=FONT1,width=50)
E2.pack()

#############
L = Label(T1,text='หมายเหตุ',font=FONT1)
L.pack()

v_others = StringVar()
E3 = ttk.Entry(T1,textvariable=v_others ,font=FONT1,width=50)
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

B1 = ttk.Button(T1,text='Save',command=Save)
B1.pack(ipadx=20,ipady=10,pady=20)

########################TAB2#########################

header = ['ID','รายการ','ค่าใช้จ่าย','หมายเหตุ','วัน-เวลา']
hwidth = [50,200,100,200,120]

table = ttk.Treeview(T2, columns=header,show='headings',height=20)
table.pack()

for h,w in zip(header,hwidth):
    table.heading(h,text=h)
    table.column(h,width=w)

table.insert('','end',values=[1,'น้ำดื่ม',10,'ร้านป้าแดง','2024-10-19 15:15:10'])

GUI.mainloop()