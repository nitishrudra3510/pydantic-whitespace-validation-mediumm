#!/usr/bin/env python3
"""Test using Pydantic models directly (avoids TypeAdapter issues)."""
import sys
sys.path.insert(0, '/Users/nitishkumar/Documents/GitHub/pydantic')

from typing import Annotated
from pydantic import BaseModel, ValidationError
from pydantic.types import StringConstraints

print("=" * 70)
print("Testing Whitespace Validation with Pydantic Models")
print("=" * 70)

# Define models with string constraints
print("\n[Model Definition]")
print("-" * 70)

class UserProfile(BaseModel):
    username: Annotated[str, StringConstraints(min_length=3)]
    bio: Annotated[str, StringConstraints(min_length=0)] | None = None

print("Created UserProfile model with:")
print("  - username: min_length=3 (rejects whitespace-only)")
print("  - bio: min_length=0 (allows whitespace-only)")

# Test 1: Valid usernames
print("\n[TEST 1] Valid usernames")
print("-" * 70)

valid_usernames = [
    ("alice", "Valid username with text"),
    ("bob123", "Username with numbers"),
    ("  john  ", "Username with whitespace padding"),
]

for username, description in valid_usernames:
    try:
        user = UserProfile(username=username, bio="Some bio")
        print(f"  ✓ PASS: {username:12} accepted - {description}")
    except ValidationError as e:
        print(f"  ✗ FAIL: {username:12} rejected - {e.errors()[0]['msg']}")

# Test 2: Invalid usernames (whitespace-only)
print("\n[TEST 2] Invalid usernames (whitespace-only)")
print("-" * 70)

invalid_usernames = [
    ("   ", "3 spaces"),
    ("\t\t", "2 tabs"),
    ("\n", "newline"),
    ("", "empty string"),
]

for username, description in invalid_usernames:
    try:
        user = UserProfile(username=username, bio="Some bio")
        print(f"  ✗ FAIL: {repr(username):12} accepted - {description}")
    except ValidationError as e:
        print(f"  ✓ PASS: {repr(username):12} rejected - {description}")

# Test 3: Bio field allows whitespace-only
print("\n[TEST 3] Bio field (min_length=0) allows whitespace-only")
print("-" * 70)

bio_tests = [
    ("alice", None, "No bio provided"),
    ("bob", "", "Empty bio"),
    ("charlie", "   ", "Whitespace-only bio"),
    ("dave", "\t\t", "Tab-only bio"),
]

for username, bio, description in bio_tests:
    try:
        user = UserProfile(username=username, bio=bio)
        print(f"  ✓ PASS: username={username:8} bio={repr(bio):8} accepted - {description}")
    except ValidationError as e:
        print(f"  ✗ FAIL: username={username:8} bio={repr(bio):8} rejected - {e.errors()[0]['msg']}")

print("\n" + "=" * 70)
print("All Pydantic model tests completed!")
print("=" * 70)
