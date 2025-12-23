# copyhovno

A simple Python implementation of the `dd` (data duplicator) utility for copying data with configurable block sizes.

## Features

- Copy data from input to output files
- Configurable block size
- Support for stdin/stdout
- Limit number of blocks to copy
- Progress reporting

## Installation

No installation required. Just run the script directly:

```bash
python3 dd.py --if input.txt --of output.txt
```

## Usage

```bash
# Copy a file
python3 dd.py --if source.txt --of destination.txt

# Copy with custom block size (1024 bytes)
python3 dd.py --if source.txt --of destination.txt --bs 1024

# Copy only first 10 blocks
python3 dd.py --if source.txt --of destination.txt --bs 512 --count 10

# Copy from stdin to file
cat input.txt | python3 dd.py --of output.txt

# Copy from file to stdout
python3 dd.py --if input.txt > output.txt
```

## Options

- `--if <file>`: Input file (default: stdin, use `-` for stdin)
- `--of <file>`: Output file (default: stdout, use `-` for stdout)
- `--bs <size>`: Block size in bytes (default: 512)
- `--count <n>`: Number of blocks to copy (default: all)

## Testing

Run the test suite:

```bash
python3 test_dd.py
```

## License

This is a simple educational implementation.