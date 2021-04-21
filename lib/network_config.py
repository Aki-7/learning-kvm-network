from pathlib import Path
import os

class NetworkConfig:
    def __init__(self, path: Path):
        self.path = path
    
    def create(self, config: str):
        self.path.write_text(config)

    def delete(self):
        if self.path.exists():
            os.remove(self.path)
