from __future__ import annotations

import random

from . import db
from .models import NewsEvent, PriceHistory, Stock


def apply_news_impact(sector: str, impact: float, volatility: float) -> None:
    stocks = Stock.query.filter_by(sector=sector).all()
    for stock in stocks:
        drift = random.uniform(-volatility, volatility)
        multiplier = max(0.2, 1 + impact + drift)
        stock.current_price = round(stock.current_price * multiplier, 2)
        db.session.add(PriceHistory(stock_id=stock.id, price=stock.current_price))
    db.session.commit()


def add_news(title: str, sector: str, impact: float, volatility: float) -> None:
    db.session.add(NewsEvent(title=title, sector=sector, impact=impact))
    db.session.commit()
    apply_news_impact(sector, impact, volatility)
