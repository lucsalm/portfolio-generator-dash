from dash import *
import dash_bootstrap_components as dbc
from app.resources.options import years_options_all, assets_options_all
from app.resources.graphs import graph1, graph2, graph3

html_dash = html.Div([
    dbc.Container(children=[
        dcc.Location(id='url', refresh=False),
        html.H1("Portfolio Generator", className="text-center display-3 mb-2 mt-2"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col([
                    dbc.Label("Select 1st asset:"),
                    dbc.Select(
                        placeholder="Select 1st asset...",
                        id='asset-1',
                        options=assets_options_all,
                        value=None,
                    )
                ]

                ),
                dbc.Col([
                    dbc.Label("Select 2nd asset:"),
                    dbc.Select(
                        placeholder="Select 2nd asset...",
                        id='asset-2',
                        options=assets_options_all,
                        value=None,
                    )
                ]

                ),
                dbc.Col(
                    [
                        dbc.Label("Select 3rd asset:"),
                        dbc.Select(
                            placeholder="Select 3rd asset...",
                            id='asset-3',
                            options=assets_options_all,
                            value=None,
                        )
                    ]

                ),
            ], className="mb-3"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Select years:"),
                        dbc.Select(placeholder="Select years...",
                                   id='years',
                                   options=years_options_all,
                                   value=None,
                                   )
                    ]
                    ,
                    width="md-4",
                )],
            className="mb-3"
        ),
        dbc.Row(
            dbc.Col(
                dbc.Button("Generate", color="light", className="mr-1", id="submit-button", n_clicks=0),
                width="1", style={"width": "max-content"}
            )
            , className="mb-3"),
        html.Hr(),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=graph1, id='graph1'),
                width="md-4"
            ),
            dbc.Col(
                dcc.Graph(figure=graph2, id='graph2'),
                width="md-4"
            ),
            dbc.Col(
                dcc.Graph(figure=graph3, id='graph3'),
                width="md-4"
            )
        ]),

        dbc.Row([
            html.Div(id='mean_portfolio_optimized')
        ]),
        dbc.Row([
            html.Div(id='stddev_portfolio_optimized')
        ]),
        html.Hr()
    ], fluid=True)
])
