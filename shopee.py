import pandas as pd
import numpy as np



#import data
excel_file = r'F:\Downloads\03 Python test and Dataset.xlsx'

pp_data = pd.read_excel(excel_file, sheet_name='pricing_project_dataset')
platform_number = pd.read_excel(excel_file, sheet_name='platform_number')
ex_rate = pd.read_excel(excel_file, sheet_name='exchange_rate')

#1. Cluster item lv into each portion (dataset is at model lv)

##order coverage
order_coverage = pp_data.groupby('grass_region')['shopee_order'].sum() / platform_number.groupby('region')['platform order'].sum()

##net competitiveness
net_competitiveness = pp_data.groupby('grass_region')['shopee_model_competitiveness_status'].apply(lambda x: (x.value_counts().get('Shopee < CPT', 0) - x.value_counts().get('Shopee > CPT', 0)) / x.count())

##number of item
total_items = pp_data.groupby('grass_region').size()

##ans 1
ans_1 = pd.DataFrame({
    'Order Coverage': order_coverage,
    'Net Competitiveness': net_competitiveness,
    '# of Item': total_items
}).reset_index()

##print(ans_1)


#2.write a python or pyspark code to re-arrange the data set to item_lv with the given priority

grouping = pp_data.groupby('shopee_item_id')

rearranged_data = []

for item_id, group in grouping:
    shopee_competitiveness_status = 'Others'

    # Check conditions
    if 'Shopee < CPT' in group['shopee_model_competitiveness_status'].values:
        shopee_competitiveness_status = 'Shopee < CPT'
    elif 'Shopee = CPT' in group['shopee_model_competitiveness_status'].values:
        shopee_competitiveness_status = 'Shopee = CPT'
    elif 'Shopee > CPT' in group['shopee_model_competitiveness_status'].values:
        shopee_competitiveness_status = 'Shopee > CPT'

    rearranged_data.append({
        'shopee_item_id': item_id,
        'shopee_competitiveness_status': shopee_competitiveness_status
    })

## ans_2
rearranged_df = pd.DataFrame(rearranged_data)

#print(rearranged_df)

#3. How many item at top 30% of model that contribute in highest order to platform by each country/region?

grouping = pp_data.groupby('grass_region')

top_30_percent_items = []

for region, group in grouping:
    # total order by item
    item_order = group.groupby('shopee_item_id')['shopee_order'].sum()

    # Sort item by order
    sorted_items = item_order.sort_values(ascending=False)

    #  top 30% items of models
    top_30_percent_threshold = int(0.3 * len(sorted_items))
    top_30_percent_items_count = len(sorted_items[:top_30_percent_threshold])

    top_30_percent_items.append({
        'Region': region,
        'Top 30% Items Count': top_30_percent_items_count
    })

# ans_3
top_30_percent_items_df = pd.DataFrame(top_30_percent_items)

#sorting
top_30_percent_items_df = top_30_percent_items_df.sort_values(by='Top 30% Items Count', ascending=False)

#print(top_30_percent_items_df)

#4 making visualization

import matplotlib.pyplot as mpl
import seaborn as sb

#order count by region
mpl.figure(figsize=(10, 6))
sb.countplot(data=pp_data, x='grass_region')
mpl.title('Order Counts by Region')
mpl.xlabel('Region')
mpl.ylabel('Order Count')
mpl.xticks(rotation=45)
mpl.tight_layout()

#top 30 item
top_30_percent_threshold = pp_data['shopee_order'].quantile(0.7)
top_30_percent_items = pp_data[pp_data['shopee_order'] >= top_30_percent_threshold]

#top 30 item by region
mpl.figure(figsize=(10, 6))
sb.countplot(data=top_30_percent_items, x='grass_region')
mpl.title('Number of Top 30% Items by Region')
mpl.xlabel('Region')
mpl.ylabel('Number of Items')
mpl.xticks(rotation=45)
mpl.show()

#competitiveness_status
mpl.figure(figsize=(8, 8))
rearranged_df['shopee_competitiveness_status'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140)
mpl.title('Distribution of Competitiveness Status')
mpl.ylabel('')
mpl.tight_layout()

#competitive status by region
mpl.figure(figsize=(10, 6))
sb.countplot(data=rearranged_df, x='grass_region', hue='shopee_model_competitiveness_status')
mpl.title('Competitiveness Status Distribution by Region')
mpl.xlabel('Region')
mpl.ylabel('Count')
mpl.xticks(rotation=45)
mpl.legend(title='Competitiveness Status')
mpl.tight_layout()


mpl.show()



