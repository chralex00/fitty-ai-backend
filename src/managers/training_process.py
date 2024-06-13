from typing import Final

class TrainingProcessManager:
    def __init__(self) -> None:
        self.running = False

    async def training_process(self):
        self.running = True

        # to do - manage the training process

        self.running = False

TRAINING_PROCESS_MANAGER: Final[TrainingProcessManager] = TrainingProcessManager()