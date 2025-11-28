from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class categoryClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System ")
        self.root.config(bg="white")
        self.root.focus_force()

        self.var_cat_id = StringVar()
        self.var_name = StringVar()

        lbl_title = Label(self.root, text="Quản lý danh mục sản phẩm",
                          font=("times new roman", 30),
                          bg="#184a45", fg="white",
                          bd=3, relief=RIDGE)
        lbl_title.pack(side=TOP, fill=X, padx=10, pady=20)

        lbl_name = Label(self.root, text="Thêm danh mục sản phẩm:",
                         font=("times new roman", 30),
                         bg="white")
        lbl_name.place(x=50, y=100)

        txt_name = Entry(self.root, textvariable=self.var_name,
                         font=("times new roman", 22),
                         bg="lightyellow")
        txt_name.place(x=50, y=170, width=300, height=30)

        btn_add = Button(self.root, text="Thêm", command=self.add,
                         font=("times new roman", 15),
                         bg="#4caf50", fg="white", cursor="hand2")
        btn_add.place(x=360, y=170, width=150, height=30)

        btn_delete = Button(self.root, text="Xóa", command=self.delete,
                            font=("times new roman", 15),
                            bg="#dc3545", fg="white", cursor="hand2")
        btn_delete.place(x=530, y=170, width=150, height=30)

        cat_frame = Frame(self.root, bd=3, relief=RIDGE)
        cat_frame.place(x=700, y=100, width=380, height=390)

        scrolly = Scrollbar(cat_frame, orient=VERTICAL)
        scrollx = Scrollbar(cat_frame, orient=HORIZONTAL)
        self.category_table = ttk.Treeview(cat_frame,
                                           columns=("cid", "name"),
                                           yscrollcommand=scrolly.set,
                                           xscrollcommand=scrollx.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)

        scrollx.config(command=self.category_table.xview)
        scrolly.config(command=self.category_table.yview)

        self.category_table.heading("cid", text="Category ID")
        self.category_table.heading("name", text="Tên")
        self.category_table["show"] = "headings"

        self.category_table.column("cid", width=90)
        self.category_table.column("name", width=100)
        self.category_table.pack(fill=BOTH, expand=1)
        self.category_table.bind("<ButtonRelease-1>", self.get_data)

        self.show()

    def add(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Lỗi", "Chưa nhập tên danh mục", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE name=?", (self.var_name.get(),))
                row = cur.fetchone()
                if row:
                    messagebox.showerror("Lỗi", "Danh mục đã có sẵn", parent=self.root)
                else:
                    cur.execute("INSERT INTO category (name) VALUES (?)", (self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Thông báo", "Thêm danh mục thành công", parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def show(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM category")
            rows = cur.fetchall()
            self.category_table.delete(*self.category_table.get_children())
            for row in rows:
                self.category_table.insert("", END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.category_table.focus()
        if not f:
            return
        content = self.category_table.item(f)
        row = content["values"]
        if not row:
            return
        self.var_cat_id.set(row[0])
        self.var_name.set(row[1])

    def delete(self):
        con = sqlite3.connect("ims.db")
        cur = con.cursor()
        try:
            if self.var_cat_id.get() == "":
                messagebox.showerror("Lỗi", "Chưa chọn danh mục để xóa", parent=self.root)
            else:
                cur.execute("SELECT * FROM category WHERE cid=?", (self.var_cat_id.get(),))
                row = cur.fetchone()

                if not row:
                    messagebox.showerror("Error", "Error, please try again", parent=self.root)
                else:
                    confirm = messagebox.askyesno("Thông báo", "Bạn chắc chắn muốn xóa?", parent=self.root)
                    if confirm:
                        cur.execute("DELETE FROM category WHERE cid=?", (self.var_cat_id.get(),))
                        con.commit()

                        # === RESET AUTO INCREMENT IF TABLE IS EMPTY ===
                        cur.execute("SELECT COUNT(*) FROM category")
                        count = cur.fetchone()[0]
                        if count == 0:
                            cur.execute("DELETE FROM sqlite_sequence WHERE name='category'")
                            con.commit()

                        messagebox.showinfo("Thông báo", "Xóa danh mục thành công", parent=self.root)
                        self.show()
                        self.var_cat_id.set("")
                        self.var_name.set("")
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = categoryClass(root)
    root.mainloop()
