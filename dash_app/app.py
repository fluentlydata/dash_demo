from flask import Flask
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# load data
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

# build/start the server
server = Flask(__name__)
app = dash.Dash(name='Bootstrap_docker_app',
                server=server,
                csrf_protect=False)

# layout
colors = {
    'background': '#dddddd',
    'text': '#7FDBFF'
}

markdown_text = '''
### Dash and Markdown

Dash apps can be written in Markdown.
Dash uses the [CommonMark](http://commonmark.org/)
specification of Markdown.
Check out their [60 Second Markdown Tutorial](http://commonmark.org/help/)
if this is your first introduction to Markdown!
'''


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(style={'columnCount': 2}, children=[
        html.Label('Continents'),
        dcc.Dropdown(
            id="continent",
            options=[
                {'label': 'Asia', 'value': 'Asia'},
                {'label': 'Africa', 'value': 'Africa'},
                {'label': 'America', 'value': 'Americas'},
                {'label': 'Europe', 'value': 'Europe'},
                {'label': 'Oceania', 'value': 'Oceania'}
            ],
            value=['Africa', 'Europe'],
            multi=True
        ),
        dcc.Slider(
            id='year-slider',
            min=df['year'].min(),
            max=df['year'].max(),
            value=df['year'].min(),
            step=None,
            marks={str(year): str(year) for year in df['year'].unique()}
        )
    ]),
    dcc.Markdown(children=markdown_text),
    dcc.Graph(id='example-graph-2'),
    html.Table(id='table')
])


# Output: sets (or appends if non-existing) the property "figure"
@app.callback(
    Output(component_id='example-graph-2', component_property='figure'),
    [Input('year-slider', 'value'), Input(component_id='continent', component_property='value')]
)
def select_continent(selected_year, continents):
    filtered_df = df[df.year == selected_year]
    traces = []
    for i in continents:
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'type': 'log', 'title': 'GDP Per Capita'},
            yaxis={'title': 'Life Expectancy'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


@app.callback(
    Output(component_id='table', component_property='children'),
    [Input('year-slider', 'value'), Input(component_id='continent', component_property='value')]
)
def filter_table(year, continents):
    table = [html.Tr([html.Th(col) for col in df.columns])]
    table += [html.Tr([html.Td(df.iloc[i][col])
                       for col in df.columns])
              for i in range(min(len(df), 10000)) if df.iloc[i]['continent'] in continents and df.iloc[i]['year'] == year]
    return table


if __name__ == '__main__':
    app.run_server(debug=True)
