# kaggle-hm-kedro

##### install kedro with:
```
pip install kedro
```
```
kedro new
    [New Kedro Project]: Kaggle H&M
    [kaggle-h&m]: kedro
    [kaggle_h&m]: main
```

```
cd kedro
conda create --name kedro
conda activate kedro
conda install pip
pip install -r src/requirements.txt
```

##### 1. generate sampled datasets from raw CSVs and save them as parquet files (HERE JUST AS AN EXAMPLE AS NO SAMPLING NODES AND NO RAW DATA IS PROVIDED IN THE REPO)
kedro run --pipeline sample -e sample

##### 2. clean the data for the purpose of feature engineering
```
kedro run --pipeline clean -e sample
```
See the results in the notebook [here](notebooks/data_check.ipynb)

##### 3. generate customers- and articles- feature stores
```
kedro run --pipeline create_fs -e sample
```
See the results in the notebook [here](notebooks/feature_store_check.ipynb) 

##### 4. generate customers- feature store with more variables using extend_customers_fs environment
 ```
kedro run --pipeline create_fs -n customer -e extend_customers_fs
 ```
See the results in the notebook [here] (notebooks/feature_store_check.ipynb) 
