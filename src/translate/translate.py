import json
import deepl

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
        deepl_api_key = "YOUR_API_KEY"
        translator = deepl.Translator(auth_key=deepl_api_key)
        result = str(translator.translate_text(sentence, target_lang=lang))
        return result


def translate_dataset(df, lang, which_df):
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
