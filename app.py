from flask import Flask, request, redirect, url_for, render_template, make_response, jsonify
app = Flask(__name__)
users = {}
@app.route('/')
def home():
    return render_template('welcome.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)

        username = request.form['username']
        userpassword = request.form['password']
        user_pinno = request.form['userpinno']

        # Check if user already exists
        if username not in users:
            users[username] = {
                'user_password': userpassword,
                'user_pinno': user_pinno,
                'Amount': 0
            }

            print(users)

            # Redirect to login page after registration
            return redirect(url_for('login'))

        else:
            return 'User already exists'

    return render_template('register.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)

        login_username = request.form['username']
        login_password = request.form['password']

        # Check username exists
        if login_username in users:

            # Check password
            if users[login_username]['user_password'] == login_password:

                # Create response and set cookie
                resp = make_response(redirect(url_for('dashboard')))
                resp.set_cookie('user', login_username)

                return resp

            else:
                return 'Wrong password'

        else:
            return 'Username is wrong'

    return render_template('login.html')
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if request.cookies.get('user'):
        username = request.cookies.get('user')
        return render_template('dashboard.html', username=username)

    else:
        return redirect(url_for('login'))
@app.route('/deposit', methods=['GET', 'PUT'])
def deposit():
    if request.cookies.get('user'):

        if request.method == 'PUT':
            username = request.cookies.get('user')

            print(request.get_json())

            deposit_amount = int(request.get_json()['amount'])

            # Validation
            if deposit_amount > 0:

                if deposit_amount % 100 == 0:

                    if deposit_amount <= 50000:

                        # Update balance
                        users[username]['Amount'] += deposit_amount

                        return jsonify({
                            "message": f"{deposit_amount} deposited successfully",
                            "balance": users[username]['Amount']
                        })

                    else:
                        return jsonify({
                            "message": "Amount should be less than or equal to 50000"
                        })

                else:
                    return jsonify({
                        "message": "Amount should be multiple of 100"
                    })

            else:
                return jsonify({
                    "message": "Amount should be greater than 0"
                })

        return render_template('deposit.html')

    else:
        return redirect(url_for('login'))
@app.route('/withdraw', methods=['GET', 'PUT'])
def withdraw():
    if request.cookies.get('user'):

        if request.method == 'PUT':
            username = request.cookies.get('user')

            print(request.get_json())

            withdraw_amount = int(request.get_json()['amount'])

            balance_amount = users[username]['Amount']

            
            if withdraw_amount > 0:

                if withdraw_amount % 100 == 0:

                    if withdraw_amount <= balance_amount:

                        # Deduct balance
                        users[username]['Amount'] = balance_amount - withdraw_amount

                        return jsonify({
                            "message": f"{withdraw_amount} withdrawn successfully",
                            "balance": users[username]['Amount']
                        })

                    else:
                        return jsonify({
                            "message": f"Insufficient balance. Available balance is {balance_amount}"
                        })

                else:
                    return jsonify({
                        "message": "Amount should be multiple of 100"
                    })

            else:
                return jsonify({
                    "message": "Amount should be greater than 0"
                })

        return render_template('withdraw.html')

    else:
        return redirect(url_for('login'))

@app.route('/balance', methods=['GET'])
def balance():
    if request.cookies.get('user'):

        username = request.cookies.get('user')

        balance_amount = users[username]['Amount']

        return render_template(
            'balance.html',
            balance_amount=balance_amount,
            username=username
        )

    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))

    # Remove cookie
    resp.set_cookie('user', '', expires=0)

    return resp
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)


