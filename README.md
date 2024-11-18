Um das environement zu activieren:
    Set-ExecutionPolicy Unrestricted -Scope Process
    .\.venv\Scripts\Activate

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))