import pandas as pd
import requests
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import plotly.express as px

from constants.districts import DISTRICTS, RE_TYPES
from constants.url import API_URL, API_PORT
from maindash import app, master_token
from time import time

from translate.translate import translate

custom_re_graph_hm_area_vs_price = html.Div(
    [
        dcc.Graph(
            id='custom_re_graph_hm_area_vs_price', figure={}
        )
    ]
)


@app.callback(
    Output("custom_re_graph_hm_area_vs_price", "children"),
    Input("custom_re_graph_hm_area_vs_price", "value")
)
def input_triggers_spinner(value):
    # sleep(1)
    return value


@app.callback(
    Output("custom_re_graph_hm_area_vs_price", "figure"),
    Input("city_dropdown", "value"),
    Input("re_type_dropdown", "value"),
    Input("set_language", "value")
)
def create_custom_density_heatmap_per_re(city, re_type, lang):
    params = {
        "re_type": re_type,
        "district": city,
        "token": master_token
    }

    start = time()
    # df = get_real_estate(what=re_type, where=city, projection=projection)
    url = f"http://{API_URL}:{API_PORT}/re_density_heatmap"
    # url = f"{API_URL}:{API_PORT}/re_density_heatmap"

    data = requests.get(url=url, params=params)
    end = time()
    print(f"pulling data for density map: {end-start} sec.")
    df = pd.DataFrame.from_dict(data.json())

    # nbinsx = int(len(df_filtered.index) / 40)
    # nbinsy = int(int(len(df_filtered.index) / 40) / 2)

    nbinsx = 80
    nbinsy = int(nbinsx / 2)

    start = time()
    sentence = "DisPlot - vyjadrenie ceny vs. plochy objektu na XY súradnicovej osy"
    figure = px.density_heatmap(
        df,
        # id="loading_test_figure",
        x="price",
        y='parameter_info.uzit_plocha',
        # text_auto=True,
        title=translate(lang, sentence),
        labels=translate(lang),
        height=700,
        nbinsx=nbinsx,
        nbinsy=nbinsy,
        color_continuous_scale=[
            (0.00, "white"), (0.00, "white"),
            (0.01, "lightblue"), (0.02, "lightblue"),
            (0.99, "darkblue"), (1.00, "darkblue")
        ],
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
    end = time()
    print(f"creating figure: {end - start} sec.")

    # del df_filtered
    return figure


@app.callback(
    Output("title_density_heatmap", "children"),
    Input("set_language", "value"),
)
def get_title(lang):
    title = 'Density HeatMap podľa typu nehnutelnosti a okresu.'
    title_final = translate(lang, sentence=title)

    return title_final


final_custom_re_graph_hm_area_vs_price = [
    html.H1(id="title_density_heatmap", style={'textAlign': 'center'}),
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
        id="custom_re_graph_hm_area_vs_price",
        parent_className="loading_wrapper",
        children=[custom_re_graph_hm_area_vs_price],
        type="circle",
        fullscreen=False
    )
]
