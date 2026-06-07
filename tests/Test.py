import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from core.config import OPENAI_API_KEY

print("API Key Loaded:", OPENAI_API_KEY[:10], "...")