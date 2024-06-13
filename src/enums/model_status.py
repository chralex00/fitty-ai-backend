from enum import Enum

class ModelStatus(str, Enum):
    CREATED = "CREATED"  # The model has just been created
    
    PROCESS_STARTED = "PROCESS_STARTED"  # The model has just started training. From this moment it is no longer possible to modify the model.

    DATASET_LINKED = "DATASET_LINKED"  # The dataset has been created and is ready to be used in the training phase
    DATASET_SPLIT = "DATASET_SPLIT"  # The dataset was divided into test dataset and training dataset

    TRAINING = "TRAINING"  # The model is being trained and is considering only the training dataset
    TRAINED = "TRAINED"  # The model has been properly trained using the training dataset

    TESTING = "TESTING"  # The model is being tested and is considered the test dataset
    TESTED = "TESTED"  # The model has completed the testing phase (test dataset)

    EVALUING = "EVALUING"  # Model performance metrics are being calculated
    EVALUED = "EVALUED"  # All model metrics have been created and evaluated

    READY = "READY"  # The model is ready to be used

    ERROR = "ERROR"  # The training process led to an error, for some strange reason