from sklearn import linear_model, neural_network, tree
from typing import List, Tuple
from pandas import DataFrame

def logistic_classifier(dataset: DataFrame, random_state: int, X_columns: List[str], y_column: str) -> linear_model.LogisticRegression:
    linear_regression_classifier = linear_model.LogisticRegression(random_state = random_state)
    linear_regression_classifier.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values,
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return linear_regression_classifier

def multilayer_perceptron_classifier(dataset: DataFrame, random_state: int, hidden_layer_sizes: Tuple[int], max_iter: int, X_columns: List[str], y_column: str) -> neural_network.MLPClassifier:
    artificial_neural_network_classifier = neural_network.MLPClassifier(random_state = random_state, hidden_layer_sizes = hidden_layer_sizes, max_iter = max_iter)
    artificial_neural_network_classifier.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values, 
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return artificial_neural_network_classifier


def decision_tree_classifier(dataset: DataFrame, random_state: int, max_depth: int, class_weight: str, X_columns: List[str], y_column: str) -> tree.DecisionTreeClassifier:
    decision_tree_classifier = tree.DecisionTreeClassifier(random_state = random_state, max_depth = max_depth, class_weight = class_weight)
    decision_tree_classifier.fit(
        dataset.loc[dataset["is_train_sample"], X_columns].values, 
        dataset.loc[dataset["is_train_sample"], y_column].values
    )
    return decision_tree_classifier