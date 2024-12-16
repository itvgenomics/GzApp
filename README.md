[![Test GzApp Script](https://github.com/itvgenomics/GzApp/actions/workflows/GzApp_script.yml/badge.svg)](https://github.com/itvgenomics/GzApp/actions/workflows/GzApp_script.yml) [![GzApp Testing with Conda](https://github.com/itvgenomics/GzApp/actions/workflows/GzApp_conda.yml/badge.svg)](https://github.com/itvgenomics/GzApp/actions/workflows/GzApp_conda.yml) [![Pylint](https://github.com/itvgenomics/GzApp/actions/workflows/GzApp_pylint.yml/badge.svg)](https://github.com/itvgenomics/GzApp/actions/workflows/GzApp_pylint.yml)

# GzApp: FASTA, FASTQ, SAM, and BAM Compression Tool

GzApp is a tool designed to compress bioinformatics files, specifically FASTA, FASTQ, SAM and BAM formats, into `.gz` format to save storage space. It also verifies the integrity of the compressed files and generates a detailed Excel log with the status of each file.

## Features

- **File Compression**: Compresses all `.fasta`, `.fastq`, `.sam` and `.bam` files in a specified directory.
- **Integrity Check**: Confirms that each compressed file is intact and uncorrupted.
- **Logging**: Records detailed information, including original and compressed file sizes, and integrity status for each file in an Excel file.
- **Original File Deletion**: Deletes the original file if both compression and integrity check are successful.

## Requirements

- Python 3.10+
- Anaconda (Optional)
- Required Libraries:
  - `os`
  - `argparse`
  - `pandas`
  - `subprocess`
  - `time`

## Cloning GzApp from GitHub

To obtain the latest version of GzApp, clone the repository directly from GitHub. This will allow you to stay up to date with any new features or fixes.
---

### Step 1: Clone the Repository

Run the following command to clone the GzApp repository:

```bash
git clone https://github.com/luanrabelo/GzApp.git
cd GzApp
```

This will create a local copy of the repository on your machine, allowing you to run GzApp or make modifications as needed.

### Step 2: Install Dependencies

#### Option A: Install with `pip`

To install dependencies with `pip`, run:

```bash
pip install -r requirements.txt
```

or

```bash
pip install pandas openpyxl
```
---

#### Option B: Install with Conda

If you prefer Conda, use the environment file to set up the dependencies:

1. Ensure you have [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html) installed on your system.
2. Create an `environment.yml` file with the following content if it doesn’t exist:

```yml
name: gzapp-env
channels:
  - conda-forge
dependencies:
  - python=3.10
  - pandas
  - openpyxl
```

3. Then set up and activate the Conda environment:

```bash
conda env create -f environment.yml
conda activate gzapp-env
```

## Running GzApp

With all dependencies installed, you can run the GzApp script. Make sure to specify the required parameters:

### Arguments

- `--folder`: Path to the directory containing the files to be compressed. (Required)
- `--log`: Path to the directory where the log file will be saved. (Required)
- `--fasta`: Flag to process FASTA files. (Optional)
- `--fastq`: Flag to process FASTQ files. (Optional)
- `--sam`: Flag to process SAM files. (Optional)
- `--bam`: Flag to process BAM files. (Optional)

## Execution Examples

1. Compress FASTA files in a directory and save the log:
    ```sh
    python GzApp.py --folder /path/to/directory --log /path/to/log --fasta
    ```

2. Compress FASTQ files in a directory and save the log:
    ```sh
    python GzApp.py --folder /path/to/directory --log /path/to/log --fastq
    ```

3. Compress all supported file types (FASTA, FASTQ, SAM, BAM) in a directory and save the log:
    ```sh
    python GzApp.py --folder /path/to/directory --log /path/to/log --fasta --fastq --sam --bam 
    ```

## Log Structure

The generated log is saved as an Excel file with the following columns:

- **Original File**: Full path of the original file.
- **Compressed File**: Full path of the compressed file.
- **Original Size**: Size of the original file.
- **Compressed Size**: Size of the compressed file.
- **Compression Efficiency**: Percentage reduction in size from the original to the compressed file, calculated as:
  \[(Original Size - Compressed Size) / Original Size * 100\]
- **Integrity Check**: Indicates whether the compressed file passed the integrity test (`Pass` or `Fail`).

### Sample Log Structure
<table>
  <thead>
    <tr>
      <th>Original File</th>
      <th>Compressed File</th>
      <th>Original Size</th>
      <th>Compressed Size</th>
      <th>Compression Efficiency</th>
      <th>Integrity Check</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>/path/to/folder/file1.fasta</td>
      <td>file1.fasta.tar.gz</td>
      <td>50.00 MB</td>
      <td>10.00 MB</td>
      <td>80%</td>
      <td>Pass</td>
    </tr>
    <tr>
      <td>/path/to/folder/file2.fastq</td>
      <td>file2.fastq.tar.gz</td>
      <td>60.00 MB</td>
      <td>15.00 MB</td>
      <td>75%</td>
      <td>Fail</td>
    </tr>
  </tbody>
</table>

### Example of Space Efficiency Summary Output

In addition to the Excel log, a text summary file is generated with information on the overall space savings.

Example output in `<log_file>.txt`:

```
Space Before Compression: 100.00 MB
Space After Compression: 20.00 MB
Compression Efficiency: 80.00%
```

This summary provides a quick overview of the total storage saved by the compression process.

## Example PBS Scheduling Script

For those using a PBS cluster, here is an example `.pbs` script to schedule the task:

```bash
#PBS -l nodes=1:ppn=1
#PBS -N GzApp
#PBS -o job_run-GzApp.log
#PBS -e job_run-GzApp.err

CORES=$[ `cat $PBS_NODEFILE | wc -l` ]
NODES=$[ `uniq $PBS_NODEFILE | wc -l` ]

printf "Inicio: `date`\n";
TBEGIN=`echo "print time();" | perl`

printf "\n"
printf "> Executando job_code7\n";
printf "> Rodando em $CORES nucleos, em $NODES nos\n"
cd $PBS_O_WORKDIR

python /path/to/GzApp.py --folder /path/to/folder --log /path/to/log --fasta --fastq --sam --bam

TEND=`echo "print time();" | perl`

printf "\n"
printf "Fim: `date`\n";
printf "Tempo decorrido (s): `expr $TEND - $TBEGIN`\n";
printf "Tempo decorrido (min): `expr $(( ($TEND - $TBEGIN)/60 ))`\n";
echo "TERMINADO"
```

## Contribution

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Luan Rabelo – [luanrabelo@outlook.com](mailto:luanrabelo@outlook.com)
