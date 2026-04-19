import sys
from pathlib import Path

# Ajouter le répertoire racine du service au PYTHONPATH pour que pytest
# puisse importer les modules depuis src/
root_dir = Path(__file__).parent.resolve()
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
