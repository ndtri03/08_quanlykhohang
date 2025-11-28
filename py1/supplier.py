from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class supplierClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # Variables
        self.var_searchtxt = StringVar()
        self.var_sup_invoice = StringVar()
        self.var_name = StringVar()
        self.var_contact = StringVar()
        self.old_invoice = None   

        # Title
        title = Label(self.root, text="Nhà cung cấp", font=("times new roman", 20, "bold"),
                      bg="#0f4d7d", fg="white")
        title.place(x=50, y=10, width=1000, height=40)

        # Search Section
        lbl_search = Label(self.root, text="Mã đơn hàng:", bg="white", font=("times new roman", 15))
        lbl_search.place(x=700, y=80)
        txt_search = Entry(self.root, textvariable=self.var_searchtxt, font=("times new roman", 15),
                           bg="lightyellow")
        txt_search.place(x=830, y=80, width=130, height=27)
        btn_search = Button(self.root, text="Tìm kiếm", command=self.search, font=("times new roman", 15),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_search.place(x=980, y=80, width=100, height=27)

        # Input Fields
        lbl_supplier_invoice = Label(self.root, text="Mã đơn hàng:", font=("times new roman", 15), bg="white")
        lbl_supplier_invoice.place(x=50, y=80)
        txt_supplier_invoice = Entry(self.root, textvariable=self.var_sup_invoice, font=("times new roman", 15),
                                      bg="lightyellow")
        txt_supplier_invoice.place(x=180, y=80, width=180)

        lbl_name = Label(self.root, text="Tên:", font=("times new roman", 15), bg="white")
        lbl_name.place(x=50, y=120)
        txt_name = Entry(self.root, textvariable=self.var_name, font=("times new roman", 15), bg="lightyellow")
        txt_name.place(x=180, y=120, width=180)

        lbl_contact = Label(self.root, text="Liên hệ:", font=("times new roman", 15), bg="white")
        lbl_contact.place(x=50, y=160)
        txt_contact = Entry(self.root, textvariable=self.var_contact, font=("times new roman", 15), bg="lightyellow")
        txt_contact.place(x=180, y=160, width=180)

        lbl_desc = Label(self.root, text="Mô tả:", font=("times new roman", 15), bg="white")
        lbl_desc.place(x=50, y=200)
        self.txt_desc = Text(self.root, font=("times new roman", 15), bg="lightyellow")
        self.txt_desc.place(x=180, y=200, width=500, height=90)

        # Buttons
        btn_add = Button(self.root, text="Thêm mới", command=self.add, font=("times new roman", 15),
                         bg="#2196f3", fg="white", cursor="hand2")
        btn_add.place(x=180, y=320, width=110, height=35)

        btn_update = Button(self.root, text="Cập nhật", command=self.update, font=("times new roman", 15),
                            bg="#4caf50", fg="white", cursor="hand2")
        btn_update.place(x=300, y=320, width=110, height=35)

        btn_delete = Button(self.root, text="Xóa", command=self.delete, font=("times new roman", 15),
                            bg="#f44336", fg="white", cursor="hand2")
        btn_delete.place(x=420, y=320, width=110, height=35)

        btn_clear = Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15),
                           bg="#607d8b", fg="white", cursor="hand2")
        btn_clear.place(x=540, y=320, width=110, height=35)

        # Table Frame
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=700, y=120, width=380, height=350)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)
        self.supplierTable = ttk.Treeview(emp_frame, columns=("invoice", "name", "contact", "desc"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.supplierTable.xview)
        scrolly.config(command=self.supplierTable.yview)

        self.supplierTable.heading("invoice", text="Mã đơn hàng")
        self.supplierTable.heading("name", text="Tên")
        self.supplierTable.heading("contact", text="Liên hệ")
        self.supplierTable.heading("desc", text="Mô tả")
        self.supplierTable["show"] = "headings"

        self.supplierTable.column("invoice", width=90)
        self.supplierTable.column("name", width=50)
        self.supplierTable.column("contact", width=100)
        self.supplierTable.column("desc", width=100)
        self.supplierTable.pack(fill=BOTH, expand=1)
        self.supplierTable.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # Add Supplier
    def add(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            invoice = self.var_sup_invoice.get().strip()

            if invoice == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập mã đơn hàng!", parent=self.root)
                return

            cur.execute("SELECT * FROM supplier WHERE invoice=?", (invoice,))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Lỗi", "Mã đơn hàng đã tồn tại!", parent=self.root)
                return

            cur.execute("INSERT INTO supplier (invoice, name, contact, desc) VALUES (?, ?, ?, ?)",
                        (invoice, self.var_name.get(), self.var_contact.get(),
                         self.txt_desc.get("1.0", END).strip()))
            con.commit()
            messagebox.showinfo("Thông báo", "Thêm mới thành công!", parent=self.root)
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi: {str(ex)}", parent=self.root)

    # Show Supplier
    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM supplier")
            rows = cur.fetchall()
            self.supplierTable.delete(*self.supplierTable.get_children())
            for row in rows:
                self.supplierTable.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi: {str(ex)}", parent=self.root)

    # Get Data
    def get_data(self, ev):
        f = self.supplierTable.focus()
        if not f:
            return
        content = self.supplierTable.item(f)
        row = content["values"]
        if not row:
            return

        self.var_sup_invoice.set(row[0])
        self.old_invoice = row[0]     

        self.var_name.set(row[1])
        self.var_contact.set(row[2])
        self.txt_desc.delete("1.0", END)
        self.txt_desc.insert(END, row[3])

    # Update
    def update(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()

        try:
            if self.var_sup_invoice.get().strip() == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập mã đơn hàng!", parent=self.root)
                return

            # kiểm tra xem mã gốc có tồn tại không
            cur.execute("SELECT * FROM supplier WHERE invoice=?", (self.old_invoice,))
            row = cur.fetchone()
            if not row:
                messagebox.showerror("Lỗi", "Mã đơn hàng đã tồn tại!", parent=self.root)
                return

            # Cập nhật, không check trùng mã
            cur.execute(
                "UPDATE supplier SET invoice=?, name=?, contact=?, desc=? WHERE invoice=?",
                (
                    self.var_sup_invoice.get().strip(),
                    self.var_name.get(),
                    self.var_contact.get(),
                    self.txt_desc.get('1.0', END).strip(),
                    self.old_invoice   # update theo mã cũ
                )
            )

            con.commit()
            messagebox.showinfo("Thông báo", "Cập nhật thành công!", parent=self.root)
            self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi: {str(ex)}", parent=self.root)


    # Delete Supplier
    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            invoice = self.var_sup_invoice.get().strip()

            if invoice == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập nhà cung cấp!", parent=self.root)
                return

            cur.execute("SELECT * FROM supplier WHERE invoice=?", (invoice,))
            row = cur.fetchone()
            if not row:
                messagebox.showerror("Lỗi", "Mã đơn hàng không tồn tại!", parent=self.root)
                return

            confirm = messagebox.askyesno("Thông báo", "Bạn có chắc muốn xóa?", parent=self.root)
            if confirm:
                cur.execute("DELETE FROM supplier WHERE invoice=?", (invoice,))
                con.commit()
                messagebox.showinfo("Thông báo", "Xóa thành công!", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi: {str(ex)}", parent=self.root)

    # Clear Fields
    def clear(self):
        self.var_sup_invoice.set("")
        self.var_name.set("")
        self.var_contact.set("")
        self.txt_desc.delete("1.0", END)
        self.var_searchtxt.set("")
        self.old_invoice = None 
        self.show()

    # Search Supplier
    def search(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            invoice = self.var_searchtxt.get().strip()

            if invoice == "":
                messagebox.showerror("Lỗi", "Vui lòng nhập mã đơn hàng!", parent=self.root)
                return

            cur.execute("SELECT * FROM supplier WHERE invoice=?", (invoice,))
            row = cur.fetchone()
            if row:
                self.supplierTable.delete(*self.supplierTable.get_children())
                self.supplierTable.insert("", END, values=row)
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy mã đơn hàng!", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = supplierClass(root)
    root.mainloop()
