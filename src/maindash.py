import dash
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = "Salary & RealEstate Dashboard"
app.description = "Custom description..."
app.index_string = """<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <!-- # <script async src="https://www.googletagmanager.com/gtag/js?id=G-15C7GNBCP3"></script> -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-TCCQ5ZTRYP"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'G-TCCQ5ZTRYP');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <meta property="og:type" content="article">
        <meta property="og:title" content="Mzdy a ceny nehnuteľností"">
        <meta property="og:site_name" content="https://marcel-suleiman-salary-dashboard.onrender.com">
        <meta property="og:url" content="https://marcel-suleiman-salary-dashboard.onrender.com">
        <meta property="og:image" content="https://i.ibb.co/6DfwZX3/salary.png">
        <meta property="article:published_time" content="2023-07-08">
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>"""
