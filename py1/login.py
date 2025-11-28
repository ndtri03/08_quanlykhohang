from tkinter import *
from PIL import Image, ImageTk, ImageFilter
from tkinter import messagebox
import sqlite3
import os

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng nhập")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#fafafa")
        bg = Image.open("images/anhnenlogin.jpg")
        bg = bg.resize((1350, 700))
        bg = bg.filter(ImageFilter.GaussianBlur(3))
        self.bg_image = ImageTk.PhotoImage(bg)

        bg_lbl = Label(self.root, image=self.bg_image)
        bg_lbl.place(x=0, y=0, relwidth=1, relheight=1)

        # Biến lưu dữ liệu đăng nhập
        self.employee_id = StringVar()
        self.password = StringVar()

        # ========== FRAME ĐĂNG NHẬP Ở GIỮA ==========
        login_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        login_frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=420)

        title = Label(login_frame, text="Đăng nhập", font=("Arial", 28, "bold"), bg="white", fg="#000000")
        title.pack(pady=20)

        # Employee ID
        lbl_user = Label(login_frame, text="Tên đăng nhập", font=("Arial", 14), bg="white", fg="#767171", anchor="w")
        lbl_user.pack(pady=5, padx=20, fill="x")

        txt_employee_id = Entry(login_frame, textvariable=self.employee_id, font=("Arial", 15), bg="#ECECEC")
        txt_employee_id.pack(pady=5, padx=20, fill="x", ipady=5)

        # Password
        lbl_pass = Label(login_frame, text="Mật khẩu", font=("Arial", 14), bg="white", fg="#767171", anchor="w")
        lbl_pass.pack(pady=5, padx=20, fill="x")

        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("Arial", 15), bg="#ECECEC")
        txt_pass.pack(pady=5, padx=20, fill="x", ipady=5)

        # Quên mật khẩu
        lbl_forget = Label(login_frame, text="Quên mật khẩu?", font=("Arial", 12),
                           bg="white", fg="#767171", anchor="e", cursor="hand2")
        lbl_forget.pack(pady=5, padx=20, fill="x")

        # Nút Login
        btn_login = Button(login_frame, command=self.login, text="Đăng nhập",
                           font=("Arial", 15), bg="#00B0F0", fg="white",
                           cursor="hand2", activebackground="#00B0F0")
        btn_login.pack(pady=15, padx=20, fill="x", ipady=5)

    # ================= Hàm đăng nhập ==================
    def login(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Lỗi', "Vui lòng nhập đầy đủ thông tin", parent=self.root)
            else:
                cur.execute("select utype from employee where eid=? and pass=?",
                            (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                if user is None:
                    messagebox.showerror('Lỗi', "Tài khoản hoặc mật khẩu không chính xác", parent=self.root)
                else:
                    if user[0] == "Admin":
                        self.root.destroy()
                        os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        os.system("python billing.py")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=self.root)

root = Tk()
obj = Login_System(root)
root.mainloop()
