"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline

from .feature_engineering import *

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="article",
                func=calculate_entity_fs,
                inputs=["articles_cleaned", 
                        "customers_cleaned", 
                        "transactions_cleaned", 
                        "baskets_cleaned", 
                        "params:intresting_articles_values_dict",
                        "params:interesting_baskets_values_dict",
                        "params:interesting_customers_values_dict",
                        "params:articles_entity",
                        "params:selected_fs_dates",
                        "params:selected_fs_windows",
                        "params:selected_agg_primitives",
                        "params:selected_trans_primitives",
                        "params:selected_where_primitives",
                        "params:articles_max_depth",
                        "params:fs_n_jobs"
                       ],
                outputs="articles_fs",
            ),
            node(
                name="customer",
                func=calculate_entity_fs,
                inputs=["articles_cleaned", 
                        "customers_cleaned", 
                        "transactions_cleaned", 
                        "baskets_cleaned", 
                        "params:intresting_articles_values_dict",
                        "params:interesting_baskets_values_dict",
                        "params:interesting_customers_values_dict",
                        "params:customers_entity",
                        "params:selected_fs_dates",
                        "params:selected_fs_windows",
                        "params:selected_agg_primitives",
                        "params:selected_trans_primitives",
                        "params:selected_where_primitives",
                        "params:articles_max_depth",
                        "params:fs_n_jobs"
                       ],
                outputs="customers_fs",
            ),
            node(
                name="preselect_features_customers",
                func=automatically_preselect_features,
                inputs=["customers_fs",
                        "params:remove_single_value",
                        "params:remove_low_information",
                        "params:remove_highly_null",
                        "params:pct_null_threshold",
                        "params:remove_highly_correlated",
                        "params:pct_corr_threshold"
                       ],
                outputs="customers_fs_preselected",
            ),
            node(
                name="preselect_features_articles",
                func=automatically_preselect_features,
                inputs=["articles_fs",
                        "params:remove_single_value",
                        "params:remove_low_information",
                        "params:remove_highly_null",
                        "params:pct_null_threshold",
                        "params:remove_highly_correlated",
                        "params:pct_corr_threshold"
                       ],
                outputs="articles_fs_preselected",
            )
        ]
    )



