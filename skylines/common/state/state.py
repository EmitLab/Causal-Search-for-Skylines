import os
from datetime import datetime
from pathlib import Path

from skylines.common.utils import format_num


class State:

    def __init__(self, n_samples: int = 0, working_dir: str = 'out'):
        self.samples = format_num(n_samples)
        self.working_dir = working_dir

        if os.path.exists('timestamp.txt'):
            with open('timestamp.txt', 'r') as f:
                self.timestamp = f.readline()
        else:
            self.timestamp = None

    def refresh(self):
        # update the timestamp
        self.timestamp = datetime.now().strftime('%Y_%m_%d__%H_%M')
        with open('timestamp.txt', 'w') as f:
            f.write(self.timestamp)
        return self.timestamp

    def get_file(self, directory: str, filename: str) -> str:
        # read the file
        filepath = os.path.join(self.working_dir, self.timestamp, self.samples, directory, filename)
        path: Path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path.resolve())
