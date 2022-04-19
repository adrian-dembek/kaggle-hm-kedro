"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.0
"""
def define_entity_set(articles, 
                      customers, 
                      transactions, 
                      baskets,
                      intresting_articles_values_dict,
                      interesting_baskets_values_dict,
                      interesting_customers_values_dict):
    
    # https://featuretools.alteryx.com/en/stable/getting_started/using_entitysets.html#Creating-an-EntitySet
        
    import featuretools as ft
    from woodwork.logical_types import Boolean, Double, Categorical, Ordinal, PostalCode, Datetime, AgeNullable, NaturalLanguage

    es = ft.EntitySet(id='hm')

    # add dataframes
    es = es.add_dataframe(
        dataframe_name="baskets",
        dataframe=baskets,
        index="basket_id",
        time_index="t_date",
        logical_types={
            "basket_id": Categorical,
            "customer_id": Categorical,
            "if_online_sales_channel": Boolean,
            "t_date": Datetime
            },
        ).add_dataframe(
        dataframe_name="transactions",
        dataframe=transactions,
        index="basket_item_id",
        logical_types={
            "basket_item_id": Categorical,
            "basket_id": Categorical,
            "article_id": Categorical,
            "price": Double,
            },
        ).add_dataframe(
        dataframe_name="customers",
        dataframe=customers,
        index="customer_id",
        logical_types={
            "customer_id": Categorical,
            "club_member_status": Categorical,
            "fashion_news_frequency": Ordinal(order=['None', 'Monthly', 'Regularly']),
            "age": AgeNullable,
            "postal_code": PostalCode,
            "if_fashion_news": Boolean,
            "if_active": Boolean
            },
        ).add_dataframe(
        dataframe_name="articles",
        dataframe=articles,
        index="article_id",
        logical_types={
            "article_id": Categorical,
            "prod_name": Categorical,
            "product_group_name": Categorical,
            "product_type_name": Categorical,
            "colour_group_name": Categorical,
            "perceived_colour_value_name": Categorical,
            "detail_desc": NaturalLanguage
            }
        )
        
    ####################
    # RELATIONSHIPS
    # https://featuretools.alteryx.com/en/stable/getting_started/using_entitysets.html#Adding-a-Relationship
    es = es\
        .add_relationship("articles", "article_id", "transactions", "article_id")\
        .add_relationship("baskets", "basket_id", "transactions", "basket_id")\
        .add_relationship("customers", "customer_id", "baskets", "customer_id")
    
    ####################
    # INTERESTING VALUES
    es.add_interesting_values(dataframe_name='customers', values=interesting_customers_values_dict)
    es.add_interesting_values(dataframe_name='articles', values=intresting_articles_values_dict)
    es.add_interesting_values(dataframe_name='baskets', values=interesting_baskets_values_dict)
    
    ####################
    # LAST TIME INDEXES
    # add last time indexes - https://docs.featuretools.com/en/v0.16.0/automated_feature_engineering/handling_time.html
    es.add_last_time_indexes()
    
    print(es)
    
    return es


def get_selected_fs_params(selected_fs_dates, 
                           selected_fs_windows, 
                           selected_agg_primitives,
                           selected_trans_primitives,
                           selected_where_primitives):
    
    import pandas as pd
    from featuretools import Timedelta
    from featuretools import primitives
    
    ##########
    # FS DATES
    # for each date, create timestamp object - needed as featuretools input
    
    
    selected_fs_dates_timestamps = pd.DataFrame([pd.Timestamp(x) for x in selected_fs_dates], 
                                                columns=['time'])
    
    print(selected_fs_dates_timestamps)
    
    ##########
    # WINDOWS
    # provide all possible arguments that fs will be choosing from
    windows_dict = {'EVER': None,
                       '1Y': Timedelta(1, unit='Y'),
                       '9M': Timedelta(9, unit='mo'),
                       '6M': Timedelta(6, unit='mo'),
                       '3M': Timedelta(3, unit='mo'),
                       '8W': Timedelta(56, unit='d'),
                       '4W': Timedelta(28, unit='d'),
                       '2W': Timedelta(14, unit='d'),
                       '1W': Timedelta(7, unit='d')
                      }

    selected_fs_windows_dict = {selected: windows_dict[selected] for selected in selected_fs_windows}
    
    
    ##########
    # AGG

    selected_agg_primitives_ft = [getattr(primitives, x) for x in selected_agg_primitives if '(' not in x] + \
                                    [getattr(primitives, x.split('(')[0])(**eval(x.split('(')[1][:-1])) for x in selected_agg_primitives if '(' in x]
    print('selected_agg_primitives_ft:', selected_agg_primitives_ft)

    ##########
    # TRANS
    selected_trans_primitives_ft = [getattr(primitives, x) for x in selected_trans_primitives if '(' not in x] + \
                                    [getattr(primitives, x.split('(')[0])(**eval(x.split('(')[1][:-1])) for x in selected_trans_primitives if '(' in x]

    print('selected_trans_primitives_ft:', selected_trans_primitives_ft)
    
    ##########
    # WHERE
    selected_where_primitives_ft = [getattr(primitives, x) for x in selected_where_primitives if '(' not in x] + \
                                    [getattr(primitives, x.split('(')[0])(**eval(x.split('(')[1][:-1])) for x in selected_where_primitives if '(' in x]

    print('selected_where_primitives_ft:', selected_where_primitives_ft)
    
    return selected_fs_dates_timestamps, selected_fs_windows_dict, selected_agg_primitives_ft, selected_trans_primitives_ft, selected_where_primitives_ft


def calculate_entity_fs(articles, 
                        customers, 
                        transactions, 
                        baskets, 
                        intresting_articles_values_dict,
                        interesting_baskets_values_dict,
                        interesting_customers_values_dict,
                        entity,
                        selected_fs_dates,
                        selected_fs_windows,
                        selected_agg_primitives,
                        selected_trans_primitives,
                        selected_where_primitives,
                        max_depth, n_jobs):
    
    '''
    PARAMS
    entity: type of observations for which the fs is calculated, e.g. 'articles', 'customers'
    '''
    
   
    import pandas as pd
    from dask.distributed import LocalCluster
    import featuretools as ft
    from featuretools import Timedelta
    import warnings

    from woodwork.logical_types import Boolean, Double, Categorical, Ordinal, PostalCode, Datetime, AgeNullable, NaturalLanguage


    # set up cluster and workers
    local_cluster = LocalCluster(n_workers=96, 
                                 threads_per_worker=2,
                                 dashboard_address=':8787',
                                 memory_limit='3.75GB')
    
    print('Running cluster:', '\n', 
          local_cluster)
    
    
    # get processed fs params based on conf   
    selected_fs_dates_timestamps, \
    selected_fs_windows_dict, \
    selected_agg_primitives_ft, \
    selected_trans_primitives_ft, \
    selected_where_primitives_ft = \
                                    get_selected_fs_params(selected_fs_dates, 
                                                            selected_fs_windows, 
                                                            selected_agg_primitives, 
                                                            selected_trans_primitives, 
                                                            selected_where_primitives)
    
    print('selected_fs_dates:', selected_fs_dates)
    print('selected_fs_windows_dict:', selected_fs_windows_dict)

    ##################################
    # ENTITY SET DEFINITION
    es = define_entity_set(articles, 
                           customers, 
                           transactions, 
                           baskets,
                           intresting_articles_values_dict,
                           interesting_baskets_values_dict,
                           interesting_customers_values_dict)
    
    print('Entity set defined')
    
    print(es[entity].head(5))
    
    # calculate how many columns will be taken from the source table as is
    n_cols_entity_source = len(list(x for x in es[entity].columns if '_id' not in x and x!='detail_desc'))
    entity_fs_dates = es[entity]\
                    [[es[entity].columns[0]]]\
                    .join(selected_fs_dates_timestamps, how='cross')\
                    .sort_values(['time', es[entity].columns[0]])    
    print('Index of cutoff_time deinfed - cartesian product of selected dates and customer_ids')
    print(entity_fs_dates.head())

    print(entity_fs_dates.dtypes)


    # iterate over different windows definitions
    for window_label in list(selected_fs_windows_dict.keys()):
        
        # I expect to see "Mean of empty slice" warning message in this block
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            
            print('calculating fs for window:', window_label)
            curr_cutoff_fs, curr_cutoff_features_definitions = ft.dfs(entityset = es,
                                                                      target_dataframe_name = entity, 
                                                                      agg_primitives = selected_agg_primitives_ft,
                                                                      trans_primitives = selected_trans_primitives_ft,
                                                                      where_primitives = selected_where_primitives_ft,
                                                                      max_depth = max_depth,
                                                                      cutoff_time = entity_fs_dates,
                                                                      cutoff_time_in_index = True,
                                                                      training_window = selected_fs_windows_dict[window_label],
                                                                      dask_kwargs={'cluster': local_cluster, 'diagnostics port': 49286}, 
                                                                      verbose=True
                                                                  )
            print('done')

        curr_cutoff_fs.columns = list(curr_cutoff_fs.columns[:n_cols_entity_source]) + \
                                    list(curr_cutoff_fs.columns[n_cols_entity_source:] + '_' + window_label)
        
        print(curr_cutoff_fs.index[:5])
        print(curr_cutoff_fs[curr_cutoff_fs.columns[:3]].head(5))

        # if entity_fs exists, add new set of columns calculated for the current window
        try: 
            entity_fs = entity_fs.merge(curr_cutoff_fs[curr_cutoff_fs.columns[n_cols_entity_source:]], 
                                        on=[es[entity].columns[0], 'time'],
                                        how='left') # to 'EVER' records left join these with shorter windows
            print('merged new window fs to entity_fs on ['+ es[entity].columns[0]+', "time"]'+ ' index' )

        except:
            print('creating entity_fs')
            entity_fs = curr_cutoff_fs.copy()
            
            
    entity_fs = entity_fs.reset_index()
    #entity_fs.columns = ['`' + x + '`' for x in entity_fs.columns]
    
    print('\n', 'FINISHED')
    return entity_fs


def automatically_preselect_features(fs,
                                      remove_single_value,
                                      remove_low_information,
                                      remove_highly_null,
                                      pct_null_threshold,
                                      remove_highly_correlated,
                                      pct_corr_threshold
                                     ):

    import featuretools as ft
    
    curr_n_cols = fs.shape[1]
    print('input df number of features: ' + str(curr_n_cols))
    
    if remove_single_value==True:
        fs = ft.selection.remove_single_value_features(fs, count_nan_as_value=True) # to prevent removing "if had_sth==1 else null" features
        removed_n_cols = curr_n_cols - fs.shape[1]
        print('removed ' + str(removed_n_cols) + ' features with single value')
        curr_n_cols = fs.shape[1]    
        print('curr_n_cols:', curr_n_cols)
        
    if remove_low_information==True:
        fs = ft.selection.remove_low_information_features(fs)
        removed_n_cols = curr_n_cols - fs.shape[1]
        print('removed ' + str(removed_n_cols) + ' features with low information')
        curr_n_cols = fs.shape[1]
        print('curr_n_cols:', curr_n_cols)
    
    if remove_highly_null==True:
        fs = ft.selection.remove_highly_null_features(fs, pct_null_threshold=pct_null_threshold)
        removed_n_cols = curr_n_cols - fs.shape[1]
        print('removed ' + str(removed_n_cols) + ' highly null features')
        curr_n_cols = fs.shape[1]  
        print('curr_n_cols:', curr_n_cols)
        
    if remove_highly_correlated==True:
        fs = ft.selection.remove_highly_correlated_features(fs, pct_corr_threshold=pct_corr_threshold)
        removed_n_cols = curr_n_cols - fs.shape[1]
        print('removed ' + str(removed_n_cols) + ' highly correlated features')
        curr_n_cols = fs.shape[1]  
        print('curr_n_cols:', curr_n_cols)

    # not working
    # ft.selection.remove_highly_correlated_features(feature_matrix_customers)
        
    print('Remaining number of features after automatic selection: ' + str(curr_n_cols))
    
    
    return fs

    


