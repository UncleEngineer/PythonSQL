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

c.execute("""CREATE TABLE IF NOT EXISTS expense_status (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER,
                checkstatus TEXT,
                comment TEXT )""")


def insert_expense(title,price,others):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with conn:
        command = 'INSERT INTO expense VALUES (?,?,?,?,?)' # SQL
        c.execute(command,(None,title,price,others,ts))
    conn.commit() # save to database
    print('saved')

    # select last record
    with conn:
        c.execute('SELECT * FROM expense ORDER BY ID DESC LIMIT 1')
        last_record = c.fetchone()
        print(last_record)
        last_id = last_record[0]
        insert_expense_status(last_id,'ยังไม่ตรวจสอบ','')


def view_expense():
    with conn:
        command = 'SELECT * FROM expense'
        c.execute(command)
        result = c.fetchall()
    return result

def delete_expense(ID):
    with conn:
        command = 'DELETE FROM expense WHERE ID=(?)'
        c.execute(command,([ID]))
    conn.commit()

def update_expense(ID,field,newvalue):
    with conn:
        command = 'UPDATE expense SET {} = (?) WHERE ID = (?)'.format(field)
        c.execute(command,(newvalue,ID))
    conn.commit()

def update_table(event=None):
    table.delete(*table.get_children()) #clear data in table
    for row in view_expense():
        table.insert('','end',values=row)

def search_expense(keyword):
    with conn:
        command = 'SELECT * FROM expense WHERE ID=(?) OR title LIKE ? OR others LIKE ?'
        text_search = '%{}%'.format(keyword)
        c.execute(command,(keyword,text_search,text_search))
        result = c.fetchall()
    return result

###################EXPENSE_STATUS###################
def insert_expense_status(expense_id,checkstatus,comment):
    with conn:
        command = 'INSERT INTO expense_status VALUES (?,?,?,?)' # SQL
        c.execute(command,(None,expense_id,checkstatus,comment))
    conn.commit() # save to database
    print('saved')

def view_expense_status():
    with conn:
        command = 'SELECT * FROM expense_status'
        c.execute(command)
        result = c.fetchall()
    return result

def delete_expense_status(ID):
    with conn:
        command = 'DELETE FROM expense_status WHERE expense_id=(?)'
        c.execute(command,([ID]))
    conn.commit()

def update_expense_status(expense_id,field,newvalue):
    with conn:
        command = 'UPDATE expense_status SET {} = (?) WHERE expense_id = (?)'.format(field)
        c.execute(command,(newvalue,expense_id))
    conn.commit()

#######################
GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by ลุง')
GUI.geometry('700x600')


FONT1 = ('Angsana New',20)

######TAB#######
PATH = os.getcwd() # check current folder

mainicon = os.path.join(PATH,'wallet.ico')
GUI.iconbitmap(mainicon)

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
        #add expense status
        # insert_expense_status(expense_id,checkstatus,comment)

        v_title.set('')
        v_price.set('')
        v_others.set('')
        E1.focus()
        update_table()
        # messagebox.showinfo('Message',title)

E3.bind('<Return>',Save) # ใส่ event=None ในฟังชั่น

B1 = ttk.Button(T1,text='Save',command=Save)
B1.pack(ipadx=20,ipady=10,pady=20)

########################TAB2#########################

F1 = Frame(T2)
F1.pack(pady=20)

v_search = StringVar()
ESearch = ttk.Entry(F1,textvariable=v_search,font=FONT1,width=30)
ESearch.grid(row=0,column=0)

def searchdata(event=None):
    search = v_search.get()
    data = search_expense(search)
    print(data)
    table.delete(*table.get_children()) #clear data in table
    for row in data:
        table.insert('','end',values=row)

ESearch.bind('<Return>',searchdata)

def cleardata(event=None):
    update_table()
    v_search.set('')
    ESearch.focus()

GUI.bind('<F12>',cleardata)

BSearch = ttk.Button(F1,text='ค้นหา',command=searchdata)
BSearch.grid(row=0,column=1,ipadx=20,ipady=10,padx=20)

header = ['ID','รายการ','ค่าใช้จ่าย','หมายเหตุ','วัน-เวลา']
hwidth = [50,200,100,200,120]

table = ttk.Treeview(T2, columns=header,show='headings',height=20)
table.pack()

for h,w in zip(header,hwidth):
    table.heading(h,text=h)
    table.column(h,width=w)

# table.insert('','end',values=[1,'น้ำดื่ม',10,'ร้านป้าแดง','2024-10-19 15:15:10'])

#########DELETE##########
def delete_table(event=None):
    try:
        print('delete..')
        select = table.selection()
        ID = table.item(select)['values'][0]
        choice = messagebox.askyesno('ลบข้อมูล','คุณต้องการลบข้อมูลใช่หรือไม่?')
        if choice == True:
            delete_expense(ID)
            #delete status
            delete_expense_status(ID)
            update_table()
    except Exception as e:
        print(e)
        messagebox.showwarning('เลือกรายการ','กรุณาเลือกรายการที่ต้องการลบ')

table.bind('<Delete>',delete_table)
############################

def updatedata(event=None):
    try:
        
        select = table.selection()
        data = table.item(select)['values']
        print(data)
        
        GUI2 = Toplevel()
        GUI2.title('แก้ไขข้อมูลการบันทึก')
        GUI2.geometry('700x600')

        L = Label(GUI2,text='รายการ',font=FONT1)
        L.pack()

        v_title_e = StringVar()
        v_title_e.set(data[1])
        E1 = ttk.Entry(GUI2,textvariable=v_title_e ,font=FONT1,width=50)
        E1.pack()

        #############
        L = Label(GUI2,text='ราคา',font=FONT1)
        L.pack()

        v_price_e = StringVar()
        v_price_e.set(data[2])
        E2 = ttk.Entry(GUI2,textvariable=v_price_e ,font=FONT1,width=50)
        E2.pack()

        #############
        L = Label(GUI2,text='หมายเหตุ',font=FONT1)
        L.pack()

        v_others_e = StringVar()
        v_others_e.set(data[3])
        E3 = ttk.Entry(GUI2,textvariable=v_others_e ,font=FONT1,width=50)
        E3.pack()


        expenseid = data[0]
        with conn:
            command = 'SELECT * FROM expense_status WHERE expense_id=(?)'
            c.execute(command,([expenseid]))
            d = c.fetchone()


        v_check = StringVar()
        FR1 = Frame(GUI2)
        FR1.pack(pady=20)
        R1 = ttk.Radiobutton(FR1,text='ตรวจสอบแล้ว',value='ตรวจสอบแล้ว',variable=v_check)
        R2 = ttk.Radiobutton(FR1,text='ยังไม่ตรวจสอบ',value='ยังไม่ตรวจสอบ',variable=v_check)
        
        print('Data:',d)
        if d[2] == 'ยังไม่ตรวจสอบ':
            R2.invoke() #เลือกค่าเริ่มต้น
        else:
            R1.invoke()
        
        
        
        R1.grid(row=0,column=0)
        R2.grid(row=0,column=1)


        L = Label(GUI2,text='เพิ่มเติม',font=FONT1)
        L.pack()
        v_comment = StringVar()
        v_comment.set(d[3])
        E4 = ttk.Entry(GUI2,textvariable=v_comment,font=FONT1,width=50)
        E4.pack()


    




        def Edit():
            ID = data[0]
            title_e = v_title_e.get()
            price_e = float(v_price_e.get())
            other_e = v_others_e.get()
            update_expense(ID,'title',title_e)
            update_expense(ID,'price',price_e)
            update_expense(ID,'others',other_e)

            check = v_check.get()
            comment = v_comment.get()
            update_expense_status(ID,'checkstatus',check)
            update_expense_status(ID,'comment',comment)

            update_table() #อัพเดทข้อมูลใหม่ใน table
            GUI2.destroy()          

        B1 = ttk.Button(GUI2,text='Save',command=Edit)
        B1.pack(ipadx=20,ipady=10,pady=20)

        GUI2.mainloop()


    except Exception as e:
        print(e)
        messagebox.showwarning('เลือกรายการ','กรุณาเลือกรายการที่ต้องการลบ')


table.bind('<Double-1>',updatedata)



update_table()
GUI.mainloop()