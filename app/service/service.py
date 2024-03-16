from scipy.optimize import minimize
from sympy import *
from app.sources.sources import *


def find_portfolio(investment_names, years):
    daily_yields, quotes = get_daily_yields(investment_names, years)
    optimized_weight, mean_portfolio_optimized, stddev_portfolio_optimized = optimize(daily_yields)
    return daily_yields, quotes, optimized_weight, mean_portfolio_optimized, stddev_portfolio_optimized


def optimize(investments):
    weights, stddev_portfolio_function_x, mean_portfolio_function_x, \
        constraint_function_x, mean_per_stddev_function_x = prepare_expression_functions_and_symbols(investments)

    num_of_weights = len(investments.columns)

    # Defines that any weight is a value between 0 and 1
    weight_bounds = num_of_weights * ((0, 1),)

    # Defines that the optimization respects the constraint that the sum of the weights is equal to 1
    constraints = ({'type': 'eq', 'fun': lambda x: replace_weights(constraint_function_x, weights, x)})

    # Defines the initial value of the weights with a single one and the remaining zeros as example (1,0,...,0)
    initial_weight = np.concatenate((np.ones(1), np.zeros(num_of_weights - 1)))

    # Minimize the stddev and maximize the return (mean) at the same time
    optimized = minimize(lambda x: replace_weights(mean_per_stddev_function_x, weights, x),
                         initial_weight,
                         bounds=weight_bounds, constraints=constraints)

    optimized_weights = optimized.x
    mean_portfolio_optimized = replace_weights(mean_portfolio_function_x, weights, optimized_weights)
    stddev_portfolio_optimized = replace_weights(stddev_portfolio_function_x, weights, optimized_weights)

    return_portfolio = annualize_return(mean_portfolio_optimized)
    risk_portfolio = annualize_risk(stddev_portfolio_optimized)

    return to_percent(optimized_weights), to_percent(return_portfolio), to_percent(risk_portfolio)


def prepare_expression_functions_and_symbols(investments):
    num_symbols = len(investments.columns)
    weights = create_symbols(num_symbols)
    stddev_portfolio_function_x = stddev_portfolio_function(investments, weights)
    mean_portfolio_function_x = mean_portfolio_function(investments, weights)
    constraint_function_x = constraint_portfolio_function(weights)
    mean_per_stddev_function_x = -mean_portfolio_function_x / stddev_portfolio_function_x

    return weights, stddev_portfolio_function_x, \
        mean_portfolio_function_x, constraint_function_x, mean_per_stddev_function_x


def stddev_portfolio_function(investments, weights):
    cov_matrix = investments.cov().to_numpy()
    stddev_port = np.dot(weights, np.dot(cov_matrix, weights.T)) ** (1 / 2)
    return stddev_port


def mean_portfolio_function(investments, weights):
    means = investments.mean().to_numpy()
    return np.dot(weights, means)


def constraint_portfolio_function(weights):
    return 1 - weights.sum()


def create_symbols(n):
    weight_symbols = np.array([Symbol("w" + str(i + 1)) for i in range(n)])
    return weight_symbols


def replace_weights(function, weights, values):
    for i in range(len(weights)):
        function = function.subs({weights[i]: values[i]})
    return function


def to_percent(input):
    if isinstance(input, np.ndarray):
        return list(np.round(input * 100))
    return round(input * 100)


def annualize_return(daily_return):
    return (1 + daily_return) ** 252 - 1


def annualize_risk(daily_risk):
    return daily_risk * (252**(1/2))
