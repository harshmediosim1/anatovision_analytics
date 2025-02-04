from dash.dependencies import Input, Output
from dash import dcc
import pandas as pd
import plotly.express as px
from apps.data_processing import fetch_data  # ✅ Import function to get data
from apps.charts import create_pie_chart, create_stacked_bar_chart, create_treemap, create_heatmap

# ✅ Fetch data globally
df = fetch_data()

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
            Output('table-title', 'style')  # ✅ Add title visibility as an output
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
        filtered_df = df.copy()

        # ✅ Ensure the date is formatted as 'YYYY-MM-DD'
        filtered_df['date'] = pd.to_datetime(filtered_df['date']).dt.strftime('%Y-%m-%d')

        # ✅ Ensure the date and time columns are in datetime format
        filtered_df['datetime'] = pd.to_datetime(
            filtered_df['date'].astype(str) + ' ' + filtered_df['time'].astype(str), errors='coerce'
        )

        # ✅ Apply filters
        if user_id:
            filtered_df = filtered_df[filtered_df['user_id'].isin(user_id)]
        if module:
            filtered_df = filtered_df[filtered_df['module'].isin(module)]
        if start_date and end_date:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date).replace(hour=23, minute=59, second=59, microsecond=999999)
            filtered_df = filtered_df[
                (filtered_df['datetime'] >= start_date) & (filtered_df['datetime'] <= end_date)
            ]
        if version:
            filtered_df = filtered_df[filtered_df['version'].isin(version)]
        if location:
            filtered_df = filtered_df[filtered_df['location'].isin(location)]

        active_users_fig = {}

        # ✅ Generate Active Users graph with annotations
        if 'active-users' in visualizations:
            active_users_fig = px.line(
                filtered_df.groupby('datetime').user_id.nunique().reset_index(),
                x='datetime',
                y='user_id',
                title="Active Users Over Time"
            )

            # ✅ Add annotations with active users metrics
            total_users = filtered_df['user_id'].nunique()
            active_users_last_hour = filtered_df[
                filtered_df['datetime'] >= pd.Timestamp.now() - pd.Timedelta(hours=1)
            ]['user_id'].nunique()
            active_users_last_7_days = filtered_df[
                filtered_df['datetime'] >= pd.Timestamp.now() - pd.Timedelta(days=7)
            ]['user_id'].nunique()

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

        # ✅ Placeholder for other graphs
        pie_fig = {}
        stacked_bar_fig = {}
        treemap_fig = {}
        heatmap_fig = {}

        # ✅ Generate Pie Chart
        if 'pie' in visualizations:
            pie_fig = create_pie_chart(filtered_df)

        # ✅ Generate Stacked Bar Chart
        if 'stacked-bar' in visualizations:
            stacked_bar_fig = create_stacked_bar_chart(filtered_df)

        # ✅ Generate Treemap
        if 'treemap' in visualizations:
            treemap_fig = create_treemap(filtered_df)

        # ✅ Generate Heatmap
        if 'heatmap' in visualizations:
            heatmap_fig = create_heatmap(filtered_df)

        # ✅ Handle visibility for the graphs and the table
        graph_styles = {'display': 'none'}  # Initially hide all graphs and table
        table_style = {'display': 'none'}   # Hide data table initially
        table_title_style = {'display': 'none'}  # Initially hide the title

        # ✅ Set the style to block for the selected visualizations
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
            table_title_style = {'display': 'block'}  # ✅ Show the title when the table is selected

        # ✅ Update Data Table and title visibility
        return (
            active_users_fig, pie_fig, stacked_bar_fig, treemap_fig, heatmap_fig,
            filtered_df.to_dict('records'),
            active_users_style, pie_style, stacked_bar_style, treemap_style, heatmap_style,
            table_style, table_title_style
        )


