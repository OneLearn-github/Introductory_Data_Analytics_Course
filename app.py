# import the libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

from final_dashboard.prep_data import dashboard_data,genre

# Create the Dash app
app = dash.Dash(__name__)
server = app.server

# Set up the app layout
app.layout = html.Div(children=[
    html.H1(children='Imdb vs Rotten tomatoes Ratings Dashboard'),
    html.H2(children='Year Released'),
    dcc.RangeSlider(
            id='year-released-range-slider',
            min=dashboard_data.year.min(),
            max=dashboard_data.year.max(),
            marks={str(y): str(y) for y in range(int(dashboard_data.year.min()), int(dashboard_data.year.max()), 5)},
            value=[dashboard_data.year.min(), dashboard_data.year.max()]
        ),
    html.Br(),
    html.H2(children='Box Office Earnings (in millions)'),
    dcc.RangeSlider(
            id='box-office-range-slider',
            min=dashboard_data.worldwide_gross_income.min(),
            max=dashboard_data.worldwide_gross_income.max(),
            marks={str(y): str(y) for y in range(int(dashboard_data.worldwide_gross_income.min()), \
                                                 int(dashboard_data.worldwide_gross_income.max()), 200)},
            value=[dashboard_data.worldwide_gross_income.min(), dashboard_data.worldwide_gross_income.max()]
        ),
    html.Br(),
    html.H2(children='Genre'),
    dcc.Dropdown(
        id = 'genre-dropdown',
        options=[{'label':i,'value':i} for i in genre],
        value='All Genre'
    ),
    html.Br(),
    dcc.Graph(id='rating-graph')
])


# Set up the callback function
@app.callback(
    Output(component_id='rating-graph', component_property='figure'),
    [
     Input(component_id='year-released-range-slider', component_property='value'),
     Input(component_id='box-office-range-slider',component_property='value'),
     Input(component_id='genre-dropdown',component_property='value')
    ]
)
def update_graph(selected_year,gross_income,genre_name):
    year_released_start, year_released_end = selected_year
    gross_income_start,gross_income_end = gross_income
    filtered_df1 = dashboard_data.loc[(dashboard_data['year'] >= year_released_start)&(dashboard_data['year'] <= year_released_end)]
    filtered_df2 = filtered_df1.loc[(filtered_df1['worldwide_gross_income']>=gross_income_start)&(filtered_df1['worldwide_gross_income']<=gross_income_end)]
    if genre_name == 'All Genre':
        genre_name_select = ''
    else:
        genre_name_select = genre_name
    filtered_final = filtered_df2.loc[filtered_df2['genre'].str.contains(genre_name_select)]
    scatter_fig = px.scatter(filtered_final,
                       x='imdb_scaled', y='tomatometer_rating',hover_name='original_title',
                       hover_data=['genre','worldwide_gross_income','year'],
                       range_x = [0,100],range_y=[-10,110],
                       title=f'Rating comparison - years selected {selected_year} - box office range {gross_income} - genre {genre_name}')
    return scatter_fig



# Run local server
if __name__ == '__main__':
    app.run_server(debug=True)