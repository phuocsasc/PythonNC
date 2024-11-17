from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response
import psycopg2
from psycopg2 import sql
from database import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Bảo mật session


# Trang đăng nhập
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        db = Database(db_name='quanlysinhvien', user=user, password=password, host='localhost', port=5432)
        if db.connect():
            session['user'] = user
            session['password'] = password
            db.cur.close()
            db.conn.close()
            return redirect(url_for('home'))
        else:
            flash("Kết nối không thành công. Vui lòng kiểm tra thông tin đăng nhập.", 'error')
    return render_template('index.html')


# Trang chính
@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' in session and 'password' in session:
        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            db.cur.execute('SELECT * FROM khoacntt ORDER BY id')
            data = db.cur.fetchall()
            db.cur.close()
            db.conn.close()
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

        if not new_name or not new_mssv or not new_class:
            flash("Tất cả các trường (name, mssv, class) đều bắt buộc.", 'error')
            return redirect(url_for('home'))

        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            try:
                # Kiểm tra mssv trùng lặp
                db.cur.execute("SELECT COUNT(*) FROM khoacntt WHERE mssv = %s", (new_mssv,))
                if db.cur.fetchone()[0] > 0:
                    flash("MSSV đã tồn tại, vui lòng nhập MSSV khác.", 'error')
                else:
                    # Thêm dữ liệu mới
                    db.cur.execute("INSERT INTO khoacntt (name, mssv, class) VALUES (%s, %s, %s)",
                                   (new_name, new_mssv, new_class))
                    db.conn.commit()
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
        selected_ids = request.form.getlist('selected')
        if not selected_ids:
            flash("Vui lòng chọn hàng cần xóa.", 'error')
            return redirect(url_for('home'))

        db = Database(db_name='quanlysinhvien', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            try:
                db.cur.execute(
                    "DELETE FROM khoacntt WHERE id IN (%s)" % ','.join(map(str, selected_ids)))
                db.conn.commit()
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
                db.cur.execute(query, (mssv,))
                data = db.cur.fetchall()
                
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

if __name__ == '__main__':
    app.run(debug=True)
