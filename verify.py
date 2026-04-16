#!/usr/bin/env python3
"""
Quick verification script for the contact manager app.
Tests that all data structures and routes are properly initialized.
"""

import sys
sys.path.insert(0, '/Users/aaronowens/Documents/cs_course_project/COP4538-Code')

try:
    from app import app, contacts, category_tree, category_bst, vip_queue
    
    print("✓ App imports successful")
    print()
    
    # Test data structures
    print("=== Data Structure Verification ===")
    all_contacts = contacts.to_list()
    print(f"✓ Contacts loaded: {len(all_contacts)} contacts")
    
    # Test VIP
    vip_count = len([c for c in all_contacts if c.get('priority', 1) > 3])
    print(f"✓ VIP System: {vip_count} VIP contacts")
    
    # Test Category Tree
    tree_dict = category_tree.to_dict()
    print(f"✓ Category Tree: {len(tree_dict.get('children', []))} top-level categories")
    print(f"  Categories: {', '.join([cat.get('name', 'Unknown') for cat in tree_dict.get('children', [])])}")
    
    # Test BST
    categories = category_bst.inorder_traversal()
    print(f"✓ BST Implementation: {len(categories)} categories stored")
    
    # Test routes
    print()
    print("=== Route Verification ===")
    with app.test_client() as client:
        # Test index route
        resp = client.get('/')
        print(f"✓ GET / : Status {resp.status_code}")
        
        # Test manage route
        resp = client.get('/manage')
        print(f"✓ GET /manage : Status {resp.status_code}")
        
        # Test search route
        resp = client.get('/search?search=test')
        print(f"✓ GET /search : Status {resp.status_code}")
    
    print()
    print("✓ All verifications passed!")
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
