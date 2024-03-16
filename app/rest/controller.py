from app.service.service import *
from app.validation.validator import *


def get_portfolio(assets, years=1):
    if isValid(assets):
        return find_portfolio(assets, years)
    return None
