import numpy as np
import glob


def load_files():
    """Load arrays from files."""
    for name in glob.glob("*.npy"):
        if name.startswith("WSM"):
            WSM = np.load(name)
            yield {"name": name, "WSM": WSM}

for result in load_files():
    print(result['WSM'].dtype)
