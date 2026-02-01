"""
Test suite for translator.py functions
Tests property data extraction and translation functions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from translator import (
    get_property_type,
    get_habitable_rooms,
    get_floor_area,
    get_epc_values,
    get_desc_df
)


def test_get_property_type():
    """Test property type extraction"""
    print("\n🧪 Testing get_property_type()...")
    try:
        # Test with a known postcode and address
        result = get_property_type("SW1A", "10 Downing Street")
        print(f"   Property type for 10 Downing Street: {result}")
        assert result in ["F", "D", "S", "T", None], f"Invalid property type: {result}"
        print("   ✓ PASS")
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")


def test_get_habitable_rooms():
    """Test habitable rooms extraction"""
    print("\n🧪 Testing get_habitable_rooms()...")
    try:
        result = get_habitable_rooms("SW1A", "10 Downing Street")
        print(f"   Habitable rooms for 10 Downing Street: {result}")
        if result is not None:
            assert isinstance(result, (int, float)) and result > 0, f"Invalid room count: {result}"
        print("   ✓ PASS")
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")


def test_get_floor_area():
    """Test floor area extraction"""
    print("\n🧪 Testing get_floor_area()...")
    try:
        result = get_floor_area("SW1A", "10 Downing Street")
        print(f"   Floor area for 10 Downing Street: {result} sqm")
        if result is not None:
            assert isinstance(result, (int, float)) and result > 0, f"Invalid floor area: {result}"
        print("   ✓ PASS")
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")


def test_get_epc_values():
    """Test EPC values extraction"""
    print("\n🧪 Testing get_epc_values()...")
    try:
        result = get_epc_values("SW1A", "10 Downing Street")
        print(f"   EPC values keys: {list(result.keys())}")
        print(f"   Sample: {dict(list(result.items())[:2])}")
        assert isinstance(result, dict), f"Expected dict, got {type(result)}"
        print("   ✓ PASS")
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")


def test_get_desc_df():
    """Test description dataframe extraction"""
    print("\n🧪 Testing get_desc_df()...")
    try:
        result = get_desc_df("SW1A", "10 Downing Street")
        print(f"   Description dataframe shape: {result.shape if result is not None else 'None'}")
        if result is not None:
            print(f"   Columns: {list(result.columns)}")
        print("   ✓ PASS")
    except Exception as e:
        print(f"   ❌ FAIL: {str(e)}")


def run_all_tests():
    """Run all translator tests"""
    print("=" * 60)
    print("TRANSLATOR.PY TEST SUITE")
    print("=" * 60)
    
    test_get_property_type()
    test_get_habitable_rooms()
    test_get_floor_area()
    test_get_epc_values()
    test_get_desc_df()
    
    print("\n" + "=" * 60)
    print("✓ Test suite completed")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
