from flask import Flask, render_template, redirect, request, session, url_for
from backend_controller.loginController import *
from backend_controller.ordersController import ordersController, getorder, getorderproducts
from backend_controller.productsController import *
from backend_controller.accountsController import *
from backend_controller.reportsController import getDatedReport, getStockReport
from backend_controller.profileController import *

app = Flask(__name__, template_folder='backend/', static_folder='static')
app.secret_key = 'akeythatissecret'


@app.route("/", defaults={'message': None})
@app.route("/<message>")
def enterpage(message):
    return render_template('login (2).html', message=message)


@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")


@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    session['amount'] = 0
    return logincontroller(email=email, password=password)


@app.route("/profile")
def profile():
    admin = getUser(session['admin'])
    return render_template("profile.html", user1=admin)


@app.route("/products")
def products():
    productsp = getProducts()
    return render_template("products.html", products=productsp)


@app.route("/orders")
def orders():
    all_orders = ordersController()
    return render_template("orders.html", orders=all_orders)


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/report", methods=['POST'])
def report():
    date_report = {}
    stock_report = {}
    total = 0

    if 'report_day' in request.form:
        date_report = getDatedReport()
    if 'report_week' in request.form:
        date_report = getDatedReport()
    if 'report_month' in request.form:
        date_report = getDatedReport()
    if 'stock_report' in request.form:
        stock_report = getStockReport()

    if date_report:
        total = sum(order['total_price'] for order in date_report.values())

    return render_template("report.html", date_report=date_report, stock_report=stock_report, total=total)



if __name__ == "__main__":
    app.run(debug=True)

