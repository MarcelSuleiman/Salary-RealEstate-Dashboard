import json
import time

import requests
import pandas as pd

from dash import html
from dash import dcc
import plotly.express as px

from constants.districts import CITIES
from constants.url import API_URL, API_PORT
from maindash import app, master_token
from dash.dependencies import Input, Output

from translate.translate import translate


custom_salary_graph_by_distribution = html.Div(
    [
        dcc.Graph(id='salary_distribution_per_employees', figure={})
    ],
)


custom_salary_graph_by_distribution_2 = html.Div(
    [
        dcc.Graph(id='salary_distribution_per_position', figure={})
    ]
)


# def memoize(func):
#     cache = {}
#     print(cache)
#
#     def wrapper(*args):
#         if args in cache:
#             print(cache[args])
#             return cache[args]
#         else:
#             result = func(*args)
#             cache[args] = result
#             return result
#
#     return wrapper


# @memoize
def get_data(place):
    url = f"http://{API_URL}:{API_PORT}/salary_distribution"
    # url = f"{API_URL}:{API_PORT}/salary_distribution"
    # url = f"http://localhost:7777/salary_distribution"

    params = {"token": master_token}

    if place is not None:
        params["place"] = place

    start = time.time()
    r = requests.get(url, params=params)
    end = time.time()
    print(f"pulling data for salaries distribition {end - start} sec...")

    res = json.loads(r.text)
    df_filtered = pd.DataFrame.from_dict(res)

    return df_filtered


@app.callback(
    Output("salary_distribution_per_employees", "figure"),
    [
        Input("salary_distribution_place_dropdown", "value"),
        Input("set_language", "value")
    ]
)
def get_distribution_salary(place, lang):
    df_filtered = get_data(place)

    if place is not None:
        df_filtered = df_filtered[df_filtered["place"] == place]

    sentence = "Histogram nám vyjadruje, koľko zamestnancov sa nachádza v danom platovom rozsahu."
    figure = px.histogram(
        df_filtered,
        x="salary",
        marginal="box",
        barmode='overlay',
        # template="simple_white",
        # cumulative=True,
        # histnorm="percent",  # ['', 'percent', 'probability', 'density']
        labels=translate(lang),
        title=translate(lang, sentence),
        nbins=100,
        height=650,
    )
    figure.add_annotation(
        xref='paper',
        yref='paper',
        x=1.04,
        y=-0.15,
        text=translate(lang, sentence="<b>© vytvorené Marcelom Suleimanom</b>"),
        showarrow=False,
        font=dict(
           family="Courier New",
           size=11,
           color='#101010',
        ),
    )

    figure.update_layout(
        bargap=0.05,
    )

    sentence = "Priemerný plat:"
    annotation_text = translate(lang, sentence)

    figure.add_vline(
        x=round(df_filtered["salary"].mean()),
        line_width=0.75, line_dash="dash",
        line_color='black',
        annotation=dict(text=f'{annotation_text} {str(round(df_filtered["salary"].mean()))} €'),
        annotation_position='bottom right',
    )

    sentence = "Mediánový plat:"
    annotation_text = translate(lang, sentence)

    figure.add_vline(
        x=round(df_filtered["salary"].median()),
        line_width=0.75, line_dash="dash",
        line_color='black',
        annotation=dict(text=f'{annotation_text} {str(round(df_filtered["salary"].median()))} €'),
        annotation_position='top left',
    )

    return figure


@app.callback(
    Output("salary_distribution_per_position", "figure"),
    [
        Input("salary_distribution_place_dropdown", "value"),
        Input("set_language", "value")
    ]
)
def get_distribution_salary_2(place, lang):
    df_filtered = get_data(place)

    if place is not None:
        df_filtered = df_filtered[df_filtered["place"] == place]

    df_id_grouped = df_filtered.groupby(by="position")["salary"]\
        .mean()\
        .apply(lambda x: round(x, 0))\
        .sort_values(ascending=True)

    counts = df_filtered['position'].value_counts(ascending=True)
    df_id_grouped_2 = pd.concat([df_id_grouped, counts], axis="columns", ignore_index=False)

    sentence = "Po vyradení outlierov na základe pracovnej pozície.<br> Histogram nám vyjadruje, koľko pracovných pozícií s mediánovou mzdou sa nachádza v danom platovom rozsahu."

    figure = px.histogram(
        df_id_grouped_2,
        x="salary",
        # y="count",
        marginal="box",
        barmode='overlay',
        labels=translate(lang),
        title=translate(lang, sentence),
        nbins=100,
        height=650
    )

    figure.add_annotation(
        xref='paper',
        yref='paper',
        x=1.04,
        y=-0.15,
        text=translate(lang, sentence="<b>© vytvorené Marcelom Suleimanom</b>"),
        showarrow=False,
        font=dict(
            family="Courier New",
            size=11,
            color='#101010',
        ),
    )

    figure.update_layout(bargap=0.05)
    return figure


@app.callback(
    Output("title_salary_graph_distribution", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Distribúcia mzdy podľa počtu obsadených miest / respondentov'
    title_final = translate(lang, sentence=title)

    return title_final


@app.callback(
    Output("get_tab_title_per_employee", "label"),
    Input("set_language", "value"),
)
def get_tab_title_gender_only(lang):
    sentence = 'Podľa zamestnancov'
    return translate(lang, sentence=sentence)


@app.callback(
    Output("get_tab_title_per_position", "label"),
    Input("set_language", "value"),
)
def get_tab_title_gender_only(lang):
    sentence = 'Podľa pozízií'
    return translate(lang, sentence=sentence)


final_custom_salary_graph_distribution = [
    html.H1(id="title_salary_graph_distribution", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='salary_distribution_place_dropdown',
        options=pd.Series(CITIES).drop_duplicates().tolist()
    ),
    dcc.Loading(
        id="salary_distribution_loading",
        children=[
            dcc.Tabs(
                children=[
                    dcc.Tab(
                        id="get_tab_title_per_employee",
                        children=custom_salary_graph_by_distribution
                    ),
                    dcc.Tab(
                        id="get_tab_title_per_position",
                        children=custom_salary_graph_by_distribution_2
                    )
                ]
            )
        ],
        type="circle",
        fullscreen=False
    ),
]
