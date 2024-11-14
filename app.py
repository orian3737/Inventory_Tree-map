import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from color_themes import get_categorical_colors, get_continuous_colors  # Import theme functions
#excel file reder and interpretor


def main():
    st.set_page_config(page_title="Data Visualization App", layout="wide")
    st.title("📊 Data Visualization App")

    # Select color theme options
    categorical_theme = st.sidebar.selectbox("Select Categorical Color Theme", ["theme1", "theme2"])
    continuous_theme = st.sidebar.selectbox("Select Continuous Color Gradient", ["warm_gradient", "cool_gradient"])

    # Get selected color themes
    custom_categorical_colors = get_categorical_colors(categorical_theme)
    custom_continuous_colors = get_continuous_colors(continuous_theme)

    # File uploader
    uploaded_file = st.file_uploader("Upload a data file", type=['xls', 'xlsx', 'csv', 'sql'])

    # Check if a file has been uploaded
    if uploaded_file:
        file_extension = uploaded_file.name.split('.')[-1]
        try:
            # Load data based on file extension
            if file_extension in ['xls', 'xlsx']:
                inventory_df = pd.read_excel(uploaded_file)
            elif file_extension == 'csv':
                inventory_df = pd.read_csv(uploaded_file)
            elif file_extension == 'sql':
                conn = sqlite3.connect(":memory:")
                with open(uploaded_file, 'r') as f:
                    conn.executescript(f.read())
                table_name = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn).iloc[0, 0]
                inventory_df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
                conn.close()

            st.success("File uploaded successfully!")
            st.write("**Preview of the data:**")
            st.dataframe(inventory_df)

            if inventory_df.empty:
                st.warning("The uploaded file seems empty or improperly formatted.")
                return

            # Analyze columns to select appropriate visualization
            st.subheader("Generated Visualization")
            categorical_columns = inventory_df.select_dtypes(include=['object']).columns
            numeric_columns = inventory_df.select_dtypes(include=['float64', 'int64']).columns

            # Apply rules to select the appropriate graph
            if len(categorical_columns) == 1 and len(numeric_columns) == 1:
                fig = px.bar(
                    inventory_df, 
                    x=categorical_columns[0], 
                    y=numeric_columns[0], 
                    title='Bar Chart',
                    text_auto=True,
                    color=numeric_columns[0], 
                    color_discrete_sequence=custom_categorical_colors
                )
                fig.update_layout(xaxis_title=categorical_columns[0], yaxis_title=numeric_columns[0])
                st.plotly_chart(fig, use_container_width=True)
                
            elif len(numeric_columns) == 2:
                fig = px.scatter(
                    inventory_df, 
                    x=numeric_columns[0], 
                    y=numeric_columns[1], 
                    title='Scatter Plot',
                    trendline="ols",
                    color=numeric_columns[0], 
                    size=numeric_columns[1],
                    color_continuous_scale=custom_continuous_colors
                )
                fig.update_layout(xaxis_title=numeric_columns[0], yaxis_title=numeric_columns[1])
                st.plotly_chart(fig, use_container_width=True)

            elif len(numeric_columns) > 2:
                fig = px.scatter_matrix(
                    inventory_df, 
                    dimensions=numeric_columns, 
                    title='Scatter Matrix',
                    color=categorical_columns[0] if len(categorical_columns) > 0 else None,
                    color_discrete_sequence=custom_categorical_colors
                )
                fig.update_traces(diagonal_visible=False)
                st.plotly_chart(fig, use_container_width=True)
                
            elif len(categorical_columns) == 1 and len(numeric_columns) == 1:
                fig = px.treemap(
                    inventory_df, 
                    path=[categorical_columns[0]], 
                    values=numeric_columns[0], 
                    title='Treemap',
                    color=numeric_columns[0],
                    color_continuous_scale=custom_continuous_colors
                )
                fig.update_traces(root_color="lightgrey")
                st.plotly_chart(fig, use_container_width=True)
                
            else:
                if numeric_columns.any():
                    fig = px.histogram(
                        inventory_df, 
                        x=numeric_columns[0], 
                        title='Histogram',
                        nbins=30,
                        color_discrete_sequence=custom_categorical_colors[:1]
                    )
                    fig.update_layout(xaxis_title=numeric_columns[0], yaxis_title="Frequency")
                    st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")
            st.write("""
            **Troubleshooting Tips**:
            - Ensure the file format matches the selected file type.
            - If it’s a SQL file, confirm that it contains valid SQL commands.
            - Check if the table name in the SQL file matches your data structure.
            """)

if __name__ == "__main__":
    main()
