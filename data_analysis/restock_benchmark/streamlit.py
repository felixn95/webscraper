import pandas as pd
import streamlit as st

# How to run the app
# have streamlit installed (pip install streamlit)
# run the app with streamlit run streamlit.py

# read in kpis
df_combined = pd.read_csv('data/combined_kpis.csv')

# discard columns 'reorder_stock_level', 'avg_time_to_restock'
#df_combined = df_combined.drop(columns=['reorder_stock_level', 'avg_time_to_restock'])

# Rearrange columns to make store_name the first column and put store id to the end
columns = list(df_combined.columns)
columns.insert(0, columns.pop(columns.index('store_name')))
columns.append(columns.pop(columns.index('store_storeId')))
df_combined = df_combined[columns]

# Streamlit app
st.title('Stock Management Analysis')


# Filters for interactive exploration
st.sidebar.header('Filter Data')
sub_category_filter = st.sidebar.multiselect(
    'Select Sub Categories',
    options=df_combined['sub_category'].unique(),
    default=df_combined['sub_category'].unique()
)

price_range_filter = st.sidebar.multiselect(
    'Select Price Ranges',
    options=df_combined['price_range'].unique(),
    default=df_combined['price_range'].unique()
)

store_name_filter = st.sidebar.multiselect(
    'Select Store Names',
    options=df_combined['store_name'].unique(),
    default=df_combined['store_name'].unique()
)

filtered_data = df_combined[
    (df_combined['sub_category'].isin(sub_category_filter)) &
    (df_combined['price_range'].isin(price_range_filter)) &
    (df_combined['store_name'].isin(store_name_filter))
]

# Display filtered data
st.header('Filtered Combined Data')
st.write('Oberserved 12 stores in central NRW from mid-may to end of june 2024')
st.dataframe(filtered_data)

# Additional aggregation options
st.sidebar.header('Aggregation Options')
aggregation_column = st.sidebar.selectbox(
    'Select column to aggregate',
    options=df_combined.columns.difference(['sub_category', 'price_range', 'store_name'])
)

aggregation_function = st.sidebar.selectbox(
    'Select aggregation function',
    options=['sum', 'mean', 'max', 'min']
)

if aggregation_function == 'sum':
    aggregated_data = filtered_data.groupby('sub_category').sum()[aggregation_column]
elif aggregation_function == 'mean':
    aggregated_data = filtered_data.groupby('sub_category').mean()[aggregation_column]
elif aggregation_function == 'max':
    aggregated_data = filtered_data.groupby('sub_category').max()[aggregation_column]
elif aggregation_function == 'min':
    aggregated_data = filtered_data.groupby('sub_category').min()[aggregation_column]

st.header('Aggregated Data')
st.write(aggregated_data)