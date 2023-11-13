import json
from pathlib import Path
from time import time
import requests

from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from constants.url import API_URL, API_PORT
from maindash import app, master_token
from translate.translate import translate


custom_salary_map = html.Div(
    [
        dcc.Graph(
            id="custom_salary_map", figure={}
        )
    ]
)


@app.callback(
    Output("custom_salary_map", "children"),
    Input("custom_salary_map", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_salary_map", "figure"),
    Input("set_language", "value")
)
def create_sk_map_salary(lang):
    start = time()
    params = {"token": master_token}
    url = f"http://{API_URL}:{API_PORT}/salary_map"
    # url = f"{API_URL}:{API_PORT}/salary_map"
    # url = f"http://localhost:7777/salary_map"

    r = requests.get(url, params=params)
    end = time()
    print(f"pulling salaries for salary map: {end - start} sec...")

    res = json.loads(r.text)
    df = pd.DataFrame.from_dict(res)

    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "okresy.json"
    slovakia_districts = json.load(open(my_path, "r"))

    fig = px.choropleth(
        df,
        geojson=slovakia_districts,
        featureidkey='properties.TXT',
        locations="place",
        color='salary',
        labels=translate(lang),
    )

    fig.update_layout(
        # autosize=False,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
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
        y=-0.002,
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
    Output("title_graph_map_salary", "children"),
    Input("set_language", "value"),
)
def get_sentence(lang):
    sentence = "<br>Mapa nám vyjadruje, aká je priemerná mzda v regiónoch."
    sentence_final = translate(lang, sentence=sentence)

    return sentence_final


@app.callback(
    Output("title_map_salary", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Mzdy v regiónoch.'
    title_final = translate(lang, sentence=title)

    return title_final


custom_map_salary = [
    dbc.Spinner(
        children=[html.H1(id="title_map_salary", style={'textAlign': 'center'})],
        fullscreen=False
    ),
    html.P(id="title_graph_map_salary"),
    dcc.Loading(
        id="custom_salary_map",
        parent_className="loading_wrapper",
        children=[custom_salary_map],
        type="circle",
        fullscreen=False
    ),
]
