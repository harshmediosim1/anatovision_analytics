import plotly.express as px
import pandas as pd

def create_pie_chart(filtered_df):
    return px.pie(
        filtered_df, 
        names='module', 
        values='duration', 
        title="Total Time Spent per Module",
        color_discrete_sequence=px.colors.qualitative.Plotly 
    )

def create_stacked_bar_chart(filtered_df ,title_color='Red'):
    filtered_df['duration'] = pd.to_numeric(filtered_df['duration'], errors='coerce')
    top_modules = filtered_df.groupby('module')['duration'].sum().nlargest(5).index
    top_modules_df = filtered_df[filtered_df['module'].isin(top_modules)]
    
    fig = px.bar(
        top_modules_df, 
        x='date', 
        y='duration', 
        color='module',  
        title="Total Usage (Top 5 Modules) vs Date", 
        barmode='stack',  
        color_discrete_sequence=px.colors.qualitative.Plotly,  
        hover_data={  
            'module': True, 
            'duration': True, 
            'date': True,  
        }
    )

    return fig

def create_line_chart(filtered_df):
    filtered_df['duration'] = pd.to_numeric(filtered_df['duration'], errors='coerce')
    filtered_df['date'] = pd.to_datetime(filtered_df['date'], errors='coerce')

    duration_by_college = filtered_df.groupby(['date', 'college'])['duration'].sum().reset_index()

    fig = px.line(
        duration_by_college,
        x='date',            
        y='duration',       
        color='college',    
        title="Total Duration (College) Vs Date",  
        labels={"duration": "Total Duration", "date": "Date", "college": "College"},  
        line_shape='linear', 
        markers=True         
    )
    fig.update_traces(
        hovertemplate="<b>College:</b> %<br><b>Date:</b> %{x}<br><b>Duration:</b> %{y} Minutes",
        text=duration_by_college['college']
    )
    fig.update_layout(
        xaxis_title="Date",         
        yaxis_title="Total Duration (Minutes)", 
        title_font=dict(size=18),  
        xaxis=dict(tickformat="%Y-%m-%d"),  
        hovermode="x unified"      
    )

    return fig

def create_pie_chart_for_date(filtered_df, start_date, title_color='Green'):
    single_day_data = filtered_df[filtered_df['date'] == start_date.strftime('%Y-%m-%d')]
    module_duration = single_day_data.groupby('module')['duration'].sum().reset_index()
    module_duration.columns = ['module', 'total_duration']
    
    pie_fig_2 = px.pie(
        module_duration, 
        names='module', 
        values='total_duration', 
        title=f"Module Usage Duration on {start_date.strftime('%Y-%m-%d')}"
    )

    return pie_fig_2
