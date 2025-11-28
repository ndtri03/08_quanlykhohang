from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3


class productClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_pid = StringVar()
        self.var_cat = StringVar()
        self.var_sup = StringVar()
        self.cat_list = []
        self.sup_list = []
        self.fetch_cat_sp()
        self.var_name = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_status = StringVar()

        # ========================= Đổi tiếng Việt cho search =========================
        self.search_map = {
            "Danh mục": "Category",
            "Nhà cung cấp": "Supplier",
            "Tên": "name"
        }

        # ============================ UI ==============================
        product_Frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        product_Frame.place(x=10, y=10, width=450, height=480)

        title = Label(product_Frame, text="Quản lý sản phẩm", font=("times new roman", 18), bg="#0f4d7d", fg="white").pack(side=TOP, fill=X)

        lbl_category = Label(product_Frame, text="Danh mục", font=("times new roman", 18), bg="white").place(x=30, y=60)
        lbl_supplier = Label(product_Frame, text="Nhà cung cấp", font=("times new roman", 18), bg="white").place(x=30, y=110)
        lbl_product_name = Label(product_Frame, text="Tên", font=("times new roman", 18), bg="white").place(x=30, y=160)
        lbl_price = Label(product_Frame, text="Giá", font=("times new roman", 18), bg="white").place(x=30, y=210)
        lbl_quantity = Label(product_Frame, text="Số lượng", font=("times new roman", 18), bg="white").place(x=30, y=260)
        lbl_status = Label(product_Frame, text="Trạng thái", font=("times new roman", 18), bg="white").place(x=30, y=310)

        cmb_cat = ttk.Combobox(product_Frame, textvariable=self.var_cat, values=self.cat_list, state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_cat.place(x=200, y=60, width=200)
        cmb_sup = ttk.Combobox(product_Frame, textvariable=self.var_sup, values=self.sup_list, state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_sup.place(x=200, y=110, width=200)

        Entry(product_Frame, textvariable=self.var_name, font=("times new roman", 15), bg='lightyellow').place(x=200, y=160, width=200)
        Entry(product_Frame, textvariable=self.var_price, font=("times new roman", 15), bg='lightyellow').place(x=200, y=210, width=200)
        Entry(product_Frame, textvariable=self.var_qty, font=("times new roman", 15), bg='lightyellow').place(x=200, y=260, width=200)

        cmb_status = ttk.Combobox(product_Frame, textvariable=self.var_status, values=("Active", "Inactive"), state='readonly', justify=CENTER, font=("times new roman", 15))
        cmb_status.place(x=200, y=310, width=200)

        Button(product_Frame, text="Thêm mới", command=self.add, font=("times new roman", 15), bg="#2196f3", fg="white").place(x=10, y=400, width=100, height=40)
        Button(product_Frame, text="Cập nhật", command=self.update, font=("times new roman", 15), bg="#4caf50", fg="white").place(x=120, y=400, width=100, height=40)
        Button(product_Frame, text="Xóa", command=self.delete, font=("times new roman", 15), bg="#f44336", fg="white").place(x=230, y=400, width=100, height=40)
        Button(product_Frame, text="Clear", command=self.clear, font=("times new roman", 15), bg="#9c27b0", fg="white").place(x=340, y=400, width=100, height=40)

        # ===================== Search frame ======================
        SearchFrame = LabelFrame(self.root, text="Tìm kiếm sản phẩm", font=("times new roman", 12, "bold"), bd=2, relief=RIDGE, bg="white")
        SearchFrame.place(x=480, y=10, width=600, height=80)

        cmb_search = ttk.Combobox(
            SearchFrame,
            textvariable=self.var_searchby,
            values=("Danh mục", "Nhà cung cấp", "Tên"),
            state='readonly',
            justify=CENTER,
            font=("times new roman", 15)
        )
        cmb_search.place(x=10, y=10, width=180, height=30)
        cmb_search.current(0)

        Entry(SearchFrame, textvariable=self.var_searchtxt, font=("times new roman", 15), bg="lightyellow").place(x=200, y=10, width=200, height=30)
        Button(SearchFrame, text="Tìm kiếm", command=self.search, font=("times new roman", 15), bg="#4caf50", fg="white").place(x=420, y=10, width=150, height=30)

        # ===================== Table frame ======================
        p_frame = Frame(self.root, bd=3, relief=RIDGE)
        p_frame.place(x=480, y=100, width=600, height=390)

        scrolly = Scrollbar(p_frame, orient=VERTICAL)
        scrollx = Scrollbar(p_frame, orient=HORIZONTAL)
        self.product_table = ttk.Treeview(p_frame, columns=("pid", "Supplier", "Category", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)

        self.product_table.heading("pid", text="Product ID")
        self.product_table.heading("Supplier", text="Nhà cung cấp")
        self.product_table.heading("Category", text="Danh mục")
        self.product_table.heading("name", text="Tên sản phẩm")
        self.product_table.heading("price", text="Giá")
        self.product_table.heading("qty", text="Số lượng")
        self.product_table.heading("status", text="Trạng thái")

        self.product_table["show"] = "headings"

        self.product_table.column("pid", width=10)
        self.product_table.column("Supplier", width=50)
        self.product_table.column("Category", width=50)
        self.product_table.column("name", width=70)
        self.product_table.column("price", width=60)
        self.product_table.column("qty", width=10)
        self.product_table.column("status", width=20)
        self.product_table.pack(fill=BOTH, expand=1)
        self.product_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    # =====================================================================
    def fetch_cat_sp(self):
        self.cat_list.append("Select")
        self.sup_list.append("Select")
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            cur.execute("select name from category")
            self.cat_list = [i[0] for i in cur.fetchall()]

            cur.execute("select name from supplier")
            self.sup_list = [i[0] for i in cur.fetchall()]
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # =====================================================================
    def add(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_cat.get() == "Select" or self.var_sup.get() == "Select" or self.var_name.get() == "":
                messagebox.showerror("Lỗi", "Chưa nhập đầy đủ thông tin", parent=self.root)
            else:
                cur.execute("Select * from product where name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Lỗi", "Sản phẩm đã tồn tại!", parent=self.root)
                else:
                    cur.execute("Insert into product(Category,Supplier,name,price,qty,status) values (?,?,?,?,?,?)",
                                (self.var_cat.get(), self.var_sup.get(), self.var_name.get(),
                                 self.var_price.get(), self.var_qty.get(), self.var_status.get()))
                    con.commit()
                    messagebox.showinfo("Thông báo", "Đã thêm sản phẩm", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # =====================================================================
    def show(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            cur.execute("select * from product")
            rows = cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # =====================================================================
    def get_data(self, ev):
        f = self.product_table.focus()
        if f == "":
            return

        content = self.product_table.item(f)
        row = content['values']

        if row == "":
            return

        self.var_pid.set(row[0])
        self.var_sup.set(row[1])
        self.var_cat.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    # =====================================================================
    def update(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Lỗi", "Chưa chọn sản phẩm", parent=self.root)
            else:
                cur.execute("select * from product where pid=?", (self.var_pid.get(),))
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Lỗi", "Sản phẩm không hợp lệ", parent=self.root)
                else:
                    cur.execute("update product set Category=?, Supplier=?, name=?, price=?, qty=?, status=? where pid=?",
                                (self.var_cat.get(), self.var_sup.get(), self.var_name.get(),
                                 self.var_price.get(), self.var_qty.get(), self.var_status.get(),
                                 self.var_pid.get()))
                    con.commit()
                    messagebox.showinfo("Thông báo", "Cập nhật sản phẩm thành công", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # =====================================================================
    def delete(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_pid.get() == "":
                messagebox.showerror("Lỗi", "Chưa chọn sản phẩm", parent=self.root)
            else:
                op = messagebox.askyesno("Xác nhận", "Bạn chắc chắn muốn xóa?", parent=self.root)
                if op:
                    cur.execute("delete from product where pid=?", (self.var_pid.get(),))
                    con.commit()

                    # RESET AUTO_INCREMENT NẾU BẢNG TRỐNG
                    cur.execute("SELECT COUNT(*) FROM product")
                    count = cur.fetchone()[0]

                    if count == 0:
                        cur.execute("DELETE FROM sqlite_sequence WHERE name='product'")
                        con.commit()

                    messagebox.showinfo("Thông báo", "Xóa sản phẩm thành công", parent=self.root)
                    self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    # =====================================================================
    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Danh mục")
        self.show()

    # =====================================================================
    def search(self):
        con = sqlite3.connect(database='ims.db')
        cur = con.cursor()
        try:
            if self.var_searchby.get() == "":
                messagebox.showerror("Lỗi", "Vui lòng chọn kiểu tìm kiếm", parent=self.root)
            elif self.var_searchtxt.get().strip() == "":
                messagebox.showerror("Lỗi", "Chưa nhập nội dung tìm kiếm", parent=self.root)
            else:
                column = self.search_map[self.var_searchby.get()]
                query = f"SELECT * FROM product WHERE {column} LIKE ?"
                search_text = f"%{self.var_searchtxt.get().strip()}%"

                cur.execute(query, (search_text,))
                rows = cur.fetchall()

                if rows:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('', END, values=row)
                else:
                    messagebox.showerror("Lỗi", "Không tìm thấy sản phẩm!", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)



if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()
