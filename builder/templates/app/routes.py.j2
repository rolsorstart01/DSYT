from __future__ import annotations

from collections import defaultdict

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .market_engine import add_news
from .models import Holding, PriceHistory, Stock, Trade, User


def _portfolio_value(user_id: int) -> float:
    holdings = Holding.query.filter_by(user_id=user_id).all()
    total = 0.0
    for h in holdings:
        stock = Stock.query.get(h.stock_id)
        total += h.quantity * stock.current_price
    return total


def register_routes(app):
    @app.route("/")
    def index():
        return render_template("index.html", config=app.config["APP_CONFIG"])

    @app.route("/auth", methods=["GET", "POST"])
    def auth():
        config = app.config["APP_CONFIG"]
        if request.method == "POST":
            action = request.form["action"]
            username = request.form["username"]
            password = request.form["password"]
            if action == "register":
                if User.query.filter_by(username=username).first():
                    flash("Username already exists")
                else:
                    user = User(username=username, password_hash=generate_password_hash(password), cash=config["starting_cash"])
                    db.session.add(user)
                    db.session.commit()
                    login_user(user)
                    return redirect(url_for("market"))
            else:
                user = User.query.filter_by(username=username).first()
                if user and check_password_hash(user.password_hash, password):
                    login_user(user)
                    return redirect(url_for("market"))
                flash("Invalid credentials")
        return render_template("auth.html", config=config)

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    @app.route("/market", methods=["GET", "POST"])
    @login_required
    def market():
        config = app.config["APP_CONFIG"]
        if request.method == "POST":
            stock_id = int(request.form["stock_id"])
            qty = int(request.form["quantity"])
            side = request.form["side"]
            stock = Stock.query.get(stock_id)
            fee = config["rules"]["broker_fee_percent"] / 100
            cost = qty * stock.current_price * (1 + fee)
            if side == "BUY" and current_user.cash >= cost:
                current_user.cash -= cost
                holding = Holding.query.filter_by(user_id=current_user.id, stock_id=stock.id).first()
                if not holding:
                    holding = Holding(user_id=current_user.id, stock_id=stock.id, quantity=0)
                    db.session.add(holding)
                holding.quantity += qty
                db.session.add(Trade(user_id=current_user.id, stock_id=stock.id, side="BUY", quantity=qty, price=stock.current_price))
                db.session.commit()
            elif side == "SELL":
                holding = Holding.query.filter_by(user_id=current_user.id, stock_id=stock.id).first()
                if holding and holding.quantity >= qty:
                    holding.quantity -= qty
                    current_user.cash += qty * stock.current_price * (1 - fee)
                    db.session.add(Trade(user_id=current_user.id, stock_id=stock.id, side="SELL", quantity=qty, price=stock.current_price))
                    db.session.commit()
        stocks = Stock.query.order_by(Stock.symbol).all()
        chart_data = defaultdict(list)
        for stock in stocks:
            points = PriceHistory.query.filter_by(stock_id=stock.id).order_by(PriceHistory.created_at.desc()).limit(20).all()
            chart_data[stock.symbol] = [p.price for p in reversed(points)]
        return render_template("market.html", config=config, stocks=stocks, chart_data=dict(chart_data))

    @app.route("/portfolio")
    @login_required
    def portfolio():
        holdings = Holding.query.filter_by(user_id=current_user.id).all()
        rows = []
        for h in holdings:
            stock = Stock.query.get(h.stock_id)
            rows.append({"symbol": stock.symbol, "qty": h.quantity, "price": stock.current_price, "value": h.quantity * stock.current_price})
        total_value = sum(r["value"] for r in rows)
        net_worth = current_user.cash + total_value
        return render_template("portfolio.html", rows=rows, net_worth=net_worth, cash=current_user.cash)

    @app.route("/leaderboard")
    @login_required
    def leaderboard():
        users = User.query.all()
        board = []
        for user in users:
            board.append({"username": user.username, "net_worth": round(user.cash + _portfolio_value(user.id), 2)})
        board.sort(key=lambda x: x["net_worth"], reverse=True)
        return render_template("leaderboard.html", board=board)

    @app.route("/admin", methods=["GET", "POST"])
    @login_required
    def admin():
        config = app.config["APP_CONFIG"]
        if current_user.username != config["admin"]["username"]:
            flash("Admin only")
            return redirect(url_for("market"))
        if request.method == "POST":
            title = request.form["title"]
            sector = request.form["sector"]
            impact = float(request.form["impact"])
            add_news(title, sector, impact, config["volatility"])
            flash("News applied and prices updated")
        return render_template("admin.html", config=config)
