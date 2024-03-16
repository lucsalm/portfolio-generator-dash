import dash_bootstrap_components as dbc
import pandas as pd
from dash import *

from app.rest.controller import get_portfolio
from app.resources.graphs import graph1, graph2, graph3
from app.resources.html import html_dash
from app.resources.options import assets_options_all

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html_dash

n_clicks_done = 0
# "#25c964", "#e6d74b", "#de4e86",
colors = ["#25c964", "#de4e86", "#e6d74b"]
lock = False


@callback(
    [Output('asset-1', 'style'), Output('asset-2', 'style'), Output('asset-3', 'style'), Output('years', 'style')],
    [Input('submit-button', 'n_clicks')],
    [State('asset-1', 'value'), State('asset-2', 'value'), State('asset-3', 'value'), State('years', 'value')],
    prevent_initial_call=True
)
def define_style(n_clicks, *assets):
    styles = [{}] * len(assets)
    global n_clicks_done
    if n_clicks > n_clicks_done:
        n_clicks_done = n_clicks
        invalid_bord, valid_board = {'border-color': '#f06f6f'}, {}
        styles = [invalid_bord if asset is None else valid_board for asset in assets]
        global lock
        lock = invalid_bord in styles
    return styles


@callback(
    [Output('graph1', 'figure'), Output('graph2', 'figure'), Output('graph3', 'figure'),
     Output('mean_portfolio_optimized', 'children'), Output('stddev_portfolio_optimized', 'children')],
    [Input('submit-button', 'n_clicks')],
    [State('years', 'value')],
    [Input('url', 'pathname')],
    [State('asset-1', 'value'), State('asset-2', 'value'), State('asset-3', 'value')],
    prevent_initial_call=True
)
def update_graph(n_clicks, years, pathname, *assets):
    global n_clicks_done
    if n_clicks >= n_clicks_done and lock is False and years is not None:
        assets = filter_assets(assets)
        n_clicks_done = n_clicks
        return mount_portfolio(assets, years)
    elif pathname == '/':
        graph1.data, graph2.data, graph3.data = [], [], []
    return graph1, graph2, graph3, "", ""


@callback([Output('asset-1', 'options'), Output('asset-2', 'options'), Output('asset-3', 'options')],
          [Input('asset-1', 'value'), Input('asset-2', 'value'), Input('asset-3', 'value')],
          prevent_initial_call=True
          )
def disable_used(*assets):
    assets_able = list(filter(lambda asset: asset not in assets, assets_options_all))
    assets_able_list = [assets_able.copy() for _ in range(len(assets))]
    filtered_assets = filter_assets(assets)
    lists = []
    for i, asset in enumerate(assets):
        if asset is None:
            lists += sorted([assets_able_list[i] + filtered_assets])
        elif asset not in assets_able_list[i]:
            lists += sorted([assets_able_list[i] + [asset]])
    return *lists,


def mount_portfolio(assets, years):
    assets_list = map_assets(assets)
    daily_yields, quotes, optimized_weight, \
        mean_portfolio_optimized, stddev_portfolio_optimized = get_portfolio(assets_list, float(years))

    graph1.data = []
    for i, col in enumerate(quotes.columns):
        graph1.add_scatter(x=quotes.index, y=quotes[col], mode='lines', name=col, line_color=colors[i])

    graph2.data = []
    for i, col in enumerate(daily_yields.columns):
        graph2.add_scatter(x=daily_yields.index, y=daily_yields[col], mode='lines', name=col, line_color=colors[i])

    weights = pd.DataFrame(data={
        'assets': quotes.columns,
        'weights': optimized_weight
    })
    graph3.data = []
    graph3.add_bar(x=weights['assets'], y=weights['weights'], marker_color=colors)
    mean_portfolio_optimized_str = f"Expected Return: {mean_portfolio_optimized:.2f}%"
    stddev_portfolio_optimized_str = f"Expected Risk: {stddev_portfolio_optimized:.2f}%"

    return graph1, graph2, graph3, mean_portfolio_optimized_str, stddev_portfolio_optimized_str


def filter_assets(assets):
    return list(filter(lambda item: item is not None, assets))


def map_assets(assets):
    return list(map(lambda item: item.split(' ')[0], assets))


if __name__ == '__main__':
    # Use this for build:
    app.run(host='0.0.0.0', debug=True)
    # Use this for local:
    # app.run(debug=True)
