"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline
from main.pipelines import data_cleaning
from main.pipelines import feature_engineering

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    create_cleaned_data_pipeline = data_cleaning.create_pipeline()
    create_feature_engineering_pipeline = feature_engineering.create_pipeline()


    return {"__default__": pipeline([]),
            "clean": create_cleaned_data_pipeline,
            "create_fs": create_feature_engineering_pipeline}
