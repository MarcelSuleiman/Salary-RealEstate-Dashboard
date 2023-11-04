import requests
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

from constants.districts import RE_TYPES, DISTRICTS
from constants.url import API_URL, API_PORT
from maindash import app
from translate.translate import translate, translate_dataset

custom_re_rent_graph_condition_boxplot = dcc.Graph(
    id='custom_re_rent_graph_condition_boxplot', figure={}
)


@app.callback(
    Output("custom_re_rent_graph_condition_boxplot", "children"),
    Input("custom_re_rent_graph_condition_boxplot", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_re_rent_graph_condition_boxplot", "figure"),
    Input("city_dropdown", "value"),
    Input("utility_checkbox", "value"),
    Input("re_type_dropdown", "value"),
    Input("set_language", "value")
)
def create_custom_re_graph_condition_boxplot(city, utility, re_type, lang):

    if utility == [1]:
        utility = "1"
        params = {
            "re_type": re_type,
            "district": city,
            "utility": utility
        }

        url = f"http://{API_URL}:{API_PORT}/re_condition_boxplot"
        # url = f"{API_URL}:{API_PORT}/re_condition_boxplot"

        data = requests.get(url=url, params=params)
        final_df = pd.DataFrame.from_dict(data.json())

    else:
        utility = "0"
        params = {
            "re_type": re_type,
            "district": city,
            "utility": utility
        }

        url = f"http://{API_URL}:{API_PORT}/re_condition_boxplot_rent"
        # url = f"{API_URL}:{API_PORT}/re_condition_boxplot_rent"

        data = requests.get(url=url, params=params)
        final_df = pd.DataFrame.from_dict(data.json())

    which_df = "re_boxplot_by_condition_rent"
    final_df = translate_dataset(final_df, lang, which_df)

    figure = px.box(
        final_df,
        y="price",
        x="stav",
        color="stav",
        hover_data=["price", "stav"],
        labels=translate(lang),
        height=750,
    )

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

    # A way to be 100% sure of the order of the pictured boxplots, set them manually.
    if lang == "SK":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                'Pôvodný stav',
                'Čiastočná rekonštrukcia',
                'Kompletná rekonštrukcia',
                'Novostavba',
                'Vo výstavbe',
                'Developerský projekt',
            ]
        )
    elif lang == "EN":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                'Original state',
                'Partial reconstruction',
                'Complete reconstruction',
                'New construction',
                'Under construction',
                'Developer project',
            ]
        )
    elif lang == "FR":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                "État d'origine",
                'Reconstruction partielle',
                'Reconstruction complète',
                'Nouveau bâtiment',
                'En cours de construction',
                'Projet de développement',
            ]
        )

    return figure


@app.callback(
    Output("title_custom_re_rent_graph_condition_boxplot", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Ceny nájmov vybraných nehnuteľností podľa stavu.'
    title_final = translate(lang, sentence=title)

    return title_final


final_custom_re_rent_graph_condition_boxplot = [
    html.H1(id="title_custom_re_rent_graph_condition_boxplot", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id="city_dropdown",
        options=DISTRICTS,
        value="okres Bratislava",
        clearable=False,
    ),
    dbc.Checklist(
        options=[{"label": "Iba bez energií", "value": 1, 'disabled': True}],
        # value=[0],
        id="utility_checkbox",
        switch=True,
    ),
    dcc.Dropdown(
        id="re_type_dropdown",
        options=RE_TYPES,
        value="3 izbový byt",
        clearable=False,
    ),
    dcc.Loading(
        id="custom_re_rent_graph_condition_boxplot",
        children=custom_re_rent_graph_condition_boxplot,
        type="circle",
        fullscreen=False
    )
    # custom_re_rent_graph_condition_boxplot,
]
