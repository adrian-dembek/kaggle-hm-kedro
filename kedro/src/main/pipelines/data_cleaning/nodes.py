"""
This is a boilerplate pipeline 'data_cleaning'
generated using Kedro 0.18.0
"""
def clean_articles(articles):

    print('cleaning articles df...')
    articles_cleaned = articles[['article_id', 
                                 'product_code',
                                 'prod_name',
                                 'product_type_name', 
                                 'product_group_name', 
                                 'graphical_appearance_name',
                                 'colour_group_name',
                                 'perceived_colour_value_name',
                                 'perceived_colour_master_name',
                                 'department_name',
                                 'index_name',
                                 'index_group_name',
                                 'section_name',
                                 'garment_group_name',
                                 'detail_desc'
                                ]]
    
    return articles_cleaned


def clean_customers(customers):
    import pandas as pd
    
    print('cleaning customers df...')
    customers['if_fashion_news'] = customers['FN'].apply(lambda x: True if x==1.0 else False)
    customers['if_active'] = customers['Active'].apply(lambda x: True if x==1.0 else False)
        
    customers['fashion_news_frequency'] = customers['fashion_news_frequency'].apply(lambda x: 'None' if pd.isna(x) or x=='NONE' else x)
    
    customers_cleaned = customers[['customer_id', 
                                   'postal_code',
                                   'age', 
                                   'if_active',
                                   'club_member_status',
                                   'if_fashion_news', 
                                   'fashion_news_frequency'
                                  ]]
    
    print('\n', 'customers_cleaned:', customers_cleaned.columns, '\n')
    
    return customers_cleaned


def clean_transactions(transactions):
    import pandas as pd
    import uuid
    
    print('cleaning transactions df...')
    transactions.rename(columns={'t_dat': 't_date'}, inplace=True)
    print('t_dat renamed to t_date')


    print('sort transactions by customer_id & t_date & sales_channel_id')
    transactions = transactions.sort_values(['customer_id', 't_date', 'sales_channel_id'])

    print('calculate nth_shopping_day_for_cust')
    transactions['nth_shopping_day_for_cust'] = transactions\
                                                .groupby('customer_id')['t_date']\
                                                .apply(lambda x: (~pd.Series(x).duplicated()).cumsum())
    
    print('create cust_nth_basket by concatenating customer_id, nth_shopping_day_for_cust and sales_channel_id')
    transactions['cust_nth_basket'] = transactions['customer_id'] + '_' + \
                                        transactions['nth_shopping_day_for_cust'].apply(lambda x: str(x)) + '_' + \
                                        transactions['sales_channel_id'].apply(lambda x: str(x)) 
    
    print('create basket_ids dataframe')
    basket_ids = transactions[['cust_nth_basket']].drop_duplicates()
    
    print('create basket_id with uuid64')
    basket_ids['basket_id'] = basket_ids['cust_nth_basket'].apply(lambda _: str(uuid.uuid4()))

    print('join basket_ids to transactions')
    transactions = transactions\
                    .merge(basket_ids, on='cust_nth_basket')\
                    .drop(columns=['nth_shopping_day_for_cust', 'cust_nth_basket'])

    print('create basket_item_id with uuid64')
    transactions['basket_item_id'] = transactions['article_id'].apply(lambda _: str(uuid.uuid4()))
    
    print('create dummy if_online_sales_channel')
    transactions['if_online_sales_channel'] = transactions['sales_channel_id'].apply(lambda x: 1 if x==1 else 0)

    print('create baskets_cleaned df')
    baskets_cleaned = transactions[['basket_id', 'customer_id', 't_date', 'if_online_sales_channel']].drop_duplicates()\
        .reset_index().drop(columns='index') # needed to prevent error: feather does not support serializing a non-default index for the index; you can .reset_index() to make the index into column(s)

    print('create transactions_cleaned df')
    transactions_cleaned = transactions[['basket_item_id', 'basket_id', 'article_id', 'price']]

    return transactions_cleaned, baskets_cleaned