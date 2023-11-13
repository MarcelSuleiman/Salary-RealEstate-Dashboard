import json
import time

import requests
import pandas as pd

from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import plotly.express as px

from constants.districts import CITIES
from constants.url import API_URL, API_PORT
from maindash import app, master_token

from translate.translate import translate, translate_salary
from util.render_graph_height import render_graph_height

custom_salary_graph_by_industry = html.Div([dcc.Graph(
    id='salary_by_industry', figure={}
)])


@app.callback(
    Output("salary_by_industry", "children"),
    Input("salary_by_industry", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("salary_by_industry", "figure"),
    Input("industry_salary_dropdown", "value"),
    Input("outliers_checkbox_2", "value"),
    Input("industry_place_dropdown", "value"),
    Input("set_language", "value")
)
def create_custom_bar_per_industry(calcul_type, outliers_checkbox, place, lang):
    url = f"http://{API_URL}:{API_PORT}/salary_by_industry"
    # url = f"{API_URL}:{API_PORT}/salary_by_industry"

    params = {"token": master_token}

    if outliers_checkbox == [0]:
        params["outliers"] = 0

    if place is not None:
        params["place"] = place

    if calcul_type == "mean":
        params["calcul_type"] = calcul_type
    else:
        params["calcul_type"] = "median"

    start = time.time()
    r = requests.get(url, params=params)
    end = time.time()
    print(f"pulling data for salary by industry {end-start} sec.")

    res = json.loads(r.text)
    df_id_grouped = pd.DataFrame.from_dict(res)

    df_id_grouped = df_id_grouped.reset_index(drop=True)
    df_id_grouped.rename(columns={"position_place": "position_industry"}, inplace=True)
    df_id_grouped.rename(columns={"count": "count_of_respondents"}, inplace=True)

    rendered_height = render_graph_height(df_id_grouped, by="count_of_respondents")

    # if lang == "EN":
    #     lang_deepl = "EN-GB"
    # else:
    #     lang_deepl = lang

    which = "position_industry"
    page = "industry"
    df_id_grouped = translate_salary(df_id_grouped, lang, which, page)

    figure = px.bar(
        df_id_grouped,
        barmode='group',
        x='salary',
        y='position_industry',
        text_auto=True,
        hover_data=["count_of_respondents"],
        labels=translate(lang),
        height=rendered_height
    )

    figure.add_annotation(
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.05,
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
    Output("salary_per_industry_header", "children"),
    Input("set_language", "value"),
)
def get_title(lang):

    title = 'Platy podľa odvetvia v SR'
    title_final = translate(lang, sentence=title)

    return title_final


@app.callback(
    Output("industry_salary_dropdown", "options"),
    Input("set_language", "value"),
)
def get_dropdown_option(lang):
    sentence = "Medián"
    median_label = translate(lang, sentence=sentence)
    sentence = "Priemer"
    mean_label = translate(lang, sentence=sentence)

    options = [
        {"label": f"{median_label}", "value": "median"},
        {"label": f"{mean_label}", "value": "mean"},
    ]

    return options


final_custom_salary_graph_by_industry = [
    html.H1(id="salary_per_industry_header", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="industry_salary_dropdown",
        options=[],
        value="mean",
        clearable=False,
    ),
    html.Div(
        [
            dbc.Checklist(
                options=[],
                id="outliers_checkbox_2",
                switch=True,
            )
        ]
    ),
    dcc.Dropdown(
        id="industry_place_dropdown", options=CITIES,
    ),
    dcc.Loading(
        id="salary_by_industry",
        children=custom_salary_graph_by_industry,
        type="circle",
    ),
]
