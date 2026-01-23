import kagglehub
import shutil
from pathlib import Path

script_folder = Path(__file__).parent.resolve()
project_root = script_folder.parent
target_dir = project_root / "data" / "raw"
new_filename = "fraud_dataset.csv"
final_file_path = target_dir / new_filename

print(f"Target localization: {final_file_path}")

download_path = Path(kagglehub.dataset_download("ealaxi/paysim1"))

if not final_file_path.exists():
    target_dir.mkdir(parents=True, exist_ok=True)

    found_files = list(download_path.glob("*.csv"))

    if found_files:
        source_file = found_files[0]
        print(f"Found file: {source_file.name}")

        shutil.copy(source_file, final_file_path)
        print(f"File successfully copied as {new_filename}")
    else:
        raise Exception("Error: CSV file not found in download folder")
else:
    raise Exception(f"File {new_filename} already exists {target_dir}. No need to copy")