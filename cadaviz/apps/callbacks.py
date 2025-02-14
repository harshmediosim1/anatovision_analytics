import logging
from dash.dependencies import Input, Output
from dash import no_update
import pandas as pd
import plotly.express as px
from apps.data_processing import fetch_data
from apps.charts import create_pie_chart, create_stacked_bar_chart, create_treemap, create_heatmap

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Global variable to store existing data
existing_data = pd.DataFrame()

def register_callbacks(app):
    @app.callback(
        [
            Output('active-users-line-chart', 'figure'),
            Output('pie-chart', 'figure'),
            Output('stacked-bar-chart', 'figure'),
            Output('treemap', 'figure'),
            Output('heatmap', 'figure'),
            Output('data-table', 'data'),
            Output('active-users-line-chart', 'style'),
            Output('pie-chart', 'style'),
            Output('stacked-bar-chart', 'style'),
            Output('treemap', 'style'),
            Output('heatmap', 'style'),
            Output('data-table-container', 'style'),
            Output('table-title', 'style')
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
                return no_update  

            filtered_df = existing_data.copy()
            filtered_df['date'] = pd.to_datetime(filtered_df['date']).dt.strftime('%Y-%m-%d')
            filtered_df['datetime'] = pd.to_datetime(
                filtered_df['date'].astype(str) + ' ' + filtered_df['time'].astype(str), errors='coerce'
            )

            if user_id:
                filtered_df = filtered_df[filtered_df['user_id'].isin(user_id)]
            if module:
                filtered_df = filtered_df[filtered_df['module'].isin(module)]
            if start_date and end_date:
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
                filtered_df = filtered_df[(filtered_df['datetime'] >= start_date) & (filtered_df['datetime'] <= end_date)]
            if version:
                filtered_df = filtered_df[filtered_df['version'].isin(version)]
            if location:
                filtered_df = filtered_df[filtered_df['location'].isin(location)]

            # ✅ Fixed Condition to Ensure "No Data Available" Message Works
            if not visualizations or len(visualizations) == 0:
                print("No visualizations selected. Showing 'No Data Available' message.")
                no_data_message = {
                   # "data": [], 
                    "layout": {
                        "xaxis": {"visible": False},
                        "yaxis": {"visible": False},
                        "annotations": [
                            {
                                "text": "No Data Available",
                                "xref": "paper",
                                "yref": "paper",
                                "x": 0.5,
                                "y": 0.5,
                                "showarrow": False,
                                "font": {"size": 24, "color": "Blue"},
                                "align": "center",
                                "xanchor": "center",
                                "yanchor": "middle",
                                "bgcolor": "rgba(255, 255, 255, 0.9)",
                                "bordercolor": "blue",
                                "borderwidth": 2
                            }
                        ]
                    }
                }
                
                return (
                    no_data_message, no_data_message, no_data_message, no_data_message, no_data_message, 
                    [],  # Empty table
                    {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'},  
                    {'display': 'none'}, {'display': 'none'}
                )

            #  Generate Charts
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

                # Add annotations with active user metrics for the entire data
                total_users = filtered_df['user_id'].nunique()
                active_users_last_hour = filtered_df[
                    filtered_df['datetime'] >= pd.Timestamp.now() - pd.Timedelta(hours=1)
                ]['user_id'].nunique()
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
            treemap_fig = {}
            heatmap_fig = {}

            if 'pie' in visualizations:
                pie_fig = create_pie_chart(filtered_df)

            if 'stacked-bar' in visualizations:
                stacked_bar_fig = create_stacked_bar_chart(filtered_df)

            if 'treemap' in visualizations:
                treemap_fig = create_treemap(filtered_df)

            if 'heatmap' in visualizations:
                heatmap_fig = create_heatmap(filtered_df)

            graph_styles = {'display': 'none'}
            table_style = {'display': 'none'}
            table_title_style = {'display': 'none'}

            active_users_style = pie_style = stacked_bar_style = treemap_style = heatmap_style = table_style = graph_styles.copy()
            if 'active-users' in visualizations:
                active_users_style = {'display': 'block'}
            if 'pie' in visualizations:
                pie_style = {'display': 'block'}
            if 'stacked-bar' in visualizations:
                stacked_bar_style = {'display': 'block'}
            if 'treemap' in visualizations:
                treemap_style = {'display': 'block'}
            if 'heatmap' in visualizations:
                heatmap_style = {'display': 'block'}
            if 'table' in visualizations:
                table_style = {'display': 'block'}
                table_title_style = {'display': 'block'}

            return (
                active_users_fig, pie_fig, stacked_bar_fig, treemap_fig, heatmap_fig,
                filtered_df.to_dict('records'),
                active_users_style, pie_style, stacked_bar_style, treemap_style, heatmap_style,
                table_style, table_title_style
            )

        except Exception as e:
            logging.error(f"Error in update_graphs: {e}", exc_info=True)
            return [no_update] * 13  
