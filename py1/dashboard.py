from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
from tkinter import messagebox
import os
import time

class IMS:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System ")
        self.root.config(bg="white")

        # === title =====
        img = Image.open("images/logo1.png").resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(img)
        title = Label(self.root, text="Hệ thống quản lý kho hàng", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20)
        title.place(x=0, y=0, relwidth=1, height=70)

        # === btn_logout ===
        btn_logout = Button(self.root, text="Đăng xuất", command=self.logout,
                            font=("times new roman", 15, "bold"), bg="yellow", cursor="hand2")
        btn_logout.place(x=1150, y=10, height=50, width=150)

        # === clock =====
        self.lbl_clock = Label(self.root, text="\t\t Date: DD-MM-YYYY\t\t Time: HH:MM:SS",
                               font=("times new roman", 15), bg="#010c48", fg="white")
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        # ==== Left Menu ==
        self.MenuLogo = Image.open("images/logodb.jpg")
        self.MenuLogo = self.MenuLogo.resize((180, 180), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo)

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=220, height=550)

        lbl_menuLogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menuLogo.pack(side=TOP, fill=X)

        def close_program():
            root.destroy()

        img1 = Image.open("images/side.png").resize((33, 33), Image.Resampling.LANCZOS)
        self.icon_side = ImageTk.PhotoImage(img1)

        Label(LeftMenu, text="Menu", font=("times new roman", 20), bg="#009688").pack(side=TOP, fill=X)
        Button(LeftMenu, text="Nhân viên", command=self.employee, image=self.icon_side, compound=LEFT,
               padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        Button(LeftMenu, text="Nhà cung cấp", command=self.supplier, image=self.icon_side, compound=LEFT,
               padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        Button(LeftMenu, text="Danh mục", command=self.category, image=self.icon_side, compound=LEFT,
               padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        Button(LeftMenu, text="Sản phẩm", command=self.product, image=self.icon_side, compound=LEFT,
               padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        Button(LeftMenu, text="Đơn hàng", image=self.icon_side, command=self.sales, compound=LEFT,
               padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        Button(LeftMenu, text="Thoát", image=self.icon_side, command=close_program, compound=LEFT,
               padx=5, anchor="w", font=("times new roman", 20, "bold"), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)

        # === content =======
        self.lbl_employee = Label(self.root, text="Số nhân viên\n[ 0 ]", bd=5, relief=RIDGE, bg="#33bbf9",
                                  fg="white", font=("times new roman", 20, "bold"))
        self.lbl_employee.place(x=300, y=120, height=150, width=300)

        self.lbl_supplier = Label(self.root, text="Số nhà cung cấp\n[ 0 ]", bd=5, relief=RIDGE, bg="#ff5722",
                                  fg="white", font=("times new roman", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        self.lbl_category = Label(self.root, text="Số danh mục\n[ 0 ]", bd=5, relief=RIDGE, bg="#009688",
                                  fg="white", font=("times new roman", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        self.lbl_product = Label(self.root, text="Số sản phẩm\n[ 0 ]", bd=5, relief=RIDGE, bg="#607d8b",
                                 fg="white", font=("times new roman", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        self.lbl_sales = Label(self.root, text="Số đơn hàng\n[ 0 ]", bd=5, relief=RIDGE, bg="#ffc107",
                               fg="white", font=("times new roman", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)

        # === Thêm vùng hiển thị sản phẩm sắp hết hàng ===
        self.lbl_low_stock_frame = LabelFrame(self.root, text="Sản phẩm sắp hết hàng",
                                              font=("times new roman", 15, "bold"), bd=5, relief=RIDGE)
        self.lbl_low_stock_frame.place(x=1000, y=300, width=300, height=350)

        self.lbl_low_stock = Label(self.lbl_low_stock_frame, text="", justify=LEFT,
                                   font=("times new roman", 12), fg="red")
        self.lbl_low_stock.pack(fill=BOTH, expand=1)

        self.update_content()

#============================================================================
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)

    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
        # --- cập nhật số lượng các bảng ---
            cur.execute("SELECT * FROM product")
            product = cur.fetchall()
            self.lbl_product.config(text=f'Số sản phẩm\n[ {str(len(product))} ]')

            cur.execute("SELECT * FROM supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f'Số nhà cung cấp\n[ {str(len(supplier))} ]')

            cur.execute("SELECT * FROM category")
            category = cur.fetchall()
            self.lbl_category.config(text=f'Số danh mục\n[ {str(len(category))} ]')

            cur.execute("SELECT * FROM employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Số nhân viên\n[ {str(len(employee))} ]')

            bill = len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Số đơn hàng\n[ {str(bill)} ]')

        # --- cập nhật sản phẩm sắp hết hàng ---
            cur.execute("SELECT name, qty, status FROM product")
            products = cur.fetchall()

            low_stock = [f"{p[0]:<20} - Số lượng: {p[1]}" for p in products if int(p[1]) <= 30 and p[2]=='Active']

            if low_stock:
                display_text = "\n".join(low_stock)
            else:
                display_text = "Sản phẩm sắp hết hàng:\nKhông có"
            self.lbl_low_stock.config(text=display_text)

        # --- cập nhật thời gian ---
            time_ = time.strftime("%I:%M:%S")
            date_ = time.strftime("%d-%m-%Y")
            self.lbl_clock.config(text=f"\t\t\t\t\t\t\t\t\t\t\t  Ngày: {str(date_)}\t\t Giờ: {str(time_)}")
            self.lbl_clock.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to : {str(ex)}", parent=root)


    def logout(self):
        self.root.destroy()
        os.system("python login.py")


if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
