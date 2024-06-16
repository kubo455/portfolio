import os

from flask import Flask, redirect, render_template, request, session
from flask_session import Session 
import datetime
import sqlite3
from datetime import datetime as dt
from helper import chart_color
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
DATABASE = "database.db"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/register', methods=["GET", "POST"])
def register():

    # Forget user_id
    session.clear()
    conn = sqlite3.connect(DATABASE)

    if request.method == 'POST':
        # If not user name return warning
        username = request.form.get('username')
        if not username:
            msg = "MUST PROVIDE NEW USERNAME"
            return render_template('error_message.html', msg=msg)
        
        # If not password return warning
        password = request.form.get('password')
        if not password:
            msg = "MUST PROVIDE PASSWORD"
            return render_template('error_message.html', msg=msg)

        # If not password confirmattion return warning
        password_confirm = request.form.get('confirmation')
        if not  password_confirm:
            msg = "MUST PROVIDE PASSWORD CONFIRMATION"
            return render_template('error_message.html', msg=msg)
        # Check if password equals confirmation
        if password_confirm != password:
            msg = "YOUR PASSWORD IS NOT SAME AS PASSWORD CONFIRMATION"
            return render_template('error_message.html', msg=msg)
        
        cursor = conn.cursor()
        rows = conn.execute('SELECT * FROM users')
        for row in rows:
            if row[1] == username:
                msg = "CHOOSE DIFFERENT USERNAME THIS ONE ALREADY EXIST"
                return render_template('error_message.html', msg=msg)

        staring_balance = 0

        # Hash the users password and save it in users table
        password_hash = bcrypt.generate_password_hash(password)

        cursor.execute('INSERT INTO users (username, password, balance) VALUES (?, ?, ?)', (username, password_hash, staring_balance))
        conn.commit()

        # Look for user in database
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        # rememeber loged user 
        session["user_id"] = user[0]

        conn.close()

        return redirect('/')
    else:
        return render_template("register.html")
    

@app.route('/login', methods=["GET", "POST"])
def login():
    # Forget user_id
    session.clear()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Chech the user and sign him in
    if request.method == 'POST':
        username = request.form.get('username')
        if not username:
            msg = "MUST PROVIDE PASSWORD"
            return render_template('error_message.html', msg=msg)
        password = request.form.get('password')
        if not password:
            msg = "MUST PROVIDE USERNAME"
            return render_template('error_message.html', msg=msg)
        
        # Look for user in database
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        # Check user name and the hashed password
        if user is None:
            msg = "Invalid username"
            return render_template('error_message.html', msg=msg)
        else:
            check_password = bcrypt.check_password_hash(user[2], password)
            if check_password != True:
                msg = "Invalid password"
                return render_template('error_message.html', msg=msg)
            else:
                session["user_id"] = user[0]
                return redirect('/')
            
    else:
        return render_template("login.html")
    
@app.route('/logout')
def log_out():
    # clear the session
    session.clear()

    # redirect user to log in form
    return redirect('login')

@app.route('/message')
def message():
    # Message after successfull action
    message = 'Your action was successfull'
    return render_template('message.html', message=message)

@app.route('/error_message')
def e_message():
    # Message after wrong action
    msg = "ERROR"
    return render_template("error_message.html", msg=msg)

@app.route('/', methods=["GET", "POST"])
def index():
    try:
        user_id = session['user_id']
    # Proceed with the rest of the code
    except KeyError:
        return render_template('login.html')

    data  = []
    date = (datetime.date.today())
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Default expence types for user to choose
    default_exp_type = ["Bills", "Groceries", "Transportation", "Entertainment", "Shopping", "Healthcare", "Travel", "Debts and Loans"]

    # User data from users table
    user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id, ))
    if user == None:
        balance = 0
    else:
        balance = (user.fetchone()[3])

    # Add balance to the users account
    expence_type = request.form.get('expence_type')
    add_balance = request.form.get('balance')
    if request.method == 'POST':
        if 'balance' in request.form:
            is_numeric = add_balance.isnumeric()
            if not add_balance:
                msg = "Must provide how much money want to add"
                return render_template('error_message.html', msg=msg)
                # return "Must provide how much money want to add"
            if not is_numeric:
                msg = "You can use only number"
                return render_template('error_message.html', msg=msg)
            if float(add_balance) <= 0:
                msg = "Must providee only positive number"
                return render_template('error_message.html', msg=msg)

            # Update users balance
            cursor.execute('UPDATE users SET balance = ? WHERE id = ?', ((balance + int(add_balance)), user_id) )

            # Add income and date information to user wallet 
            cursor.execute('INSERT INTO wallet (income, user_id, date, new_balance) VALUES (?, ?, ?, ?)', (int(add_balance), user_id, date, (balance + int(add_balance))))

            conn.commit()

            return redirect('/message')
        
        # Here user add his expences
        elif 'expence_type' in request.form and 'sum' in request.form and 'date' in request.form:
            if not expence_type:
                msg = "Please choose expence type"
                return render_template('error_message.html', msg=msg)
            amount = request.form.get('sum')
            if not amount:
                msg = "Must provide amount"
                return render_template('error_message.html', msg=msg)
            date = request.form.get('date')
            formatted_date = dt.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
            if not date:
                msg = "Must provide datet"
                return render_template('error_message.html', msg=msg)
            if balance < int(amount):
                msg = "You don't have enought balance"
                return render_template('error_message.html', msg=msg)
            else:
                # Add expence in to expeces table
                cursor.execute('INSERT INTO expences (expence_type, amount, user_id, date) VALUES (?, ?, ?, ?)', (expence_type, amount, user_id, formatted_date))

                # Update users balance
                cursor.execute('UPDATE users SET balance = ? WHERE id =?', ((balance - int(amount)), user_id))

            conn.commit()

            return redirect('/message')

    # Users upadet balance
    user_balance = cursor.execute('SELECT balance FROM users WHERE id = ?', (user_id, ))
    updated_balance = (user_balance.fetchone()[0])

    # Sum of total expences and total income of user
    sum_exp = cursor.execute('SELECT SUM(amount) FROM expences WHERE user_id = ?', (user_id,))
    total_exp = sum_exp.fetchone()
    income = cursor.execute('SELECT SUM(income) FROM wallet WHERE user_id = ?', (user_id,))
    total_income= income.fetchone()

    data.append(total_exp[0])
    data.append(total_income[0])

    # All expences chart data
    exp_labels = []
    exp_values = []

    # User expences used for labels in chart and user expence types
    all_expences = cursor.execute('SELECT * FROM expences WHERE user_id = ?', (user_id, ))
    for i in all_expences:
        if i[1] not in default_exp_type:
            default_exp_type.append(i[1])
        if i[1] in exp_labels:
            continue
        else:
            exp_labels.append(i[1])

    # Set the color for expences chart
    num_of_exp = len(exp_labels)
    chart_colors = chart_color(100, 173, 255, num_of_exp)
    
    # Sum of one expence type used for chart
    for j in exp_labels:
        tot_value = cursor.execute('SELECT SUM(amount) FROM expences WHERE expence_type = ?', (j, ))
        tot = tot_value.fetchone()
        exp_values.append(tot[0])

    percetage = []

    # Count the percentage of each expence in portfolio
    for i in exp_values:
        percetage.append(int((i / sum(exp_values)) * 100))

    conn.commit()

    # User created expence types
    expences = cursor.execute('SELECT * FROM expences WHERE user_id = ?', (user_id, ))
    
    return render_template('index.html', balance=updated_balance, def_type=default_exp_type, expences=expences, data=data, exp_labels=exp_labels, exp_values=percetage,
                           chart_colors=chart_colors)
    

@app.route('/settings', methods=["GET", "POST"])
def settings():
    try:
        user_id = session['user_id']
    # Proceed with the rest of the code
    except KeyError:
        return render_template('login.html')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    user_password = cursor.execute("SELECT * FROM users WHERE id = ?", (user_id, ))
    password = user_password.fetchone()

    all_exp = []
    expences = cursor.execute('SELECT * FROM expences WHERE user_id = ?', (user_id, ))

    for row in expences:
        if row[1] in all_exp:
            continue
        else:
            all_exp.append(row[1])

    # Change the users password
    if request.method == 'POST':
        if "new_password" in request.form:
            new_password = request.form.get("new_password")
            if not new_password:
                msg = "Must provide new password"
                return render_template('error_message.html', msg=msg)
            password_confirmation = request.form.get("password_confirmation")
            if not password_confirmation:
                msg = "Must provide password confirmationd"
                return render_template('error_message.html', msg=msg)
            if new_password != password_confirmation:
                msg = "Your password and confirmation does not match"
                return render_template('error_message.html', msg=msg)
            # Create hash for new password and save it in table
            old_password = request.form.get("old_password")
            check_hash = bcrypt.check_password_hash(password[2], old_password)
            if check_hash != True:
                msg = "Incorect old password"
                return render_template('error_message.html', msg=msg)
            else:
                new_hash_password = bcrypt.generate_password_hash(new_password)
                cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_hash_password, user_id ))
                conn.commit()

        # Add new expence type to the users expences
        if "add_type" in request.form:
            exp_type = request.form.get("add_type")
            if not exp_type:
                msg = "Must provide expece type"
                return render_template('error_message.html', msg=msg)

            formated_type = exp_type.capitalize()

            # Add new expence type
            if formated_type in all_exp:
                msg = "This expence already exist"
                return render_template('error_message.html', msg=msg)
            else:
                cursor.execute("INSERT INTO expences (expence_type, user_id, amount) VALUES(?, ?, ?)", (formated_type, user_id, 0))
                conn.commit()
                return redirect('/')
        
    return render_template('settings.html')
    
if __name__ == '__main__':
    app.run(debug=True)