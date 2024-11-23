from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import psycopg2
from psycopg2 import sql
from database import Database

app = Flask(__name__) #khởi tạo một đối tượng Flask
app.secret_key = 'your_secret_key'  # Bảo mật session Quản lý trạng thái người dùng trong thời gian đăng nhập


# Trang đăng nhập
# GET: Hiển thị giao diện đăng nhập (index.html).
# POST: Xử lý dữ liệu đăng nhập.
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user'] #Lấy thông tin user và password từ form.
        password = request.form['password']
        db = Database(db_name='quanlysinhvien', user=user, password=password, host='localhost', port=5432) # Tạo kết nối tới cơ sở dữ liệu qua lớp Database.
        if db.connect():
            session['user'] = user # Lưu thông tin đăng nhập vào session.
            session['password'] = password
            db.cur.close()
            db.conn.close()
            return redirect(url_for('home')) 
        else:
            flash("Kết nối không thành công.", 'error')
    return render_template('index.html')


# Trang chính
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' in session and 'password' in session:
        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            db.cur.execute('SELECT * FROM khoacntt ORDER BY id') # sắp xếp theo cột id.
            data = db.cur.fetchall() # Lấy toàn bộ kết quả truy vấn và lưu trong biến data.
            db.cur.close() # Đóng con trỏ (cursor) để giải phóng tài nguyên.
            db.conn.close() # Đóng kết nối cơ sở dữ liệu.
            return render_template('home.html', data=data)
    flash("Bạn cần đăng nhập để truy cập trang này.", 'error')
    return redirect(url_for('login'))


# Thêm dữ liệu mới
@app.route('/home/add', methods=['POST'])
def add_data():
    if 'user' in session and 'password' in session:
        new_name = request.form.get('name', '').strip()
        new_mssv = request.form.get('mssv', '').strip()
        new_class = request.form.get('class', '').strip()
        # Loại bỏ khoảng trắng thừa ở đầu và cuối chuỗi, giúp tăng tính chính xác của dữ liệu.
        
        if not new_name or not new_mssv or not new_class:
            flash("Tất cả các trường (name, mssv, class) đều bắt buộc.", 'error')
            return redirect(url_for('home'))
        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            try:
                # Kiểm tra mssv trùng lặp
                db.cur.execute("SELECT COUNT(*) FROM khoacntt WHERE mssv = %s", (new_mssv,))
                # Đếm số lượng bản ghi (hàng) trong bảng khoacntt mà thỏa mãn điều kiện 
                # Chỉ đếm các hàng có giá trị cột mssv trùng với giá trị của new_mssv.
                if db.cur.fetchone()[0] > 0: 
                    flash("MSSV đã tồn tại, vui lòng nhập MSSV khác.", 'error')
                else:
                    # Thêm dữ liệu mới
                    db.cur.execute("INSERT INTO khoacntt (name, mssv, class) VALUES (%s, %s, %s)",
                                   (new_name, new_mssv, new_class))
                    db.conn.commit() # Lưu thay đổi vào cơ sở dữ liệu.
                    flash("Thêm dữ liệu thành công.", 'success')
            except Exception as e:
                flash(f"Lỗi khi thêm dữ liệu: {e}", 'error')
            finally:
                db.cur.close()
                db.conn.close()
    return redirect(url_for('home'))


# Xóa dữ liệu đã chọn
@app.route('/home/delete', methods=['POST'])
def delete_data():
    if 'user' in session and 'password' in session:
        selected_ids = request.form.getlist('selected') # Lấy danh sách các ID (giá trị id) mà người dùng đã chọn từ form.
        if not selected_ids:
            flash("Vui lòng chọn hàng cần xóa.", 'error')
            return redirect(url_for('home'))

        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            try:
                db.cur.execute(
                    "DELETE FROM khoacntt WHERE id IN (%s)" % ','.join(map(str, selected_ids)))
                    # Chỉ xóa các bản ghi có id nằm trong danh sách các ID mà người dùng đã chọn.
                db.conn.commit() # Lưu thay đổi vào cơ sở dữ liệu.
                flash("Xóa dữ liệu thành công.", 'success')
            except Exception as e:
                flash(f"Lỗi khi xóa dữ liệu: {e}", 'error')
            finally:
                db.cur.close()
                db.conn.close()
    return redirect(url_for('home'))


# Tìm kiếm sinh viên theo MSSV
@app.route('/home/search', methods=['POST'])
def search_data():
    if 'user' in session and 'password' in session:
        mssv = request.form['mssv']  # Lấy MSSV từ form tìm kiếm
        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            try:
                # Tìm kiếm sinh viên theo MSSV
                query = "SELECT * FROM khoacntt WHERE mssv = %s"
                db.cur.execute(query, (mssv,)) # Chạy truy vấn với giá trị tham số là mssv
                data = db.cur.fetchall() # lấy kết quả vừa chạy lưu vào biến data
                
                db.cur.close()
                db.conn.close()

                if data:
                    # Truyền kết quả tìm kiếm vào trang details.html
                    return render_template('details.html', data=data)
                else:
                    flash("Không tìm thấy sinh viên với MSSV đã nhập.", 'error')
            except Exception as e:
                flash(f"Lỗi khi tìm kiếm: {e}", 'error')
            finally:
                db.cur.close()
                db.conn.close()

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    # Xóa toàn bộ session
    session.clear()
    # Chuyển hướng về trang đăng nhập
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
