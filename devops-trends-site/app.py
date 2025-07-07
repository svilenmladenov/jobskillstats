from flask import Flask, render_template, request, redirect, url_for, session
from db_config import get_db_connection
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            session['user'] = 'admin'
            return redirect(url_for('home'))
        return render_template('login.html', error="Грешни данни.")
    return render_template('login.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/trends')
def trends():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    query = "SELECT * FROM project.jobs_total WHERE date > CURDATE() - INTERVAL 30 DAY"
    df = pd.read_sql(query, conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df = df.groupby('date')['jobs_total'].sum().reset_index()

    labels = df['date'].tolist()
    values = df['jobs_total'].tolist()

    return render_template('trends.html', labels=labels, values=values)

@app.route('/skills')
def skills():
    if 'user' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    query = """
        SELECT skill, COUNT(*) AS total 
        FROM project.skills 
        WHERE jobid in (SELECT jobid FROM project.jobs WHERE last_seen = CURDATE())
        GROUP BY skill 
        ORDER BY total DESC 
        LIMIT 20
    """
    df = pd.read_sql(query, conn)
    conn.close()

    labels = df['skill'].tolist()
    values = df['total'].tolist()

    return render_template('skills.html', labels=labels, values=values)

@app.route('/about')
def about():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
