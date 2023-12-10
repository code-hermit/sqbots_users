import streamlit as st
import plotly.express as px
import pandas as pd

# Sample DataFrame with a single row of data

import random

def _generate_random_hex_color():
    """Generate a random hex color code."""
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))




def bar_plot_df(df,var_name,value_name,title):

# Transform the DataFrame to long format for plotting
    df_long = df.melt(var_name=var_name, value_name=value_name)

    # Streamlit app layout
    

    # Creating a bar plot
    fig = px.bar(df_long, x=var_name, y=value_name, 
                color=var_name,
                color_continuous_scale='Viridis', # Cool color scheme
                template='plotly_white') # Modern dark theme

    # Customize layout
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=var_name,
        yaxis_title=value_name,
        font=dict(family="Courier New, monospace", size=18, color="white")
    )
    return fig
    # Display the plot
    
def line_plot_df(data,var_name,value_name,title):
  

    # Convert the Series to a DataFrame for Plotly
    df = pd.DataFrame({var_name: data.index, value_name: data.values})

    # Streamlit app layout
    

    # Line plot using Plotly
    fig = px.line(df, x=var_name, y=value_name, 
                title=title,
                template='plotly_dark')

    # Customizing the plot
    fig.update_traces(line=dict(width=2, color=_generate_random_hex_color()), mode='lines+markers')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=var_name,
        yaxis_title=value_name,
        font=dict(family="Arial, sans-serif", size=16, color="white")
    )

    # Adding hover interaction
    fig.update_layout(hovermode='x unified')
    return fig
    # Display the plot in Streamlit
    

