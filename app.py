#sebelum ditambahkan
#from flask import Flask, render_template, request, redirect, url_for
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import text
#import sqlite3

# Ditambah kan from flask_login import LoginManager, login_user, login_required, logout_user, current_user 
#untuk membantu menangani login
# dan import flash untuk membantu mengirim pesan error
#berikut setelah penambahan :

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from sqlalchemy import text
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Ditambahkan secret key untuk memperketat keamanan
app.config['SECRET_KEY'] = 'putriAnggota9Naga'
#mengonfigurasi Flask-Login untuk mengelola autentikasi pengguna
login_manager = LoginManager()
login_manager.login_view = 'login' 
login_manager.init_app(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

#bagian tambahan bukan bawaan dari soal
#menambahkan kelas user untuk membantu autentikasi pengguna
class User:
    #
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self._authenticated = False #untuk cek pengguna berhasil login tidak
        self._active = True  #untuk ngasih tanda bahwa pengguna aktif

    #method untuk mengembalikan id dari objek pengguna
    def get_id(self):
        return self.id
    #bernilai benar ketika pengguna berhasil login
    def is_authenticated(self):
        return self._authenticated
    #cek pengguna active atau tidak
    def is_active(self):
        return self._active
    #method untuk pengguna anonim atau bukan
    def is_anonymous(self):
        return not self._authenticated
    
# membuat wadah untuk menampung pengguna yang diizinkan
#karena ini merupakan web sekolah untuk CRUD data siswa maka dibatasi 
#pengguna yang diizinkan hanya admin dan guru
pengguna_AksesSah = {
    "admin": "adminBisa98",
    "guru": "guruAja12"  
}

#fungsi untuk menampung atau memuat informasi pengguna sesuai idnya
#kalo sistem butuh informasi seperti pengguna saat ini maka diambil dari sini informasinya
#cara kerjanya user_id ada di pengguna_aksesSah jika ditemukan dikembalikan datanya
@login_manager.user_loader
def load_user(user_id):
    if user_id in pengguna_AksesSah:
        return User(id=user_id, username=user_id, password=pengguna_AksesSah[user_id])
    return None

#membuat endPoint untuk login
@app.route('/login', methods=['GET', 'POST'])
#membuat Fungsi untuk Login 
# agar hanya pengguna sah yang bisa melakukan CRUD dan mengakses data
def login():
    if request.method == 'POST':

        #ambil data user dari form
        username = request.form['username']
        password = request.form['password']

        #cek usernamenya termasuk dalam pengguna yang dikasih izin dan sah tidak
        #jika usernamenya tidak ada dalam data pengguna_Akses sah maka tampilkan pesan error
        #setelah ditampilkan pesan error jika bukan pengguna yang sah kemudian  diarahkan kembali kehalaman login
        if username not in pengguna_AksesSah:
            flash('Anda tidak memiliki akses', 'error')  
            return redirect(url_for('login'))

        #memvalidasi apakah dengan username yang dimasukkan passwordnya juga sesuai dengan password penggunaSah
        #akan dicek password yang dimasukkan dicocokkan dengan password yang berada pada data pengguna Sah
        #kemudian jika data password tidak sesuai akan dikembalikan ke login dan ditampilkan pesan error
        if pengguna_AksesSah[username] != password:  
            flash('Password atau Username yang dimasukkan tidak valid', 'error')  
            return redirect(url_for('login'))

        #jika sudah sesuai dan cocok dibuat objek pengguna
        user = User(id=username, username=username, password=pengguna_AksesSah[username])
        #nilai autentikasi nya menjadi true karena berhasil login 
        user._authenticated = True  


        #kemudian fungsi login_user untuk menandai pengguna login
        #agar nanti mudah dilacak pengguna nya sudah masuk dan untuk data sesi
        login_user(user)
        #login berhasil kirim ke halaman index untuk mengakses data atau melakukan CRUD
        return redirect(url_for('index'))

    return render_template('login.html')

#tambahan tidak dari soal
#agar membantu fleksibilitas pengguna diseddiakan fitur logout
#membuat endPoint logout
@app.route('/logout')
#ditambahakan @login_required agar sebelum logout wajib log in terlebih dahulu
#dan memastikan juga bahwa cuma pengguna yang login yang bisa akses route ini
@login_required
#fungsi logout
def logout():
    logout_user()
    #ketika sudah logout diarahkan kembali ke halaman login
    return redirect(url_for('login'))

#sebelum ditambahkan 
#@app.route('/')
#def index():
    # RAW Query
    #students = db.session.execute(text('SELECT * FROM student')).fetchall()
    #return render_template('index.html', students=students)

#setelah ditambahkan
@app.route('/')
@login_required #untuk memastikan sebelum mengakses route ini wajib sudah login dulu
def index():
    # RAW Query
    students = db.session.execute(text('SELECT * FROM student')).fetchall()
    return render_template('index.html', students=students)

#sebelum ditambahkan 
#@app.route('/add', methods=['POST'])
#def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    

    connection = sqlite3.connect('instance/students.db')
    cursor = connection.cursor()

    # RAW Query
    # db.session.execute(
    #     text("INSERT INTO student (name, age, grade) VALUES (:name, :age, :grade)"),
    #     {'name': name, 'age': age, 'grade': grade}
    # )
    # db.session.commit()
    query = f"INSERT INTO student (name, age, grade) VALUES ('{name}', {age}, '{grade}')"
    cursor.execute(query)
    connection.commit()
    connection.close()
    return redirect(url_for('index'))

#setelah ditambahkan 
@app.route('/add', methods=['POST'])
@login_required #untuk memastikan sebelum mengakses route ini wajib sudah login dulu
def add_student():
    name = request.form['name']
    age = request.form['age']
    grade = request.form['grade']
    

    connection = sqlite3.connect('instance/students.db')
    cursor = connection.cursor()
    #meskipun bukan termasuk kedalam cwe 306, namun pengamanan ini juga penting
    #maka dari itu juga dilakukan agar tidak terjadi hal-hal yang tidak diinginkan
    # Tambahan juga agar data yang ditambahkan bukan sqlinjection
    # RAW Query
    db.session.execute(
        text("INSERT INTO student (name, age, grade) VALUES (:name, :age, :grade)"),
        {'name': name, 'age': age, 'grade': grade}
     )
    db.session.commit()
    ##query = f"INSERT INTO student (name, age, grade) VALUES ('{name}', {age}, '{grade}')"
    #cursor.execute(query)
    #connection.commit()
    connection.close()
    return redirect(url_for('index'))

#sebelum ditambahkan 
#@app.route('/delete/<string:id>') 
#def delete_student(id):
    # RAW Query
    db.session.execute(text(f"DELETE FROM student WHERE id={id}"))
    db.session.commit()
    return redirect(url_for('index'))

#setelah ditambahkan
@app.route('/delete/<string:id>') 
@login_required #untuk memastikan sebelum mengakses route ini wajib sudah login dulu
def delete_student(id):
    # RAW Query
    #meskipun bukan termasuk kedalam cwe 306, namun pengamanan ini juga penting
    #maka dari itu juga dilakukan agar tidak terjadi hal-hal yang tidak diinginkan
    db.session.execute(text("DELETE FROM student WHERE id = :id"), {"id": id})
    db.session.commit()
    return redirect(url_for('index'))

#sebelum ditamabahkan
#@app.route('/edit/<int:id>', methods=['GET', 'POST'])
#def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        
        # RAW Query
        db.session.execute(text(f"UPDATE student SET name='{name}', age={age}, grade='{grade}' WHERE id={id}"))
        db.session.commit()
        return redirect(url_for('index'))
    else:
        # RAW Query
        student = db.session.execute(text(f"SELECT * FROM student WHERE id={id}")).fetchone()
        return render_template('edit.html', student=student)

#setelah ditambahkan
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required #untuk memastikan sebelum mengakses route ini wajib sudah login dulu
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
            #meskipun bukan termasuk kedalam cwe 306, namun pengamanan ini juga penting
    #maka dari itu juga dilakukan agar tidak terjadi hal-hal yang tidak diinginkan
        # RAW Query
        db.session.execute(
            text("UPDATE student SET name = :name, age = :age, grade = :grade WHERE id = :id"),
            {"name": name, "age": age, "grade": grade, "id": id}
        )
        db.session.commit()
        return redirect(url_for('index'))
    else:
        # RAW Query
            #meskipun bukan termasuk kedalam cwe 306, namun pengamanan ini juga penting
             #maka dari itu juga dilakukan agar tidak terjadi hal-hal yang tidak diinginkan
        student = db.session.execute(text("SELECT * FROM student WHERE id = :id"), {"id": id}).fetchone()
        return render_template('edit.html', student=student)



# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)