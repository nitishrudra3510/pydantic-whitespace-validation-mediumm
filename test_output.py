#!/usr/bin/env python3
"""Simple test to verify whitespace constraint implementation."""
import sys
sys.path.insert(0, '/Users/nitishkumar/Documents/GitHub/pydantic')

from typing import Annotated
from pydantic import ValidationError
from pydantic.types import StringConstraints
from pydantic import TypeAdapter

print("=" * 70)
print("Testing Constrained String Validation with Whitespace Check")
print("=" * 70)

# Test 1: Basic whitespace rejection
print("\n[TEST 1] min_length=1 should reject whitespace-only strings")
print("-" * 70)
ta = TypeAdapter(Annotated[str, StringConstraints(min_length=1)])

test_cases_1 = [
    ("'a'", "a", True),
    ("' a '", " a ", True),
    ("'   '", "   ", False),
    ("'\\t'", "\t", False),
    ("'\\n'", "\n", False),
    ("''", "", False),
]

for display, value, should_pass in test_cases_1:
    try:
        result = ta.validate_python(value)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted -> {result!r}")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected) -> {result!r}")
    except ValidationError as e:
        if not should_pass:
            print(f"  ✓ PASS: {display:12} rejected as expected")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")
            print(f"    Error: {e.errors()[0]['msg']}")

# Test 2: min_length=0 allows whitespace
print("\n[TEST 2] min_length=0 should allow whitespace-only strings")
print("-" * 70)
ta = TypeAdapter(Annotated[str, StringConstraints(min_length=0)])

test_cases_2 = [
    ("''", "", True),
    ("'   '", "   ", True),
    ("'a'", "a", True),
]

for display, value, should_pass in test_cases_2:
    try:
        result = ta.validate_python(value)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted -> {result!r}")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected)")
    except ValidationError as e:
        if not should_pass:
            print(f"  ✓ PASS: {display:12} rejected as expected")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")

# Test 3: No constraint allows whitespace
print("\n[TEST 3] No min_length constraint should allow whitespace")
print("-" * 70)
ta = TypeAdapter(str)

test_cases_3 = [
    ("''", "", True),
    ("'   '", "   ", True),
    ("'a'", "a", True),
]

for display, value, should_pass in test_cases_3:
    try:
        result = ta.validate_python(value)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted -> {result!r}")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected)")
    except ValidationError as e:
        if not should_pass:
            print(f"  ✓ PASS: {display:12} rejected as expected")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")

# Test 4: min_length=3 on various inputs
print("\n[TEST 4] min_length=3 on various inputs")
print("-" * 70)
ta = TypeAdapter(Annotated[str, StringConstraints(min_length=3)])

test_cases_4 = [
    ("'ab'", "ab", False),
    ("'abc'", "abc", True),
    ("'  a '", "  a ", True),
    ("'   '", "   ", False),
    ("'     '", "     ", True),  # 5 spaces >= 3
]

for display, value, should_pass in test_cases_4:
    try:
        result = ta.validate_python(value)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted -> {result!r} (len={len(result)})")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected) -> {result!r}")
    except ValidationError as e:
        if not should_pass:
            error_msg = e.errors()[0]['msg']
            print(f"  ✓ PASS: {display:12} rejected: {error_msg}")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")

print("\n" + "=" * 70)
print("All tests completed!")
print("=" * 70)
