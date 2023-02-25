import sqlite3
import tkinter
try:
    cnn=sqlite3.connect("shop.db")
    print('opened database seccessfully')
except:
    print('an error occured in db connection')

##########creat tables
##query='''CREATE TABLE users
##(ID INTEGER PRIMARY KEY,
##user CHAR(25) NOT NULL,
##pass CHAR(25) NOT NULL,
##addr CHAR(50) NOT NULL,
##comment CHAR(50)
##)'''
##cnn.execute(query)
##print('table created successfully')
##cnn.close()
    
##query='''CREATE TABLE finalShop
##(ID INTEGER PRIMARY KEY,
##uid int  NOT NULL,
##pid int NOT NULL,
##qnt int NOT NULL
##)'''
##cnn.execute(query)
##print('table created successfully')
##cnn.close()


##########insert initial record in users table
##query='''INSERT INTO users(user,pass,addr)
##VALUES("admin","123456789","rasht")''' 
##cnn.execute(query)
##cnn.commit()
##cnn.close()
    
##########creat  new tables
##query='''CREATE TABLE products
##(ID INTEGER PRIMARY KEY,
##pname CHAR(25) NOT NULL,
##price CHAR(25) NOT NULL,
##qnt CHAR(50) NOT NULL
##)'''
##cnn.execute(query)
##print('table created successfully')
##cnn.close()

##query='''INSERT INTO products (pname,price,qnt)
##VALUES('nokia n35',100,20)''' 
##cnn.execute(query)
##cnn.commit()
##cnn.close()

    
############fuction 
def login():
    global userID
    user=user_txt.get()
    pas=pass_txt.get()
    query='''SELECT id FROM users WHERE user=? AND pass=?'''
    result=cnn.execute(query,(user,pas))
    rows=result.fetchall()
    if len(rows)<1:
        msg_lbl.configure(text='wrong username or password',fg='red')
        return
    userID=rows[0][0]
    
    msg_lbl.configure(text='welcome to your account',fg='green')
    btn_login.configure(state='disabled')
    btn_logout.configure(state='active')
    btn_shop.configure(state='active')
    btn_myshop.configure(state='active')
    user_txt.delete(0,'end')
    pass_txt.delete(0,'end')
    user_txt.configure(state='disabled')
    pass_txt.configure(state='disabled')

def logout():
    msg_lbl.configure(text='youn are logged out now',fg='green')
    btn_login.configure(state='active')
    btn_logout.configure(state='disabled')
    btn_shop.configure(state='disabled')
    user_txt.configure(state='normal')
    pass_txt.configure(state='normal')

        
    
def shop_win():
    global txt_id,txt_qnt,lbl_msg2,lstbox
    shp_win=tkinter.Toplevel(win)
    shp_win.geometry('500x500')
    shp_win.title('shopping')
    shp_win.resizable(False,False)
    ##------------------listbox
    lstbox=tkinter.Listbox(shp_win,width=350)
    lstbox.pack(pady=10)
    
#_____fetch all products
    query='''SELECT * FROM products'''
    result=cnn.execute(query)
    rows=result.fetchall()

    
#----------shop widgets
    global txt_id,txt_qnt,lbl_msg2
    lbl_id=tkinter.Label(shp_win,text='product ID:')
    lbl_id.pack()
    txt_id=tkinter.Entry(shp_win,width=25)
    txt_id.pack()

    lbl_qnt=tkinter.Label(shp_win,text='product qnt:')
    lbl_qnt.pack()
    txt_qnt=tkinter.Entry(shp_win,width=25)
    txt_qnt.pack()
    lbl_msg2=tkinter.Label(shp_win,text=" ")
    lbl_msg2.pack()
    btn_final_shop=tkinter.Button(shp_win,text="shop now!",command=final_shop)
    btn_final_shop.pack(pady=10)

    
###-------insert data to listbox
    for i in  rows:
        # msg=str(i[0])+"   "+ i[1]+"  price:  "+str(i[2]) +"  QNT:  "+ str(i[3])
        msg=f"{i[0]}-----{i[1]}----price:{i[2]}----qnt:{i[3]}"
        lstbox.insert("end",msg)
        update_shp()
    shp_win.mainloop()
    
    
    
def final_shop():
    global pid,pqn
    pid=txt_id.get()
    pqn=txt_qnt.get()
    if pid=="" or pqn =="":
        lbl_msg2.configure(text="please fill All the Blanks",fg="red")
        return
    
    query='''SELECT * FROM products WHERE id=?'''
    result=cnn.execute(query,(pid,))
    rows=result.fetchall()
    # print(rows)
    if len(rows)==0:
        lbl_msg2.configure(text="wrong product id ",fg="red")
        return

    real_pqnt=int(rows[0][3])
    
    if int(pqn)>real_pqnt:
        lbl_msg2.configure(text="Not enough product quantity ",fg="red")
        return
   ######------insert 
    query_final='''INSERT INTO finalShop(uid,pid,qnt)
               VALUES(?,?,?)'''
    cnn.execute(query_final,(userID,pid,pqn))
    cnn.commit()
    ######----update products
    new_qnt=real_pqnt-int(pqn)
    query='''UPDATE products SET qnt=? WHERE id=?'''
    cnn.execute(query,(new_qnt,pid))
    cnn.commit()
    lbl_msg2.configure(text="seccessfully added to cart",fg="green")
    txt_id.delete(0,"end")
    txt_qnt.delete(0,"end")
    update_shp()
    
    

    
def update_shp():
 
    query_ushp='''SELECT * FROM products'''
    result=cnn.execute(query_ushp)
    rows=result.fetchall()
    lstbox.delete(0,"end")
    for item in rows:
        msg=f"{item[0]}-------{item[1]}------price:{item[2]}-------qnt:{item[3]}"
        lstbox.insert("end",msg)


    
########----submit------
def submit():
    global txt_usr,txt_pas,txt_pasc,txt_adrs,lbl_msg3
    sub_win=tkinter.Toplevel(win)
    sub_win.geometry('500x500')
    sub_win.title('submit')
    lbl_usr=tkinter.Label(sub_win,text='username!:')
    lbl_usr.pack()
    txt_usr=tkinter.Entry(sub_win,width=25)
    txt_usr.pack()
    lbl_pas=tkinter.Label(sub_win,text='password:')
    lbl_pas.pack()
    txt_pas=tkinter.Entry(sub_win,width=25)
    txt_pas.pack()
    lbl_pasc=tkinter.Label(sub_win,text='password confirmation:')
    lbl_pasc.pack()
    txt_pasc=tkinter.Entry(sub_win,width=25)
    txt_pasc.pack()
    lbl_adrs=tkinter.Label(sub_win,text='address:')
    lbl_adrs.pack()
    txt_adrs=tkinter.Entry(sub_win,width=25)
    txt_adrs.pack()
    btn_sub=tkinter.Button(sub_win,text="insert product!",command=new_sub)
    btn_sub.pack(pady=20)
    lbl_msg3=tkinter.Label(sub_win,text="")
    lbl_msg3.pack(pady=20)
    sub_win.mainloop()
    
def new_sub():
    usersb=txt_usr.get()
    pssub=txt_pas.get()
    pascsub=txt_pasc.get()
    adrss=txt_adrs.get()
    if usersb=="" or pssub=="" or pascsub=="" or adrss=="" :
       lbl_msg3.configure(text="please fill All the Blanks",fg="red")
       return
    querysb='''INSERT INTO users(user,pass,addr)
            VALUES(?,?,?)'''
    cnn.execute(querysb,(usersb,pssub,adrss))
    cnn.commit()
    lbl_msg3.configure(text="successfully submit!",fg="purple")
    txt_usr.delete(0,"end")
    txt_pas.delete(0,"end")
    txt_pasc.delete(0,"end")
    txt_adrs.delete(0,"end")

    
    
############my shop---------
    
def myshop():
   mshp_win=tkinter.Toplevel(win)
   mshp_win.geometry('300x400')
   mshp_win.title('my shop')
   mlst=tkinter.Listbox(mshp_win,width=400)
   mlst.pack(pady=20)
   query_mshp='''SELECT * FROM finalShop WHERE pid=? and pqn=?'''
   rows=cnn.execute(query_mshp)
   for it in rows:
##    msg=str(it[0])+"   "+ it[1]+"  price:  "+str(it[2]) +"  QNT:  "+ str(it[3])
     msg=f"{it[0]}-----{it[1]}----price:{it[2]}----qnt:{it[3]}"
     mlst.insert("end",msg)
     mshp_win.mainloop()
  
##error mide va nmidonam chera say kardm nashod!



##########admin_plan------------------------
def admin_panel():
    global txt_padm,txt_prc,txt_qnti,lbl_msg4
    adm_win=tkinter.Toplevel(win)
    adm_win.geometry('500x500')
    adm_win.title('admin panel')
    lbl_padm=tkinter.Label(adm_win,text='PRODUCT NAME:')
    lbl_padm.pack()
    txt_padm=tkinter.Entry(adm_win,width=25)
    txt_padm.pack()
    lbl_prc=tkinter.Label(adm_win,text='PRICE:')
    lbl_prc.pack()
    txt_prc=tkinter.Entry(adm_win,width=25)
    txt_prc.pack()
    lbl_qnti=tkinter.Label(adm_win,text='QUANTITY:')
    lbl_qnti.pack()
    txt_qnti=tkinter.Entry(adm_win,width=25)
    txt_qnti.pack()
    btn_adm=tkinter.Button(adm_win,text="insert product!",command=insert_product)
    btn_adm.pack(pady=20)
    lbl_msg4=tkinter.Label(adm_win,text="")
    lbl_msg4.pack(pady=20)

def insert_product():
    product=txt_padm.get()
    pric=txt_prc.get()
    qntt=txt_qnti.get()
    if product=="" or pric=="" or qntt=="" :
       lbl_msg4.configure(text="please fill All the Blanks",fg="blue")
       return
    query_adm='''INSERT INTO products(pname,price,qnt)
              VALUES(?,?,?)'''
    cnn.execute(query_adm,(product,pric,qntt))
    cnn.commit()
    lbl_msg4.configure(text="added successfully",fg="purple")
    txt_padm.delete(0,"end")
    txt_prc.delete(0,"end")
    txt_qnti.delete(0,"end")
    
########## main
win=tkinter.Tk()
win.geometry("400x300")
win.title('login')

user_lbl=tkinter.Label(win,text='users: ')
user_lbl.pack()
user_txt=tkinter.Entry(win,width=25)
user_txt.pack()

pass_lbl=tkinter.Label(win,text='password: ')
pass_lbl.pack()
pass_txt=tkinter.Entry(win,width=25)
pass_txt.pack()

msg_lbl=tkinter.Label(win,text=" ")
msg_lbl.pack()

btn_admin=tkinter.Button(win,text='admin panel',command=admin_panel)
btn_admin.pack()

btn_login=tkinter.Button(win,text='login',command=login)
btn_login.pack()

btn_submit=tkinter.Button(win,text='submit',command=submit)
btn_submit.pack()

btn_logout=tkinter.Button(win,text='logout',state='disabled',command=logout)
btn_logout.pack()

btn_shop=tkinter.Button(win,text='shop',state='disabled',command=shop_win)
btn_shop.pack()

btn_myshop=tkinter.Button(win,text='my shop',state='disabled',command=myshop)
btn_myshop.pack()


win.mainloop()
