from typing import Final
from .to_dataset_linked_status import to_dataset_linked_status
from .to_dataset_split_status import to_dataset_split_status
from .to_training_and_trained_status import to_training_and_trained_status

class TrainingProcessManager:
    def __init__(self) -> None:
        self.running = False

    async def training_process(self):
        self.running = True

        await to_dataset_linked_status()
        await to_dataset_split_status()
        await to_training_and_trained_status()
        # to do - manage the training process

        self.running = False

TRAINING_PROCESS_MANAGER: Final[TrainingProcessManager] = TrainingProcessManager()