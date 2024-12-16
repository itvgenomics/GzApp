import argparse
import os
import subprocess
import time

import pandas as pd

__author__ = "Luan Rabelo"
__license__ = "MIT"
__version__ = "0.0.2"
__maintainers__ = "Luan Rabelo"
__email__ = "luanrabelo@outlook.com"
__toolname__ = "GzApp"
__date__ = "2024/11/05"
__github__ = "luanrabelo/gzapp"
__status__ = "Stable"


def format_size(**kwargs):
    """
    Converts a file size in bytes to a human-readable format.
    
    Parameters:
        size (int): The size of the file in bytes. Must be a non-negative integer.
        
    Returns:
        str: The file size formatted as a string with the appropriate unit (e.g., '1024 KB', '1.00 MB').
        
    Raises:
        ValueError: If the size parameter is negative or not an integer.
        TypeError: If the size parameter is not provided.
    """
    # Retrieve the size value from kwargs
    size = kwargs.get('size')
    
    # Validate the size parameter
    if size is None:
        raise TypeError("The 'size' parameter is required.")
    if not isinstance(size, (int, float)):
        raise ValueError("The 'size' parameter must be an integer or float.")
    if size < 0:
        raise ValueError("The 'size' parameter must be non-negative.")
    
    # Format size with the appropriate unit
    for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024  # Divide by 1024 to convert to the next unit
    
    # Handle very large sizes in petabytes
    return f"{size:.2f} PB"



if __name__ == "__main__":
    description = 'Compress bioinformatics files to save storage space.'
    parser = argparse.ArgumentParser(description=description)
    folderarg = 'Path to the directory containing the files to be compressed.'
    parser.add_argument('--folder', help=folderarg, required=True, type=str)
    logarg = 'Path to the directory where the log file will be saved.'
    parser.add_argument('--log', help=logarg, required=False, type=str)
    farg = 'Flag to process FASTA files.'
    parser.add_argument('--fasta', help=farg, action='store_true', default=False)
    fqarg = 'Flag to process FASTQ files.'
    parser.add_argument('--fastq', help=fqarg, action='store_true', default=False)
    sarg = 'Flag to process SAM files.'
    parser.add_argument('--sam', help=sarg, action='store_true', default=False)
    barg = 'Flag to process BAM files.'
    parser.add_argument('--bam', help=barg, action='store_true', default=False)
    _args = parser.parse_args()

    _folderUser = _args.folder
    _logFile = os.path.join(_args.log, f"log_{time.strftime('%Y%m%d%H%M%S', time.localtime())}") if _args.log else None
    logEntries = []  # Initialize log entries list for recording details of each file
    _originalSize = []
    _compressedSize = []
    for root, dirs, files in os.walk(_folderUser):
        for file in files:
            ABSOLUTE_PATH = os.path.join(root, file)  # Get the absolute path of the file
            COMPRESSED_FILE = f"{ABSOLUTE_PATH}.gz"  # Define the output compressed file path
            if file.endswith(".fasta") or file.endswith(".fna") or file.endswith(".fas") or file.endswith(".fa") and _args.fasta:
                startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(f"\n{startTime} - Compressing file {os.path.basename(ABSOLUTE_PATH)} to {os.path.basename(COMPRESSED_FILE)}")
                cmd = subprocess.run(
                    ["tar", "-czf", COMPRESSED_FILE, ABSOLUTE_PATH],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if cmd.returncode == 0:  # Verify if compression was successful
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f"{end_time} - Successfully compressed {ABSOLUTE_PATH} to {COMPRESSED_FILE}")
                    # Get size before and after compression
                    originalSize = os.path.getsize(ABSOLUTE_PATH)
                    compressedSize = os.path.getsize(COMPRESSED_FILE)
                    _originalSize.append(originalSize)
                    _compressedSize.append(compressedSize)
                    print(f"{end_time} - Checking integrity of {COMPRESSED_FILE}")
                    integrity_cmd = subprocess.run(
                        ["tar", "-tzf", COMPRESSED_FILE],
                        check=True,  # Add check=True
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    INTEGRITY_STATUS = 'Pass' if integrity_cmd.returncode == 0 else 'Fail'
                    print(f"{end_time} - Integrity check for {COMPRESSED_FILE}: {INTEGRITY_STATUS}")
                    # Log entry with details
                    logEntries.append({
                        'Original File': ABSOLUTE_PATH,
                        'Compressed File': os.path.basename(COMPRESSED_FILE),
                        'Original Size': format_size(size=originalSize),
                        'Compressed Size': format_size(size=compressedSize),
                        'Compression Efficiency': f"{(1 - compressedSize/originalSize) * 100:.2f}%",
                        'Integrity Check': INTEGRITY_STATUS
                    })
                    # Remove original file after successful compression
                    if INTEGRITY_STATUS == 'Pass':
                        # Remove original file after successful compression and integrity check
                        try:
                            os.remove(ABSOLUTE_PATH)
                            print(f"{end_time} - Removed original file {ABSOLUTE_PATH} after compression")
                        except OSError as e:  # Catch more specific exception
                            print(f"Error removing file {ABSOLUTE_PATH}: {e}")
                    else:
                        print(f"Integrity check failed for {COMPRESSED_FILE}, keeping the original file.")
                else:
                    # Log compression error
                    print(f"Error compressing {ABSOLUTE_PATH}: {cmd.stderr}")
            elif file.endswith(".fastq") or file.endswith(".fq") and _args.fastq:
                startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(f"\n{startTime} - Compressing file {os.path.basename(ABSOLUTE_PATH)} to {os.path.basename(COMPRESSED_FILE)}")
                cmd = subprocess.run(
                    ["tar", "-czf", COMPRESSED_FILE, ABSOLUTE_PATH],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if cmd.returncode == 0:  # Verify if compression was successful
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f"{end_time} - Successfully compressed {ABSOLUTE_PATH} to {COMPRESSED_FILE}")
                    # Get size before and after compression
                    originalSize = os.path.getsize(ABSOLUTE_PATH)
                    compressedSize = os.path.getsize(COMPRESSED_FILE)
                    _originalSize.append(originalSize)
                    _compressedSize.append(compressedSize)
                    print(f"{end_time} - Checking integrity of {COMPRESSED_FILE}")  # Integrity check for the compressed file
                    integrity_cmd = subprocess.run(
                        ["tar", "-tzf", COMPRESSED_FILE],
                        check=True,  # Add check=True
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    INTEGRITY_STATUS = 'Pass' if integrity_cmd.returncode == 0 else 'Fail'  # Check if the integrity check passed or failed
                    print(f"{end_time} - Integrity check for {COMPRESSED_FILE}: {INTEGRITY_STATUS}")
                    # Log entry with details
                    logEntries.append({
                        'Original File': ABSOLUTE_PATH,
                        'Compressed File': os.path.basename(COMPRESSED_FILE),
                        'Original Size': format_size(size=originalSize),
                        'Compressed Size': format_size(size=compressedSize),
                        'Compression Efficiency': f"{(1 - compressedSize/originalSize) * 100:.2f}%",
                        'Integrity Check': INTEGRITY_STATUS
                    })
                    # Remove original file after successful compression
                    if INTEGRITY_STATUS == 'Pass':
                        # Remove original file after successful compression and integrity check
                        try:
                            os.remove(ABSOLUTE_PATH)
                            print(f"{end_time} - Removed original file {ABSOLUTE_PATH} after compression")
                        except OSError as e:  # Catch more specific exception
                            print(f"Error removing file {ABSOLUTE_PATH}: {e}")
                    else:
                        print(f"Integrity check failed for {COMPRESSED_FILE}, keeping the original file.")
                else:
                    # Log compression error
                    print(f"Error compressing {ABSOLUTE_PATH}: {cmd.stderr}")
            elif file.endswith(".sam") and _args.sam:
                startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(f"\n{startTime} - Compressing file {os.path.basename(ABSOLUTE_PATH)} to {os.path.basename(COMPRESSED_FILE)}")
                cmd = subprocess.run(
                    ["tar", "-czf", COMPRESSED_FILE, ABSOLUTE_PATH],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if cmd.returncode == 0:  # Verify if compression was successful
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f"{end_time} - Successfully compressed {ABSOLUTE_PATH} to {COMPRESSED_FILE}")
                    # Get size before and after compression
                    originalSize = os.path.getsize(ABSOLUTE_PATH)
                    compressedSize = os.path.getsize(COMPRESSED_FILE)
                    _originalSize.append(originalSize)
                    _compressedSize.append(compressedSize)
                    print(f"{end_time} - Checking integrity of {COMPRESSED_FILE}")  # Integrity check for the compressed file
                    integrity_cmd = subprocess.run(
                        ["tar", "-tzf", COMPRESSED_FILE],
                        check=True,  # Add check=True
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    INTEGRITY_STATUS = 'Pass' if integrity_cmd.returncode == 0 else 'Fail'  # Check if the integrity check passed or failed
                    print(f"{end_time} - Integrity check for {COMPRESSED_FILE}: {INTEGRITY_STATUS}")
                    # Log entry with details
                    logEntries.append({
                        'Original File': ABSOLUTE_PATH,
                        'Compressed File': os.path.basename(COMPRESSED_FILE),
                        'Original Size': format_size(size=originalSize),
                        'Compressed Size': format_size(size=compressedSize),
                        'Compression Efficiency': f"{(1 - compressedSize/originalSize) * 100:.2f}%",
                        'Integrity Check': INTEGRITY_STATUS
                    })
                    # Remove original file after successful compression
                    if INTEGRITY_STATUS == 'Pass':
                        # Remove original file after successful compression and integrity check
                        try:
                            os.remove(ABSOLUTE_PATH)
                            print(f"{end_time} - Removed original file {ABSOLUTE_PATH} after compression")
                        except OSError as e:  # Catch more specific exception
                            print(f"Error removing file {ABSOLUTE_PATH}: {e}")
                    else:
                        print(f"Integrity check failed for {COMPRESSED_FILE}, keeping the original file.")
                else:
                    # Log compression error
                    print(f"Error compressing {ABSOLUTE_PATH}: {cmd.stderr}")
            elif file.endswith(".bam") and _args.bam:
                startTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                print(f"\n{startTime} - Compressing file {os.path.basename(ABSOLUTE_PATH)} to {os.path.basename(COMPRESSED_FILE)}")
                cmd = subprocess.run(
                    ["tar", "-czf", COMPRESSED_FILE, ABSOLUTE_PATH],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                if cmd.returncode == 0:  # Verify if compression was successful
                    end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    print(f"{end_time} - Successfully compressed {ABSOLUTE_PATH} to {COMPRESSED_FILE}")
                    # Get size before and after compression
                    originalSize = os.path.getsize(ABSOLUTE_PATH)
                    compressedSize = os.path.getsize(COMPRESSED_FILE)
                    _originalSize.append(originalSize)
                    _compressedSize.append(compressedSize)
                    print(f"{end_time} - Checking integrity of {COMPRESSED_FILE}")  # Integrity check for the compressed file
                    integrity_cmd = subprocess.run(
                        ["tar", "-tzf", COMPRESSED_FILE],
                        check=True,  # Add check=True
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    INTEGRITY_STATUS = 'Pass' if integrity_cmd.returncode == 0 else 'Fail'  # Check if the integrity check passed or failed
                    print(f"{end_time} - Integrity check for {COMPRESSED_FILE}: {INTEGRITY_STATUS}")
                    # Log entry with details
                    logEntries.append({
                        'Original File': ABSOLUTE_PATH,
                        'Compressed File': os.path.basename(COMPRESSED_FILE),
                        'Original Size': format_size(size=originalSize),
                        'Compressed Size': format_size(size=compressedSize),
                        'Compression Efficiency': f"{(1 - compressedSize/originalSize) * 100:.2f}%",
                        'Integrity Check': INTEGRITY_STATUS
                    })
                    # Remove original file after successful compression
                    if INTEGRITY_STATUS == 'Pass':
                        # Remove original file after successful compression and integrity check
                        try:
                            os.remove(ABSOLUTE_PATH)
                            print(f"{end_time} - Removed original file {ABSOLUTE_PATH} after compression")
                        except OSError as e:  # Catch more specific exception
                            print(f"Error removing file {ABSOLUTE_PATH}: {e}")
                    else:
                        print(f"Integrity check failed for {COMPRESSED_FILE}, keeping the original file.")
                else:
                    # Log compression error
                    print(f"Error compressing {ABSOLUTE_PATH}: {cmd.stderr}")
            else:
                pass
    # Save log to Excel if a log file path is provided
    if _logFile and logEntries:
        try:
            pd.DataFrame(logEntries).to_excel(f"{_logFile}.xlsx", index=False)
            print(f"Log saved to {_logFile}")
        except Exception as e:
            print(f"Error writing log to {_logFile}: {e}")
        with open(f'{_logFile}.txt', 'w', encoding='utf-8') as f:  # Specify encoding
            b = format_size(size=sum(_originalSize))
            a = format_size(size=sum(_compressedSize))
            e = abs(100 - sum(_compressedSize) / sum(_originalSize) * 100)
            f.write(f"Before Compression: {b}\n")
            f.write(f"After Compression: {a}\n")
            f.write(f"Compression Efficiency: {e:.2f}%\n")
_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
print(f"{_time} - Compression process completed.")
