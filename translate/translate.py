from os.path import exists

import json
import deepl
import pandas as pd

from maindash import deel_l_api_key

with open("translate/en.json", "r") as f:
    en_dictionary = json.load(f)

with open("translate/fr.json", "r") as f:
    fr_dictionary = json.load(f)

with open("translate/sk.json", "r") as f:
    sk_dictionary = json.load(f)


def translate(lang, sentence=None):

    if sentence is None:
        if lang == "EN":
            return en_dictionary.get("labels")

        elif lang == "FR":
            return fr_dictionary.get("labels")

        elif lang == "SK":
            return sk_dictionary.get("labels")

        # elif lang == "HU":
        #     return en_dictionary.get("labels")

    if lang == "EN":
        return en_dictionary.get(sentence)

    elif lang == "FR":
        return fr_dictionary.get(sentence)

    elif lang == "SK":
        return sk_dictionary.get(sentence)

    elif lang == "HU":
        deepl_api_key = deel_l_api_key
        translator = deepl.Translator(auth_key=deepl_api_key)
        result = str(translator.translate_text(sentence, target_lang=lang))
        return result


def translate_dataset(df: pd.DataFrame, lang: str, which_df: str) -> pd.DataFrame:
    # NOTE
    # I'm not sure why I didn't use the JSON translation as in other parts of the project... 🤷‍♂️

    if which_df == "re_boxplot_by_condition":
        if lang == "SK":
            return df
        elif lang == "EN":
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Pôvodný stav', 'Original state', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Čiastočná rekonštrukcia', 'Partial reconstruction', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Kompletná rekonštrukcia', 'Complete reconstruction', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Novostavba', 'New construction', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Vo výstavbe', 'Under construction', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Developerský projekt', 'Developer project', inplace=True)
            return df
        elif lang == "FR":
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Pôvodný stav', "État d'origine", inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Čiastočná rekonštrukcia', 'Reconstruction partielle', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Kompletná rekonštrukcia', 'Reconstruction complète', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Novostavba', 'Nouveau bâtiment', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Vo výstavbe', 'En cours de construction', inplace=True)
            df['parameter_info.stav'].mask(df['parameter_info.stav'] == 'Developerský projekt', 'Projet de développement', inplace=True)
            return df
        else:
            return df

    if which_df == "re_boxplot_by_condition_rent":
        if lang == "SK":
            return df
        elif lang == "EN":
            df['stav'].mask(df['stav'] == 'Pôvodný stav', 'Original state', inplace=True)
            df['stav'].mask(df['stav'] == 'Čiastočná rekonštrukcia', 'Partial reconstruction', inplace=True)
            df['stav'].mask(df['stav'] == 'Kompletná rekonštrukcia', 'Complete reconstruction', inplace=True)
            df['stav'].mask(df['stav'] == 'Novostavba', 'New construction', inplace=True)
            df['stav'].mask(df['stav'] == 'Vo výstavbe', 'Under construction', inplace=True)
            df['stav'].mask(df['stav'] == 'Developerský projekt', 'Developer project', inplace=True)
            return df
        elif lang == "FR":
            df['stav'].mask(df['stav'] == 'Pôvodný stav', "État d'origine", inplace=True)
            df['stav'].mask(df['stav'] == 'Čiastočná rekonštrukcia', 'Reconstruction partielle', inplace=True)
            df['stav'].mask(df['stav'] == 'Kompletná rekonštrukcia', 'Reconstruction complète', inplace=True)
            df['stav'].mask(df['stav'] == 'Novostavba', 'Nouveau bâtiment', inplace=True)
            df['stav'].mask(df['stav'] == 'Vo výstavbe', 'En cours de construction', inplace=True)
            df['stav'].mask(df['stav'] == 'Developerský projekt', 'Projet de développement', inplace=True)
            return df
        else:
            return df

    if which_df == "salary_boxplot_by_age" or which_df == "salary_boxplot_by_gender":
        if lang == "SK":
            df['gender'].mask(df['gender'] == 'Man', 'Muži', inplace=True)
            df['gender'].mask(df['gender'] == 'Woman', 'Ženy', inplace=True)

            df['age'].mask(df['age'] == '', 'Neuvedené', inplace=True)
            return df
        elif lang == "EN":
            df['age'].mask(df['age'] == '<24 rokov', '<24 years old', inplace=True)
            df['age'].mask(df['age'] == '25-34 rokov', '25-34 years old', inplace=True)
            df['age'].mask(df['age'] == '35-44 rokov', '35-44 years old', inplace=True)
            df['age'].mask(df['age'] == '45-54 rokov', '45-54 years old', inplace=True)
            df['age'].mask(df['age'] == '55+ rokov', '55+ years', inplace=True)
            df['age'].mask(df['age'] == '', 'Not listed', inplace=True)
            return df
        elif lang == "FR":
            df['gender'].mask(df['gender'] == 'Man', 'Hommes', inplace=True)
            df['gender'].mask(df['gender'] == 'Woman', 'Femmes', inplace=True)

            df['age'].mask(df['age'] == '<24 rokov', '<24 ans', inplace=True)
            df['age'].mask(df['age'] == '25-34 rokov', '25-34 ans', inplace=True)
            df['age'].mask(df['age'] == '35-44 rokov', '35-44 ans', inplace=True)
            df['age'].mask(df['age'] == '45-54 rokov', '45-54 ans', inplace=True)
            df['age'].mask(df['age'] == '55+ rokov', '55+ ans', inplace=True)
            df['age'].mask(df['age'] == '', 'Non listé', inplace=True)
            return df
        else:
            return df


def translate_salary(df: pd.DataFrame, lang: str,  which: str, page: str) -> pd.DataFrame:
    # If language is Slovak, do nothing
    if lang == "SK":
        return df

    translator = deepl.Translator(auth_key=deel_l_api_key)

    json_file = f"translate/sk_{lang.lower()}_{page}.json"
    # try because if I use new language, I don't have JSON file prepared
    # it will crash - load all translated position from DeepL
    # and after that will crate JSON file and fill it by new keywords
    if not exists(json_file):
        with open(json_file, "w+", encoding="utf-8") as json_file:
            json_file.write("{}")

    json_file = f"translate/sk_{lang.lower()}_{page}.json"
    with open(json_file, "r", encoding="utf-8") as json_file:
        json_decoded = json.load(json_file)

    def _translate(sentence, json_decoded, deep_l_lang):
        translated_position_name = str(json_decoded.get(sentence))

        if translated_position_name == "None":
            translated_position_name = str(translator.translate_text(sentence, target_lang=deep_l_lang))

        return translated_position_name

    if lang == "EN":
        deep_l_lang = "EN-GB"
    else:
        deep_l_lang = lang

    df[f"translated_{which}"] = df[which].apply(
        lambda position_industry: _translate(position_industry, json_decoded, deep_l_lang)
    )

    # prepare DF to crate local JSON file with translations
    my_df = df.drop("salary", axis="columns")
    my_df = my_df.drop("count_of_respondents", axis="columns")
    my_df_as_dict = my_df.to_dict()
    create_local_translator(my_df_as_dict, lang, which, page)

    df.drop(which, axis="columns", inplace=True)
    df.rename(columns={f"translated_{which}": which}, inplace=True)

    return df


def create_local_translator(position_dictionary: pd.DataFrame, lang: str, which, page) -> None:

    try:
        json_file = f"translate/sk_{lang.lower()}_{page}.json"
        with open(json_file, "r", encoding="utf-8") as json_file:
            json_decoded = json.load(json_file)
    except FileNotFoundError:
        json_file = f"translate/sk_{lang.lower()}_{page}.json"
        with open(json_file, "w+", encoding="utf-8") as json_file:
            json_file.write("{}")
    finally:
        json_file = f"translate/sk_{lang.lower()}_{page}.json"
        with open(json_file, "r", encoding="utf-8") as json_file:
            json_decoded = json.load(json_file)

    my_dict = {}
    count = len(position_dictionary.get(which))
    for i in range(0, count):
        key = position_dictionary[which][i]
        value = position_dictionary[f"translated_{which}"][i]
        json_decoded[key] = value

        my_dict[position_dictionary[which][i]] = position_dictionary[f"translated_{which}"][i]

    json_file = f"translate/sk_{lang.lower()}_{page}.json"
    with open(json_file, 'w', encoding="utf-8") as json_file:
        json.dump(json_decoded, json_file, indent=2, ensure_ascii=False)
