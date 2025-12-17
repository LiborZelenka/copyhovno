#!/usr/bin/env python3
"""
Tests for the dd module.
"""

import unittest
import tempfile
import os
from dd import copy_data


class TestDDCopy(unittest.TestCase):
    """Test cases for the dd copy functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up test files."""
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)
    
    def test_copy_small_file(self):
        """Test copying a small file."""
        input_file = os.path.join(self.test_dir, 'input.txt')
        output_file = os.path.join(self.test_dir, 'output.txt')
        
        # Create input file
        test_data = b'Hello, World!'
        with open(input_file, 'wb') as f:
            f.write(test_data)
        
        # Copy the file
        blocks, bytes_copied = copy_data(input_file, output_file, block_size=512)
        
        # Verify
        self.assertEqual(bytes_copied, len(test_data))
        self.assertEqual(blocks, 1)
        
        with open(output_file, 'rb') as f:
            result = f.read()
        
        self.assertEqual(result, test_data)
    
    def test_copy_with_block_size(self):
        """Test copying with custom block size."""
        input_file = os.path.join(self.test_dir, 'input.txt')
        output_file = os.path.join(self.test_dir, 'output.txt')
        
        # Create input file with more data
        test_data = b'A' * 1024
        with open(input_file, 'wb') as f:
            f.write(test_data)
        
        # Copy with 256 byte blocks
        blocks, bytes_copied = copy_data(input_file, output_file, block_size=256)
        
        # Verify
        self.assertEqual(bytes_copied, 1024)
        self.assertEqual(blocks, 4)
        
        with open(output_file, 'rb') as f:
            result = f.read()
        
        self.assertEqual(result, test_data)
    
    def test_copy_with_count(self):
        """Test copying a limited number of blocks."""
        input_file = os.path.join(self.test_dir, 'input.txt')
        output_file = os.path.join(self.test_dir, 'output.txt')
        
        # Create input file
        test_data = b'A' * 1024
        with open(input_file, 'wb') as f:
            f.write(test_data)
        
        # Copy only 2 blocks of 256 bytes
        blocks, bytes_copied = copy_data(
            input_file, output_file, 
            block_size=256, count=2
        )
        
        # Verify
        self.assertEqual(bytes_copied, 512)
        self.assertEqual(blocks, 2)
        
        with open(output_file, 'rb') as f:
            result = f.read()
        
        self.assertEqual(len(result), 512)
        self.assertEqual(result, test_data[:512])
    
    def test_copy_empty_file(self):
        """Test copying an empty file."""
        input_file = os.path.join(self.test_dir, 'empty.txt')
        output_file = os.path.join(self.test_dir, 'output.txt')
        
        # Create empty file
        with open(input_file, 'wb') as f:
            pass
        
        # Copy
        blocks, bytes_copied = copy_data(input_file, output_file)
        
        # Verify
        self.assertEqual(bytes_copied, 0)
        self.assertEqual(blocks, 0)
        
        self.assertTrue(os.path.exists(output_file))
        self.assertEqual(os.path.getsize(output_file), 0)
    
    def test_copy_binary_data(self):
        """Test copying binary data."""
        input_file = os.path.join(self.test_dir, 'binary.dat')
        output_file = os.path.join(self.test_dir, 'output.dat')
        
        # Create binary file
        test_data = bytes(range(256))
        with open(input_file, 'wb') as f:
            f.write(test_data)
        
        # Copy
        blocks, bytes_copied = copy_data(input_file, output_file, block_size=100)
        
        # Verify
        self.assertEqual(bytes_copied, 256)
        
        with open(output_file, 'rb') as f:
            result = f.read()
        
        self.assertEqual(result, test_data)


if __name__ == '__main__':
    unittest.main()
