from tkinter import *
from PIL import Image, ImageTk  # pip install pillow
from tkinter import ttk, messagebox
import sqlite3
import time
import os
import tempfile
class BillClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        # ====title====
        img = Image.open("images/logo1.png").resize((50, 50), Image.Resampling.LANCZOS)
        self.icon_title = ImageTk.PhotoImage(img)
        title = Label(self.root, text="Hệ thống quản lý kho hàng", image=self.icon_title, compound=LEFT,
                      font=("times new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0,y=0,relwidth=1,height=70)

        btn_logout = Button(self.root, text="Đăng xuất",command=self.logout, font=("times new roman", 15, "bold"), bg="yellow",
                            cursor="hand2").place(x=1150, y=25, height=30, width=150)

        self.lbl_clock = Label(self.root,
                               text="\t\t\t\t\t\t\t\t Ngày: DD-MM-YY\t\t Giờ: HH:MM:SS",
                               font=("times new roman", 15), bg="#4d636d", fg="white", anchor="w", padx=20)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        ProductFrame1 = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        ProductFrame1.place(x=6, y=110, width=410, height=550)

        pTitle = Label(ProductFrame1, text="Sản phẩm", font=("times new roman", 20, "bold"), bg="#262626",
                       fg="white").pack(side=TOP, fill=X)

        self.var_search = StringVar()
        ProductFrame2 = Frame(ProductFrame1, bd=2, relief=RIDGE, bg="white")
        ProductFrame2.place(x=2, y=42, width=398, height=90)

        lbl_search = Label(ProductFrame2, text="Tìm kiếm sản phẩm", font=("time new roman", 17, "bold"),
                           bg="white", fg="green").place(x=2, y=5)

        lbl_search = Label(ProductFrame2, text="Tên sản phẩm", font=("times new roman", 15, "bold"), bg="white").place(
            x=2, y=45)
        txt_search = Entry(ProductFrame2, textvariable=self.var_search, font=("times new roman", 15),
                           bg="lightyellow").place(x=128, y=47, width=150, height=22)
        btn_search = Button(ProductFrame2, text="Tìm kiếm",command=self.search, font=("times new roman", 15), bg="#2196f3", fg="white",
                            cursor="hand2").place(x=285, y=45, width=100, height=25)
        btn_show_all = Button(ProductFrame2, text="Show All",command=self.show, font=("times new roman", 15), bg="#083531", fg="white",
                              cursor="hand2").place(x=285, y=10, width=100, height=25)

        ProductFrame3 = Frame(ProductFrame1, bd=3, relief=RIDGE)
        ProductFrame3.place(x=2, y=140, width=398, height=375)

        scrolly = Scrollbar(ProductFrame3, orient=VERTICAL)
        scrollx = Scrollbar(ProductFrame3, orient=HORIZONTAL)

        self.product_Table = ttk.Treeview(ProductFrame3, columns=("pid", "name", "price", "qty", "status"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("pid", text="ID sản phẩm")
        self.product_Table.heading("name", text="Tên")
        self.product_Table.heading("price", text="Giá")
        self.product_Table.heading("qty", text="Số lượng")
        self.product_Table.heading("status", text="Trạng thái")
        self.product_Table["show"] = "headings"
        self.product_Table.column("pid", width=75)
        self.product_Table.column("name", width=70)
        self.product_Table.column("price", width=70)
        self.product_Table.column("qty", width=45)
        self.product_Table.column("status", width=65)
        self.product_Table.pack(fill=BOTH, expand=1)
        self.product_Table.bind("<ButtonRelease-1>", self.get_data)

        lbl_note = Label(ProductFrame1, text="Lưu ý: Nhập số lượng 0 để xóa sản phẩm khỏi Giỏ hàng'",
                         font=("times new roman", 12), anchor='w', bg="white", fg="red").pack(side=BOTTOM, fill=X)

        self.var_cname = StringVar()
        self.var_contact = StringVar()
        CustomerFrame = Frame(self.root, bd=4, relief=RIDGE, bg="white")
        CustomerFrame.place(x=420, y=110, width=530, height=70)

        cTitle = Label(CustomerFrame, text="Thông tin Khách hàng", font=("times new roman", 15), bg="lightgray").pack(
            side=TOP, fill=X)
        lbl_name = Label(CustomerFrame, text="Tên:", font=("time new roman", 15), bg="white").place(x=5, y=35)
        txt_name = Entry(CustomerFrame, textvariable=self.var_cname, font=("time new roman", 13),
                         bg="lightyellow").place(x=80, y=35, width=180, height=25)

        lbl_contact = Label(CustomerFrame, text="Số ĐT:", font=("time new roman", 15), bg="white").place(x=270,
                                                                                                              y=35)
        txt_contact = Entry(CustomerFrame, textvariable=self.var_contact, font=("time new roman", 13),
                            bg="lightyellow").place(x=370, y=35, width=140, height=25)

        Cal_Cart_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Cal_Cart_Frame.place(x=420, y=190, width=530, height=360)

        cart_Frame = Frame(Cal_Cart_Frame, bd=3, relief=RIDGE)
        cart_Frame.place(x=5, y=10, width=510, height=342)
        self.cartTitle = Label(cart_Frame, text="Giỏ hàng \t\t Tổng số sản phẩm: [0]", font=("times new roman", 15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill =X)

        scrolly = Scrollbar(cart_Frame, orient=VERTICAL)
        scrollx = Scrollbar(cart_Frame, orient=HORIZONTAL)

        self.CartTable = ttk.Treeview(cart_Frame, columns=("pid", "name", "price", "qty", ),
                                      yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("pid", text="ID sản phẩm")
        self.CartTable.heading("name", text="Tên")
        self.CartTable.heading("price", text="Giá")
        self.CartTable.heading("qty", text="Số lượng")
        
        self.CartTable["show"] = "headings"
        self.CartTable.column("pid", width=40)
        self.CartTable.column("name", width=90)
        self.CartTable.column("price", width=90)
        self.CartTable.column("qty", width=40)
      
        self.CartTable.pack(fill=BOTH, expand=1)
        self.CartTable.bind("<ButtonRelease-1>", self.get_data_cart)

        self.var_pid = StringVar()
        self.var_pname = StringVar()
        self.var_price = StringVar()
        self.var_qty = StringVar()
        self.var_stock = StringVar()

        Add_CartWidgetsFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        Add_CartWidgetsFrame.place(x=420, y=550, width=530, height=110)

        lbl_p_name = Label(Add_CartWidgetsFrame, text="Tên sản phẩm", font=("times new roman", 15), bg="white").place(
            x=5, y=5)
        txt_p_name = Entry(Add_CartWidgetsFrame, textvariable=self.var_pname, font=("times new roman", 15),
                           bg="lightyellow", state='readonly').place(x=5, y=35, width=150, height=22)

        lbl_p_price = Label(Add_CartWidgetsFrame, text="Giá/1 sản phẩm", font=("times new roman", 15), bg="white").place(
            x=210, y=5)
        txt_p_price = Entry(Add_CartWidgetsFrame, textvariable=self.var_price, font=("times new roman", 15),
                            bg="lightyellow", state='readonly').place(x=210, y=35, width=130, height=22)

        lbl_p_qty = Label(Add_CartWidgetsFrame, text="Số lượng", font=("times new roman", 15), bg="white").place(x=390,
                                                                                                                 y=5)
        txt_p_qty = Entry(Add_CartWidgetsFrame, textvariable=self.var_qty, font=("times new roman", 15),
                          bg="lightyellow").place(x=390, y=35, width=120, height=22)

        self.lbl_inStock = Label(Add_CartWidgetsFrame, text="Có sẵn trong kho: ", font=("times new roman", 15),
                                 bg="white")
        self.lbl_inStock.place(x=5, y=70)

        btn_add_cart = Button(Add_CartWidgetsFrame, text="Thêm | Cập nhật đơn hàng",command=self.add_update_cart, font=("times new roman", 15, "bold"),
                              bg="orange", cursor="hand2").place(x=290, y=70, width=220, height=30)

        billFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billFrame.place(x=940, y=110, width=410, height=410)

        BTitle = Label(billFrame, text="Hóa đơn", font=("times new roman", 20, "bold"), bg="#262626",
                       fg="white").pack(side=TOP, fill=X)
        scrolly = Scrollbar(billFrame, orient=VERTICAL)
        scrolly.pack(side=RIGHT, fill=Y)

        self.txt_bill_area = Text(billFrame, yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH, expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

        billMenuFrame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        billMenuFrame.place(x=940, y=520, width=410, height=140)

        self.lbl_amnt = Label(billMenuFrame, text='Tổng cộng(VNĐ)\n[0]', font=("times new roman", 12, "bold"),
                              bg="#3f51b5", fg="white")
        self.lbl_amnt.place(x=2, y=5, width=130, height=70)

        self.lbl_discount = Label(billMenuFrame, text='Giảm giá \n[5%]', font=("times new roman", 12, "bold"),
                                  bg="#8bc34a", fg="white")
        self.lbl_discount.place(x=135, y=5, width=85, height=70)

        self.lbl_net_pay = Label(billMenuFrame, text='Tổng tiền thanh toán(VNĐ)\n[0]', font=("times new roman", 12, "bold"), bg="#067d8b",
                                 fg="white")
        self.lbl_net_pay.place(x=223, y=5, width=182, height=70)

        btn_print = Button(billMenuFrame, text='In hóa đơn',command=self.print_bill, cursor="hand2", font=("times new roman", 12, "bold"),
                           bg="darkgreen", fg="white")
        btn_print.place(x=2, y=80, width=130, height=50)

        btn_clear_all = Button(billMenuFrame, text='Clear All',command=self.clear_all, cursor="hand2", font=("times new roman", 12, "bold"),
                               bg="#D32F2F", fg="white")
        btn_clear_all.place(x=135, y=80, width=85, height=50)

        btn_generate = Button(billMenuFrame, text='Tạo/Lưu hóa đơn',command=self.generate_bill, cursor="hand2",
                              font=("times new roman", 12, "bold"), bg="#F57C00", fg="white")
        btn_generate.place(x=223, y=80, width=182, height=50)

        self.show()
        self.update_date_time()
       
    # ==============================ALL Functions=======================

    def get_input(self, num):
        xnum = self.var_cal_input.get() + str(num)
        self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')

    def perform_cal(self):
        result = self.var_cal_input.get()
        self.var_cal_input.set(eval(result))

    def show(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("select pid, name, price, qty, status from product where status = 'Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def search(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Lỗi", "Không có tên sản phẩm để tìm", parent=self.root)
            else:
                cur.execute("select pid, name, price, qty, status from product where name LIKE '%"+self.var_search.get()+"%' and status = 'Active'")
                rows= cur.fetchall()
                if len(rows) !=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('', END, values=row)
                else:
                    messagebox.showerror("Thông báo", "Không có sản phẩm", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def get_data(self, ev):
        f = self.product_Table.focus()
        if f == "":
            return
        content = self.product_Table.item(f)
        row = content.get("values", [])
        if row == "" or len(row) < 4:
            return
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.lbl_inStock.config(text=f"Có sẵn trong kho: [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_qty.set('1')

    def get_data_cart(self, ev):
        f = self.CartTable.focus()
        if f == "":
            return
        content = self.CartTable.item(f)
        row = content.get("values", [])
        if row == "" or len(row) < 4:
            return
        self.var_pid.set(row[0])
        self.var_pname.set(row[1])
        self.var_price.set(row[2])
        self.var_qty.set(row[3])

        if len(row) >= 5:
            self.lbl_inStock.config(text=f"Có sẵn trong kho: [{str(row[4])}]")
            self.var_stock.set(row[4])
        else:
            self.lbl_inStock.config(text="Có sẵn trong kho: [ ]")
            self.var_stock.set("")

    
    def add_update_cart(self):
        if self.var_pid.get() == '':
            messagebox.showerror('Lỗi', "Chưa chọn sản phẩm", parent=self.root)
            return
        if self.var_qty.get() == '':
            messagebox.showerror('Lỗi', "Chưa nhập số lượng", parent=self.root)
            return
        if int(self.var_qty.get()) > int(self.var_stock.get()):
            messagebox.showerror('Lỗi', "Số lượng không hợp lệ", parent=self.root)
            return

        price_cal = self.var_price.get()
        cart_data = [self.var_pid.get(), self.var_pname.get(), price_cal, self.var_qty.get(), self.var_stock.get()]

        index_ = None
        for i, row in enumerate(self.cart_list):
            if self.var_pid.get() == row[0]:
                index_ = i
                break

        if index_ is not None:  
            op = messagebox.askyesno('Xác nhận',
                                    "Sản phẩm đã có sẵn.\nXác nhận cập nhật hoặc xóa sản phẩm?",
                                    parent=self.root)
            if op:
                if self.var_qty.get() == "0":  # xoá
                    self.cart_list.pop(index_)
                else: 
                    self.cart_list[index_][2] = price_cal
                    self.cart_list[index_][3] = self.var_qty.get()
        else:
            self.cart_list.append(cart_data)

        self.show_cart()
        self.bill_update()


    def bill_update(self):
        self.bill_amnt = 0
        self.net_pay = 0
        self.discount = 0
        for row in self.cart_list:
            self.bill_amnt = self.bill_amnt + (float(row[2])*int(row[3]))
        self.discount = (self.bill_amnt*5)/100
        self.net_pay = self.bill_amnt - (self.bill_amnt*5)/100
        self.lbl_amnt.config(text = f'Tổng cộng(VNĐ)\n[{str(self.bill_amnt)}]')
        self.lbl_net_pay.config(text = f'Tổng tiền thanh toán(VNĐ)\n[{str(self.net_pay)}]')
        self.cartTitle.config(text = f"Giỏ hàng \t\t Tổng số sản phẩm: [{str(len(self.cart_list))}]")
    
    def show_cart(self):
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def generate_bill(self):
        if self.var_cname.get() == '' or self.var_contact.get() == '':
            messagebox.showerror('Lỗi',f"Chưa nhập thông tin khách hàng",parent = self.root)
        elif len(self.cart_list) == 0:
            messagebox.showerror('Lỗi',f"Không có sản phẩm trong giỏ hàng", parent = self.root)
        else:
            if not os.path.exists('bill'):
                os.makedirs('bill')

            self.bill_top()
            self.bill_middle()
            self.bill_bottom()
        
            try:
                file_path = f'bill/{str(self.invoice)}.txt'
            
                with open(file_path, 'w', encoding='utf-8') as fp:
                    fp.write(self.txt_bill_area.get('1.0', END))
            
                messagebox.showinfo('Đã lưu',"Hóa đơn đã được tạo và lưu")
                self.chk_print = 1
            
            except Exception as ex:
                messagebox.showerror('Lỗi', f"Lỗi trong quá trình lưu file: {str(ex)}", parent=self.root)

    def bill_top(self):
        WIDTH = 47 
        
        self.invoice = int(time.strftime("%H%M%S")) + int(time.strftime("%d%m%Y"))
        
        bill_top_temp = f'''
{str("Hóa đơn bán hàng").center(WIDTH)}
{str("Đại học Công nghiệp Hà Nội").center(WIDTH)}
{str("Nguyên Xá, Cầu Diễn, P.Minh Khai, Q.Bắc Từ Liêm").center(WIDTH)}
{str("="*WIDTH)}
Khách hàng: {self.var_cname.get()}
Số điện thoại: {self.var_contact.get()}
Hóa đơn số: {str(self.invoice).ljust(15)} Ngày: {str(time.strftime("%d/%m/%Y")).rjust(10)}
{str("="*WIDTH)}
{"Tên hàng".ljust(25)}{"SL".center(8)}{"Giá".rjust(14)}
{str("="* WIDTH)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_middle(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        COL_NAME_WIDTH = 25
        COL_QTY_WIDTH = 8
        COL_PRICE_WIDTH = 14
    
        try:
            for row in self.cart_list:
                
                pid = row[0]
                name = row[1]
                qty_remaining = int(row[4]) - int(row[3])
                status = 'Inactive' if qty_remaining <= 0 else 'Active'

                price_total = float(row[2])*int(row[3])
                price_str = str(price_total) + "VNĐ"
                
                product_line = f"{name.ljust(COL_NAME_WIDTH)}{row[3].center(COL_QTY_WIDTH)}{price_str.rjust(COL_PRICE_WIDTH)}"
                
                self.txt_bill_area.insert(END, "\n" + product_line)
                
                cur.execute('Update product set qty=?, status=? where pid=?',(
                    qty_remaining,
                    status,
                    pid
                ))
                con.commit()
                
            con.close()
            self.show() 
            
        except Exception as ex:
            messagebox.showerror("Error", f"Lỗi do: {str(ex)}", parent=self.root)

    def bill_bottom(self):
        WIDTH = 47
        COL_LABEL_WIDTH = 30
        COL_VALUE_WIDTH = 17 
        
        total_amnt_str = (str(self.bill_amnt) + "VNĐ").rjust(COL_VALUE_WIDTH)
        discount_str = (str(self.discount) + "VNĐ").rjust(COL_VALUE_WIDTH)
        net_pay_str = (str(self.net_pay) + "VNĐ").rjust(COL_VALUE_WIDTH)
        
        bill_bottom_temp = f'''
{str("="*WIDTH)}
{"Tổng cộng".ljust(COL_LABEL_WIDTH)}{total_amnt_str}
{"Giảm giá".ljust(COL_LABEL_WIDTH)}{discount_str}
{"Tổng tiền thanh toán".ljust(COL_LABEL_WIDTH)}{net_pay_str}
{str("="*WIDTH)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)

    def clear_cart(self):
        self.var_pid.set('')
        self.var_pname.set('')
        self.var_price.set('')
        self.var_qty.set('')
        self.lbl_inStock.config(text=f"Có sẵn trong kho: ")
        self.var_stock.set('')

    def clear_all(self):
        del self.cart_list[:]
        self.var_cname.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text = f"Giỏ hàng \t\t Tổng số sản phẩm: [0]")
        self.var_search.set('')
        self.clear_cart()
        self.show()
        self.show_cart()
        self.chk_print=0
        self.lbl_amnt.config(text = f'Tổng cộng(VNĐ)\n[0]')
        self.lbl_net_pay.config(text = f'Tổng tiền thanh toán(VNĐ)\n[0]')

    def update_date_time(self):
        time_ = time.strftime("%I:%M:%S")
        date_ = time.strftime("%d-%m-%Y")
        self.lbl_clock.config(text=f"\t\t\t\t\t\t Ngày: {str(date_)}\t\t Giờ: {str(time_)}")
        self.lbl_clock.after(200,self.update_date_time)

    def print_bill(self):
        if self.chk_print == 1:
            messagebox.showinfo('Print', 'Vui lòng chờ khi in', parent=self.root)
            new_file = tempfile.mktemp('.txt')
        
            with open(new_file, 'w', encoding='utf-8') as f:
                f.write(self.txt_bill_area.get('1.0', END))
        
            os.startfile(new_file, 'print')
        else:
            messagebox.showerror('Print', 'Không có hóa đơn để in', parent=self.root)


    def logout(self):
        self.root.destroy()
        os.system("python login.py")

if __name__ == '__main__':
    root = Tk()
    obj = BillClass(root)
    root.mainloop()
