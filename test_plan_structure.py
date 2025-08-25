#!/usr/bin/env python3
"""Test script to verify subscription plan data structure"""

from subscription_manager import SubscriptionManager
import json

def test_plan_structure():
    """Test the structure of all subscription plans"""
    sm = SubscriptionManager()
    
    print("Testing subscription plan data structure...")
    print("=" * 50)
    
    for plan_key, plan_data in sm.plans.items():
        print(f"\n📋 Plan: {plan_key.upper()}")
        print(f"   Name: {plan_data.get('name', 'MISSING')}")
        
        # Test pricing structure
        pricing = plan_data.get('pricing', {})
        print(f"   Pricing:")
        for period in ['weekly', 'monthly', 'quarterly', 'yearly']:
            price = pricing.get(period, 'MISSING')
            print(f"     {period}: {price} (type: {type(price)})")
        
        # Test limits structure
        limits = plan_data.get('limits', {})
        print(f"   Limits:")
        for limit_key in ['questions_per_day', 'documents', 'users']:
            limit_value = limits.get(limit_key, 'MISSING')
            print(f"     {limit_key}: {limit_value} (type: {type(limit_value)})")
        
        print("-" * 30)
    
    print("\n✅ Structure test complete!")

if __name__ == "__main__":
    test_plan_structure()
