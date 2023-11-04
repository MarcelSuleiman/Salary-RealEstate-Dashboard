import json
import requests
import pandas as pd

from dash.dependencies import Input, Output
from dash import dcc
import plotly.express as px
from dash import html

from constants.districts import CITIES
from constants.url import API_URL, API_PORT
from maindash import app
from translate.translate import translate, translate_dataset

compare_gender_salary_base = dcc.Graph(
    id='compare_gender_salary_base', figure={}
)

compare_gender_and_age_salary = dcc.Graph(
    id='compare_gender_and_age_salary', figure={}
)


@app.callback(
    Output("compare_gender_salary_base", "figure"),
    Input("set_language", "value"),
    Input("salary_by_gender_position_dropdown", "value"),
    Input("salary_by_gender_city_dropdown", "value"),

)
def create_graph_test(lang, position_name=None, city_name=None):

    # bug? when I open new page, everything is ok, when I set some position, also fine,
    # but when I delete position, empty field is not empty like none, but [] empty list

    # patch
    if not position_name:
        position_name = None
    if not city_name:
        city_name = None

    if position_name is not None:
        position_name = ";".join(position_name)

    # unnecessary because I don't have multi selection on cities like positions
    # if city_name is not None:
    #     city_name = ";".join(city_name)

    url = f"http://{API_URL}:{API_PORT}/salary_by_gender"
    # url = f"{API_URL}:{API_PORT}/salary_by_gender"
    # url = f"http://localhost:7777/salary_by_gender"

    params = {}

    if position_name is not None:
        params["position"] = position_name

    if city_name is not None:
        params["place"] = city_name

    r = requests.get(url, params=params)
    res = json.loads(r.text)
    df = pd.DataFrame.from_dict(res)

    which_df = "salary_boxplot_by_gender"
    df = translate_dataset(df, lang, which_df)

    figure = px.box(
        df,
        y="salary",
        x="gender",
        color="gender",
        hover_data=["position", "position_place"],
        labels=translate(lang),
        height=750,
        color_discrete_map={  # replaces default color mapping by value
            "Man": "blue", "Woman": "red",
            "Hommes": "blue", "Femmes": "red",
            "Muži": "blue", "Ženy": "red"
        },
        # template="simple_white",
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

    if lang == "SK":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                'Muži',
                'Ženy',
            ]
        )
    elif lang == "EN":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                'Hommes',
                'Femmes',
            ]
        )
    elif lang == "FR":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                'Man',
                'Woman',
            ]
        )

    return figure


@app.callback(
    Output("compare_gender_and_age_salary", "figure"),
    Input("salary_by_gender_position_dropdown", "value"),
    Input("salary_by_gender_city_dropdown", "value"),
    Input("set_language", "value"),
)
def create_graph_test_2(position_name, city_name, lang):
    if position_name is not None:
        position_name = ";".join(position_name)

    url = f"http://{API_URL}:{API_PORT}/salary_by_gender"
    # url = f"{API_URL}:{API_PORT}/salary_by_gender"
    # url = f"http://localhost:7777/salary_by_gender"

    params = {}

    if position_name is not None:
        params["position"] = position_name

    if city_name is not None:
        params["place"] = city_name

    r = requests.get(url, params=params)
    res = json.loads(r.text)
    df = pd.DataFrame.from_dict(res)

    which_df = "salary_boxplot_by_age"
    df = translate_dataset(df, lang, which_df)

    figure = px.box(
        df,
        y="salary",
        x="age",
        color="gender",
        hover_data=["position", "position_place"],
        labels=translate(lang),
        height=750,
        color_discrete_map={  # replaces default color mapping by value
            "Man": "blue", "Woman": "red",
            "Hommes": "blue", "Femmes": "red",
            "Muži": "blue", "Ženy": "red"
        },
        # template="simple_white",
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

    if lang == "SK":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                '<24 rokov',
                '25-34 rokov',
                '35-44 rokov',
                '45-54 rokov',
                '55+ rokov',
            ]
        )
    elif lang == "EN":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                '<24 years old',
                '25-34 years old',
                '35-44 years old',
                '45-54 years old',
                '55+ years',
                'Not listed',
            ]
        )
    elif lang == "FR":
        figure.update_xaxes(
            categoryorder='array',
            categoryarray=[
                '<24 ans',
                '25-34 ans',
                '35-44 ans',
                '45-54 ans',
                '55+ ans',
                'Non listé',
            ]
        )

    return figure


@app.callback(
    Output("title_salary_by_gender", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Porovnanie celkových platov muži / ženy'
    title_final = translate(lang, sentence=title)

    return title_final


def get_position_names():

    url = f"http://{API_URL}:{API_PORT}/position_names"
    # url = f"{API_URL}:{API_PORT}/position_names"
    # url = f"http://localhost:7777/position_names"

    data = requests.get(url=url)
    df = pd.DataFrame.from_dict(data.json())

    return sorted(p for p in df["position"])


@app.callback(
    Output("get_tab_title_gender_only", "label"),
    Input("set_language", "value"),
)
def get_tab_title_gender_only(lang):
    sentence = 'Len na základe pohlavia'
    return translate(lang, sentence=sentence)


@app.callback(
    Output("get_tab_title_also_age_range", "label"),
    Input("set_language", "value"),
)
def get_tab_title_gender_only(lang):
    sentence = 'Aj s vekovým rozpätím'
    return translate(lang, sentence=sentence)


final_custom_salary_graph_by_gender = [
    html.H1(id="title_salary_by_gender", style={'textAlign': 'center'}),
    dcc.Dropdown(
        id='salary_by_gender_position_dropdown',
        options=pd.Series(get_position_names()).drop_duplicates().tolist(),
        multi=True,
        ),
    html.Frame(id="and_or", lang="EN", children="a / alebo"),
    dcc.Dropdown(
        id='salary_by_gender_city_dropdown',
        options=pd.Series(CITIES).drop_duplicates().tolist()
    ),
    dcc.Loading(
        id="salary_by_gender_loading",
        children=[
            dcc.Tabs(
                # style={
                #     'width': '50%',
                #     'font-size': '150%',
                #     'height': '50%'
                # },
                children=[
                    dcc.Tab(
                        id="get_tab_title_gender_only",
                        children=compare_gender_salary_base,
                        # style={'padding': '0', 'line-height': tab_height},
                        # selected_style={'padding': '0', 'line-height': tab_height}
                    ),
                    dcc.Tab(
                        id="get_tab_title_also_age_range",
                        children=compare_gender_and_age_salary,
                        # style={'padding': '0', 'line-height': tab_height},
                        # selected_style={'padding': '0', 'line-height': tab_height}
                    ),
                ],
            ),
        ],
        type="circle",
        fullscreen=False
    ),
]
