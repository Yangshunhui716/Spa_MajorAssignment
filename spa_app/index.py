from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("appointments.html")

@app.route('/1')
def index1():
    return render_template("servicessheet.html")

@app.route('/2')
def index2():
    return render_template("payment.html")

if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)