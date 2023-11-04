from maindash import app
from dash.dependencies import Input, Output

from translate.translate import translate


@app.callback(
    Output("outliers_checkbox", "options"),
    Input("position_salary_dropdown", "value"),
    Input("set_language", "value"),
    Prevent_initial_call=True
)
def disable_radio_switch_remove_outliers(value, lang):
    sentence = "Odstrániť outlierov"
    label = translate(lang, sentence=sentence)

    if value == "median":
        return [{"label": f"{label}", "value": 1, "disabled": True}]
    return [{"label": f"{label}", "value": 0, "disabled": False}]


@app.callback(
    Output("outliers_checkbox_2", "options"),
    Input("industry_salary_dropdown", "value"),
    Input("set_language", "value"),
    Prevent_initial_call=True
)
def disable_radio_switch_remove_outliers(value, lang):
    sentence = "Odstrániť outlierov"
    label = translate(lang, sentence=sentence)
    if value == "median":
        return [{"label": f"{label}", "value": 1, "disabled": True}]
    return [{"label": f"{label}", "value": 0, "disabled": False}]


@app.callback(
    Output("position_place_dropdown", "placeholder"),
    Input("set_language", "value"),
    Prevent_initial_call=True
)
def get_dropdown_option(lang):
    sentence = "Celé Slovensko... alebo vyber mesto."
    placeholder = translate(lang, sentence=sentence)

    return placeholder


@app.callback(
    Output("industry_place_dropdown", "placeholder"),
    Input("set_language", "value"),
    Prevent_initial_call=True
)
def get_dropdown_option(lang):
    sentence = "Celé Slovensko... alebo vyber mesto."
    placeholder = translate(lang, sentence=sentence)

    return placeholder


@app.callback(
    Output("salary_distribution_place_dropdown", "placeholder"),
    Input("set_language", "value"),
    Prevent_initial_call=True
)
def get_dropdown_option(lang):
    sentence = "Celé Slovensko... alebo vyber mesto."
    placeholder = translate(lang, sentence=sentence)

    return placeholder


@app.callback(
    Output("salary_by_gender_position_dropdown", "placeholder"),
    Input("set_language", "value"),
    Prevent_initial_call=True
)
def get_dropdown_option(lang):
    sentence = "Vyber si povolanie..."
    placeholder = translate(lang, sentence=sentence)

    return placeholder


@app.callback(
    Output("salary_by_gender_city_dropdown", "placeholder"),
    Input("set_language", "value"),
    Prevent_initial_call=True
)
def get_dropdown_option(lang):
    sentence = "Vyber si mesto..."
    placeholder = translate(lang, sentence=sentence)

    return placeholder
