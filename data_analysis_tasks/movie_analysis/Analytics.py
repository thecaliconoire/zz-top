import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

actors_df = pd.read_csv('../data/Movie_Actors.csv')
additional_ratings_df = pd.read_csv('../data/Movie_AdditionalRating.csv')
genres_df = pd.read_csv('../data/Movie_Genres.csv')
movies_df = pd.read_csv('../data/Movie_Movies.csv')
writers_df = pd.read_csv('../data/Movie_Writer.csv')

# Set up top movie directors data
movies_directors = movies_df['Director'].value_counts().to_frame().reset_index()
rename = movies_directors.rename(columns={'index': 'Director', 'Director': 'NumberOfMoviesProduced'})
top_directors = rename[:10]

# Director active
years = movies_df[['Director', 'Year']]
active_years = pd.merge(top_directors, years, how='left', on='Director') 

# Runtime
Runtime = movies_df[['Director', 'Runtime', 'Year']]
Runtime_Top_10 = pd.merge(top_directors, Runtime, how='left', on='Director')


# Set up dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}
# Define Charts
Number_Of_Movies = px.bar(movies_df, x=top_directors.Director, y=top_directors.NumberOfMoviesProduced, color=top_directors.Director, barmode="group")
Directors_Active = px.box(movies_df, x=Runtime_Top_10.Director, y= Runtime_Top_10.Year, color=Runtime_Top_10.Director)

#Style Charts
Number_Of_Movies.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

Directors_Active.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(
    style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Top 10 Movie Producers',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.H5(children='How many movies did each director produce?', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='movie-graph-1',
        figure=Number_Of_Movies
    ),

    html.H5(children='Years Director Was Active', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
        dcc.Graph(
        id='movie-graph-2',
        figure=Directors_Active
    ),

    html.H5(children='Years Director Was Active', style={
        'textAlign': 'center',
        'color': colors['text']
    }),
])

if __name__ == '__main__':
    app.run_server(debug=True)