import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, no_update
import pandas as pd
import plotly.express as px
from apps.data_processing import fetch_data, validate_user
from apps.layout import dashboard_layout, login_layout ,Main_layout
from apps.charts import create_pie_chart, create_stacked_bar_chart, create_line_chart, create_pie_chart_for_date
import logging
from apps.socket_manager import socketio

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

existing_data = pd.DataFrame()
def register_callbacks(app):
    @app.callback(
        [Output('page-content', 'children'),
         Output('login-feedback', 'children'),
         Output('login-state', 'data')],
        [Input('login-button', 'n_clicks')],
        [State('username', 'value'),
         State('password', 'value'),
         State('login-state', 'data')]
    )
    def manage_login(login_clicks, username, password, login_state):
        ctx = dash.callback_context
        print("Callback triggered!")

        if not ctx.triggered:
            print("No trigger detected. Returning login layout.")
            return login_layout, "", login_state  

        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(f"Button clicked: {button_id}")

        if button_id == 'login-button':
            print(f"Attempting login with Username: {username} and Password: {password}")

            if not username or not password:
                print("Login failed: Missing username or password")
                return login_layout, "Please enter username and password", False  

            is_valid, message = validate_user(username, password)
            if is_valid:
                print("Login successful!")
                return dashboard_layout, "", True 
            else:
                print("Login failed: Invalid credentials")
                return login_layout, "Invalid username or password", False  

        return no_update, no_update, no_update
    @app.callback(
        [
            Output('active-users-line-chart', 'figure'),
            Output('pie-chart', 'figure'),
            Output('stacked-bar-chart', 'figure'),
            Output('line-chart', 'figure'),
            Output('pie-chart-2', 'figure'),
            Output('data-table', 'data'),
            Output('active-users-line-chart', 'style'),
            Output('pie-chart', 'style'),
            Output('stacked-bar-chart', 'style'),
            Output('line-chart', 'style'),
            Output('pie-chart-2', 'style'),
            Output('data-table-container', 'style'),
            Output('table-title', 'style'),
            Output('user-id-filter', 'options'),
            Output('module-filter', 'options'),
            Output('version-filter', 'options'),
            Output('location-filter', 'options')
        ],
        [
            Input('user-id-filter', 'value'),
            Input('module-filter', 'value'),
            Input('date-picker-range', 'start_date'),
            Input('date-picker-range', 'end_date'),
            Input('version-filter', 'value'),
            Input('location-filter', 'value'),
            Input('visualization-filter', 'value')
        ]  
    )
    def update_graphs(user_id, module, start_date, end_date, version, location, visualizations):
        global existing_data  

        try:
            new_data, latest_update_time = fetch_data()

            if not new_data.empty:
                new_data = new_data[~new_data.isin(existing_data)].dropna()
                if not new_data.empty:
                    existing_data = pd.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True)

            if existing_data.empty:
                return [no_update] * 17   

            filtered_df = existing_data.copy()

            # Fix inconsistent time format (add seconds if missing)
            filtered_df["time"] = filtered_df["time"].astype(str)
            filtered_df["time"] = filtered_df["time"].apply(lambda x: x if len(x) == 8 else x + ":00")

            # Create datetime column
            filtered_df["datetime"] = pd.to_datetime(
                filtered_df["date"].astype(str) + " " + filtered_df["time"].astype(str), 
                format="%Y-%m-%d %H:%M:%S", 
                errors="coerce"
            )
            filtered_df = filtered_df.dropna(subset=["datetime"])  # Drop invalid dates

            # Ensure date format is consistent for the table
            filtered_df["date"] = filtered_df["datetime"].dt.strftime("%Y-%m-%d")

            if user_id:
                filtered_df = filtered_df[filtered_df["user_id"].isin(user_id)]
            if module:
                filtered_df = filtered_df[filtered_df["module"].isin(module)]
            if start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
                filtered_df = filtered_df[(filtered_df["datetime"] >= start_date) & (filtered_df["datetime"] <= end_date)]
            if version:
                filtered_df = filtered_df[filtered_df["version"].isin(version)]
            if location:
                filtered_df = filtered_df[filtered_df["location"].isin(location)]

            active_users_fig = {}
            last_7_days_df = pd.DataFrame()

            if 'active-users' in visualizations:
                last_7_days_df = filtered_df[filtered_df['datetime'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
                active_users_fig = px.line(
                    last_7_days_df.groupby('datetime').user_id.nunique().reset_index(),
                    x='datetime',
                    y='user_id',
                    title="Active Users Over Time (Last 7 Days)"
                )

                total_users = filtered_df['user_id'].nunique()
                active_users_last_hour = filtered_df[filtered_df['datetime'] >= pd.Timestamp.now() - pd.Timedelta(hours=1)]['user_id'].nunique()
                active_users_last_7_days = last_7_days_df['user_id'].nunique()

                active_users_fig.add_annotation(
                    x=0.5, 
                    y=1.1,
                    xref="paper",
                    yref="paper", 
                    text=f"Total Users: {total_users}<br>Active Users (Last 1 Hour): {active_users_last_hour}<br>Active Users (Last 7 Days): {active_users_last_7_days}",
                    showarrow=False,  
                    font=dict(size=14),  
                    align="center", 
                    bgcolor="rgba(255, 255, 255, 0.7)" 
                )

                active_users_fig.update_xaxes(
                    tickmode="array",
                    tickformat="%Y-%m-%d", 
                    tickvals=[(pd.Timestamp.now() - pd.Timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)],
                    range=[(pd.Timestamp.now() - pd.Timedelta(days=7)).strftime('%Y-%m-%d'), pd.Timestamp.now().strftime('%Y-%m-%d')]
                )
                active_users_fig.update_layout(
                    xaxis_title=None,
                    yaxis_title=None
                )

            pie_fig = {}
            stacked_bar_fig = {}
            line_chart_fig = {}
            pie_fig_2 = {}

            if 'pie' in visualizations:
                pie_fig = create_pie_chart(filtered_df)

            if 'stacked-bar' in visualizations:
                stacked_bar_fig = create_stacked_bar_chart(filtered_df)

            if 'line-chart' in visualizations:
                line_chart_fig = create_line_chart(filtered_df) 
        
            if 'pie-2' in visualizations:
                if start_date:
                    pie_fig_2 = create_pie_chart_for_date(filtered_df, start_date)

            # Define visibility styles for the visualizations
            graph_styles = {'display': 'none'}
            table_style = {'display': 'none'}
            table_title_style = {'display': 'none'}

            active_users_style = pie_style = stacked_bar_style = line_chart_style = pie_style_2 = table_style = graph_styles.copy()
            if 'active-users' in visualizations:
                active_users_style = {'display': 'block'}
            if 'pie' in visualizations:
                pie_style = {'display': 'block'}
            if 'stacked-bar' in visualizations:
                stacked_bar_style = {'display': 'block'}
            if 'line-chart' in visualizations:
                line_chart_style = {'display': 'block'}
            if 'pie-2' in visualizations:
                pie_style_2 = {'display': 'block'}
            if 'table' in visualizations:
                table_style = {'display': 'block'}
                table_title_style = {'display': 'block'}

            return (
                active_users_fig, pie_fig, stacked_bar_fig, line_chart_fig, pie_fig_2,
                filtered_df.to_dict('records'),
                active_users_style, pie_style, stacked_bar_style,line_chart_style, pie_style_2,
                table_style, table_title_style,
                [{'label': user, 'value': user} for user in existing_data['user_id'].unique()],
                [{'label': module, 'value': module} for module in existing_data['module'].unique()],
                [{'label': version, 'value': version} for version in existing_data['version'].unique()],
                [{'label': location, 'value': location} for location in existing_data['location'].unique()]
            )

        except Exception as e:
            logging.error(f"Error in update_graphs: {e}", exc_info=True)
            return [no_update] * 17