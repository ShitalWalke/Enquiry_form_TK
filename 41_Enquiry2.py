from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # pip install pillow
import pymysql

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Enquiry Window")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="white")

        self.bg = ImageTk.PhotoImage(file="bg.png")
        bg = Label(self.root, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)

        self.left = ImageTk.PhotoImage(file="side.png")
        left = Label(self.root, image=self.left).place(x=180, y=100, width=400, height=500)

        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=100, width=700, height=500)

        title = Label(frame1, text="ENQUIRY HERE ", font=("times new roman", 20, "bold"), bg="white", fg="green").place(x=50, y=30)

        # First Name
        f_name = Label(frame1, text="First Name: ", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        # Last Name
        l_name = Label(frame1, text="Last Name: ", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=365, y=100)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)

        # Contacts
        f_contacts = Label(frame1, text="Contact No: ", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=160)
        self.txt_contacts = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contacts.place(x=50, y=190, width=250)

        # Email
        l_email = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=365, y=160)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=190, width=250)

        # Security Question
        s_question = Label(frame1, text="Security Question: ", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=225)
        self.comb_question = ttk.Combobox(frame1, font=("times new roman", 12), state='readonly', justify=CENTER)
        self.comb_question['values'] = ("Select", "your first name", "Your Last Name", "Your Birth Date")
        self.comb_question.place(x=50, y=255, width=250)
        self.comb_question.current(0)

        # Answer
        s_answer = Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=365, y=225)
        self.txt_answer = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=370, y=255, width=250)

        # Password
        c_password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(
            x=50, y=300)
        self.txt_psw = Entry(frame1, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_psw.place(x=50, y=340, width=250)

        # Confirm Password
        con_password = Label(frame1, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white",
                             fg="gray").place(x=365, y=300)
        self.txt_cpsw = Entry(frame1, font=("times new roman", 15), bg="lightgray", show="*")
        self.txt_cpsw.place(x=370, y=340, width=250)

        # Terms and Conditions
        self.chk = IntVar()
        chk = Checkbutton(frame1, text="I agree to the terms and conditions", variable=self.chk, onvalue=1, offvalue=0, bg="White", font=("times new roman", 12)).place(x=50, y=380)

        # Submit Button
        self.btn_smb = Button(frame1, text="Submit", font=("times new roman", 15, "bold"), bg="green", fg="gray", command=self.register_data).place(x=50, y=420)

        # Sign In Button
        b_signin = Button(self.root, text="Sign In", font=("times new roman", 20), bd=0).place(x=250, y=490)

    def clear(self):
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contacts.delete(0, END)
        self.txt_email.delete(0, END)
        self.comb_question.current(0)  # Corrected line
        self.txt_answer.delete(0, END)
        self.txt_psw.delete(0, END)
        self.txt_cpsw.delete(0, END)

    def register_data(self):
        if (self.txt_fname.get() == "" or
                self.txt_contacts.get() == "" or
                self.txt_email.get() == "" or
                self.comb_question.get() == "Select" or
                self.txt_answer.get() == "" or
                self.txt_psw.get() == "" or
                self.txt_cpsw.get() == ""):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.txt_psw.get() != self.txt_cpsw.get():
            messagebox.showerror("Error", "Password & Confirm Password should be same", parent=self.root)
        elif self.chk.get() == 0:
            messagebox.showerror("Error", "Please agree to our Terms and Conditions", parent=self.root)
        else:
            try:
                con = pymysql.connect(
                    host="localhost",  # or IP address if remote
                    user="root",
                    password="",
                    database="employee"
                )
                cur = con.cursor()

                cur.execute("select * from employee where email=%s", self.txt_email.get())
                row = cur.fetchone()

                if row is not None:
                    messagebox.showerror("Error", "User already exists", parent=self.root)
                else:
                    cur.execute(
                        "insert into employee(f_name, l_name, contact, email, question, answer, password) values(%s, %s, %s, %s, %s, %s, %s)",
                        (self.txt_fname.get(),
                         self.txt_lname.get(),
                         self.txt_contacts.get(),
                         self.txt_email.get(),
                         self.comb_question.get(),
                         self.txt_answer.get(),
                         self.txt_psw.get())
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Registration Successful", parent=self.root)
                    self.clear()
                con.close()
            except Exception as es:
                messagebox.showerror("Error", f"Error due to: {str(es)}", parent=self.root)


root = Tk()
obj = Register(root)
root.mainloop()
