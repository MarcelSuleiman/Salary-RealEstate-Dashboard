import json
import requests
from time import time
import pandas as pd

import plotly.express as px

from dash import Output, Input, dcc, html

from constants.url import API_URL, API_PORT
from maindash import app
from translate.translate import translate
from util.render_graph_height import render_graph_height


custom_salary_graph_by_districts = dcc.Graph(
    id='custom_salary_graph_by_districts', figure={}
)


@app.callback(
    Output("custom_salary_graph_by_districts", "children"),
    Input("custom_salary_graph_by_districts", "value")
)
def input_triggers_spinner(value):
    return value


@app.callback(
    Output("custom_salary_graph_by_districts", "figure"),
    Input("set_language", "value"),
)
def get_median_salary_by_city(lang):
    start = time()
    url = f"http://{API_URL}:{API_PORT}/salary_by_district"
    # url = f"{API_URL}:{API_PORT}/salary_by_district"

    r = requests.get(url)
    end = time()
    print(f"pulling data for salaries by district {end-start} sec...")

    res = json.loads(r.text)
    df_id_grouped = pd.DataFrame.from_dict(res["df_data"])
    df_id_grouped = df_id_grouped.reset_index()
    df_id_grouped.rename(columns={"index": "place"}, inplace=True)

    rendered_height = render_graph_height(df_id_grouped, by="count_of_respondents")
    salary_value = res["salary_value"]
    salary_type = "Mediánový plat:"

    figure = px.bar(
        df_id_grouped,
        barmode='group',
        x='salary',
        y="place",
        height=rendered_height,
        text_auto=True,
        hover_data=["count_of_respondents"],
        labels=translate(lang),
    )

    figure.add_annotation(
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.03,
        text=translate(lang, sentence="<b>© vytvorené Marcelom Suleimanom</b>"),
        showarrow=False,
        font=dict(
            family="Courier New",
            size=11,
            color='#101010',
        ),
    )

    annotation_text = translate(lang, salary_type)

    figure.add_vline(
        x=round(salary_value),
        line_width=0.75, line_dash="dash",
        line_color='black',
        annotation=dict(text=f'{annotation_text} {salary_value} €'),
        annotation_position='bottom right',
    )

    return figure


@app.callback(
    Output("lll", "children"),
    Input("set_language", "value"),
)
def get_title(lang):

    title = 'Mediánové platy podľa miest v SR'
    title_final = translate(lang, sentence=title)

    return title_final


final_custom_salary_graph_by_districts = [
    html.H1(id="lll", style={'textAlign': 'center'}),
    dcc.Loading(
        id="custom_salary_graph_by_districts",
        children=custom_salary_graph_by_districts,
        type="circle",
        fullscreen=False
    ),
]
