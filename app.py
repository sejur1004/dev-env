from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

# 데이터베이스 연결 설정
db = pymysql.connect(
    host="db-no308.vpc-pub-cdb-sg.ntruss.com",
    user="sikadmin",
    password="ncp123!@#",
    db="sikdata",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    nickname = data['nickname']
    distance = data['distance']
    pace = data['pace']
    other = data['other']

    with db.cursor() as cursor:
        sql = "INSERT INTO DATA (nickname, distance, pace, other) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nickname, distance, pace, other))
        db.commit()

    return jsonify({'status': 'success'})

@app.route('/dashboard')
def dashboard():
    with db.cursor() as cursor:
        sql = "SELECT * FROM DATA"
        cursor.execute(sql)
        result = cursor.fetchall()
    
    return render_template('dashboard.html', data=result)

if __name__ == '__main__':
    app.run(debug=True)
