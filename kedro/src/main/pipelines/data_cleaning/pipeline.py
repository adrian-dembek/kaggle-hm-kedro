"""
This is a boilerplate pipeline 'data_cleaning'
generated using Kedro 0.18.0
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import clean_customers, clean_articles, clean_transactions

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                name="customers",
                func=clean_customers,
                inputs="customers",
                outputs="customers_cleaned",
            ),
            node(
                name="articles",
                func=clean_articles,
                inputs="articles", 
                outputs="articles_cleaned",
            ),
            node(
                name="transactions",
                func=clean_transactions,
                inputs="transactions", 
                outputs=["transactions_cleaned", "baskets_cleaned"],
            )
        ]
    )