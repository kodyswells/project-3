from flask import Flask, render_template, session, flash, redirect, request
import jinja2
from melons import Melon
from forms import LoginForm
from customers import customers, get_by_username

app = Flask(__name__)
app.secret_key = 'dev'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def homepage():
    return render_template("base.html")

@app.route("/melons")
def all_melons():
    melon_list = Melon.get_all()  # Updated call
    return render_template("melons.html", melon_list=melon_list)

@app.route("/melons/<melon_id>")
def melon_details(melon_id):
    melon = Melon.get_by_id(melon_id)
    return render_template("melon_details.html", melon=melon)

@app.route("/cart")
def get_cart():
    if 'username' not in session:
        return redirect("/login")
    """Display contents of shopping cart."""

    order_total = 0
    cart_melons = []

    # Get cart dict from session (or an empty one if none exists yet)
    cart = session.get("cart", {})

    for melon_id, quantity in cart.items():
        melon = Melon.get_by_id(melon_id)

        # Calculate total cost for this type of melon and add to order total
        total_cost = quantity * melon.price
        order_total += total_cost

        # Add the quantity and total cost as attributes on the Melon object
        melon.quantity = quantity
        melon.total_cost = total_cost

        cart_melons.append(melon)

    return render_template("cart.html", cart_melons=cart_melons, order_total=order_total)

@app.route("/add_to_cart/<melon_id>")
def add_to_cart(melon_id):
   if 'username' not in session:
    return redirect("/login")
   """Add a melon to the cart and redirect to the shopping cart page."""

   if 'cart' not in session:
      session['cart'] = {}
   cart = session['cart']  # store cart in local variable to make things easier

   cart[melon_id] = cart.get(melon_id, 0) + 1
   session.modified = True
   flash(f"Melon {melon_id} successfully added to cart.")
   print(cart)

   return redirect("/cart")

@app.route("/empty-cart")
def empty_cart():
   session["cart"] = {}

   return redirect("/cart")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = get_by_username(username)

        if not user or user['password'] != password:
            flash("Invalid username or password")
            return redirect('/login')

        session["username"] = user['username']
        flash("Logged in.")
        return redirect("/melons")

    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
   """Log user out."""

   del session["username"]
   flash("Logged out.")
   return redirect("/login")

@app.errorhandler(404)
def error_404(e):
   return render_template("404.html")

if __name__ == "__main__":
    app.env = "development"
    app.run(debug=True, port=8000, host="localhost")
