import json
import requests
from time import time
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

custom_salary_graph_by_position = dcc.Graph(
    id='custom_salary_graph_by_position', figure={}
)


@app.callback(
    Output("custom_salary_graph_by_position", "children"),
    Input("custom_salary_graph_by_position", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_salary_graph_by_position", "figure"),
    Input("position_salary_dropdown", "value"),
    Input("outliers_checkbox", "value"),
    Input("position_place_dropdown", "value"),
    Input("set_language", "value"),
)
def create_custom_bar_per_position(calcul_type, outliers_checkbox, place, lang):

    start = time()
    url = f"http://{API_URL}:{API_PORT}/salary_by_position"
    # url = f"http://localhost:{API_PORT}/salary_by_position"

    params = {"token": master_token}

    if outliers_checkbox == [0]:
        params["outliers"] = 0

    if place is not None:
        params["place"] = place

    if calcul_type == "priemer":
        params["calcul_type"] = calcul_type
    else:
        params["calcul_type"] = "median"

    r = requests.get(url, params=params)
    end = time()
    print(f"pulling data for salaries by positions {end - start} sec...")

    res = json.loads(r.text)
    df_id_grouped = pd.DataFrame.from_dict(res["df_data"])
    df_id_grouped = df_id_grouped.reset_index()
    df_id_grouped.rename(columns={"index": "position"}, inplace=True)

    rendered_height = render_graph_height(df_id_grouped, by="position")
    salary_value = res["salary_value"]

    # if place == "Medzilaborce":

    if lang == "EN":
        lang_deepl = "EN-GB"
    else:
        lang_deepl = lang

    # which = "positions"
    # df_id_grouped = translate_positions(df_id_grouped, lang_deepl)

    which = "position"
    page = "positions"
    df_id_grouped = translate_salary(df_id_grouped, lang_deepl, which, page)

    figure = px.bar(
        df_id_grouped,
        barmode='group',
        x='salary',
        y='position',
        text_auto=True,
        hover_data=["count_of_respondents"],
        labels=translate(lang),
        height=rendered_height
    )

    figure.add_annotation(
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.003,
        text=translate(lang, sentence="<b>© vytvorené Marcelom Suleimanom</b>"),
        showarrow=False,
        font=dict(
            family="Courier New",
            size=11,
            color='#101010',
        ),
    )

    if calcul_type == "median":
        salary_type = "Mediánový plat:"
    else:
        salary_type = "Priemerný plat:"

    annotation_text = translate(lang, salary_type)
    figure.add_vline(
        x=round(salary_value),
        line_width=0.75, line_dash="dash",
        line_color='black',
        annotation=dict(text=f'{annotation_text} {salary_value} €'),
        annotation_position='bottom right',
    )

    return figure


# html.Div(
#     [
#         html.Label("spodní outlieri"),
#         # https://mathematikos.github.io/outliers
#         dcc.Slider(
#             min=0.00, max=0.25, value=0, id="low_outliers", step=0.05, tooltip={"placement": "bottom"}
#         ),
#         dcc.Slider(
#             min=0.75, max=1, value=1, id="high_outliers",step=0.05, tooltip={"placement": "bottom"}
#         ),
#         html.Label("horní outlieri"),
#
#     ],
#     style={"display": "grid", "grid-template-columns": "10% 40% 40% 10%"}
# ),



@app.callback(
    Output("qqq", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Platy na pozíciach v SR'
    title_final = translate(lang, sentence=title)

    return title_final


@app.callback(
    Output("position_salary_dropdown", "options"),
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


final_custom_salary_graph_by_position = [
    html.H1(id="qqq", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="position_salary_dropdown",
        options=[],
        value="mean",
        clearable=False,
    ),
    html.Div(
        [
            dbc.Checklist(
                options=[],
                id="outliers_checkbox",
                switch=True,
            )
        ]
    ),
    dcc.Dropdown(
        id="position_place_dropdown", options=CITIES,
    ),
    dcc.Loading(
        id="custom_salary_graph_by_position",
        children=[custom_salary_graph_by_position],
        type="circle",
        fullscreen=False
    ),
]
