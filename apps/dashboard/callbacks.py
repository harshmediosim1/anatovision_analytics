import dash
from dash.dependencies import Input, Output, State
from dash import no_update
import pandas as pd
import plotly.express as px
from apps.dashboard.data_processing import fetch_data
from apps.dashboard.charts import create_pie_chart, create_stacked_bar_chart, create_line_chart, create_pie_chart_for_date
from apps.dashboard.logger import logger

def register_callbacks(app):
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
            Output('location-filter', 'options'),
            Output('no-visualization-message', 'style') 
        ],
        [
            Input('user-id-filter', 'value'),
            Input('module-filter', 'value'),
            Input('date-picker-range', 'start_date'),
            Input('date-picker-range', 'end_date'),
            Input('version-filter', 'value'),
            Input('location-filter', 'value'),
            Input('visualization-filter', 'value'),
            Input('interval-component', 'n_intervals') # Added interval for auto-refresh
        ]  
    )
    def update_graphs(user_id, module, start_date, end_date, version, location, visualizations, n_intervals):
        try:
            filtered_df, _ = fetch_data()

            if filtered_df.empty:
                logger.warning("No data available for filtering")
                return [no_update] * 18

            # Fix inconsistent time format (add seconds if missing)
            filtered_df["time"] = filtered_df["time"].astype(str)
            filtered_df["time"] = filtered_df["time"].apply(lambda x: x if len(x) == 8 else x + ":00")

            # Create datetime column
            filtered_df["datetime"] = pd.to_datetime(
                filtered_df["date"].astype(str) + " " + filtered_df["time"].astype(str), 
                format="%Y-%m-%d %H:%M:%S", 
                errors="coerce"
            )
            filtered_df = filtered_df.dropna(subset=["datetime"])  
            filtered_df["date"] = filtered_df["datetime"].dt.strftime("%Y-%m-%d")

            # Filter data based on user selections
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

            if filtered_df.empty:
                logger.warning("Filtered DataFrame is empty after applying filters.")
                return [no_update] * 18

            active_users_fig = {}
            last_7_days_df = pd.DataFrame()

            visualizations = visualizations or []

            if 'active-users' in visualizations:
               last_7_days_df = filtered_df[filtered_df['datetime'] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
               active_users_df = last_7_days_df.groupby('datetime').user_id.nunique().reset_index()

               # Create the active users line chart
               active_users_fig = px.line(
                   active_users_df,
                   x='datetime',
                   y='user_id',
                   title="Active Users Over Time (Last 7 Days)"
               )

               # Calculate total unique users, active users in the last hour, and active users in the last 7 days
               total_users = filtered_df['user_id'].nunique()
               active_users_last_hour = filtered_df[filtered_df['datetime'] >= pd.Timestamp.now() - pd.Timedelta(hours=1)]['user_id'].nunique()
               active_users_last_7_days = last_7_days_df['user_id'].nunique()

               # Add an annotation with these statistics
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
                modebar=dict(
                    remove=[
                        "zoomIn", "zoomOut", "pan", "resetScale", "zoom", "saveImage", 
                        "select2d", "lasso2d", "hoverClosestCartesian", "hoverCompareCartesian", 
                        "Box Select", "Autoscale" ]
                ),
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
                    pie_fig_2 = create_pie_chart_for_date(filtered_df, pd.to_datetime(start_date))

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

             # Show the message if no visualizations are selected
            no_visualization_message_style = {'display': 'block', 'fontWeight': 'bold','fontSize': '25px','color': '#0010d3','textAlign': 'center',} if not visualizations else {'display': 'none'}
            
            # Recompute options to match available data
            df_full, _ = fetch_data()
            return (
                active_users_fig, pie_fig, stacked_bar_fig, line_chart_fig, pie_fig_2,
                filtered_df.to_dict('records'),
                active_users_style, pie_style, stacked_bar_style,line_chart_style, pie_style_2,
                table_style, table_title_style,
                [{'label': user, 'value': user} for user in df_full['user_id'].unique()],
                [{'label': module, 'value': module} for module in df_full['module'].unique()],
                [{'label': version, 'value': version} for version in df_full['version'].unique()],
                [{'label': location, 'value': location} for location in df_full['location'].unique()],
                no_visualization_message_style
            )
        except Exception as e:
            logger.error(f"Error in update_graphs: {e}", exc_info=True)
            return [no_update] * 18
