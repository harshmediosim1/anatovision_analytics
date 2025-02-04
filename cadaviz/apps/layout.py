from dash import dcc, html, dash_table
from apps.data_processing import fetch_data  # ✅ Correct import

# ✅ Fetch data
df = fetch_data()

# ✅ Default visualization selection
DEFAULT_VISUALIZATIONS = ['active-users', 'table']  # ✅ Default selected visualizations

# ✅ Ensure `layout` is correctly defined as a single Dash component
layout = html.Div(children=[
    # 🔹 Header Section with Logo & Title
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

    # 🔹 Main Dashboard Layout (Filters + Visualizations)
    html.Div(
        style={'display': 'flex', 'height': '100vh', 'backgroundColor': '#2F3440'},
        children=[
            # 🎛 Filters Section (Left Side - 30%)
            html.Div(
                style={
                    'width': '30%', 'backgroundColor': '#37474F', 'padding': '30px', 'height': '100vh',
                    'overflowY': 'auto', 'position': 'sticky', 'top': '0', 'borderRadius': '10px',
                    'boxShadow': '2px 4px 10px rgba(0, 0, 0, 0.1)', 'color': 'black', 'fontFamily': 'Arial, sans-serif',
                    'border': '1px solid #F2C94C', 'marginRight': '20px'
                },
                children=[
                    html.H3('Filters', style={'textAlign': 'center', 'color': '#693efe', 'fontSize': '24px', 'fontWeight': 'bold'}),

                    # 🔹 User ID Filter
                    html.Div(
                        children=[
                            html.Label("Select User ID(s):"),
                            dcc.Dropdown(
                                id='user-id-filter',
                                options=[{'label': user, 'value': user} for user in df['user_id'].unique()],
                                multi=True,
                                placeholder="Select User ID(s)",
                                style={'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold'}
                            ),
                        ], style={'marginBottom': '20px', 'backgroundColor': '#280429', 'padding': '10px', 'borderRadius': '5px'}
                    ),

                    # 🔹 Module Filter
                    html.Div(
                        children=[
                            html.Label("Select Module(s):"),
                            dcc.Dropdown(
                                id='module-filter',
                                options=[{'label': module, 'value': module} for module in df['module'].unique()],
                                multi=True,
                                placeholder="Select Module(s)",
                                style={'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold'}
                            ),
                        ], style={'marginBottom': '20px', 'backgroundColor': '#280429', 'padding': '10px', 'borderRadius': '5px'}
                    ),

                    # 🔹 Version Filter
                    html.Div(
                        children=[
                            html.Label("Select Version(s):"),
                            dcc.Dropdown(
                                id='version-filter',
                                options=[{'label': version, 'value': version} for version in df['version'].unique()],
                                multi=True,
                                placeholder="Select Version(s)",
                                style={'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold'}
                            ),
                        ], style={'marginBottom': '20px', 'backgroundColor': '#280429', 'padding': '10px', 'borderRadius': '5px'}
                    ),

                    # 🔹 Location Filter
                    html.Div(
                        children=[
                            html.Label("Select location(s):"),
                            dcc.Dropdown(
                                id='location-filter',
                                options=[{'label': location, 'value': location} for location in df['location'].unique()],
                                multi=True,
                                placeholder="Select location(s)",
                                style={'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold'}
                            ),
                        ], style={'marginBottom': '20px', 'backgroundColor': '#280429', 'padding': '10px', 'borderRadius': '5px'}
                    ),

                    # 🔹 Date Picker Filter
                    html.Div(
                        children=[
                            html.Label("Select Date Range:"),
                            dcc.DatePickerRange(
                                id='date-picker-range',
                                start_date=None,
                                end_date=None,
                                display_format='YYYY-MM-DD',
                                clearable=True,
                                style={'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold'}
                            ),
                        ], style={'marginBottom': '20px', 'backgroundColor': '#280429', 'padding': '10px', 'borderRadius': '5px'}
                    ),

                    # 🔹 Visualization Filter
                    html.Div(
                        children=[
                            html.Label("Select Visualization(s):"),
                            dcc.Dropdown(
                                id='visualization-filter',
                                options=[
                                    {'label': 'Active Users (Line Chart)', 'value': 'active-users'},
                                    {'label': 'Pie Chart', 'value': 'pie'},
                                    {'label': 'Stacked Bar Chart', 'value': 'stacked-bar'},
                                    {'label': 'Treemap', 'value': 'treemap'},
                                    {'label': 'Heatmap', 'value': 'heatmap'},
                                    {'label': 'Data Table', 'value': 'table'},
                                ],
                                value=DEFAULT_VISUALIZATIONS,
                                multi=True,
                                placeholder="Select Visualizations",
                                style={'borderRadius': '10px', 'padding': '10px', 'backgroundColor': '#F2F2F2', 'fontWeight': 'bold'}
                            ),
                        ], style={'marginBottom': '20px', 'backgroundColor': '#280429', 'padding': '10px', 'borderRadius': '5px'}
                    ),
                ]    
            ),

            # 📊 Visualizations Section (Right Side - 70%)
            html.Div(
                style={'width': '70%', 'padding': '30px', 'marginLeft': '5%', 'height': '100vh', 'overflowY': 'auto', 'borderRadius': '10px', 'backgroundColor': '#FFFFFF'},
                children=[
                    dcc.Graph(id='active-users-line-chart', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='pie-chart', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='stacked-bar-chart', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='treemap', style={'height': '500px', 'display': 'none'}),
                    dcc.Graph(id='heatmap', style={'height': '500px', 'display': 'none'}),

                    # Data Table with required columns and styling
                    html.H3('User Data Table', id="table-title", style={'textAlign': 'center', 'display': 'none', 'fontSize': '22px', 'fontWeight': 'bold'}),
                    html.Div(
                        id='data-table-container',  # The div container for DataTable visibility
                        children=[
                            dash_table.DataTable(
                                id='data-table',
                                columns=[  
                                    {"name": "User ID", "id": "user_id"},
                                    {"name": "Version", "id": "version"},
                                    {"name": "Date", "id": "date"},
                                    {"name": "Time", "id": "time"},
                                    {"name": "Location", "id": "location"},
                                    {"name": "College", "id": "college"},
                                    {"name": "Module", "id": "module"},
                                    {"name": "Submodule", "id": "submodule"},
                                    {"name": "Duration (sec)", "id": "duration"},
                                ],
                                style_table={
                                    'height': '600px',
                                    'overflowY': 'auto',
                                    'backgroundColor': '#F5F5F5'
                                },
                                style_cell={
                                    'textAlign': 'center',
                                    'padding': '10px',
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
                        style={'display': 'none'}  # Initially hide the Data Table container
                    ),
                ]
            ),
        ]
    )
])
