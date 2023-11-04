import json
from pathlib import Path
from time import time

import requests

from constants.districts import RE_TYPES
from constants.url import API_URL, API_PORT
from maindash import app

from dash import html
from dash import dcc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

from translate.translate import translate

custom_re_map_salary_price_ratio = html.Div([dcc.Graph(
    id="custom_re_map_salary_price_ratio", figure={}
)])


@app.callback(
    Output("custom_re_map_salary_price_ratio", "children"),
    Input("custom_re_map_salary_price_ratio", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_re_map_salary_price_ratio", "figure"),
    Input("re_type_dropdown", "value"),
    Input("set_language", "value")
)
def create_a(re_type, lang):

    params = {
        "re_type": re_type
    }

    start = time()
    url = f"http://{API_URL}:{API_PORT}/price_salary_ratio"
    # url = f"{API_URL}:{API_PORT}/price_salary_ratio"
    # url = f"http://localhost:7777/price_salary_ratio"

    r = requests.get(url, params=params)
    end = time()
    print(f"pulling salaries for salary map: {end - start} sec...")

    res = json.loads(r.text)
    data_test = pd.DataFrame.from_dict(res)

    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "okresy.json"
    slovakia_districts = json.load(open(my_path, "r"))

    sentence = "Mapa nám vyjadruje, koľko priemerných ročných platov v danom regióne potrebuješ, aby si si mohol kúpiť priemernú nehnuteľnosť daného typu."

    fig = px.choropleth(
        data_test,
        geojson=slovakia_districts,
        featureidkey='properties.TXT',
        locations="place",
        color='no_years',
        labels=translate(lang),
        # color_continuous_scale="Viridis",
        title=translate(lang, sentence)
    )

    fig.update_layout(
        # autosize=False,
        margin=dict(
            l=0,
            r=0,
            b=10,
            t=50,
            pad=0,
            autoexpand=True
        ),
        # margin=dict(l=60, r=60, t=50, b=50),
        # width=800,
        height=800,
    )

    fig.add_annotation(
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.007,
        text=translate(lang, sentence="<b>© vytvorené Marcelom Suleimanom</b>"),
        showarrow=False,
        font=dict(
            family="Courier New",
            size=11,
            color='#101010',
        ),
    )

    fig.update_geos(fitbounds="locations", visible=False)
    return fig


@app.callback(
    Output("title_re_map_salary_price_ratio", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Pomer mzdy a ceny bývania podľa okresu.'
    title_final = translate(lang, sentence=title)

    return title_final


custom_re_map_salary_price_ratio = html.Div([
    html.H1(id="title_re_map_salary_price_ratio", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="re_type_dropdown",
        options=RE_TYPES,
        value="3 izbový byt",
        clearable=False,
    ),
    dcc.Loading(
        id="custom_re_map_salary_price_ratio",
        parent_className="loading_wrapper",
        children=[custom_re_map_salary_price_ratio],
        type="circle",
        fullscreen=False
    ),
])
