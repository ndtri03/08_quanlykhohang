from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import os

class salesClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list = []
        self.var_invoice = StringVar()

        # ================= Title =================
        lbl_title = Label(
            self.root,
            text="Hóa đơn",
            font=("times new roman", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=20)

        # ================= Invoice Input =================
        Label(self.root, text="Số hóa đơn", font=("times new roman", 15), bg="white").place(x=50, y=100)
        Entry(self.root, textvariable=self.var_invoice, font=("times new roman", 15), bg="lightyellow").place(x=160, y=100, width=180, height=28)

        Button(self.root, text="Tìm kiếm", command=self.search, font=("times new roman", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2").place(x=360, y=100, width=120, height=28)
        Button(self.root, text="Clear", command=self.clear, font=("times new roman", 15, "bold"), bg="lightgray", cursor="hand2").place(x=490, y=100, width=120, height=28)

        # ================= Sales List =================
        sales_Frame = Frame(self.root, bd=3, relief=RIDGE)
        sales_Frame.place(x=50, y=140, width=200, height=330)

        scrolly = Scrollbar(sales_Frame, orient=VERTICAL)
        self.Sale_List = Listbox(sales_Frame, font=("times new roman", 15), bg="white", yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT, fill=Y)
        scrolly.config(command=self.Sale_List.yview)
        self.Sale_List.pack(fill=BOTH, expand=1)
        self.Sale_List.bind("<ButtonRelease-1>", self.get_data)

        # ================= Bill Area =================
        bill_Frame = Frame(self.root, bd=3, relief=RIDGE)
        bill_Frame.place(x=280, y=140, width=410, height=330)

        Label(bill_Frame, text="Hóa đơn", font=("times new roman", 20), bg="orange").pack(side=TOP, fill=X)

        scrolly2 = Scrollbar(bill_Frame, orient=VERTICAL)
        self.bill_area = Text(bill_Frame, bg="lightyellow", yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT, fill=Y)
        scrolly2.config(command=self.bill_area.yview)
        self.bill_area.pack(fill=BOTH, expand=1)

        # Path thư mục hóa đơn
        self.bill_path = os.path.join(os.getcwd(), "bill")

        self.show()

    # ===================== Load list of bills =====================
    def show(self):
        self.bill_list.clear()
        self.Sale_List.delete(0, END)

        if not os.path.exists(self.bill_path):
            os.makedirs(self.bill_path)

        files = sorted(os.listdir(self.bill_path))
        for f in files:
            if f.endswith(".txt"):
                self.Sale_List.insert(END, f)
                self.bill_list.append(f[:-4])  # lưu tên không có .txt

    # ===================== Get selected bill =====================
    def get_data(self, ev):
        try:
            index = self.Sale_List.curselection()[0]
        except:
            return

        file_name = self.Sale_List.get(index)

        self.bill_area.delete("1.0", END)
        file_path = os.path.join(self.bill_path, file_name)

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as fp:
                self.bill_area.insert(END, fp.read())
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy file hóa đơn")

    # ===================== Search bill by invoice =====================
    def search(self):
        invoice_no = self.var_invoice.get().strip()
        if not invoice_no:
            messagebox.showerror("Lỗi", "Chưa nhập mã hóa đơn", parent=self.root)
            return

        file_name = invoice_no + ".txt"
        file_path = os.path.join(self.bill_path, file_name)

        if invoice_no in self.bill_list and os.path.exists(file_path):
            self.bill_area.delete("1.0", END)
            with open(file_path, "r", encoding="utf-8") as fp:
                self.bill_area.insert(END, fp.read())
        else:
            messagebox.showerror("Thông báo", "Không có hóa đơn", parent=self.root)

    # ===================== Clear search/input =====================
    def clear(self):
        self.var_invoice.set("")
        self.bill_area.delete("1.0", END)
        self.show()


if __name__ == "__main__":
    root = Tk()
    obj = salesClass(root)
    root.mainloop()
