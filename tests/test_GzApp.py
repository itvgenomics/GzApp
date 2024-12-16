import os
import subprocess
import pandas as pd
import pytest

# Paths to test files and output folders
TEST_FOLDER = "tests/test_data"
LOG_FOLDER = "tests/test_logs"


def get_latest_log_file(log_folder):
    """Retrieve the most recently modified log file in the specified folder."""
    files = [os.path.join(log_folder, f) for f in os.listdir(log_folder) if f.endswith(".xlsx")]
    latest_file = max(files, key=os.path.getmtime) if files else None
    return latest_file


def test_compression_script():
    """Ensure the log directory exists and the script runs successfully."""
    os.makedirs(LOG_FOLDER, exist_ok=True)

    # Verify that test files exist
    tfiles = [f for f in os.listdir(TEST_FOLDER) if f.endswith(('fasta', 'fastq', 'sam', 'bam'))]
    assert tfiles, "No test files found in the test folder"

    # Run the compression script
    result = subprocess.run(
        ["python",
         "GzApp.py",
         "--folder",
         TEST_FOLDER,
         "--log",
         LOG_FOLDER,
         "--fasta",
         "--fastq",
         "--sam",
         "--bam"],
        capture_output=True, text=True, check=True,
    )
    assert result.returncode == 0, "Script did not run successfully"

    # Check if the Excel log file is created
    log_file = get_latest_log_file(LOG_FOLDER)
    assert log_file, "Log file not created"

    # Verify contents of the log
    df = pd.read_excel(log_file, engine='openpyxl')
    assert "Original File" in df.columns, "Log missing 'Original File' column"
    assert "Compressed Size" in df.columns, "Log missing 'Compressed Size' column"
    assert "Compression Efficiency" in df.columns, "Log missing 'Compression Efficiency' column"
    assert "Integrity Check" in df.columns, "Log missing 'Integrity Check' column"

    # Convert Compression Efficiency to numeric
    df["Compression Efficiency"] = pd.to_numeric(df["Compression Efficiency"].str.rstrip('%'))

    # Verify that all files were processed
    assert len(df) == len(tfiles), "Not all files were processed"

    # Verify compression efficiency and integrity check
    for index, row in df.iterrows():
        assert row["Compression Efficiency"] > 0, f"{index} Compression efficiency > 0"
        assert row["Integrity Check"] == "Pass", f"{index} Integrity failed {row['Original File']}"

    # Clean up generated files
    for file in os.listdir(TEST_FOLDER):
        if file.endswith(".gz"):
            os.remove(os.path.join(TEST_FOLDER, file))
    os.remove(log_file)


if __name__ == "__main__":
    pytest.main()
