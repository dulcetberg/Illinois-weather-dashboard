import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import random

# 1. Coordinate Grid Data Structure for Illinois
ILLINOIS_LOCATIONS = {
    "Chicago": {"lat": 41.8781, "lon": -87.6298},
    "Springfield": {"lat": 39.7817, "lon": -89.6501},
    "Northlake": {"lat": 41.916008, "lon": -87.893809},
    "Peoria": {"lat": 40.6936, "lon": -89.5890},
    "Rockford": {"lat": 42.2711, "lon": -89.0940},
    "Champaign": {"lat": 40.1164, "lon": -88.2434}
}

def generate_live_spatial_data():
    data = []
    for city, coords in ILLINOIS_LOCATIONS.items():
        data.append({
            "City": city,
            "Latitude": coords["lat"],
            "Longitude": coords["lon"],
            "Humidity (%)": random.randint(45, 95),
            "Precipitation Probability (%)": random.randint(0, 100)
        })
    return pd.DataFrame(data)

# 2. Build the Exact Application Layout
app = dash.Dash(__name__)

server=app.server

app.layout = html.Div([
    html.H1("Illinois Live Weather Map & Spatial Dashboard", 
            style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}),

    # ADDED: Your Name Subtitle Line
    html.H3("Created by Brian Bergstrom", 
            style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif', 'color': '#555555', 'marginTop': '0px', 'marginBottom': '20px'}),
    
    
    html.Div([
        # Main Map Component
        dcc.Graph(id='weather-spatial-map'),
    ], style={'padding': '20px'}),
    
    # CHANGED: 'flexDirection' is now 'column' to stack the charts vertically
    html.Div([
        dcc.Graph(id='humidity-bar-chart'),
        dcc.Graph(id='precipitation-bar-chart')
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px', 'padding': '20px'}),
    
    dcc.Interval(
        id='map-refresh-timer',
        interval=10000, 
        n_intervals=0
    )
])


# 3. Dynamic Visualization Rendering Loop with Linked IDs
@app.callback(
    [Output('weather-spatial-map', 'figure'),
     Output('humidity-bar-chart', 'figure'),
     Output('precipitation-bar-chart', 'figure')],
    Input('map-refresh-timer', 'n_intervals')
)
def update_weather_map(n):
    df = generate_live_spatial_data()
    
    # Map Generation 
    map_fig = px.scatter_map(
        df, lat="Latitude", lon="Longitude", hover_name="City",
        hover_data={"Humidity (%)": True, "Precipitation Probability (%)": True, "Latitude": False, "Longitude": False},
        color="Precipitation Probability (%)", size="Humidity (%)",
        color_continuous_scale=px.colors.sequential.Blues, size_max=30, zoom=6,
        center={"lat": 40.6331, "lon": -89.3985},
        title="Live Regional Matrix (Bubble Size = Humidity | Bubble Darkness = Rain Chance)"
    )
    map_fig.update_layout(map_style="open-street-map", margin={"r":0,"t":40,"l":0,"b":0}, height=500)
    
    # Subgraph Generations
    humidity_fig = px.bar(df, x='City', y='Humidity (%)', color='City', template='plotly_white')
    precipitation_fig = px.bar(df, x='City', y='Precipitation Probability (%)', color='City', template='plotly_white')

  # Subgraph Generations with Titles Added
    humidity_fig = px.bar(
        df, 
        x='City', 
        y='Humidity (%)', 
        color='City', 
        template='plotly_white',
        title="Current Relative Humidity Levels across Illinois Cities" # Added
    )
    
    precipitation_fig = px.bar(
        df, 
        x='City', 
        y='Precipitation Probability (%)', 
        color='City', 
        template='plotly_white',
        title="Probability of Precipitation (%) by Region" # Added
    )
    
    return map_fig, humidity_fig, precipitation_fig

if __name__ == '__main__':
    app.run(debug=False)
