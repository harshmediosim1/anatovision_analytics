import logging
from datetime import date
from dash import dcc, html, dash_table
from apps.data_processing import fetch_data  

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Dashboard is initializing...")

df, _ = fetch_data()  

DEFAULT_VISUALIZATIONS = ['active-users', 'table']  

layout = html.Div(children=[
    html.Div(
        style={
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'space-between',
            'backgroundColor': '#212121',
            'padding': '20px',
            'fontFamily': 'Arial, sans-serif',
            'borderRadius': '10px',
            'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.3)',
            'fontSize': '25px'
        },
        children=[
            html.Img(
                src='https://immersivelabz.com/wp-content/uploads/2020/08/main_logo_481X200.png',
                style={'height': '100px', 'marginRight': '20px'}
            ),
            html.H1(
                'Cadaviz Analytics Dashboard',
                style={'color': '#F2C94C', 'fontWeight': 'bold', 'flex': 1, 'textAlign': 'center', 'fontSize': '36px'}
            ),
        ]
    ),

    html.Div(
        style={'display': 'flex', 'height': '100vh', 'backgroundColor': '#2F3440', 'overflow': 'hidden'},
        children=[
            html.Div(
                style={
                    'width': '25%',  
                    'height': '100vh',
                    'padding': '8px',  
                    'backgroundColor': '#2c3e50',
                    'color': 'white',
                    'fontFamily': 'Arial, sans-serif',
                    'borderRight': '10px solid #0d08a5',
                    'overflowY': 'auto',
                    'scrollBehavior': 'smooth',
                    'maxHeight': '100vh',
                    'position': 'sticky',
                    'top': '0'
                },
                children=[
                    html.H3('Home', style={'textAlign': 'center', 'color': '#a30c4e', 'fontSize': '20px', 'fontWeight': 'bold'}), 
                    html.Div([
                        html.Label("Select Visualization(s):", style={'color': '#000080', 'fontWeight': 'bold', 'fontSize': '12px'}), 
                        dcc.Dropdown(
                            id='visualization-filter',
                            options=[
                               {'label': 'Active Users (Line Chart)', 'value': 'active-users'},
                               {'label': 'Pie Chart', 'value': 'pie'},
                               {'label': 'Total Usage (Top 5 module) Vs Date ', 'value': 'stacked-bar'},
                               {'label': 'Total Usage (College) Vs Date', 'value': 'line-chart'},
                               {'label': 'Total Usage vs Date', 'value': 'pie-2'},
                               {'label': 'Data Table', 'value': 'table'},
                            ],
                            value=DEFAULT_VISUALIZATIONS,
                            multi=True,
                            placeholder="Select Visualizations",
                            style={'borderRadius': '8px', 'padding': '3px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold', 'color': '#000000', 'fontSize': '11px' ,'textOverflow': 'ellipsis'}  
                        ),
                    ], style={'marginBottom': '4px'}),  

                    html.Div([
                        html.Label("Select User ID(s):", style={'color': '#a5081d', 'fontWeight': 'bold', 'fontSize': '12px'}),  
                        dcc.Dropdown(
                            id='user-id-filter',
                            options=[{'label': user, 'value': user} for user in df['user_id'].unique()],
                            multi=True,
                            placeholder="Select User ID(s)",
                            style={'borderRadius': '8px', 'padding': '3px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold', 'color': '#000000', 'fontSize': '11px' ,'textOverflow': 'ellipsis'})
                    ], style={'marginBottom': '4px'}), 

                    html.Div([
                        html.Label("Select Module(s):", style={'color': '#a5081d', 'fontWeight': 'bold', 'fontSize': '12px'}),  
                        dcc.Dropdown(
                            id='module-filter',
                            options=[{'label': module, 'value': module} for module in df['module'].unique()],
                            multi=True,
                            placeholder="Select Module(s)",
                            style={'borderRadius': '8px', 'padding': '3px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold', 'color': '#000000', 'fontSize': '11px','textOverflow': 'ellipsis'}
                        ),
                    ], style={'marginBottom': '4px'}),  

                    html.Div([
                        html.Label("Select Version:", style={'color': '#a5081d', 'fontWeight': 'bold', 'fontSize': '12px'}), 
                        dcc.Dropdown(
                            id='version-filter',
                            options=[{'label': version, 'value': version} for version in df['version'].unique()],
                            multi=True,
                            placeholder="Select Version(s)",
                            style={'borderRadius': '8px', 'padding': '3px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold', 'color': '#000000', 'fontSize': '11px' ,'textOverflow': 'ellipsis'}  
                        ),
                    ], style={'marginBottom': '4px'}),  

                    html.Div([
                        html.Label("Select Date Range:", style={'color': '#a5081d', 'fontWeight': 'bold', 'fontSize': '12px'}),  
                        dcc.DatePickerRange(
                            id='date-picker-range',
                            start_date=None,
                            end_date=None,
                            display_format='YYYY-MM-DD',
                            clearable=True,
                            max_date_allowed=date.today(),
                            style={'borderRadius': '5px', 'padding': '3px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold', 'color': '#000000', 'fontSize': '11px' ,'textOverflow': 'ellipsis'}  
                        ),
                    ], style={'marginBottom': '4px'}), 

                    html.Div([
                        html.Label("Select location:", style={'color': '#a5081d', 'fontWeight': 'bold', 'fontSize': '12px'}),  
                        dcc.Dropdown(
                            id='location-filter',
                            options=[{'label': location, 'value': location} for location in df['location'].unique()],
                            multi=True,
                            placeholder="Select Location(s)",
                            style={'borderRadius': '8px', 'padding': '3px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold', 'color': '#000000', 'fontSize': '11px' ,'textOverflow': 'ellipsis'}  
                        ),
                    ], style={'marginBottom': '4px'}),
        
                ]
            ),

            html.Div(
                style={
                    'width': '75%',  
                    'padding': '30px',
                    'marginLeft': '5%',
                    'overflow': 'auto',
                    'height': '100vh',
                    'overflowY': 'auto',
                    'overflowX': 'scroll',
                    'borderRadius': '10px',
                    'backgroundColor': '#FFFFFF',
                    'whiteSpace': 'nowrap'
                },
                children=[
                    dcc.Graph(id='active-users-line-chart', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='pie-chart', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='stacked-bar-chart', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='line-chart', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='pie-chart-2', style={'height': '500px', 'display': 'none'}),
                
                    html.H3(' Data Table', id="table-title", style={'textAlign': 'center', 'display': 'none', 'fontSize': '22px', 'fontWeight': 'bold'}),
                    html.Div(
                        id='data-table-container',  
                        children=[
                            dash_table.DataTable(
                                id='data-table',
                                columns=[  
                                    {"name": "User ID", "id": "user_id"},
                                    {"name": "Version", "id": "version"},
                                    {"name": "Date", "id": "date"},
                                    {"name": "Time", "id": "time"},
                                    {"name": "Location", "id": "location"},
                                 #   {"name": "State",  "id":  "state"},
                                    {"name": "College", "id": "college"},
                                    {"name": "Module", "id": "module"},
                                    {"name": "Submodule", "id": "submodule"},
                                    {"name": "Duration (min)", "id": "duration"},
                                ],
                                style_table={
                                    'height': '600px',
                                    'overflowY': 'auto',
                                    'backgroundColor': '#F5F5F5',
                                    'overflowX': 'scroll',  
                                    'backgroundColor': '#F5F5F5',  
                                    'borderBottom': '5px solid #FF5733',  
                                    'paddingBottom': '10px'
                                },
                                style_cell={
                                    'textAlign': 'center',
                                    'padding': '8px',  
                                    'color': 'black',
                                    'fontFamily': 'Arial, sans-serif'
                                },
                                style_header={
                                    'backgroundColor': '#333',
                                    'color': 'white',
                                    'fontWeight': 'bold'
                                },
                            ),
                        ],
                        style={'display': 'none'}  
                    ),
                ]
            ),
        ]
    )
])
