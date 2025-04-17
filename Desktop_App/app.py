import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk
from database import Database



class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QUẢN LÝ SINH VIÊN")

        # Database connection fields
        self.db_name = tk.StringVar(value='baitap2')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='123456')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='khoacntt')

        self.background_label = None  # Biến giữ nhãn nền

        # Create login(connect database)
        self.create_login_screen()

    def create_login_screen(self):
        font_title = font.Font(family='Trajan Pro', size=16,)
        font_text = font.Font(family='Eccentric Std', size=12)
        font_bold = font.Font(font=('Eccentric Std', 12, 'bold'))
        
        # Mở ảnh nền bằng Pillow
        image = Image.open("imgs/dai-hoc-tot-o-vn-2.png")  # Đường dẫn đến file ảnh
        image = image.resize((500, 500), Image.ANTIALIAS)  # Điều chỉnh kích thước ảnh
        bg_image = ImageTk.PhotoImage(image)

        # Tạo một Label để chứa ảnh nền
        self.background_label = tk.Label(self.root, image=bg_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Giữ tham chiếu đến ảnh nền để tránh bị garbage collected
        self.background_label.image = bg_image
                
        self.connection_frame = tk.LabelFrame(self.root, text="Login", font=font_title, bd=5, bg="#FEF9F2",  pady=10, padx=10, labelanchor='n')
        self.connection_frame.grid(row=0, column=0, padx=70, pady=(100,200))
        
        tk.Label(self.connection_frame, text="User:", font=font_text, bg="#FEF9F2", ).grid(row=0, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(self.connection_frame, textvariable=self.user, font=font_text, bd=5).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Password:", font=font_text , bg="#FEF9F2" , ).grid(row=1, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(self.connection_frame, textvariable=self.password, show="*",  font=font_text, bd=5).grid(row=1, column=1, padx=5, pady=5)
    
        tk.Button(self.connection_frame, text="Connect",font=font_bold, command=self.connect_db, bd=5, width=10, bg='#77CDFF').grid(row=2, column=1, columnspan=1, pady=10, sticky='e')

    def connect_db(self):
            self.database = Database(
                                db_name=self.db_name.get(),
                                user=self.user.get(),
                                password=self.password.get(),
                                host=self.host.get(),
                                port=self.port.get()
                                                    )

            if self.database.connect():  # Sử dụng phương thức connect từ lớp Database
                messagebox.showinfo("Success", "Kết nối vào database thành công!")
                self.connection_frame.grid_forget()
                self.background_label.place_forget()
                self.create_main_screen()
            else:
                messagebox.showerror("Error", "Kết nối vào database thất bại.")
        

    def create_main_screen(self):
        font_title = font.Font(family='Trajan Pro', size=16,)
        font_text = font.Font(family='Eccentric Std', size=12)
        font_bold = font.Font(font=('Eccentric Std', 12, 'bold'))

        # Đặt màu nền là màu #384B70 cho giao diện chính
        self.root['background'] = '#384B70'

        lable_title = tk.Label(self.root, text="QUẢN LÝ SINH VIÊN", font=font_title, fg="white", bg='#384B70')
        lable_title.grid(row=0, column=0, columnspan=2, pady=(10,0))
        
        # Query section
        query_frame = tk.LabelFrame(self.root, text="Truy cập dữ liệu", width=200, font=font_title, fg="white", bg='#384B70', bd=5)
        query_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        tk.Label(query_frame, text="Nhập tên bảng:", font=font_text, bg='#384B70', fg='white').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name, font=font_text, bd=5).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(query_frame, text="Load Data", command=self.load_data, font=font_bold,bg="#D4BDAC", bd=2).grid(row=0, column=2 , columnspan=2, padx=5, pady=5)
        
        lable_titletable = tk.Label(self.root, text="BẢNG THÔNG TIN SINH VIÊN", font=font_title, fg="#FFBD73", bg='#384B70')
        lable_titletable.grid(row=2, column=0,padx=10, sticky='w')
        
        # Data display table
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#384B70", foreground="#9A7E6F", font=font_bold)

        self.tree = ttk.Treeview(self.root, columns=('STT', 'HỌ VÀ TÊN', 'MSSV', 'LỚP'), show='headings', height=10)
                
        self.tree.column('STT', width=50, anchor='center') 
        self.tree.column('HỌ VÀ TÊN', width=180, anchor='w') 
        self.tree.column('MSSV', width=100, anchor='w') 
        self.tree.column('LỚP', width=100, anchor='center')
        

        # Set heading name
        self.tree.heading('STT', text='STT')
        self.tree.heading('HỌ VÀ TÊN', text='HỌ VÀ TÊN')
        self.tree.heading('MSSV', text='MSSV')
        self.tree.heading('LỚP', text='LỚP')
        
    
        self.tree.grid(row=3, column=0, padx=5, pady=5, )

        # Insert section
        insert_frame = tk.LabelFrame(self.root, text="Thêm Sinh Viên", font=font_title, fg="white", bg='#384B70', labelanchor='n', bd=5)
        insert_frame.grid(row=4, column=0, columnspan=1, padx=10, pady=10)

        self.column1 = tk.StringVar()  # Họ và tên
        self.column2 = tk.StringVar()  # MSSV
        self.column3 = tk.StringVar()  # Lớp

        tk.Label(insert_frame, text="HỌ VÀ TÊN:", font=font_text, bg='#384B70', fg='white').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1, width=33, font=font_text, bd=5).grid(row=0, column=1,padx=5, pady=5)
        
        tk.Label(insert_frame, text="MSSV:", font=font_text, bg='#384B70', fg='white').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(insert_frame, textvariable=self.column2, width=33, font=font_text, bd=5).grid(row=1, column=1, padx=5, pady=5)


        tk.Label(insert_frame, text="LỚP", font=font_text, bg='#384B70', fg='white').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(insert_frame, textvariable=self.column3, width=33, font=font_text, bd=5).grid(row=2, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data, width=15, font=font_bold,bg="#D4BDAC", bd=5).grid(row=3, column=1, pady=10,padx=5, sticky='e')

        # Search section
        search_frame = tk.LabelFrame(self.root, text="Lọc sinh viên", font=font_title, fg="white", bg='#384B70', bd=5)
        search_frame.grid(row=1, column=1, sticky='w', padx=(0,10))

        self.search_value = tk.StringVar()

        tk.Label(search_frame, text="Nhập lớp:", font=font_text, bg='#384B70', fg='white').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_value, font=font_text, bd=5).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(search_frame, text="Tìm Kiếm", command=self.search_data, font=font_bold,bg="#D4BDAC", bd=2).grid(row=0, column=2, padx=5, pady=5)
        
        # thêm ảnh vào root
        image = Image.open("imgs/dai-hoc-tot-o-vn-2.png")  # Đường dẫn đến ảnh của bạn
        # Thay đổi kích thước ảnh nếu cần
        image = image.resize((380, 420), Image.ANTIALIAS)  # Điều chỉnh kích thước (nếu cần)
        # Chuyển ảnh thành định dạng tkinter
        photo = ImageTk.PhotoImage(image)
        # Tạo Label và chèn ảnh vào
        label = tk.Label(root, image=photo)
        label.grid(row=3,column=1, rowspan=2, pady=10, sticky='n')
        # Giữ tham chiếu tới ảnh để tránh bị garbage collected
        label.image = photo
       
    
            
    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.database.cur.execute(query)
            rows = self.database.cur.fetchall()
            self.tree.delete(*self.tree.get_children())  # Clear previous data
            for index, row in enumerate(rows, start=1):
                self.tree.insert('', 'end', values=(index, row[1], row[2], row[3]))  # Assumes columns are [mssv, name, class]
        except Exception as e:
            messagebox.showerror("Error", f"Không tìm thấy dữ liệu: {e}")


            
    def insert_data(self):
        name = self.column1.get()
        mssv = self.column2.get()
        student_class = self.column3.get()

        if not name or not mssv or not student_class:
            messagebox.showerror("Error", "Không được bỏ trống ô nhập liệu!")
            return
        
        try:
            # Check if MSSV already exists
            check_query = sql.SQL("SELECT 1 FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name.get()))
            self.database.cur.execute(check_query, (mssv,))
            if self.database.cur.fetchone():
                messagebox.showerror("Error", "MSSV đã tồn tại!")
                return
            
            insert_query = sql.SQL("INSERT INTO {} (name, mssv, class) VALUES (%s, %s, %s)").format(sql.Identifier(self.table_name.get()))
            self.database.cur.execute(insert_query, (name, mssv, student_class))
            self.database.conn.commit()
            messagebox.showinfo("Success", "Thêm sinh viên mới thành công!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

   
    def search_data(self):
        try:
            search_query = sql.SQL("SELECT * FROM {} WHERE class = %s").format(sql.Identifier(self.table_name.get()))
            self.database.cur.execute(search_query, (self.search_value.get(),))
            rows = self.database.cur.fetchall()

            # Làm sạch Treeview trước khi hiển thị kết quả
            for item in self.tree.get_children():
                self.tree.delete(item) # Xóa tất cả các dữ liệu cũ

            # Hiển thị kết quả tìm kiếm
            if rows:
                for idx, row in enumerate(rows, start=1):
                    self.tree.insert("", "end", values=(idx, row[1], row[2], row[3]))  
            else:
                messagebox.showinfo("No Data", "Không tìm thấy lớp này!")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()
