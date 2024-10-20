import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QUẢN LÝ SINH VIÊN")

        # Database connection fields
        self.db_name = tk.StringVar(value='dbtest')
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
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            self.connection_frame.grid_forget()  # Ẩn khung đăng nhập sau khi thành công
            self.background_label.place_forget()  # Ẩn hình nền
            self.create_main_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def create_main_screen(self):
        font_title = font.Font(family='Trajan Pro', size=16,)
        font_text = font.Font(family='Eccentric Std', size=12)
        font_bold = font.Font(font=('Eccentric Std', 12, 'bold'))

        # Đặt màu nền là màu #384B70 cho giao diện chính
        self.root['background'] = '#384B70'

        lable_title = tk.Label(self.root, text="QUẢN LÝ SINH VIÊN", font=font_title, fg="white", bg='#384B70')
        lable_title.grid(row=0, column=0, columnspan=2, pady=(10,0))
        
        # Query section
        query_frame = tk.LabelFrame(self.root, text="Load Data", width=200, font=font_title, fg="white", bg='#384B70', bd=5)
        query_frame.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        tk.Label(query_frame, text="Nhập tên bảng:", font=font_text, bg='#384B70', fg='white').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name, font=font_text, bd=5).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(query_frame, text="Load Data", command=self.load_data, font=font_bold,bg="#D4BDAC", bd=2).grid(row=0, column=2 , columnspan=2, padx=5, pady=5)
        
        lable_titletable = tk.Label(self.root, text="BẢNG THÔNG TIN SINH VIÊN", font=font_title, fg="#FFBD73", bg='#384B70')
        lable_titletable.grid(row=2, column=0,padx=10, sticky='w')
        
        # Data display table
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#384B70", foreground="#9A7E6F", font=font_bold)

        self.tree = ttk.Treeview(self.root, columns=('STT', 'LỚP', 'HỌ VÀ TÊN'), show='headings', height=10)
                
        self.tree.column('STT', width=50, anchor='center') 
        self.tree.column('LỚP', width=140, anchor='center')
        self.tree.column('HỌ VÀ TÊN', width=230, anchor='w') 

        # Set heading name
        self.tree.heading('STT', text='STT')
        self.tree.heading('LỚP', text='LỚP')
        self.tree.heading('HỌ VÀ TÊN', text='HỌ VÀ TÊN')
    
        self.tree.grid(row=3, column=0, padx=5, pady=5, )

        # Insert section
        insert_frame = tk.LabelFrame(self.root, text="Insert Data", font=font_title, fg="white", bg='#384B70', labelanchor='n', bd=5)
        insert_frame.grid(row=4, column=0, columnspan=1, padx=10, pady=10)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(insert_frame, text="HỌ VÀ TÊN:", font=font_text, bg='#384B70', fg='white').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1, width=33, font=font_text, bd=5).grid(row=0, column=1,padx=5, pady=5)

        tk.Label(insert_frame, text="LỚP", font=font_text, bg='#384B70', fg='white').grid(row=1, column=0, padx=5, pady=5, sticky='w')
        tk.Entry(insert_frame, textvariable=self.column2, width=33, font=font_text, bd=5).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data, width=15, font=font_bold,bg="#D4BDAC", bd=5).grid(row=2, column=1, pady=10,padx=5, sticky='e')

        # Search section
        search_frame = tk.LabelFrame(self.root, text="Search Student", font=font_title, fg="white", bg='#384B70', bd=5)
        search_frame.grid(row=1, column=1, sticky='w', padx=(0,10))

        self.search_value = tk.StringVar()

        tk.Label(search_frame, text="Nhập lớp:", font=font_text, bg='#384B70', fg='white').grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(search_frame, textvariable=self.search_value, font=font_text, bd=5).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(search_frame, text="Search", command=self.search_data, font=font_bold,bg="#D4BDAC", bd=2).grid(row=0, column=2, padx=5, pady=5)
        
        # thêm ảnh vào root
        image = Image.open("imgs/dai-hoc-tot-o-vn-2.png")  # Đường dẫn đến ảnh của bạn
        # Thay đổi kích thước ảnh nếu cần
        image = image.resize((380, 420), Image.ANTIALIAS)  # Điều chỉnh kích thước (nếu cần)
        # Chuyển ảnh thành định dạng tkinter
        photo = ImageTk.PhotoImage(image)
        # Tạo Label và chèn ảnh vào
        label = tk.Label(root, image=photo)
        label.grid(row=3,column=1, rowspan=2, pady=10)
        # Giữ tham chiếu tới ảnh để tránh bị garbage collected
        label.image = photo
        
    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.tree.delete(*self.tree.get_children())  # Clear previous data
            for index, row in enumerate(rows, start=1):
                self.tree.insert('', 'end', values=(index, row[0], row[1]))  # Assumes columns are [name, mssv, major]
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (hoten, class) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def search_data(self):
        try:
            search_query = sql.SQL("SELECT * FROM {} WHERE class = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(search_query, (self.search_value.get(),))
            rows = self.cur.fetchall()

            # Clear previous data from Treeview
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Display search results
            if rows:
                for idx, row in enumerate(rows, start=1):
                    self.tree.insert("", "end", values=(idx, row[0], row[1]))  # Assuming the order of columns is (hoten, mssv)
            else:
                messagebox.showinfo("No Data", "No data found for the given MSSV.")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()