from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sat123@@'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)




cash_balance = 1000


items = {
    'pen': {'name': 'Pen', 'price': 5},
    'pencil': {'name': 'Pencil', 'price': 2},
    'eraser': {'name': 'Eraser', 'price': 1},
    'sharpener': {'name': 'Sharpener', 'price': 2},
    'geometry_box': {'name': 'Geometry Box', 'price': 10}
}



@app.route('/')
def index():
    cur=mysql.connection.cursor()
    cur.execute("select id,item_name,quantity,transcation_type, timestamp, rate, amount from transaction")
    trans_data=cur.fetchall()
    cur.close()
    return render_template('index1.html', cash_balance=cash_balance, items=items,transactions=trans_data)

@app.route('/purchase', methods=['POST'])

def purchase():
    global cash_balance
    item_name = request.form['item']
    quantity = int(request.form['quantity'])
    ra=int(request.form.get('price',0))
    trans_type='BUY'
    
    item = items[item_name]
    t_c = item['price'] * quantity
    ra = item['price']

    if cash_balance >= t_c:
        cash_balance -= t_c
        #alter code
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO transaction (item_name, quantity,rate,transcation_type,amount) VALUES (%s, %s,%s,%s,%s)",
                    (item_name, quantity,ra,trans_type,t_c))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    else:
        return "Insufficient cash balance."

@app.route('/sale', methods=['POST'])
def sale():
    global cash_balance
    item_name = request.form['item']
    quantity = int(request.form['quantity'])
    trans_type='SALE'
    
    item = items[item_name]
    ra=item['price']*2;
    t_e = (item['price']*2) * quantity
    cash_balance += t_e

    #alter code
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO transaction (item_name, quantity,transcation_type,rate,amount) VALUES (%s, %s,%s,%s,%s)",
                (item_name, quantity,trans_type,ra,t_e))
    mysql.connection.commit()
    cur.close()

    return redirect('/')

@app.route('/table')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT ino,iname FROM items")
    fetchdata = cur.fetchall()
    cur.close()
    return render_template("table.html", users=fetchdata)

if __name__ == '__main__':
    app.run(debug=True)
