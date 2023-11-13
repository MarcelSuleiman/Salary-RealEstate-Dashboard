import requests
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd

from constants.districts import RE_TYPES, DISTRICTS
from constants.url import API_URL, API_PORT
from maindash import app, master_token
from translate.translate import translate, translate_dataset

custom_re_graph_condition_boxplot = dcc.Graph(
    id='custom_re_graph_condition_boxplot', figure={}
)


@app.callback(
    Output("custom_re_graph_condition_boxplot", "children"),
    Input("custom_re_graph_condition_boxplot", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_re_graph_condition_boxplot", "figure"),
    [
        Input("city_dropdown", "value"),
        Input("re_type_dropdown", "value"),
        Input("set_language", "value")
    ]
)
def create_custom_re_graph_condition_boxplot(city, re_type, lang):
    params = {
        "re_type": re_type,
        "district": city,
        "token": master_token
    }

    url = f"http://{API_URL}:{API_PORT}/re_by_condition_boxplot"
    # url = f"http://localhost:7777/re_by_condition_boxplot"
    data = requests.get(url=url, params=params)

    final_df = pd.DataFrame.from_dict(data.json())

    which_df = "re_boxplot_by_condition"
    final_df = translate_dataset(final_df, lang, which_df)

    figure = px.box(
        final_df,
        y="price",
        x="parameter_info.stav",
        color="parameter_info.stav",
        hover_data=["price", "parameter_info.stav"],
        labels=translate(lang),
        height=750,
    )

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
    Output("title_re_graph_condition_boxplot", "children"),
    Input("set_language", "value"),
)
def get_title(lang):

    title = 'Ceny vybraných nehnuteľností podľa stavu.'
    title_final = translate(lang, sentence=title)
    return title_final


final_custom_re_graph_condition_boxplot = [
    html.H1(id="title_re_graph_condition_boxplot", style={'textAlign': 'center'}),
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
        id="custom_re_graph_condition_boxplot",
        children=[custom_re_graph_condition_boxplot],
        type="circle",
        fullscreen=False
    )
    # custom_re_graph_condition_boxplot,
]
