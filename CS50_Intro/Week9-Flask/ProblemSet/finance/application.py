import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Get all stock purchased by the current user
    stocks = db.execute(
        "SELECT stock_symbol AS symbol, SUM(shares) AS shares FROM user_stock WHERE user_id = ? GROUP BY stock_symbol", session["user_id"])
    # Whole record of shares
    result = []
    # Do a special treatment for each stock purchased from
    for stock in stocks:
        update = lookup(stock["symbol"])
        shares = stock["shares"]
        price = update["price"]
        name = update["name"]
        result.append({
            "symbol": stock["symbol"],
            "name": name,
            "shares": shares,
            "price": usd(price),
            "total": usd(price * shares),
            "numerical_total": price * shares
        })
    # Calculating the total wealth for the current user
    user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    total = cash = user[0]["cash"]
    for stock in result:
        total += stock["numerical_total"]
    # Render template
    return render_template("index.html", stocks=result, total=usd(total), cash=usd(cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        symbol, shares = request.form.get("symbol"), request.form.get("shares")

        # Ensure a stock symbol is entered
        if not symbol:
            return apology("must provide symbol", 400)

        # Ensure a number of shares is entered
        elif not shares:
            return apology("must provide shares", 400)

        # Ensure a number format shares is entered
        elif not shares.isnumeric():
            return apology("must provide numeric shares", 400)

        # Ensure a number larger than 0 is entered as #shares
        elif int(shares) <= 0:
            return apology("#shares must bigger than 0", 400)

        # Check if enough cash under the user account
        record = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        stock = lookup(symbol)
        # Ensure a valid stock symbol is entered
        if not stock:
            return apology("must provide a valid symbol", 400)
        # Calculate the cost of this transaction
        cost = int(shares) * stock["price"]
        # Do not approve the purchase when not enough money
        if record[0]["cash"] < cost:
            return apology("you can't afford", 400)

        # Record the purchase within the database
        # 1. Update users, deduct cost from cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", record[0]["cash"] - cost, session["user_id"])
        # 2. Update user_stock, add transactions to it
        db.execute("INSERT INTO user_stock (user_id, stock_symbol, price, shares) VALUES (?,?,?,?)",
                   session["user_id"],
                   stock["symbol"],
                   stock["price"],
                   shares
                   )
        # Redirect to quote with GET method to display the lookup result
        return redirect("/")

    # Render the quote form
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    # Get all transaction records under the current user
    transactions = db.execute("SELECT stock_symbol, shares, price, time FROM user_stock WHERE user_id = ?",
                              session["user_id"])
    # Render history template with all transactions listed
    return render_template("history.html", records=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure a stock symbol is entered
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)

        # Make API calls to check current price for this stock
        stock = lookup(request.form.get("symbol"))
        # When invalid symbol been input
        if not stock:
            return apology("invalid symbol quoted", 400)
        # Update the price with a transformed dollar string
        stock["price"] = usd(stock["price"])

        # Redirect to quote with GET method to display the lookup result
        return render_template("quote.html", stock=stock)

    # Render the quote form
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Check if the user is already existed
        elif len(db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))) == 1:
            return apology("user already exist", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Ensure password and the confirmed password matching
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation have to match", 400)

        # User inputs are correct, register the user
        user_id = db.execute("INSERT INTO users (username, hash, cash) VALUES (?, ?, ?)",
                             request.form.get("username"),
                             generate_password_hash(request.form.get("password")),
                             0.0)

        # Auto logged in the user and remember which user has logged in
        session["user_id"] = user_id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        shares_selling = int(request.form.get("shares"))
        symbol_select = request.form.get("symbolSelect")
        # Ensure a valid symbol is selected
        if symbol_select == "Sell...":
            return apology("must select a symbol to sell", 400)
        # Ensure a valid number of shares entered
        elif not shares_selling:
            return apology("must provide #shares", 400)
        # Ensure enough shares the current user owned
        stock_owned = db.execute("SELECT SUM(shares) AS shares FROM user_stock WHERE user_id = ? AND stock_symbol= ? GROUP BY stock_symbol",
                                 session["user_id"],
                                 symbol_select)
        if stock_owned[0]["shares"] < shares_selling:
            return apology("you dont have enough shares", 400)

        # Start selling process
        current_stock = lookup(symbol_select)
        # 1. Add money to user's cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   shares_selling * current_stock["price"],
                   session["user_id"])
        # 2. Add a transaction into user_stock with a negative shares value
        db.execute("INSERT INTO user_stock (user_id, stock_symbol, price, shares) VALUES (?,?,?,?)",
                   session["user_id"],
                   current_stock["symbol"],
                   current_stock["price"],
                   -shares_selling)
        # Redirect user to home page
        return redirect("/")
    else:
        # Get all shares the current user have
        stock_owned = db.execute(
            "SELECT stock_symbol AS symbols, SUM(shares) AS shares FROM user_stock WHERE user_id = ? GROUP BY stock_symbol", session["user_id"])
        # Render a sell form
        return render_template("sell.html", stocks=stock_owned)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
