from datetime import datetime
from flask import Flask, render_template, redirect, request, session
from models import db, Product
from frontend_controller.cartController import getCart, addCartController, deleteCartItem
from frontend_controller.checkoutController import getUserCheckout
from frontend_controller.invoiceController import getOrder, getOrderProducts
from frontend_controller.loginController import logincontroller
from frontend_controller.ordersController import getorder1, getorder2, getorder1products, getorder2products
from frontend_controller.profileController import getUser
from frontend_controller.shopController import getProducts, getBrands, getColors, getVideoRes, getWifi, book_page

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.secret_key = 'akeythatissecret'

# ✅ Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ✅ Initialize Database Tables
with app.app_context():
    db.create_all()


# ✅ Redirects to Login Page (Fixed)
@app.route("/", defaults={'message': None})
@app.route("/<message>")
def enterpage(message):
    return render_template('login(2).html', message=message)  # Ensure this template exists


# ✅ Logout & Clear Session
@app.route("/clear")
def clear():
    session.clear()
    return redirect("/")


# ✅ User Login Route
@app.route("/login", methods=['POST'])
def login():
    email = request.form.get('email')
    passcode = request.form.get('password')
    session['amount'] = 0
    return logincontroller(email=email, password=passcode)


# ✅ User Registration Routes
@app.route("/register/", defaults={'message': None})
@app.route('/register/<message>')
def register(message):
    return render_template('register.html', message=message)


@app.route("/registerinfo", methods=['POST'])
def registerinfo():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    pass1 = request.form.get('pass1')
    pass2 = request.form.get('pass2')

    if pass1 == pass2:
        session['amount'] = 0
        email = 'javier.negron11@upr.edu'
        passcode = 'Jav@0000'
        logincontroller(email=email, password=passcode)
        return redirect('/shop')
    else:
        return redirect('/register/error')


# ✅ Shop Page Route (Fixed)
@app.route("/shop")
def shop():
    products = getProducts()
    getCart()  # Ensures cart session is initialized

    return render_template("shop-4column.html", products=products)


# ✅ User Profile Route
@app.route("/profile")
def profile():
    if 'customer' not in session:
        return redirect("/")

    user = getUser(session['customer'])
    total = session.get('total', 0)
    num = '{:03d}-{:03d}-{:04d}'.format(
        int(str(user['c_phone_number'])[:3]),
        int(str(user['c_phone_number'])[3:6]),
        int(str(user['c_phone_number'])[6:])
    )

    return render_template("profile.html", user1=user, total=total, num=num)


@app.route("/editinfo", methods=["POST"])
def editinfo():
    return redirect("/profile")


@app.route("/password", methods=["POST"])
def password():
    return render_template("change-password.html")


# ✅ Orders Page
@app.route("/orders")
def orders():
    order1 = getorder1()
    products1 = getorder1products()
    order2 = getorder2()
    products2 = getorder2products()

    return render_template("orderlist.html", order1=order1, products1=products1, order2=order2, products2=products2)


# ✅ Cart Functions
@app.route("/addcart", methods=["POST"])
def addcart():
    addCartController()
    return redirect(request.referrer)


@app.route("/delete")
def delete():
    deleteCartItem()
    return redirect(request.referrer)


@app.route("/editcart", methods=["POST"])
def editcart():
    return redirect(request.referrer)


# ✅ Individual Book Page
@app.route("/book/<book_name>")
def book(book_name):
    return book_page(book_name)


# ✅ Checkout Route (Fixed to Avoid Errors)
@app.route("/checkout")
def checkout():
    if 'customer' not in session:
        session['checkout'] = True
        return redirect("/wrong")

    user = getUserCheckout()
    total = sum(item['total_price'] for item in session.get('cart', {}).values())

    num = '{:03d}-{:03d}-{:04d}'.format(
        int(str(user[10])[:3]),
        int(str(user[10])[3:6]),
        int(str(user[10])[6:])
    )

    return render_template("checkout.html", user1=user, num=num, total=total)


# ✅ Invoice Page
@app.route("/invoice")
def invoice():
    order = getOrder()
    products = getOrderProducts()
    return render_template("invoice.html", order=order, products=products, amount=3)


# ✅ Filtering Route (Placeholder)
@app.route("/filter")
def filter():
    return redirect("/shop")


# ✅ Run Flask
if __name__ == '__main__':
    app.run(debug=True)

