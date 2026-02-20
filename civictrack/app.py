from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
#1
app = Flask(__name__)
app.secret_key = "supersecretkey"

# --------------------------
# DATABASE INITIALIZATION
# --------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        category TEXT,
        priority TEXT,
        latitude REAL,
        longitude REAL,
        status TEXT DEFAULT 'Pending',
        date TEXT
    )
''')
    
    conn.commit()
    conn.close()

init_db()

# --------------------------
# HOME PAGE
# --------------------------
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM complaints")
    total = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved = c.fetchone()[0]
    
    pending = total - resolved
    
    conn.close()
    
    return render_template("index.html", total=total, resolved=resolved, pending=pending)

# --------------------------
# REPORT PAGE
# --------------------------
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        priority = request.form['priority']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO complaints (title, description, category, priority, latitude, longitude, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (title, description, category, priority, latitude, longitude, date))
        
        conn.commit()
        conn.close()
        
        return redirect('/')
    
    return render_template("report.html")

#login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hardcoded admin credentials
        if username == "admin" and password == "1234":
            session['admin'] = True
            return redirect('/dashboard')
        else:
            return render_template("admin.html", error="Invalid Credentials")

    return render_template("admin.html")

#logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

# --------------------------
# DASHBOARD PAGE
# --------------------------
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Get filter values from URL
    search = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    status_filter = request.args.get('status', '')

    query = "SELECT * FROM complaints WHERE 1=1"
    params = []

    if search:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")

    if category_filter:
        query += " AND category=?"
        params.append(category_filter)

    if status_filter:
        query += " AND status=?"
        params.append(status_filter)

    query += " ORDER BY id DESC"

    c.execute(query, params)
    rows = c.fetchall()

    complaints = []
    for row in rows:
        complaints.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "category": row[3],
            "priority": row[4],
            "latitude": row[5],
            "longitude": row[6],
            "status": row[7],
            "date": row[8]
        })

    # Category Chart Data
    c.execute("SELECT category, COUNT(*) FROM complaints GROUP BY category")
    category_rows = c.fetchall()
    category_data = [{"category": r[0], "count": r[1]} for r in category_rows]

    # Status Chart Data
    c.execute("SELECT status, COUNT(*) FROM complaints GROUP BY status")
    status_rows = c.fetchall()
    status_data = [{"status": r[0], "count": r[1]} for r in status_rows]

    conn.close()

    return render_template(
        "dashboard.html",
        complaints=complaints,
        category_data=category_data,
        status_data=status_data,
        search=search,
        category_filter=category_filter,
        status_filter=status_filter
    )
# --------------------------
# UPDATE STATUS (ADMIN)
# --------------------------
#####
@app.route('/update/<int:id>/<status>')
def update_status(id, status):

    # If not logged in as admin → redirect to login
    if not session.get('admin'):
        return redirect('/admin')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute("UPDATE complaints SET status=? WHERE id=?", (status, id))
    
    conn.commit()
    conn.close()
    
    return redirect('/dashboard')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    c.execute("UPDATE complaints SET status=? WHERE id=?", (status, id))
    
    conn.commit()
    conn.close()
    
    return redirect('/dashboard')
# --------------------------
# MAP
# --------------------------

# all routes above

@app.route('/map')
def map_view():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT * FROM complaints")
    rows = c.fetchall()
    conn.close()

    complaints = []
    for row in rows:
        complaints.append({
            "title": row["title"],
            "category": row["category"],
            "priority": row["priority"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "status": row["status"]
        })

    return render_template("map.html", complaints=complaints)


if __name__ == '__main__':
    app.run(debug=True)