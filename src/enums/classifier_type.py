from enum import Enum

class ClassifierType(str, Enum):
    # Classification
    LOGISTIC_CLASSIFIER = "LOGISTIC_CLASSIFIER"
    MULTILAYER_PERCEPTRON_CLASSIFIER = "MULTILAYER_PERCEPTRON_CLASSIFIER"
    DECISION_TREE_CLASSIFIER = "DECISION_TREE_CLASSIFIER"

    # Regression
    LINEAR_REGRESSION = "LINEAR_REGRESSION"
    K_NEIGHBORS_REGRESSION = "K_NEIGHBORS_REGRESSION"
    LINEAR_SUPPORT_VECTOR_MACHINE = "LINEAR_SUPPORT_VECTOR_MACHINE"
    DECISION_TREE_REGRESSION = "DECISION_TREE_REGRESSION"
    MULTILAYER_PERCEPTRON_REGRESSION = "MULTILAYER_PERCEPTRON_REGRESSION"
