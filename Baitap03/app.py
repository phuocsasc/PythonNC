from flask import Flask, render_template, request, redirect, url_for, make_response, flash, session
import psycopg2
from psycopg2 import sql
from database import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Thêm khóa bảo mật cho session

# Route trang đăng nhập (mặc định)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        user = request.form['user']
        password = request.form['password']
        
        # Tạo kết nối với thông tin từ form
        db = Database(db_name='dbtest', user=user, password=password, host='localhost', port=5432)
        if db.connect():
            # Lưu thông tin đăng nhập trong session
            session['user'] = user
            session['password'] = password
            db.cur.close()  # Đóng cursor
            db.conn.close()  # Đóng kết nối
            
            # Kết nối thành công, chuyển đến trang home
            return redirect(url_for('home'))
        else:
            # Kết nối thất bại, hiển thị thông báo lỗi
            flash("Kết nối không thành công. <br> Vui lòng kiểm tra lại thông tin đăng nhập.", 'error')
    
    return render_template('index.html')
# Trang chính khi kết nối thành công
@app.route('/home', methods=['GET', 'POST'])
def home():
    # Kiểm tra session trước khi truy cập trang home
    if 'user' in session and 'password' in session:
        db = Database(db_name='dbtest', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            db.cur.execute('SELECT * FROM khoacntt')
            data = db.cur.fetchall()
            db.cur.close()
            db.conn.close()
            return render_template('home.html', data=data)
    
    # Nếu không có thông tin đăng nhập, chuyển về trang đăng nhập
    flash("Bạn cần đăng nhập để truy cập trang này.", 'error')
    return render_template('index.html')

# Route để thêm dữ liệu mới vào database
@app.route('/home/add', methods=['POST'])
def add_data():
    # Kiểm tra session trước khi cho phép thêm dữ liệu
    if 'user' in session and 'password' in session:
        # Lấy dữ liệu từ form
        new_class = request.form['class']
        new_name = request.form['name']
        
        db = Database(db_name='dbtest', user=session['user'], password=session['password'], host='localhost', port=5432)
        if db.connect():
            try:
                # Thêm dữ liệu vào bảng khoacntt
                insert_query = "INSERT INTO khoacntt (class, hoten) VALUES (%s, %s)"
                db.cur.execute(insert_query, (new_class, new_name))
                db.conn.commit()
                flash("Thêm dữ liệu thành công.", 'success')
            except Exception as e:
                flash(f"Lỗi khi thêm dữ liệu: {e}", 'error')
            finally:
                db.cur.close()
                db.conn.close()
                
    return redirect(url_for('home'))

# Xem chi tiết với dữ liệu từ cookie
@app.route('/home/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        selected_data = request.form.getlist('selected')
        resp = make_response(redirect(url_for('details')))
        # Cookies: Lưu class đã chọn từ trang chính
        resp.set_cookie('selected_data', ','.join(selected_data))
        return resp
    
    # Lấy dữ liệu từ cookie
    selected_data = request.cookies.get('selected_data', '').split(',')
    if selected_data == ['']:
        selected_data = []
    
    # Kết nối cơ sở dữ liệu với thông tin từ session
    db = Database(db_name='dbtest', user=session['user'], password=session['password'], host='localhost', port=5432)
    if db.connect():
        if selected_data:
            query = sql.SQL("SELECT * FROM khoacntt WHERE class IN ({})").format(
                sql.SQL(', ').join(map(sql.Literal, selected_data))
            )
            db.cur.execute(query)
            data = db.cur.fetchall()
        else:
            data = []
        db.cur.close()
        db.conn.close()
    else:
        flash("Kết nối cơ sở dữ liệu không thành công.", 'error')
        return redirect(url_for('login'))
    return render_template('details.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
