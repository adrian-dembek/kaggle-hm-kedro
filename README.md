# [What is Kedro](https://kedro.readthedocs.io/en/stable/introduction/introduction.html) and [how to use it](https://kedro.readthedocs.io/en/stable/tutorial/spaceflights_tutorial.html)? 

Shortly, it is a framework for creating reproducible and modular data science experiments. Thus, we decided to use it while solving the [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations) Kaggle competition. 

Here, we decided to share a solution with a part of the approach on how to use Kedro and featuretools to **create multiple, reproducible, customizable and scalable feature stores** which can be used in Machine Learning models further in the pipeline. Also, please refer to [Kedro documentation](https://kedro.readthedocs.io/en/stable/index.html) in case of any doubts. 

Below you can find an instruction wits steps leading to the resulting feature stores. To avoid extensive data loading, I purposly ommitted "sampling" part which uses raw data and started the pipeline from the second step which is "data cleaning". I encourage you to fill in the gap, write a sampling function (node) and run the pipeline to get the sampled datasets I included in the repo.

## Set up the environment

##### 1. Clone the repository

##### 2. Install kedro with:
```
pip install kedro
```

Kedro project thar is ready to use in the repository was created with:
```
kedro new
    [New Kedro Project]: Kaggle H&M
    [kaggle-h&m]: kedro
    [kaggle_h&m]: main
```

##### 3. Create conda environment

```
cd kedro
conda create --name kedro
conda activate kedro
conda install pip
pip install -r src/requirements.txt
```

## Run kedro pipelines

##### 1. generate sampled datasets from raw CSVs and save them as parquet files (HERE JUST AS AN EXAMPLE AS NO SAMPLING NODES AND NO RAW DATA IS PROVIDED IN THE REPO)
kedro run --pipeline sample -e sample

##### 2. clean the data for the purpose of feature engineering
```
kedro run --pipeline clean -e sample
```
See the results in the notebook [here](kedro/notebooks/data_check.ipynb)

##### 3. generate customers- and articles- feature stores
```
kedro run --pipeline create_fs -e sample
```
See the results in the notebook [here](kedro/notebooks/feature_store_check.ipynb)

##### 4. generate customers- feature store with more variables using extend_customers_fs environment
 ```
kedro run --pipeline create_fs -n customer -e extend_customers_fs
 ```
See the results in the notebook [here] (notebooks/feature_store_check.ipynb) 
