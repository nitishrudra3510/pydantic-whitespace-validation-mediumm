#!/usr/bin/env python3
"""Test the whitespace constraint implementation."""
import sys
from typing import Annotated

# Add the pydantic module to the path
sys.path.insert(0, '/Users/nitishkumar/Documents/GitHub/pydantic')

from pydantic import BaseModel, ValidationError, TypeAdapter
from pydantic.types import StringConstraints


def test_basic():
    """Test basic functionality."""
    print("Test 1: Basic min_length with whitespace rejection")
    ta = TypeAdapter(Annotated[str, StringConstraints(min_length=1)])
    
    # Should pass
    try:
        result = ta.validate_python('a')
        print(f"  ✓ PASS: 'a' accepted -> {result!r}")
    except ValidationError as e:
        print(f"  ✗ FAIL: 'a' rejected: {e}")
        return False
    
    # Should fail
    try:
        result = ta.validate_python('   ')
        print(f"  ✗ FAIL: '   ' accepted (should have been rejected) -> {result!r}")
        return False
    except ValidationError as e:
        print(f"  ✓ PASS: '   ' rejected as expected")
    
    return True


def test_min_length_zero():
    """Test that min_length=0 allows whitespace."""
    print("\nTest 2: min_length=0 allows whitespace")
    ta = TypeAdapter(Annotated[str, StringConstraints(min_length=0)])
    
    try:
        result = ta.validate_python('   ')
        print(f"  ✓ PASS: '   ' accepted with min_length=0 -> {result!r}")
        return True
    except ValidationError as e:
        print(f"  ✗ FAIL: '   ' rejected with min_length=0: {e}")
        return False


def test_no_min_length():
    """Test that without min_length, whitespace is allowed."""
    print("\nTest 3: No min_length allows whitespace")
    ta = TypeAdapter(str)
    
    try:
        result = ta.validate_python('   ')
        print(f"  ✓ PASS: '   ' accepted without min_length -> {result!r}")
        return True
    except ValidationError as e:
        print(f"  ✗ FAIL: '   ' rejected without min_length: {e}")
        return False


def test_with_content():
    """Test strings with actual content."""
    print("\nTest 4: Strings with content pass")
    ta = TypeAdapter(Annotated[str, StringConstraints(min_length=1)])
    
    try:
        result = ta.validate_python(' a ')
        print(f"  ✓ PASS: ' a ' accepted -> {result!r}")
        return True
    except ValidationError as e:
        print(f"  ✗ FAIL: ' a ' rejected: {e}")
        return False


def test_various_whitespace():
    """Test various whitespace characters."""
    print("\nTest 5: Various whitespace characters")
    ta = TypeAdapter(Annotated[str, StringConstraints(min_length=1)])
    
    test_strings = ['\t', '\n', '\r', '  \t\n  ', '']
    for test_str in test_strings:
        try:
            result = ta.validate_python(test_str)
            print(f"  ✗ FAIL: {test_str!r} accepted (should have been rejected)")
            return False
        except ValidationError:
            print(f"  ✓ PASS: {test_str!r} rejected as expected")
    
    return True


if __name__ == '__main__':
    all_pass = True
    
    try:
        all_pass &= test_basic()
        all_pass &= test_min_length_zero()
        all_pass &= test_no_min_length()
        all_pass &= test_with_content()
        all_pass &= test_various_whitespace()
        
        if all_pass:
            print("\n✅ All tests PASSED!")
            sys.exit(0)
        else:
            print("\n❌ Some tests FAILED!")
            sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
