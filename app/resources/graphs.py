import plotly.express as px
from dash_bootstrap_templates import load_figure_template

load_figure_template(["minty_dark"])

graph1 = px.line(template="minty_dark", title='Asset Price', labels={'x': 'Date', 'y': 'Price'})
graph2 = px.line(template="minty_dark", title='Daily Yield', labels={'x': 'Date', 'y': 'Yield'})
graph3 = px.bar(template="minty_dark", title='Portfolio', labels={'x': 'Asset', 'y': 'Weight'})
graph3.update_layout(yaxis_range=[0, 100])
