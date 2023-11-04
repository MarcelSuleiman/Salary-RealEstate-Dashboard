from util.constants import MIN_HEIGHT, MIN_BAR_HEIGHT


def render_graph_height(df_id_grouped, by: str):
    g_height = len(df_id_grouped.groupby(by).nunique())
    rendered_height = MIN_BAR_HEIGHT*g_height
    if rendered_height < MIN_HEIGHT:
        rendered_height = MIN_HEIGHT

    return rendered_height
