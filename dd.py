#!/usr/bin/env python3
"""
A simple Python implementation of dd (data duplicator) utility.
"""

import sys
import argparse


def copy_data(input_file, output_file, block_size=512, count=None):
    """
    Copy data from input_file to output_file in blocks.
    
    Args:
        input_file: Input file path or '-' for stdin
        output_file: Output file path or '-' for stdout
        block_size: Size of each block in bytes (default: 512)
        count: Number of blocks to copy (None for all)
    
    Returns:
        Tuple of (blocks_read, bytes_copied)
    """
    blocks_read = 0
    bytes_copied = 0
    
    # Open input
    if input_file == '-':
        input_fd = sys.stdin.buffer
    else:
        input_fd = open(input_file, 'rb')
    
    try:
        # Open output
        if output_file == '-':
            output_fd = sys.stdout.buffer
        else:
            output_fd = open(output_file, 'wb')
        
        try:
            while count is None or blocks_read < count:
                block = input_fd.read(block_size)
                if not block:
                    break
                
                output_fd.write(block)
                blocks_read += 1
                bytes_copied += len(block)
            
            output_fd.flush()
            
        finally:
            if output_file != '-':
                output_fd.close()
    
    finally:
        if input_file != '-':
            input_fd.close()
    
    return blocks_read, bytes_copied


def main():
    """Main entry point for the dd command."""
    parser = argparse.ArgumentParser(
        description='Copy data from input to output with configurable block size.'
    )
    parser.add_argument(
        '--if', dest='input_file', default='-',
        help='Input file (default: stdin)'
    )
    parser.add_argument(
        '--of', dest='output_file', default='-',
        help='Output file (default: stdout)'
    )
    parser.add_argument(
        '--bs', dest='block_size', type=int, default=512,
        help='Block size in bytes (default: 512)'
    )
    parser.add_argument(
        '--count', type=int, default=None,
        help='Number of blocks to copy (default: all)'
    )
    
    args = parser.parse_args()
    
    # Validate block size
    if args.block_size <= 0:
        sys.stderr.write('Error: Block size must be positive\n')
        return 1
    
    # Validate count
    if args.count is not None and args.count < 0:
        sys.stderr.write('Error: Count must be non-negative\n')
        return 1
    
    try:
        blocks, bytes_total = copy_data(
            args.input_file,
            args.output_file,
            args.block_size,
            args.count
        )
        
        sys.stderr.write(f'{blocks} blocks ({bytes_total} bytes) copied\n')
        return 0
    
    except FileNotFoundError as e:
        sys.stderr.write(f'Error: {e}\n')
        return 1
    except PermissionError as e:
        sys.stderr.write(f'Error: {e}\n')
        return 1
    except KeyboardInterrupt:
        sys.stderr.write('\nInterrupted\n')
        return 130
    except Exception as e:
        sys.stderr.write(f'Error: {e}\n')
        return 1


if __name__ == '__main__':
    sys.exit(main())
