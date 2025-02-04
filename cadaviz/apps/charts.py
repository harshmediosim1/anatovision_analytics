import plotly.express as px

def create_pie_chart(filtered_df):
    return px.pie(
        filtered_df, 
        names='module', 
        values='duration', 
        title="Total Time Spent per Module",
        color_discrete_sequence=px.colors.qualitative.Plotly # You can choose a different set of colors like 'Set3', 'Paired', etc.
    )

# Helper function to create Stacked Bar Chart
# Helper function to create Stacked Bar Chart with hover data (including time)
def create_stacked_bar_chart(filtered_df):
    return px.bar(
        filtered_df, 
        x='module', 
        y='duration', 
        color='submodule', 
        title="Time Spent per Submodule by Module", 
        barmode='stack',
        color_continuous_scale='Cividis',
        hover_data={  # Adding time to the hover data
            'module': True, 
            'submodule': True, 
            'duration': True, 
            'time': True,
            'date': True  # Adding time to hover data
        }
    )

# Helper function to create Treemap
# Helper function to create Treemap with hover data (including time)
def create_treemap(filtered_df):
    return px.treemap(
        filtered_df, 
        path=['module', 'submodule'], 
        values='duration', 
        title="Time Spent per Module and Submodule",
        color_continuous_scale='Inferno',
        hover_data={
            'module': True, 
            'submodule': True, 
            'duration': True,
            'time': True  # Adding time to hover data
        }
    )


# Helper function to create Heatmap
def create_heatmap(filtered_df):
    return px.density_heatmap(
        filtered_df, 
        x='date', 
        y='module', 
        z='duration', 
        title="Time Spent Across Modules and Dates",
        color_continuous_scale='Rainbow'
    )