# Lab Hashing

This program demonstrates various hashing schemes including linear probing, quadratic probing, and chaining, on a given dataset.

## Requirements

Python 3.6 or higher

## Usage

Place your input file with integers, one per line, in the same directory as the script. If you don't provide a filename, the default input file name is LabHashingInput.txt.

Run the script by executing the following command in the terminal:

```
python lab_hashing.py
```

- You will be prompted to enter the input file name. Press Enter to use the default input file or enter the name of your custom input file.

- You will be prompted to enter the output file name. Press Enter to use the default output file or enter the name of your custom output file.

- You will be prompted to enter the divisor value. Press Enter to use the default value (113) or enter a custom value.

- You will be prompted to enter the probing type. Enter linear, quadratic, chaining, or all (to run all schemes) and press Enter.

- The program will generate an output file for each hashing scheme with detailed information about the hash table, including runtime, collisions, comparisons, and the resulting hash table.

The output file name will include the probing type, e.g., LabHashingOutput_linear.txt, LabHashingOutput_quadratic.txt, or LabHashingOutput_chaining.txt.
Input File Format

The input file should contain integers, one per line. The integers should be between 0 and 99999, inclusive.

Example:

12345
67890
24680
13579

## Output File Format

The output file contains the following information:

- Runtime
- Hash table size
- Bucket size
- Number of collisions
- Number of comparisons
- Number of items not inserted
- Load factor
- Resulting hash table

## Example:

- Runtime: 0.1234567ms
- Hash table size: 113
- Bucket Size: 1
- Number of collisions: 2
- Number of comparisons: 3
- Number of items not inserted: 0
- Load factor: 0.1

Resulting hash table:
[ 12345 ] [ 67890 ] [ 24680 ] [ 13579 ] [None  ]
