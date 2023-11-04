from pathlib import Path

import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from constants.url import API_URL, API_PORT
from maindash import app

import pandas as pd
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
from constants.districts import RE_TYPES, DISTRICTS
from translate.translate import translate

custom_re_graph_price_per_day = dcc.Graph(
    id='custom_re_graph_price_per_day', figure={}
)


@app.callback(
    Output("custom_re_graph_price_per_day", "children"),
    Input("custom_re_graph_price_per_day", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_re_graph_price_per_day", "figure"),
    Input("city_dropdown", "value"),
    Input("re_type_dropdown", "value"),
    Input("set_language", "value")
)
def create_custom_re_graph_price_per_day(city, re_type, lang):

    params = {
        "re_type": re_type,
        "district": city
    }

    url = f"http://{API_URL}:{API_PORT}/re_by_price_per_day"
    # url = f"{API_URL}:{API_PORT}/re_by_price_per_day"

    data = requests.get(url=url, params=params)
    final_df = pd.DataFrame.from_dict(data.json())

    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    name = "Priemerná cena [v €]"
    if lang == "SK":
        name = "Priemerná cena [v €]"
    elif lang == "EN":
        name = "Average price [in €]"
    elif lang == "FR":
        name = "Prix moyen [en €]"

    subfig.add_trace(go.Scatter(
        # final_df,
        x=final_df.the_date,
        y=final_df.average_price,
        name=name,
        line={'shape': 'spline', 'smoothing': 1}
    ))

    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "uvery.csv"

    df = pd.read_csv(my_path, delimiter=";")
    print(df.head())

    final_df = df.loc[df['loan_type'].isin(["H"])]
    final_df = final_df.groupby(by="The_date")["interest"].mean().apply(lambda x: round(x, 2)).reset_index()

    name = "Priemerná úroková sadzba [v %]"
    if lang == "SK":
        name = 'Priemerná cena [v €]'
    elif lang == "EN":
        name = "Average interest rate [in %]"
    elif lang == "FR":
        name = "Taux d'intérêt moyen [en %]"

    subfig.add_trace(
        go.Scatter(
            # final_df,
            x=final_df.The_date,
            y=final_df.interest,
            name=name,
            line={'shape': 'spline', 'smoothing': 1}
            # color='bank_name',
        ),
        secondary_y=True,
    )

    subfig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=0.95
    ))

    subfig.update_layout(height=750)  # title_text="Custom title can be inside update_layout"

    subfig.add_annotation(
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

    return subfig


@app.callback(
    Output("tite_custom_re_graph_price_per_day", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Vývoj ceny nehnuteľností podľa druhu.'
    title_final = translate(lang, sentence=title)

    return title_final


final_custom_re_graph_price_per_day = [
    html.H1(id="tite_custom_re_graph_price_per_day", style={'textAlign': 'center'}),
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
    ),
    dcc.Loading(
        id="custom_re_graph_price_per_day",
        children=custom_re_graph_price_per_day,
        type="circle",
        fullscreen=False,
    ),
]
