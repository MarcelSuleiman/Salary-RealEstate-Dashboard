import pandas as pd
import requests
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import plotly.express as px

from constants.districts import DISTRICTS, RE_TYPES
from constants.url import API_URL, API_PORT
from maindash import app, master_token

from translate.translate import translate

custom_re_graph_count_per_day = html.Div([dcc.Graph(
    id='custom_re_graph_count_per_day', figure={}
)])


@app.callback(
    Output("custom_re_graph_count_per_day", "children"),
    Input("custom_re_graph_count_per_day", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_re_graph_count_per_day", "figure"),
    Input("city_dropdown", "value"),
    Input("re_type_dropdown", "value"),
    Input("set_language", "value")
)
def create_custom_line_chart_count_re_per_day(city, re_type, lang):
    params = {
        "re_type": re_type,
        "district": city,
        "token": master_token
    }

    url = f"http://{API_URL}:{API_PORT}/re_count_per_day"
    # url = f"{API_URL}:{API_PORT}/re_count_per_day"

    data = requests.get(url=url, params=params)
    final_df = pd.DataFrame.from_dict(data.json())

    figure = px.line(
        final_df,
        x="the_date",
        y="count",
        line_shape="spline",
        # markers=True,
        height=700,
        # text="count",
        labels=translate(lang),
    )
    # figure.update_traces(textposition="bottom right")

    figure.add_annotation(
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.1,
        text=translate(lang, sentence="<b>© vytvorené Marcelom Suleimanom</b>"),
        showarrow=False,
        font=dict(
            family="Courier New",
            size=11,
            color='#101010',
        ),
    )

    return figure


@app.callback(
    Output("title_custom_re_graph_count_per_day", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Počet ponúk na predaj podľa typu nehnutelnosti a okresu.'
    title_final = translate(lang, sentence=title)

    return title_final


final_custom_re_graph_count_per_day = [
    html.H1(id="title_custom_re_graph_count_per_day", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="city_dropdown",
        options=DISTRICTS,
        value="okres Bratislava",
        clearable=False,
    ),
    dcc.Dropdown(
        id="re_type_dropdown",
        options=RE_TYPES,
        value="3 izbový byt",
        clearable=False,
        # multi=True,
    ),
    dcc.Loading(
        id="custom_re_graph_count_per_day",
        children=[custom_re_graph_count_per_day],
        type="circle",
        fullscreen=False
    ),
    # custom_re_graph_count_per_day,
]
