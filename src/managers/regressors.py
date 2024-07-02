from typing import List, Tuple
from pandas import DataFrame
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn import tree
from sklearn import ensemble
from sklearn import neural_network

def linear_regressor(dataset: DataFrame, X_columns: List[str], y_column: str) -> linear_model.LinearRegression:
    linear_regressor = linear_model.LinearRegression()
    linear_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return linear_regressor

def lasso_regressor(dataset: DataFrame, alpha: float, X_columns: List[str], y_column: str) -> linear_model.Lasso:
    lasso_regressor = linear_model.Lasso(alpha = alpha)
    lasso_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return lasso_regressor

def ridge_regressor(dataset: DataFrame, alpha: float, X_columns: List[str], y_column: str) -> linear_model.Ridge:
    ridge_regressor = linear_model.Ridge(alpha = alpha)
    ridge_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return ridge_regressor

def elastic_network_regressor(dataset: DataFrame, alpha: float, l1_ratio: float, X_columns: List[str], y_column: str) -> linear_model.ElasticNet:
    elastic_network_regressor = linear_model.ElasticNet(alpha = alpha, l1_ratio = l1_ratio)
    elastic_network_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return elastic_network_regressor

def knn_regressor(dataset: DataFrame, n_neighbors: int, weights: str, metric: str, X_columns: List[str], y_column: str) -> neighbors.KNeighborsRegressor:
    knn_regressor = neighbors.KNeighborsRegressor(n_neighbors = n_neighbors, weights = weights, metric = metric)
    knn_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return knn_regressor

def linear_support_vector_machine_regressor(dataset: DataFrame, random_state: int, X_columns: List[str], y_column: str) -> svm.LinearSVR:
    linear_support_vector_machine_regressor = svm.LinearSVR(random_state = random_state)
    linear_support_vector_machine_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return linear_support_vector_machine_regressor

def decision_tree_regressor(dataset: DataFrame, random_state: int, max_depth: int, X_columns: List[str], y_column: str) -> tree.DecisionTreeRegressor:
    decision_tree_regressor = tree.DecisionTreeRegressor(random_state = random_state, max_depth = max_depth)
    decision_tree_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return decision_tree_regressor

def random_forest_regressor(dataset: DataFrame, random_state: int, max_depth: int, n_estimators: int, X_columns: List[str], y_column: str) -> ensemble.RandomForestRegressor:
    random_forest_regressor = ensemble.RandomForestRegressor(
        random_state = random_state,
        max_depth = max_depth,
        n_estimators = n_estimators
    )
    random_forest_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return random_forest_regressor

def neural_network_regressor(dataset: DataFrame, random_state: int, hidden_layer_sizes: Tuple[int], max_iter: int, X_columns: List[str], y_column: str) -> neural_network.MLPRegressor:
    multilayer_perceptron_regressor = neural_network.MLPRegressor(
        random_state = random_state,
        hidden_layer_sizes = hidden_layer_sizes,
        max_iter = max_iter
    )
    multilayer_perceptron_regressor.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return multilayer_perceptron_regressor