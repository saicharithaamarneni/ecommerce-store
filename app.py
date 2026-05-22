from flask import Flask, render_template, request, redirect, session
from config import Config
from models.user import db, User
from models.product import Product
from models.order import Order

app = Flask(__name__)

app.secret_key = "ecommerce_secret_key"

app.config.from_object(Config)


db.init_app(app)

try:
    with app.app_context():
        db.create_all()

except Exception as e:
    print(e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing = User.query.filter_by(
            email=email
        ).first()

        if existing:
            return "Email already exists"

        user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email,
            password=password
        ).first()

        if user:

            session["user"] = user.username

            return redirect("/dashboard")

        return "Invalid credentials"

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        username=session["user"]
    )


@app.route("/logout")
def logout():

    session.pop(
        "user",
        None
    )

    return redirect("/login")

@app.route("/products")
def products():

    if "user" not in session:
        return redirect("/login")

    products = Product.query.all()

    return render_template(
        "products.html",
        products=products
    )
@app.route("/add-to-cart/<int:id>")
def add_to_cart(id):

    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    cart.append(id)

    session["cart"] = cart

    return redirect("/products")
@app.route("/cart")
def cart():

    ids = session.get(
        "cart",
        []
    )

    items = Product.query.filter(
        Product.id.in_(ids)
    ).all()

    total = sum(
        p.price
        for p in items
    )

    return render_template(
        "cart.html",
        items=items,
        total=total
    )
@app.route("/remove/<int:id>")
def remove(id):

    cart = session.get(
        "cart",
        []
    )

    if id in cart:
        cart.remove(id)

    session["cart"] = cart

    return redirect("/cart")
@app.route("/seed")
def seed():

    Product.query.delete()

    db.session.commit()

    data = [

        Product(
            name="iPhone",
            price=70000,
            image="https://images.unsplash.com/photo-1592899677977-9c10ca588bbd"
        ),

        Product(
            name="Laptop",
            price=50000,
            image="https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
        ),

        Product(
            name="Headphones",
            price=3000,
            image="https://images.unsplash.com/photo-1505740420928-5e560c06d30e"
        )

    ]

    db.session.add_all(data)

    db.session.commit()

    return redirect("/products")
@app.route("/check")
def check():

    products = Product.query.all()

    output = ""

    for p in products:
        output += f"{p.id} | {p.name}<br>"

    return output
@app.route("/checkout")
def checkout():

    ids = session.get(
        "cart",
        []
    )

    items = Product.query.filter(
        Product.id.in_(ids)
    ).all()

    total = sum(
        p.price
        for p in items
    )

    order = Order(

        username=session[
            "user"
        ],

        total=total
    )

    db.session.add(
        order
    )

    db.session.commit()

    session[
        "cart"
    ]=[]

    return redirect(
        "/orders"
    )
@app.route("/orders")
def orders():

    data = Order.query.all()

    return render_template(
        "orders.html",
        orders=data
    )
@app.route("/admin")
def admin():

    users = User.query.count()

    products = Product.query.count()

    orders = Order.query.count()

    return render_template(

        "admin.html",

        users=users,

        products=products,

        orders=orders

    )
if __name__ == "__main__":
    app.run()