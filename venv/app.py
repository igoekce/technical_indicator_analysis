import streamlit as st
import pandas as pd
import numpy as np
import base64

# Load the first dataframe
filtered_df1 = pd.read_csv('data/filtered_df_1.csv', index_col=0)

# Load the second dataframe
#filtered_df2 = pd.read_csv('data/filtered_df_2.csv', index_col=0)

# Load sentiment data from CSV file
sentiment_df = pd.read_csv('data/sentiment_data.csv')

# Add a title and some text to the app
st.title('Investment Strategy Dashboard')

# Create the sidebar navigation
nav_selection = st.sidebar.radio('Navigation', ['Stocks', 'Indices'])

if nav_selection == 'Stocks':
    st.write("Number of columns in Stocks:", len(filtered_df1.columns))

    # Get the last 5 rows of the DataFrame
    last_5_rows = filtered_df1.tail(5)

    # Get the columns that have the selected value in their last 5 rows
    select_value = st.selectbox('Select a value', [0, 1, 2, 3])
    selected_columns = last_5_rows.columns[last_5_rows.isin([select_value]).any()]

    # Display the selected columns
    #st.write("Selected Columns")
    #st.write(selected_columns)

    # Count the occurrences of the selected value in the selected columns
    value_count = last_5_rows[selected_columns].eq(select_value).sum().sum()

    # Display the count of the selected value
    st.write("Count of Selected Value:", value_count)

    # Navigation box for plotting selected item
    if selected_columns.empty:
        st.write("No items found")
    else:
        # Rest of your code, e.g. plotting the selected columns
        plot_selection = st.selectbox('Select an item to plot', selected_columns)
        st.line_chart(last_5_rows[plot_selection])


    # Display the information in an info box for Stocks
    st.info('This is Stocks. It represents the first dataset.')
    # Display the information in an info box

    st.info('This strategy tries to identify buy and sell signals.\n\n'
            'It uses the following assumptions:\n\n'
            'SMA_50 > SMA_200 = Buy\n\n'
            'SMA_50 < SMA_200 = Sell\n\n'
            'RSI < 30 = Buy\n\n'
            'RSI > 70 = Sell\n\n'
            'MACD > 0 = Buy\n\n'
            'MACD < 0 = Sell\n\n'
            'stock_price < bollinger_lband = Buy\n\n'
            'stock_price > _bollinger_hband = Sell\n\n')

elif nav_selection == 'Indices':
#    st.write("Number of columns in Indices:", len(filtered_df2.columns))

    # Create a dropdown list for column selection
#    selected_column = st.selectbox('Select a column to plot', filtered_df2.columns)

    # Plot the selected column
#    st.line_chart(filtered_df2[selected_column])

    st.info('This is Indices. It represents the second dataset.')

    # Display the sentiment data for Indices with color
    st.write("Sentiment Data for Indices")
    sentiment_df_styled = sentiment_df.style.applymap(
        lambda x: 'background-color: #90EE90' if x == 'Buy' else 'background-color: #FFC0CB' if x == 'Sell' else '')
    st.dataframe(sentiment_df_styled)

# Add a link to the app.py file
st.markdown('[Link to stockanalysis](https://stockanalysis.com/)')
