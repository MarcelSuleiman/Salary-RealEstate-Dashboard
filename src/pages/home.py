from dash import html
from maindash import app
from dash.dependencies import Input, Output
import translate.translate


def get_translate(lang, sentence):
    title_final = translate.translate.translate(lang, sentence=sentence)
    return title_final


@app.callback(
    Output("home_title", "children"),
    Input("set_language", "value"),
)
def get_title(lang):

    title = 'Vitaj'
    title_final = translate.translate.translate(lang, sentence=title)

    return title_final


@app.callback(
    Output("home_body", "children"),
    Input("set_language", "value"),
)
def get_body(lang):
    sentences = [
        "text_1",
        # "text_2",
        # "text_3"
    ]

    data = []

    for sentence in sentences:
        sen = translate.translate.translate(lang, sentence=sentence)
        data.append(sen)

    final = []
    for d in data:
        final.append(html.P(d))

    return final


home = [
    html.H1(id="home_title"),
    html.Div(id="home_body"),
]
