import datetime

import numpy as np
import yfinance as yf
from dateutil.relativedelta import relativedelta


def get_daily_yields(investment_names, years):
    initial_date, final_date = range_dates(years=years)
    quotes = yf.download(investment_names, start=initial_date, end=final_date, progress=False)['Close'].dropna()

    quotes_past_dislocated = quotes.drop(quotes.index[-1])
    quotes_present_dislocated = quotes.copy().drop(quotes.index[0])

    quotes_present_dislocated.index = quotes_past_dislocated.index

    daily_yields = np.log(quotes_present_dislocated / quotes_past_dislocated)

    quotes.index = quotes.index.strftime("%d/%m/%Y")
    daily_yields.index = daily_yields.index.strftime("%d/%m/%Y")

    return daily_yields, quotes


def range_dates(years):
    final_date = datetime.datetime.today().strftime("%Y-%m-%d")
    initial_date = (datetime.datetime.today() - relativedelta(years=years)).strftime("%Y-%m-%d")
    return initial_date, final_date
