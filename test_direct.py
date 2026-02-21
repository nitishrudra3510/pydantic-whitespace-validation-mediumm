#!/usr/bin/env python3
"""Direct test of the min_length_validator function."""
import sys
sys.path.insert(0, '/Users/nitishkumar/Documents/GitHub/pydantic')

from pydantic._internal._validators import min_length_validator
from pydantic_core import PydanticKnownError

print("=" * 70)
print("Direct Test of min_length_validator Function")
print("=" * 70)

# Test 1: Whitespace rejection with min_length > 0
print("\n[TEST 1] min_length=1 should reject whitespace-only strings")
print("-" * 70)

test_cases_1 = [
    ("'a'", "a", 1, True),
    ("' a '", " a ", 1, True),
    ("'   '", "   ", 1, False),
    ("'\\t'", "\t", 1, False),
    ("'\\n'", "\n", 1, False),
    ("''", "", 1, False),
]

for display, value, min_len, should_pass in test_cases_1:
    try:
        result = min_length_validator(value, min_len)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted -> {result!r}")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected) -> {result!r}")
    except PydanticKnownError as e:
        if not should_pass:
            print(f"  ✓ PASS: {display:12} rejected")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")

# Test 2: min_length=0 allows whitespace
print("\n[TEST 2] min_length=0 should allow whitespace-only strings")
print("-" * 70)

test_cases_2 = [
    ("''", "", 0, True),
    ("'   '", "   ", 0, True),
    ("'a'", "a", 0, True),
]

for display, value, min_len, should_pass in test_cases_2:
    try:
        result = min_length_validator(value, min_len)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted -> {result!r}")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected)")
    except PydanticKnownError as e:
        if not should_pass:
            print(f"  ✓ PASS: {display:12} rejected")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")

# Test 3: Non-string types should not trigger whitespace check
print("\n[TEST 3] Non-string types should work as before")
print("-" * 70)

test_cases_3 = [
    ("list([1])", [1], 1, True),
    ("list([1,2])", [1, 2], 1, True),
    ("list([])", [], 1, False),  # Empty list
    ("bytes(b'a')", b"a", 1, True),
    ("bytes(b'')", b"", 1, False),  # Empty bytes
]

for display, value, min_len, should_pass in test_cases_3:
    try:
        result = min_length_validator(value, min_len)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted -> {type(result).__name__}")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected)")
    except PydanticKnownError as e:
        if not should_pass:
            print(f"  ✓ PASS: {display:12} rejected")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")

# Test 4: min_length=3 on various string inputs
print("\n[TEST 4] min_length=3 with mixed whitespace/content")
print("-" * 70)

test_cases_4 = [
    ("'ab'", "ab", 3, False),        # Too short
    ("'abc'", "abc", 3, True),       # Exact length
    ("'  a '", "  a ", 3, True),     # Has content
    ("'   '", "   ", 3, False),      # Whitespace-only (fails even though len=3)
    ("'     '", "     ", 3, False),  # 5 spaces - whitespace-only still rejected
]

for display, value, min_len, should_pass in test_cases_4:
    try:
        result = min_length_validator(value, min_len)
        if should_pass:
            print(f"  ✓ PASS: {display:12} accepted (len={len(result)})")
        else:
            print(f"  ✗ FAIL: {display:12} accepted (should be rejected) (len={len(result)})")
    except PydanticKnownError as e:
        if not should_pass:
            print(f"  ✓ PASS: {display:12} rejected")
        else:
            print(f"  ✗ FAIL: {display:12} rejected (should be accepted)")

print("\n" + "=" * 70)
print("All direct validator tests completed!")
print("=" * 70)
