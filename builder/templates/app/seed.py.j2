from __future__ import annotations

from werkzeug.security import generate_password_hash

from . import db
from .models import PriceHistory, Stock, User


def seed_market(config: dict) -> None:
    if Stock.query.count() == 0:
        for sector in config["sectors"]:
            stock = Stock(
                symbol=sector["symbol"],
                name=f"{sector['name']} Index",
                sector=sector["name"],
                current_price=sector["base_price"],
            )
            db.session.add(stock)
            db.session.flush()
            db.session.add(PriceHistory(stock_id=stock.id, price=stock.current_price))

    if not User.query.filter_by(username=config["admin"]["username"]).first():
        db.session.add(
            User(
                username=config["admin"]["username"],
                password_hash=generate_password_hash(config["admin"]["password"]),
                cash=config["starting_cash"],
            )
        )

    db.session.commit()
