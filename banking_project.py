from tkinter import Tk, Frame, Label, Entry, Button, messagebox, simpledialog,filedialog
from tkinter.ttk import Combobox
import time
from PIL import Image, ImageTk
import autotable_creation
import random
import sqlite3
import gmail
from tkintertable import TableCanvas, TableModel 
import re
import shutil
import os


class SliderAnimation:
    def __init__(self, root, start_x, end_x):
     
        self.root = root
        self.label = Label(root, text='24/7 Services Available', font=('Helvetica', 20) ,bg="#F2F7F2")
        self.label.place(x=start_x, y=110)
        self.start_x = start_x
        self.end_x = end_x
        self.x = start_x  # Initialize self.x with start_x
        self.speed = 1
        self.animate()

    def animate(self):
        """
        Animates the slider by moving it horizontally.
        """
        self.label.place(x=self.x ,y=110)
        self.x +=self.speed
        if self.x > self.end_x:
            self.speed= -self.speed
        elif self.x < self.start_x:
            self.speed = - self.speed
        self.root.after(3,self.animate)

# Screen
win = Tk()
win.title("My project")
win.state("zoomed")
win.resizable(width=False, height=False)
win.configure(bg="#F2F7F2")
# Header
header_title = Label(win, text="Banking Automation", font=("arial", 40, "bold", "underline"), bg="#F2F7F2")
header_title.pack()
current_date = time.strftime("%d-%b-%Y")
header_date = Label(win, text=current_date, font=("arial", 23, "bold"), fg="#C8A2C8", bg="#F2F7F2")
header_date.pack()

slider= SliderAnimation(win, 200, 800)

# Footer
footer_title = Label(win, text="By: Bhumika Sharma\nProject Guide: Mr. Aditya", font=("arial", 25), fg="#C8A2C8", bg="#F2F7F2")
footer_title.pack(side="bottom")

# Image 1
img = Image.open('logo.png').resize((200, 138))
bitmap_img = ImageTk.PhotoImage(img, master=win)
logo_label = Label(win, image=bitmap_img)
logo_label.place(relx=0, rely=0)

# Image 2
img2 = Image.open('bank.png').resize((200, 138))
bitmap_img2 = ImageTk.PhotoImage(img2, master=win)
logo2_label = Label(win, image=bitmap_img2)
logo2_label.place(relx=.85, rely=0)


# Main screen frames(screen)
def main_screen():
    frm = Frame(win, highlightbackground="brown", highlightthickness=2)
    frm.configure(bg="#C2B97F")
    frm.place(relx=0, rely=.2, relwidth=1, relheight=.68)


    #image 3

    img3 = Image.open("debit_card.png").resize((100, 100))
    bitmap_img3 = ImageTk.PhotoImage(img3, master=win)
    photo3_label = Label(frm, image=bitmap_img3)
    photo3_label.image=bitmap_img3
    photo3_label.place(relx=0.63, rely=0.5)

    global cap
    cap=''
    def generate_captcha():
        global cap
        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(65,90))
        cap=cap+ch

        d=str(random.randint(0,9))
        cap=cap+d
        ch=chr(random.randint(65,90))
        cap=cap+ch

        return cap
# reset button command    
    def reset():
        acn_entry.delete(0,"end")
        pass_entry.delete(0,"end")
        acn_entry.focus()

    # Login click
    def login_click():
        global uacn
        uacn=acn_entry.get()
        upass=pass_entry.get()
        urole=role_cb.get()

#data validation on acn no. and pass
        if len(uacn)==0 or len(upass)==0:
            messagebox.showerror("login","Account No. or Password can't be empty")
            return
        if captcha_entry.get()!=cap:
            messagebox.showerror("login","Invalid captcha")
            return

        uacn=int(uacn)
        if uacn==0 and upass=='admin' and urole=='Admin':
            frm.destroy()
            welcome_admin_screen()
        elif urole=='User':
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select * from users where users_acno=? and users_pass=?',(uacn,upass))
            tup=cur_obj.fetchone()
            if tup==None:
                messagebox.showerror('login','Invalid A/c no./Password')
            else:
                global uname
                uname=tup[2]
                frm.destroy()
                welcome_user_screen()
        else:
            messagebox.showerror('login','Invalid Role')
    # Main screen input
    acn_label = Label(frm, font=("arial", 16, "bold"), bg="#C2B97F", text="Account no.")
    acn_label.place(relx=.2, rely=.1)

    acn_entry = Entry(frm, font=("arial", 16, "bold"), bd=5)
    acn_entry.place(relx=.4, rely=.1)
    acn_entry.focus()

    pass_label = Label(frm, font=("arial", 16, "bold"), bg="#C2B97F", text="Password")
    pass_label.place(relx=.2, rely=.25)

    pass_entry = Entry(frm, font=("arial", 16, "bold"), bd=5, show="*")
    pass_entry.place(relx=.4, rely=.25)

    role_label = Label(frm, font=("arial", 16, "bold"), bg="#C2B97F", text="Role")
    role_label.place(relx=.22, rely=.38)

    role_cb = Combobox(frm, font=('arial', 16, 'bold'), values=['User', 'Admin'])
    role_cb.current(0)
    role_cb.place(relx=.4, rely=.38)

    gen_captcha_label=Label(frm,font=('arial',16,'bold'),width=7,bg='white',fg='green',text=generate_captcha())
    gen_captcha_label.place(relx=.45,rely=.48)

    captcha_label=Label(frm,font=('arial',16,'bold'),bg='#C2B97F',text="Captcha")
    captcha_label.place(relx=.22,rely=.6)

    captcha_entry=Entry(frm,font=('arial',16,'bold'),bd=5)
    captcha_entry.place(relx=.4,rely=.6)

    login_btn=Button(frm,text='Login',font=('arial',16,'bold'),bg='#C8A2C8',bd=5,command=login_click)
    login_btn.place(relx=.4,rely=.73)

    reset_btn=Button(frm,command=reset,text='Reset',font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
    reset_btn.place(relx=.53,rely=.73)

    forgot_btn=Button(frm,command=forgot_password_screen,width=18,text='forgot password',font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
    forgot_btn.place(relx=.4,rely=.85)


#welcome screen only for admin

def welcome_admin_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='#C2B97F')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.68)

#logout click command

    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly confirm?')
        if resp:
            frm.destroy()
            main_screen()

#logout button
    logout_btn=Button(frm,command=logout_click,text='Logout',font=('arial',20,'bold'),bg='#C8A2C8',bd=5)
    logout_btn.place(relx=.9,rely=0)

#(welcome_admin_screen) choices
# create user screen
#frame
    def create_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

        def reset():
            fname_entry.delete(0,"end")
            mob_entry.delete(0,"end")
            email_entry.delete(0,"end")
            adhar_entry.delete(0,"end")
#database connection
        def open_acn():
            uname=fname_entry.get() 
            umob=mob_entry.get()
            uemail=email_entry.get()
            uadhar=adhar_entry.get()
            ubal=0
            upass=str(random.randint(100000,999999))
#for empty inputs            
            if len(uname)==0 or len(umob)==0 or len(uemail)==0 or len(uadhar)==0:
                messagebox.showerror('create','Empty fields are not allowed')
                return
            
            if not re.fullmatch('[a-zA-Z ]+',uname):
                messagebox.showerror('create','Kindly enter valid name')
                return

            if not re.fullmatch('[6-9][0-9]{9}',umob):
                messagebox.showerror('create','Kindly enter valid Mobile no')
                return
            
            if not re.fullmatch('[a-z0-9_.]+@[a-z]+[.][a-z]+',uemail):
                messagebox.showerror('create','Kindly enter valid Email')
                return
            
            if not re.fullmatch('[0-9]{12}',uadhar):
                messagebox.showerror('create','Kindly enter valid Adhar')
                return
#to be reset button command adding left
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into users(users_pass,users_name,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)',(upass,uname,umob,uemail,ubal,uadhar,current_date))
            con_obj.commit()
            con_obj.close()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select max(users_acno) from users')
            tup=cur_obj.fetchone()
            acn=tup[0]
            con_obj.close()
#gmail
            try:
                gmail_con=gmail.GMail('bhumikasharma1808@gmail.com','agym rfun zlaj zqlg')
                umsg=f'''Hello,{uname}
                Welcome to City Bank of India,
                Your A/C no. is: {acn}
                Your Password is: {upass}
                Kindly change your Password after your first login

                Thank You
                Have a Nice Day
                '''
                msg=gmail.Message(to=uemail,subject='Account Opened',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('open acn','Your Account has been successfully created! Kindly check your Email for your Account no. and Password')
                print("Email sent successfully.")

            except Exception as e:
                messagebox.showerror('open acn', f'Something Went Wrong: {e}')
                print(f"Error sending email: {e}")



# create user wlcome user text
        title_ifrm =Label(ifrm,font=('arial',20,'bold'),text='This is Create User Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()
# name entry and label
        fname_label =Label(ifrm,font=('arial',18,'bold'),text='Full Name',bg='#F2F7F2',fg='#333333')
        fname_label.place(relx=.1,rely=.1)

        fname_entry=Entry(ifrm,font=('arial',18),bd=5,bg='#F2F7F2')
        fname_entry.place(relx=.1,rely=.19)
        fname_entry.focus()
#mob entry and label
        mob_label =Label(ifrm,font=('arial',18,'bold'),text='Mobile No.',bg='#F2F7F2',fg='#333333')
        mob_label.place(relx=.5,rely=.1)

        mob_entry=Entry(ifrm,font=('arial',18),bd=5,bg='#F2F7F2')
        mob_entry.place(relx=.5,rely=.19)

#email entry and label
        email_label =Label(ifrm,font=('arial',18,'bold'),text='E-Mail',bg='#F2F7F2',fg='#333333')
        email_label.place(relx=.1,rely=.3)

        email_entry=Entry(ifrm,font=('arial',18),bd=5,bg='#F2F7F2')
        email_entry.place(relx=.1,rely=.39)


#adhar entry and label
        adhar_label =Label(ifrm,font=('arial',18,'bold'),text='Adhar No.',bg='#F2F7F2',fg='#333333')
        adhar_label.place(relx=.5,rely=.30)

        adhar_entry=Entry(ifrm,font=('arial',18),bd=5,bg='#F2F7F2')
        adhar_entry.place(relx=.5,rely=.39)

#open acn button
        open_btn=Button(ifrm,command=open_acn,text='Open Account',font=('arial',20,'bold'),bg='#C8A2C8',bd=5)
        open_btn.place(relx=.15,rely=.60)

#reset button
        reset_btn=Button(ifrm,command=reset,text='Reset',font=('arial',20,'bold'),bg='#C8A2C8',bd=5)
        reset_btn.place(relx=.55,rely=.60)

# create view screen
#frame
    def view_click():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

# veiw user wlcome user text
        title_ifrm =Label(ifrm,font=('arial',20,'bold'),text='This is View User Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()

        # Create a Frame (Fix for NoneType error)
        frame = Frame(ifrm)
        frame.place(relx=.1,rely=.1,relwidth=.7)
#showing users
        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from users")

        for tup in cur_obj:
            data[f"{i}"]= {"Acno": tup[0], "Balance":tup[5], "Adhar": tup[6],"Opendate":tup[7],"Email":tup[4],"Mob":tup[3]}
            i+=1

        con_obj.close()
        # Create Table Model
        model = TableModel()
        model.importDict(data)  # Load data into the model

        # Create Table Canvas inside Frame (Important Fix)
        table = TableCanvas(frame, model=model, editable=True)
        table.show()

# create block screen
#frame
    def block_click():
        ifrm=Frame(frm,highlightbackground='brown',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

        # block user wlcome user text
        title_ifrm =Label(ifrm,font=('arial',20,'bold'),text='This is Block User Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()

#reset func
        def reset():
            acn_entry.delete(0,"end")
            acn_entry.focus()

        def block_db():
            uacn=acn_entry.get()
            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('delete from users where users_acno=?',(uacn))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo("Block",f'User with A/c no. Deleted')

        #acn no 
        acn_label =Label(ifrm,font=('arial',18,'bold'),text='Account No.',bg='#F2F7F2',fg='#333333')
        acn_label.place(relx=.2,rely=.2)

        acn_entry=Entry(ifrm,font=('arial',18),bd=5,bg='#F2F7F2')
        acn_entry.place(relx=.2,rely=.29)
        acn_entry.focus()

        #block button
        block_btn=Button(ifrm,command=block_db,text='Block',font=('arial',20,'bold'),bg='#C8A2C8',bd=5)
        block_btn.place(relx=.15,rely=.60)
        #reset button
        reset_btn=Button(ifrm,command=reset,text='Reset',font=('arial',20,'bold'),bg='#C8A2C8',bd=5)
        reset_btn.place(relx=.55,rely=.60)


#welcome label
    wel_label = Label(frm, font=("poppins", 25, "bold"), bg="#C2B97F",fg='#333333' ,text="Welcome! Admin ")
    wel_label.place(relx=.2, rely=.1)  
#welcome text for admin
    weltext_label = Label(frm, font=("poppins", 23, "bold"), bg="#C2B97F",fg='#333333', text="Please select any of the button to proceed further...")
    weltext_label.place(relx=.2, rely=.2) 

#create user
    create_btn=Button(frm,command=create_click,text='Create User',font=('arial',20,'bold'),bg='#8b9467',bd=5)
    create_btn.place(relx=0,rely=.16)
#view user
    view_btn=Button(frm,command=view_click,text='View User',font=('arial',20,'bold'),bg='#1abc9c',bd=5)
    view_btn.place(relx=0,rely=.38 )
#delete user
    block_btn=Button(frm,command=block_click,text='Block User',font=('arial',20,'bold'),bg='#acffac',bd=5)
    block_btn.place(relx=0,rely=.59)
 
#forgot password screen

def forgot_password_screen():
    frm=Frame(win,highlightbackground='black',highlightthickness=2,)
    frm.configure(bg='#C2B97F')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.68)
#reset function
    def reset():
        acn_entry.delete(0,"end")
        mob_entry.delete(0,"end")
        email_entry.delete(0,"end")

        #back function
    def back_click():
        frm.destroy()
        main_screen() 
#password recovery
    def get_password():
        uacn=acn_entry.get()
        umob=mob_entry.get()
        uemail=email_entry.get()
               
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_name,users_pass from users where users_acno=? and users_email=? and users_mob=?',(uacn,uemail,umob))
        tup=cur_obj.fetchone()
        con_obj.close()

        if tup==None:
            messagebox.showerror('forgot pass','Invalid Details')
        else:
            try:
                gmail_con=gmail.GMail('bhumikasharma1808@gmail.com','agym rfun zlaj zqlg')
                umsg=f'''Hello,{tup[0]}
                Welcome to City Bank of India
                Your Pass is: {tup[1]}
                
                Thanks
                '''
                msg=gmail.Message(to=uemail,subject='Password Recovery',text=umsg)
                gmail_con.send(msg)
                messagebox.showinfo('Forgot password','Kindly Check your Email for your new Password')
            except Exception as e:
                messagebox.showerror('Forgot password','Something Went Wrong')
                print(e)
 #back button
    back_btn=Button(frm,command=back_click,text='🔙',font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
    back_btn.place(relx=0,rely=0)
# different inputs by user        
    acn_label=Label(frm,font=("arial",16,"bold"),bg="#C2B97F",text="Account no.-")
    acn_label.place(relx=.2,rely=.1)
        
    acn_entry=Entry(frm,font=("arial",16,"bold"),bd=5)
    acn_entry.place(relx=.4,rely=.1)
    acn_entry.focus()

    email_label=Label(frm,font=("arial",16,"bold"),bg="#C2B97F",text="E-mail-")
    email_label.place(relx=.2,rely=.25)
        
    email_entry=Entry(frm,font=("arial",16,"bold"),bd=5)
    email_entry.place(relx=.4,rely=.25)

    mob_label=Label(frm,font=("arial",16,"bold"),bg="#C2B97F",text="Mobile no.-")
    mob_label.place(relx=.2,rely=.41)
        
    mob_entry=Entry(frm,font=("arial",16,"bold"),bd=5)
    mob_entry.place(relx=.4,rely=.41)

    submit_btn=Button(frm,text='Submit',command=get_password,font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
    submit_btn.place(relx=5,rely=6)

def welcome_user_screen():
    frm=Frame(win,highlightbackground='brown',highlightthickness=2)
    frm.configure(bg='#C2B97F')
    frm.place(relx=0,rely=.2,relwidth=1,relheight=.68)

#user profile photo

    if os.path.exists(f"{uacn}.png"):
        img=ImageTk.PhotoImage(Image.open(f'{uacn}.png').resize((120,120)),master=win)
    else:
        img=ImageTk.PhotoImage(Image.open('default.png').resize((120,120)),master=win)
    pic_label=Label(frm,image=img)
    pic_label.image=img
    pic_label.place(relx=.01,rely=.05)

    def update_photo():
        path=filedialog.askopenfilename()
        shutil.copy(path,f"{uacn}.png")

        img=ImageTk.PhotoImage(Image.open(path).resize((120,120)),master=win)
        pic_label=Label(frm,image=img)
        pic_label.image=img
        pic_label.place(relx=.01,rely=.05)

    btn_update_pic=Button(frm,text="update pic",command=update_photo)
    btn_update_pic.place(relx=.12,rely=.23)

#logout click command
    def logout_click():
        resp=messagebox.askyesno('logout','Do you want to logout,Kindly confirm?')
        if resp:
            frm.destroy()
            main_screen()
        

# create check screen
#frame
    def check_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

# check user wlcome user text
        title_ifrm =Label(ifrm,font=('arial',16,'bold'),text='This is Check Balance Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()

        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select users_bal,users_opendate,users_adhar from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()

        lbl_bal=Label(ifrm,text=f'Available Balance:\t\t{tup[0]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_bal.place(relx=.2,rely=.2)

        lbl_opendate=Label(ifrm,text=f'Account opendate:\t{tup[1]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_opendate.place(relx=.2,rely=.4)

        lbl_adhar=Label(ifrm,text=f'User Adhar:\t\t{tup[2]}',fg='blue',font=('arial',15,'bold'),bg='white')
        lbl_adhar.place(relx=.2,rely=.6)


# create withdraw screen
#frame
    def withdraw_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

# withdraw wlcome user text
        title_ifrm =Label(ifrm,font=('arial',16,'bold'),text='This is Withdraw Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()


        def withdraw_db():
            uamt=float(amt_entry.get())

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()

            if ubal>=uamt:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                con_obj.commit()
                con_obj.close()

                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                con_obj.commit()
                con_obj.close()

                messagebox.showinfo("withdraw",f"Amount {uamt} withdrawn and updated bal {ubal-uamt}")
            else:
                messagebox.showerror("withdraw",f"Insufficient Bal {ubal}")
#amt 
        amt_label =Label(ifrm,font=('arial',16,'bold'),text='Amount',bg='#F2F7F2',fg='#333333')
        amt_label.place(relx=.2,rely=.2)

        amt_entry=Entry(ifrm,font=('arial',18),bd=5,bg='#F2F7F2')
        amt_entry.place(relx=.2,rely=.29)
        amt_entry.focus()

#withdraw button
        withdraw_btn=Button(ifrm,text='Withdraw',command=withdraw_db,font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
        withdraw_btn.place(relx=.15,rely=.60)



# deposit screen
#frame
    def deposit_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

#Deposit wlcome user text
        title_ifrm =Label(ifrm,font=('arial',16,'bold'),text='This is Deposit Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()


        def deposit_db():
            uamt=float(amt_entry.get())

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal from users where users_acno=?',(uacn,))
            ubal=cur_obj.fetchone()[0]
            con_obj.close()


            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,uacn))
            con_obj.commit()
            con_obj.close()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
            con_obj.commit()
            con_obj.close()

            messagebox.showinfo("deposit",f"Amount {uamt} deposited and updated bal {ubal+uamt}")    
#amount
        amt_label =Label(ifrm,font=('arial',16,'bold'),text='Amount',bg='#F2F7F2',fg='#333333')
        amt_label.place(relx=.2,rely=.2)

        amt_entry=Entry(ifrm,font=('arial',16),bd=5,bg='#F2F7F2')
        amt_entry.place(relx=.2,rely=.29)
        amt_entry.focus()

#deposit button
        deposit_btn=Button(ifrm,command=deposit_db,text='Deposit',font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
        deposit_btn.place(relx=.15,rely=.60)


# update user screen
#frame
    def update_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

# update wlcome user text
        title_ifrm =Label(ifrm,font=('arial',16,'bold'),text='This is Update Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()
        
#update_details of user
        def update_details():
            uname=fname_entry.get()
            umob=mob_entry.get()
            uemail=email_entry.get()
            upass=pass_entry.get()

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('update users set users_name=?,users_pass=?,users_email=?,users_mob=? where users_acno=?',(uname,upass,uemail,umob,uacn))
            con_obj.commit()
            con_obj.close()
            messagebox.showinfo('update','Your details has been successfully updated')

#data extraction
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute('select * from users where users_acno=?',(uacn,))
        tup=cur_obj.fetchone()
        con_obj.close()

# name entry and label
        fname_label =Label(ifrm,font=('arial',16,'bold'),text='Full Name',bg='#F2F7F2',fg='#333333')
        fname_label.place(relx=.1,rely=.2)

        fname_entry=Entry(ifrm,font=('arial',16),bd=5,bg='#F2F7F2')
        fname_entry.place(relx=.1,rely=.29)
        fname_entry.insert(0,tup[2])
        fname_entry.focus()
#mob entry and label
        mob_label =Label(ifrm,font=('arial',16,'bold'),text='Mobile No.',bg='#F2F7F2',fg='#333333')
        mob_label.place(relx=.5,rely=.2)

        mob_entry=Entry(ifrm,font=('arial',16),bd=5,bg='#F2F7F2')
        mob_entry.place(relx=.5,rely=.29)
        mob_entry.insert(0,tup[3])

#email entry and label
        email_label =Label(ifrm,font=('arial',16,'bold'),text='E-Mail',bg='#F2F7F2',fg='#333333')
        email_label.place(relx=.1,rely=.4)

        email_entry=Entry(ifrm,font=('arial',16),bd=5,bg='#F2F7F2')
        email_entry.place(relx=.1,rely=.49)
        email_entry.insert(0,tup[4])

#pass entry and label
        pass_label =Label(ifrm,font=('arial',16,'bold'),text='Password',bg='#F2F7F2',fg='#333333')
        pass_label.place(relx=.5,rely=.4)

        pass_entry=Entry(ifrm,font=('arial',16),bd=5,bg='#F2F7F2')
        pass_entry.place(relx=.5,rely=.49)
        pass_entry.insert(0,tup[1])
#update button
        update_btn=Button(ifrm,text='Update',command=update_details,font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
        update_btn.place(relx=.15,rely=.70)


# transfer amount screen
#frame
    def transfer_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

# transfer amount user wlcome user text
        title_ifrm =Label(ifrm,font=('arial',16,'bold'),text='This is Transfer Amount Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()

        def transfer_db():
            uamt=float(amt_entry.get())
            toacn=int(to_entry.get())

            con_obj=sqlite3.connect(database='bank.sqlite')
            cur_obj=con_obj.cursor()
            cur_obj.execute('select users_bal,users_email from users where users_acno=?',(uacn,))
            tup=cur_obj.fetchone()
            ubal=tup[0]
            uemail=tup[1]
            con_obj.close()

            if ubal>=uamt:
                con_obj=sqlite3.connect(database='bank.sqlite')
                cur_obj=con_obj.cursor()
                cur_obj.execute("select * from users where users_acno=?",(toacn,))
                tup=cur_obj.fetchone()
                con_obj.close()

                if tup==None:
                    messagebox.showerror("transfer","To A/c does not exist")
                else:
                    otp=random.randint(1000,9999)
                    try:
                        gmail_con=gmail.GMail('bhumikasharma1808@gmail.com','agym rfun zlaj zqlg')
                        umsg=f'''Hello,{uname}
                        Welcome to City Bank of India
                        Your OTP is: {otp}
                        
                        Kindly verify this otp to complete your transaction

                        Thanks
                        '''
                        msg=gmail.Message(to=uemail,subject='Account Opened',text=umsg)
                        gmail_con.send(msg)
                        messagebox.showinfo('txn','we have send otp to your registered email')

                        uotp=simpledialog.askinteger("OTP","Enter OTP")
                        if otp==uotp:
                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('update users set users_bal=users_bal-? where users_acno=?',(uamt,uacn))
                            cur_obj.execute('update users set users_bal=users_bal+? where users_acno=?',(uamt,toacn))
                            
                            con_obj.commit()
                            con_obj.close()

                            tobal=tup[5]

                            con_obj=sqlite3.connect(database='bank.sqlite')
                            cur_obj=con_obj.cursor()
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(uacn,'Db(-)',time.strftime('%d-%b-%Y %r'),uamt,ubal-uamt))
                            cur_obj.execute('insert into txn(txn_acno,txn_type,txn_date,txn_amt,txn_updatebal) values(?,?,?,?,?)',(toacn,'Cr(+)',time.strftime('%d-%b-%Y %r'),uamt,ubal+uamt))
                            
                            con_obj.commit()
                            con_obj.close()

                            messagebox.showinfo("transfer",f"Amount {uamt} transfered and updated bal {ubal-uamt}")
                        else:
                            messagebox.showerror('otp','Invalid OTP')
                    except:
                        messagebox.showerror('txn','something went wrong')
            else:
                messagebox.showerror("transfer",f"Insufficient Bal {ubal}")
#to 
        to_label =Label(ifrm,font=('arial',16,'bold'),text='To',bg='#F2F7F2',fg='#333333')
        to_label.place(relx=.2,rely=.2)

        to_entry=Entry(ifrm,font=('arial',16),bd=5,bg='#F2F7F2')
        to_entry.place(relx=.5,rely=.2)
        to_entry.focus()
#amount
        amt_label =Label(ifrm,font=('arial',16,'bold'),text='Amount',bg='#F2F7F2',fg='#333333')
        amt_label.place(relx=.2,rely=.5)

        amt_entry=Entry(ifrm,font=('arial',16),bd=5,bg='#F2F7F2')
        amt_entry.place(relx=.5,rely=.5)

#transfer button
        transfer_btn=Button(ifrm,command=transfer_db,text='Transfer',font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
        transfer_btn.place(relx=.15,rely=.60)

# txn history screen
#frame
    def history_click():
        ifrm=Frame(frm,highlightbackground='black',highlightthickness=2)
        ifrm.configure(bg='#F2F7F2')
        ifrm.place(relx=.2,rely=.05,relwidth=.6,relheight=.9) 

# txn history user wlcome user text
        title_ifrm =Label(ifrm,font=('arial',16,'bold'),text='This is Transaction History Screen',bg='#F2F7F2',fg='#333333')
        title_ifrm.pack()


        # Create a Frame (Fix for NoneType error)
        frame = Frame(ifrm)
        frame.place(relx=.1,rely=.1,relwidth=.7)

        data={}
        i=1
        con_obj=sqlite3.connect(database='bank.sqlite')
        cur_obj=con_obj.cursor()
        cur_obj.execute("select * from txn where txn_acno=?",(uacn,))

        for tup in cur_obj:
            data[f"{i}"]= {"Txn Id": tup[0], "Txn Amt":tup[4], "Txn Date": tup[3],"Txn Type":tup[2],"Updated Bal":tup[5]}
            i+=1

        con_obj.close()
        # Create Table Model
        model = TableModel()
        model.importDict(data)  # Load data into the model

        # Create Table Canvas inside Frame (Important Fix)
        table = TableCanvas(frame, model=model, editable=True)
        table.show()
#logout button
    logout_btn=Button(frm,command=logout_click,text='Logout',font=('arial',16,'bold'),bg='#C8A2C8',bd=5)
    logout_btn.place(relx=.93,rely=0)

#welcome label
    wel_label = Label(frm, font=("arial", 20, "bold"), bg="#C2B97F", text=f"Welcome!{uname}")
    wel_label.place(relx=.2, rely=.13)
    wel_text_label = Label(frm, font=("arial", 20, "bold"), bg="#C2B97F", text=f"""Please select any of the options given 
                           to proceed to the next screen!""" )
    wel_text_label.place(relx=.2, rely=.13)

        
#button for users
#check button
    check_btn=Button(frm,command=check_click,text='Check Balance',font=('arial',20,'bold'),bg='#1abc9c',bd=5)
    check_btn.place(relx=0,rely=.35)
#withdraw button
    withdraw_btn=Button(frm,command=withdraw_click,text='Withdraw',font=('arial',20,'bold'),bg='#1abc9c',bd=5)
    withdraw_btn.place(relx=0,rely=.57 )
#deposit button
    deposit_btn=Button(frm,command=deposit_click,text='Deposit',font=('arial',20,'bold'),bg='#1abc9c',bd=5)
    deposit_btn.place(relx=0,rely=.78)
#update details user
    update_btn=Button(frm,command=update_click,text='Update Details',font=('arial',20,'bold'),bg='#1abc9c',bd=5)
    update_btn.place(relx=.83,rely=.57)
#transfer amount user
    transfer_btn=Button(frm,command=transfer_click,text='Transfer Amount',font=('arial',20,'bold'),bg='#1abc9c',bd=5)
    transfer_btn.place(relx=.81,rely=.78)
#history
    history_btn=Button(frm,command=history_click,text='Txn History',font=('arial',20,'bold'),bg='#1abc9c',bd=5)
    history_btn.place(relx=.87,rely=.35)

# slider()
main_screen()
win.mainloop()
