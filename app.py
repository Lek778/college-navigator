from flask import Flask, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'database.db'

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE rooms (
                id INTEGER PRIMARY KEY,
                number TEXT UNIQUE NOT NULL,
                floor INTEGER NOT NULL,
                wing TEXT,
                description TEXT,
                x REAL,
                y REAL
            )
        ''')

        sample_rooms = [
    ('ВХОД', 1, 'центральное', 'Главный вход', 350, 900),
    ('101', 1, 'левое', '', 150, 800),
    ('102', 1, 'левое', '', 150, 700),
    ('103', 1, 'левое', '', 150, 600),
    ('104', 1, 'левое', '', 150, 500),
    ('105', 1, 'левое', '', 150, 400),
    ('106', 1, 'левое', '', 150, 300),
    ('107', 1, 'центральное', '', 300, 400),
    ('108', 1, 'центральное', '', 300, 500),
    ('109', 1, 'правое', '', 600, 500),
    ('110', 1, 'правое', '', 700, 500),
    ('111', 1, 'правое', '', 800, 500),
    ('ОХРАНА', 1, 'левое', 'Пост охраны', 200, 900),
    ('КАНЦЕЛЯРИЯ', 1, 'центральное', '', 550, 900),
    ('ДИРЕКТОР', 1, 'правое', 'Кабинет директора', 750, 900),

    ('201', 2, 'левое', 'напротив раздевалок', 150, 800),
    ('202', 2, 'левое', '', 150, 700),
    ('203', 2, 'левое', '', 150, 600),
    ('204', 2, 'центральное', 'рядом с лестницей', 300, 500),
    ('205', 2, 'центральное', 'напротив библиотеки', 300, 400),
    ('206', 2, 'правое', '', 600, 500),
    ('207', 2, 'правое', '', 700, 500),
    ('СТОЛОВАЯ', 2, 'правое', 'Большая столовая', 750, 400),

    ('301', 3, 'левое', '', 150, 800),
    ('302', 3, 'левое', '', 150, 700),
    ('БИБЛИОТЕКА', 3, 'центральное', 'Центральная библиотека', 350, 500),
    ('303', 3, 'правое', '', 600, 500),
    ('304', 3, 'правое', '', 700, 500),

    ('401', 4, 'левое', '', 150, 800),
    ('402', 4, 'левое', '', 150, 700),
    ('403', 4, 'центральное', '', 350, 500),
    ('404', 4, 'правое', '', 600, 500),
    ('405', 4, 'правое', '', 700, 500),
]
        
        cursor.executemany('''
            INSERT INTO rooms (number, floor, wing, description, x, y)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', sample_rooms)
        conn.commit()
        conn.close()

def get_room_by_number(room_number):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms WHERE number = ?", (room_number,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            'number': row[1],
            'floor': row[2],
            'wing': row[3] or 'центральное',
            'description': row[4] or '',
            'x': row[5],
            'y': row[6]
        }
    return None

def generate_route(target):
    steps = ["1. Начните у главного входа (1 этаж, центральная зона)."]
    
    if target['floor'] == 1:
        if target['wing'] == 'левое':
            steps.append("2. Поверните налево и идите до левого крыла.")
        elif target['wing'] == 'правое':
            steps.append("2. Поверните направо и идите до правого крыла.")
        else:
            steps.append("2. Оставайтесь в центральной зоне 1 этажа.")
    else:
        floor_word = f"{target['floor']} этаж"
        steps.append(f"2. Поднимитесь на {floor_word}.")
        if target['wing'] == 'левое':
            steps.append(f"3. Выйдя из лифта/лестницы, поверните налево — вы в левом крыле {floor_word}.")
        elif target['wing'] == 'правое':
            steps.append(f"3. Выйдя из лифта/лестницы, поверните направо — вы в правом крыле {floor_word}.")
        else:
            steps.append(f"3. Прямо перед вами — центральная зона {floor_word}.")

    if target['description']:
        steps.append(f"4. Найдите кабинет {target['number']} — {target['description']}.")
    else:
        steps.append(f"4. Ваш кабинет: {target['number']}.")

    return "<ol>" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/rooms')
def api_rooms():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT number, floor FROM rooms ORDER BY floor, number")
    rooms = [{'number': r[0], 'floor': r[1]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(rooms)

@app.route('/api/route/<room_number>')
def api_route(room_number):
    room = get_room_by_number(room_number)
    if not room:
        return jsonify({'success': False, 'error': 'Кабинет не найден'})
    route_html = generate_route(room)
    return jsonify({'success': True, 'route': route_html, 'room': room})

if __name__ == '__main__':
    init_db() 
    app.run(debug=True, port=5001)