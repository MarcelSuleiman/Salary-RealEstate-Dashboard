from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from maindash import app
from translate.translate import translate

from pages.in_by_percentage_per_day import final_custom_interest_graph_percentage_per_day
from pages.salary_by_position import final_custom_salary_graph_by_position
from pages.salary_by_district import final_custom_salary_graph_by_districts
from pages.re_by_price_per_day import final_custom_re_graph_price_per_day
from pages.re_map_salary import custom_map_salary
from pages.home import home

from pages.re_rent_by_condition_boxplot import final_custom_re_rent_graph_condition_boxplot
from pages.salary_by_gender import final_custom_salary_graph_by_gender
from pages.re_count_per_day import final_custom_re_graph_count_per_day
from pages.re_map_price_salary_ratio import custom_re_map_salary_price_ratio
from pages.re_by_condition_boxplot import final_custom_re_graph_condition_boxplot
from pages.salary_by_industry import final_custom_salary_graph_by_industry
from pages.salary_distribution import final_custom_salary_graph_distribution
from pages.re_density_heatmap import final_custom_re_graph_hm_area_vs_price

# necessary callbacks
from callbacks.callback import disable_radio_switch_remove_outliers
from callbacks.callback import get_dropdown_option

# from pages.salary_by_gender import create_graph_test, create_graph_test_2  # works without import, why?

#  https://youtu.be/B0fll6QQbCw?list=RDN7a5cboeOhA&t=157
server = app.server

NAVBAR_STYLE = {
    # "position": "sticky",
    "width": "100%",
    # "height": "2rem",
}

SIDEBAR_STYLE = {
    # "position": "fixed",
    "position": "absolute",
    # "position": "sticky",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 62.5,
    "left": "-17rem",
    "bottom": 0,
    "width": "17rem",
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0rem 0rem",
    "background-color": "#f8f9fa",
}

LINK_STYLE = {
    "padding": "2rem 1rem",
}

CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE1 = {
    "transition": "margin-left .5s",
    "margin-left": "0rem",
    "margin-right": "0rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

navbar_right = dbc.NavbarSimple(
    children=[
        dcc.Dropdown(
            id="set_language",
            # options=["SK", "EN", "FR", "HU"],
            options=["SK", "EN", "FR"],
            value="EN",
            clearable=False,
        ),
    ],
    # brand="Figures",
    # brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
    style=NAVBAR_STYLE,
)


def get_link_names(lang, text):
    return translate(lang, sentence=text)


@app.callback(
    Output("nav-bar-left", "children"),
    Input("set_language", "value")
)
def get_navbar_left(lang):
    navbar_left = dbc.NavbarSimple(
        children=[
            dbc.Button("Sidebar", outline=True, color="secondary", className="mr-1", id="btn_sidebar"),
            dbc.DropdownMenu(
                children=[
                    # dbc.DropdownMenuItem("More pages", header=True),
                    dbc.DropdownMenuItem("Home", href="/"),

                    html.P(id="001", children=get_link_names(lang, text="Údaje o platoch"), className="lead"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Platy podľa lokality"), href="/page-0"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Platy podľa pozície"), href="/page-1"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Platy podľa odvetvia"), href="/page-2"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Porovnanie platov na základe pohlavia"), href="/page-3"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Distribúcia platov"), href="/page-4"),
                    html.Br(),

                    html.P(id="001", children=get_link_names(lang, text="Údaje o nehnutelnostiach"), className="lead"),
                    dbc.DropdownMenuItem("Density HeatMap", href="/page-5"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Počet objektov na predaj v ponuke"), href="/page-6"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Ceny vybraných nehnuteľností podľa stavu"), href="/page-7"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Vývoj ceny nehnuteľností podľa druhu"), href="/page-9"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Ceny nájmov vybraných nehnuteľností podľa stavu"), href="/page-8"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Vývoj úrokových sadzieb"), href="/page-10"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Mapa Slovenska: mzdy v regiónoch"), href="/page-11"),
                    dbc.DropdownMenuItem(id="001", children=get_link_names(lang, text="Mapa Slovenska: pomer ceny nehnutelnosti a mzdy"), href="/page-12"),
                    html.Br(),

                    html.P(id="001", children=get_link_names(lang, text="Kontakt"), className="lead"),
                    html.A(
                        id="001", children=get_link_names(lang, text="Autor"),
                        href='https://www.linkedin.com/in/marcel-suleiman/',
                        target="_blank",
                        style=LINK_STYLE),  # className="ms-3"),
                ],
                direction="start",
                nav=True,
                in_navbar=False,
                label=translate(lang, sentence="Kapitoly"),
            ),
        ],
        # brand="Figures",
        # brand_href="#",
        color="dark",
        dark=True,
        fluid=True,
        style=NAVBAR_STYLE,
    )
    return navbar_left


@app.callback(
    Output("side-bar", "children"),
    Input("set_language", "value")
)
def get_sidebar(lang):
    sidebar = html.Div(
        [
            html.H2(id="001", children=get_link_names(lang, text="Kapitoly"), className="display-4"),
            html.Hr(),
            # html.P(
            #     "Kapitoly:", className="lead"
            # ),
            dbc.Nav(
                [
                    html.Div([
                        dbc.NavLink("Home", href="/"),
                        html.P(id="001", children=get_link_names(lang, text="Údaje o platoch"), className="lead"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Platy podľa lokality"), href="/page-0", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Platy podľa pozície"), href="/page-1", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Platy podľa odvetvia"), href="/page-2", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Porovnanie platov na základe pohlavia"), href="/page-3", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Distribúcia platov"), href="/page-4", active="exact"),
                    ]),
                    html.Div([
                        html.Br(),
                        html.P(id="001", children=get_link_names(lang, text="Údaje o nehnutelnostiach"), className="lead"),
                        dbc.NavLink("Density HeatMap", href="/page-5", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Počet objektov na predaj v ponuke"), href="/page-6", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Ceny vybraných nehnuteľností podľa stavu"), href="/page-7", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Vývoj ceny nehnuteľností podľa druhu"), href="/page-9", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Ceny nájmov vybraných nehnuteľností podľa stavu"), href="/page-8", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Vývoj úrokových sadzieb"), href="/page-10", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Mapa Slovenska: mzdy v regiónoch"), href="/page-11", active="exact"),
                        dbc.NavLink(id="001", children=get_link_names(lang, text="Mapa Slovenska: pomer ceny nehnutelnosti a mzdy"), href="/page-12", active="exact"),
                    ]),
                    html.Div([
                        html.Br(),
                        html.P(id="001", children=get_link_names(lang, text="Kontakt"), className="lead"),
                        html.A(
                            "Autor",
                            href='https://www.linkedin.com/in/marcel-suleiman/',
                            target="_blank",
                            style=LINK_STYLE),
                        # className="ms-3"),
                    ]),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        id="sidebar",
        #style=SIDEBAR_STYLE,
    )

    return sidebar


content = html.Div(id="page-content", children=[], style=CONTENT_STYLE)
sidebar = html.Div(id="side-bar", children=[])
navbar_left = html.Div(id="nav-bar-left", children=[])

app.layout = html.Div([
    dcc.Store(id='side_click'),
    dcc.Location(id="url"),
    # navbar_left,
    # navbar_right,
    html.Div(children=[navbar_left, navbar_right], style={"display": "grid", "grid-template-columns": "90% 10%"}),
    sidebar,
    content,
])


@app.callback(
    [
        Output("side-bar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDEN"

        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"

    else:
        sidebar_style = SIDEBAR_HIDEN
        content_style = CONTENT_STYLE1
        cur_nclick = 'HIDEN'

    return sidebar_style, content_style, cur_nclick


@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/":
        return home
    elif pathname == "/page-0":
        return final_custom_salary_graph_by_districts
    elif pathname == "/page-1":
        return final_custom_salary_graph_by_position
    elif pathname == "/page-2":
        return final_custom_salary_graph_by_industry
    elif pathname == "/page-3":
        return final_custom_salary_graph_by_gender
    elif pathname == "/page-4":
        return final_custom_salary_graph_distribution
    elif pathname == "/page-5":
        return final_custom_re_graph_hm_area_vs_price
    elif pathname == "/page-6":
        return final_custom_re_graph_count_per_day
    elif pathname == "/page-7":
        return final_custom_re_graph_condition_boxplot
    elif pathname == "/page-8":
        return final_custom_re_rent_graph_condition_boxplot
    elif pathname == "/page-9":
        return final_custom_re_graph_price_per_day
    elif pathname == "/page-10":
        return final_custom_interest_graph_percentage_per_day
    elif pathname == "/page-11":
        return custom_map_salary
    elif pathname == "/page-12":
        return custom_re_map_salary_price_ratio
    elif pathname == "/page-99":
        return [
            dcc.Location(href="https://www.linkedin.com/in/marcel-suleiman/", pathname="[Author info]", id="qxz"),
        ]
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True, port=45678)
