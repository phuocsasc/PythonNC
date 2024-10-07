import tkinter as tk
import os
from tkinter import messagebox
from tkinter import font
from tkinter import ttk

# global attribute
bg_Color = '#384B70'
color_btn_cong = '#624E88'
color_btn_tru = '#8967B3'
color_btn_nhan = '#CB80AB'
color_btn_chia = '#E6D9A2'
color_btn_reset = '#A04747'
color_text = 'white'
color_text_kq = 'red'

win = tk.Tk()
win.title('Calculations Basic')
win.geometry('500x300+400+100')
win.attributes('-topmost', True)
win.config(bg = bg_Color)
PATH_DIRECTORY = os.path.dirname(__file__) # vào thẳng folder dự án đang làm việc
PATH_IMAGES = os.path.join(PATH_DIRECTORY, 'imgs') # từ folder dự án join vào folder ảnh 'imgs'
win.iconbitmap(os.path.join(PATH_IMAGES, 'icon_cal.ico'))

font_title = font.Font(family='Trajan Pro', size=16,)
font_text = font.Font(family='Eccentric Std', size=12)
font_bold = font.Font(font=('Eccentric Std', 12, 'bold'))

# create LabelFrame 1 nhập số
label_Frame1 = tk.LabelFrame(win, text='Nhập số', font=font_title, bg=bg_Color, fg=color_text, bd=5, padx=15, pady=10)
label_Frame1.grid(row=0, column=0,padx=(10,5), pady=(10,5) )
labelA = tk.Label(label_Frame1, text='Nhập số A', font=font_text, bg=bg_Color, fg=color_text)
labelA.grid(row=0,column=0, padx=(0,10))
entryA = tk.Entry(label_Frame1, font=font_bold, width=10, bd=5 )
entryA.grid (row=0, column=1)
entryA.focus()
labelB = tk.Label(label_Frame1, text='Nhập số B', font=font_text, bg=bg_Color, fg=color_text)
labelB.grid(row=1, column=0, padx=(0,10))
entryB = tk.Entry(label_Frame1, font=font_bold, width=10, bd=5 )
entryB.grid (row=1, column=1, pady=(10,6))

# create LabelFrame 2 tính toán
label_Frame2 = tk.LabelFrame(win, text='Tính toán', font=font_title, bg=bg_Color, fg=color_text, bd=5, padx=15, pady=10)
label_Frame2.grid(row=0, column=1)
btn_cong = tk.Button(label_Frame2, text='+', font=font_text, bd=5, width=3, bg=color_btn_cong, command=lambda:cong())
btn_cong.grid(row=0,column=0)
btn_tru = tk.Button(label_Frame2, text='-', font=font_text, bd=5, width=3, bg=color_btn_tru, command=lambda:tru())
btn_tru.grid(row=0, column=1, padx=5)
btn_nhan = tk.Button(label_Frame2, text='x', font=font_text, bd=5, width=3, bg=color_btn_nhan, command=lambda:nhan())
btn_nhan.grid(row=0, column=2, padx=(0,5))
btn_chia = tk.Button(label_Frame2, text='/', font=font_text, bd=5, width=3, bg=color_btn_chia, command=lambda:chia())
btn_chia.grid(row=0, column=3)
btn_reset = tk.Button(label_Frame2, text='Reset', font=font_text, bd=5, width=19, bg=color_btn_reset, command=lambda:reset())
btn_reset.grid(row=1, column=0, columnspan=4, pady=(5,2))

# create LabelFrame 3 kết quả
label_Frame3 = tk.LabelFrame(win, text='Bảng kết quả', font=font_title, bg=bg_Color, fg=color_text, bd=5, padx=15, pady=10)
label_Frame3.grid(row=1, column=0, padx=10 ,sticky=tk.W, columnspan=2)
label_kq = tk.Label(label_Frame3, text='=', font=font_bold, bg=bg_Color, fg=color_text )
label_kq.grid(row=0, column=0)

# create function cong
def cong():
      try:
           kq = float(entryA.get()) + float(entryB.get())
           label_kq.config(text= entryA.get() + ' + ' + entryB.get() + ' = ' + str(kq), fg=color_text_kq)
           label_Frame3.config(fg=color_text_kq)
      except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            entryA.delete(0, tk.END)
            entryB.delete(0, tk.END)
            
# create function tru
def tru():
      try:
            kq = float(entryA.get()) - float(entryB.get())
            label_kq.config(text=entryA.get() + ' - ' + entryB.get() + ' = ' + str(kq), fg=color_text_kq)
            label_Frame3.config(fg=color_text_kq)
      except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            entryA.delete(0, tk.END)
            entryB.delete(0, tk.END)
            
# create function nhan
def nhan():
      try:
            kq = float(entryA.get()) * float(entryB.get())
            label_kq.config(text=entryA.get() + ' x ' + entryB.get() + ' = ' + str(kq), fg=color_text_kq)
            label_Frame3.config(fg=color_text_kq)
      except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            entryA.delete(0, tk.END)
            entryB.delete(0, tk.END)
            
# create function chia
def chia():
      try:
            b = float(entryB.get())
            if b==0:
                  messagebox.showerror('Lỗi', "Không thể chia cho 0")
            else:
                  kq = float(entryA.get()) / b
                  label_kq.config(text=entryA.get() + ' / ' + entryB.get() + ' = ' + str(kq), fg=color_text_kq)
                  label_Frame3.config(fg=color_text_kq)
                  
      except:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            entryA.delete(0, tk.END)
            entryB.delete(0, tk.END)

# create function reset          
def reset():
      entryA.delete(0, tk.END)
      entryB.delete(0, tk.END)
      label_kq.config(text='=', fg=color_text)
      label_Frame3.config(fg=color_text)
      
win.mainloop()
# end