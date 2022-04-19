"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline
from main.pipelines import data_cleaning

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """

    create_cleaned_data_pipeline = data_cleaning.create_pipeline()


    return {"__default__": pipeline([]),
            "clean": create_cleaned_data_pipeline}
