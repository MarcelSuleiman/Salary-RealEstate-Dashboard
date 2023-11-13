from pathlib import Path
import pandas as pd
import requests

from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

from constants.url import API_URL, API_PORT
from maindash import app, master_token
from translate.translate import translate


custom_interest_graph_percentage_per_day = dcc.Graph(
    id="create_final_custom_interest_graph_percentage_per_day", figure={}
)


@app.callback(
    Output("create_final_custom_interest_graph_percentage_per_day", "figure"),
    Input("set_language", "value")
)
def create_final_custom_interest_graph_percentage_per_day(lang):

    url = f"http://{API_URL}:{API_PORT}/interest_rates"
    # url = f"http://localhost:7777/interest_rates"
    params = {
        "loan_type": "H",
        "token": master_token
    }
    data = requests.get(url=url, params=params)
    df = pd.DataFrame.from_dict(data.json())

    # root_folder = Path(__file__).parents[1]
    # my_path = root_folder / "uvery.csv"
    #
    # df = pd.read_csv(my_path, delimiter=";")
    # print(df.head())

    # final_df = df.loc[df['loan_type'].isin(["H"])]

    figure = px.line(
        df,
        x="the_date",
        y="interest",
        height=750,
        color='bank_name',
        # labels={"The_date": "Dátum", "interest": "Úroková sadzba [v %]", "bank_name": "Banka"},
        labels=translate(lang),
    )

    return figure


@app.callback(
    Output("title_custom_interest_graph_percentage_per_day", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Vývoj úrokových sadzieb na hypotéky 3r fix.'
    title_final = translate(lang, sentence=title)

    return title_final


final_custom_interest_graph_percentage_per_day = [
    html.H1(
        id="title_custom_interest_graph_percentage_per_day",
        style={'textAlign': 'center'}
    ),
    custom_interest_graph_percentage_per_day,
]
