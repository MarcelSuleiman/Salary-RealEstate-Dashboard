from pathlib import Path

import requests
from plotly.subplots import make_subplots
import plotly.graph_objects as go

from constants.url import API_URL, API_PORT
from maindash import app, master_token

import pandas as pd
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
from constants.districts import RE_TYPES, DISTRICTS
from translate.translate import translate

custom_re_graph_price_per_day = dcc.Graph(
    id='custom_population_graph', figure={}
)


@app.callback(
    Output("custom_population_graph", "children"),
    Input("custom_population_graph", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_population_graph", "figure"),
    Input("city_dropdown", "value"),
    Input("re_type_dropdown", "value"),
    Input("set_language", "value")
)
def create_custom_population_graph(city, re_type, lang):

    city_population = city.replace("okres ", "")

    print(city, type(city))
    print(city_population, type(city_population))

    params = {
        "re_type": re_type,
        "district": city,
        "token": master_token
    }

    url = f"http://{API_URL}:{API_PORT}/re_by_price_per_day"
    # url = f"{API_URL}:{API_PORT}/re_by_price_per_day"

    # data = requests.get(url=url, params=params)
    # final_df = pd.DataFrame.from_dict(data.json())

    subfig = make_subplots(specs=[[{"secondary_y": True}]])

    name = "Priemerná cena [v €]"
    if lang == "SK":
        name = "Priemerná cena [v €]"
    elif lang == "EN":
        name = "Average price [in €]"
    elif lang == "FR":
        name = "Prix moyen [en €]"



    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "uvery.csv"
    df = pd.read_csv(my_path, delimiter=";")
    print(df.head())

    root_folder = Path(__file__).parents[1]
    my_path = root_folder / "datasets/lau1-population-iz.csv"
    df_population = pd.read_csv(my_path, delimiter=",")

    for column_headers in df_population.columns:
        if "-" in column_headers:
            df_population.rename(columns={column_headers: column_headers.replace("-", "_")}, inplace=True)


    # df_population.rename(columns={"Y00-04": "Y00_04"}, inplace=True)
    # df_population.rename(columns={"Y25-29": "Y25_29"}, inplace=True)
    # df_population.rename(columns={"Y80-84": "Y80_84"}, inplace=True)

    df_population = df_population.sort_values("period")

    df_population = df_population.loc[df_population['name'].isin([city_population])]
    # df_population = df_population.loc[df_population['name'].isin(["Bratislava II"])]
    # df_population = df_population.loc[df_population['gender'].isin(["total"])]

    df_population['period'] = pd.to_datetime(df_population['period'], format='%Y')

    print(df_population.head(25))

    final_df = df.loc[df['loan_type'].isin(["H"])]
    final_df = final_df.groupby(by="The_date")["interest"].mean().apply(lambda x: round(x, 2)).reset_index()

    name = "Priemerná úroková sadzba [v %]"
    if lang == "SK":
        name = 'Priemerná cena [v €]'
    elif lang == "EN":
        name = "Average interest rate [in %]"
    elif lang == "FR":
        name = "Taux d'intérêt moyen [en %]"

    df_population_total = df_population.loc[df_population['gender'].isin(["total"])]
    df_population_total['Y_retairment'] = (
            df_population_total.Y65_69 + df_population_total.Y70_74 + df_population_total.Y75_79 +
            df_population_total.Y80_84 + df_population_total.Y85_89 + df_population_total.Y90_94 +
            df_population_total.Y_GE95
    ).shift()
    # df_population_total.loc[18:24, 'Total'] = df_population_total.sum(axis=1)

    print(df_population_total)

    # df_population_total["retairment"] = sum(df_population_total.loc[df_population_total['Y_GE95']], df_population_total.loc[df_population_total['Y90_94']])
    # df_population_total["Y_retairment"] = df_population_total.sum(axis=1, numeric_only=True) # zrata vsetky dokopy
    # df_population_total = df_population_total.eval('Sum = Y_GE95 + Y90_94')


    # df_population_total.rename(columns={"Y15_64": "total_Y15_64"}, inplace=True)
    df_population_males = df_population.loc[df_population['gender'].isin(["males"])]
    df_population_males.rename(columns={"Y15_64": "males_Y15_64"}, inplace=True)
    df_population_females = df_population.loc[df_population['gender'].isin(["females"])]
    df_population_females.rename(columns={"Y15_64": "females_Y15_64"}, inplace=True)

    # for dataset in [df_population_males, df_population_females]:
    for dataset in [df_population_total]:
    # for dataset in [df_population_total, df_population_females]:
        for i, column_headers in enumerate(dataset.columns):
            if "Y" in column_headers or "TOTAL" in column_headers:

                #print(dataset)

                # if "Y15_64" in column_headers:
                #     continue

                # print(column_headers)
                # print(df_population.columns[i])
                # # print(df_population.period)
                # print(type(df_population.period))
                #
                # print(i)
                #
                ser = dataset[column_headers].squeeze()
                # print(ser)
                # print(type(ser))

                if column_headers in ["TOTAL", "Y15_64"]:

                    subfig.add_trace(
                        go.Scatter(
                            # final_df,
                            x=dataset.period,
                            # y=df_population.Y00_04,
                            y=ser,
                            name=column_headers,
                            line={'shape': 'spline', 'smoothing': 1},
                            #visible='legendonly',

                            # xperiod="D30"
                        ),
                        secondary_y=True,
                    )
                else:
                    subfig.add_trace(
                        go.Scatter(
                            # final_df,
                            x=dataset.period,
                            # y=df_population.Y00_04,
                            y=ser,
                            name=column_headers,
                            line={'shape': 'spline', 'smoothing': 1},
                            visible='legendonly',

                            # xperiod="D30"
                        ),
                        secondary_y=True,
                    )

    # subfig.add_trace(
    #     go.Scatter(
    #         # final_df,
    #         x=df_population.period,
    #         y=df_population.Y80_84,
    #         name="80 až 84 roční",
    #         line={'shape': 'spline', 'smoothing': 1},
    #         # xperiod="D30"
    #     )
    # )
    #
    # subfig.add_trace(
    #     go.Scatter(
    #         # final_df,
    #         x=df_population.period,
    #         y=df_population.Y00_04,
    #         name="0 až 4 roční",
    #         line={'shape': 'spline', 'smoothing': 1}
    #         # color='bank_name',
    #     ),
    #     secondary_y=True,
    # )
    #
    # subfig.add_trace(
    #     go.Scatter(
    #         # final_df,
    #         x=final_df.The_date,
    #         y=final_df.interest,
    #         name=name,
    #         line={'shape': 'spline', 'smoothing': 1}
    #         # color='bank_name',
    #     ),
    #     secondary_y=True,
    # )

    # subfig.update_traces(xbins_size="Y1")

    subfig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.95
        )
    )

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
    Output("tite_custom_population_graph", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Vývoj obyvateľstva v priebehu rokov.'
    title_final = translate(lang, sentence=title)

    return title_final


final_custom_population_graph = [
    html.H1(id="tite_custom_population_graph", style={'textAlign': 'center'}),
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
        id="custom_population_graph",
        children=custom_re_graph_price_per_day,
        type="circle",
        fullscreen=False,
    ),
]
