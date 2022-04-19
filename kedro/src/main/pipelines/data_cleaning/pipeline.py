"""
This is a boilerplate pipeline 'data_cleaning'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from helpers.data_cleaning import clean_customers, clean_articles, clean_transactions

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="customers",
                func=clean_customers,
                inputs="customers_raw",
                outputs="customers_cleaned",
            ),
            node(
                name="articles",
                func=clean_articles,
                inputs="articles_raw", 
                outputs="articles_cleaned",
            ),
            node(
                name="transactions",
                func=clean_transactions,
                inputs="transactions_raw", 
                outputs=["transactions_cleaned", "baskets_cleaned"],
            )
        ]
    )