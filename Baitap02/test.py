import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk


class Database:
      def connect_db(self, db_name, user, password, host, port):
        try:
            self.conn = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
            self.connection_frame.grid_forget()  # Ẩn khung đăng nhập sau khi thành công
            self.background_label.place_forget()  # Ẩn hình nền
            self.create_main_screen()
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")