#!/usr/bin/env python3
"""Quick test of current behavior."""
from typing import Annotated
from pydantic import BaseModel, ValidationError
from pydantic.types import StringConstraints

class Model(BaseModel):
    v: Annotated[str, StringConstraints(min_length=1)]

print("Test 1 - Normal string with min_length=1:")
try:
    result = Model(v='a')
    print(f"  PASS: {result.v!r}")
except ValidationError as e:
    print(f"  FAIL: {e}")

print("\nTest 2 - Whitespace-only string with min_length=1:")
try:
    result = Model(v='   ')
    print(f"  PASS (currently allows it): {result.v!r}")
except ValidationError as e:
    print(f"  FAIL (rejects it): {e}")

print("\nTest 3 - Empty string with min_length=1:")
try:
    result = Model(v='')
    print(f"  PASS: {result.v!r}")
except ValidationError as e:
    print(f"  FAIL: {e}")
