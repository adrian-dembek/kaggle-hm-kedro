# [What is Kedro](https://kedro.readthedocs.io/en/stable/introduction/introduction.html) and [how to use it](https://kedro.readthedocs.io/en/stable/tutorial/spaceflights_tutorial.html)? 

In short, it is a framework for creating reproducible and modular data science experiments. Thus, we decided to use it while taking the [H&M Personalized Fashion Recommendations](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations) Kaggle competition. 

Here, we decided to share a toy example of the approach we use taking advantage of Kedro and featuretools to **create multiple, reproducible, customizable and scalable feature stores** which can be used in Machine Learning models further in the pipeline. Also, please refer to [Kedro documentation](https://kedro.readthedocs.io/en/stable/index.html) in case of any doubts. 

What we are trying to achieve is a modular pipeline with shared functions, where we would be able to customize each and every 'data cleaning', 'feature engineering', 'propensity modelling', 'recommendation engine', 'ensembling' node and use them in pipelines to achieve a reproducible result.
![image](https://user-images.githubusercontent.com/24912552/164473659-11deebbd-2bc5-4684-8f19-767d4ab4b9fa.png)


Below you can find an instruction wits steps leading to the resulting feature stores.

## Set up the environment

##### 1. Clone the repository
```
git clone https://github.com/adrian-dembek/kaggle-hm-kedro.git
```

##### 2. Create conda environment

```
conda create --name kedro python=3.8
conda activate kedro
cd kaggle-hm-kedro/kedro
pip install -r src/requirements.txt
```

## Run kedro pipelines

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
See the results in the notebook [here] (kedro/notebooks/feature_store_check.ipynb) 


# 
# DIY :) 

### Generate sampled datasets from raw CSVs and save them as parquet files
To avoid extensive data loading, I purposly ommitted "sampling" part which uses raw data. 
The pipeline begins with the second step which is "data cleaning". 
I encourage you to fill in the gap and create a "sampling" pipeline on your own. 
[Here](https://kedro.readthedocs.io/en/stable/tutorial/create_pipelines.html) please find the documentation of the process.

Firstly, run the command below to create new pipeline directories:

```
kedro pipeline create sampling
```
Then, follow instructions provided below

1. write a "sample()" node in [kedro/src/main/pipelines/sampling/nodes.py](kedro/src/main/pipelines/sampling/nodes.py)
    
2. define parameters you will be using in the sample() node: [kedro/conf/base/parameters/sampling.yml](kedro/conf/base/parameters/sampling.yml)
    
3. define objects (datasets) in the data catalog: [kedro/conf/base/catalog.yml](kedro/conf/base/catalog.yml)
   - remember to create different names of sampled files in order to distinguish them from these already present in the repo.
    
4. create a pipeline using the node and parameters from [kedro/src/main/pipelines/sampling/pipeline.py](kedro/src/main/pipelines/sampling/pipeline.py)
    
5. add the pipeline to the pipeline registry: [kedro/src/main/pipeline_registry.py](kedro/src/main/pipeline_registry.py)
    
6. run the pipeline with the command below
    
```
kedro run --pipeline sample -e sample
```
Congratulations! Now you should see that sampled data files have been created and saved to the specified directory.
