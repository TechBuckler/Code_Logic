#!/usr/bin/env python
"""
Shadow Tree Navigation Test Script

This script tests the bubble up and drill down functionality of the Shadow Tree
to ensure it works correctly before integrating with the UI.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import the shadow tree components

def test_navigation():
    """Test the Shadow Tree navigation functionality."""
    print("\n🧪 Testing Shadow Tree Navigation")
    print("=" * 50)
    
    # Initialize the Shadow Tree API
    code_dir = Path(project_root) / "src"
    shadow_dir = Path(project_root) / "shadow_tree_output"
    
    print(f"\n📂 Code directory: {code_dir}")
    print(f"📂 Shadow directory: {shadow_dir}")
    
    # Ensure the shadow directory exists
    os.makedirs(shadow_dir, exist_ok=True)
    
    # Create or load the Shadow Tree
    api = ShadowTreeAPI(str(code_dir), str(shadow_dir))
    
    if not api.navigator or not api.navigator.tree:
        print("\n❌ Failed to initialize Shadow Tree Navigator")
        return
    
    print("\n✅ Successfully initialized Shadow Tree Navigator")
    print(f"🌳 Root node: {api.navigator.tree.name}")
    
    # Test navigation operations
    test_drill_down(api)
    test_bubble_up(api)
    test_search(api)

def test_drill_down(api):
    """Test drilling down into the Shadow Tree."""
    print("\n\n🔍 Testing Drill Down")
    print("=" * 50)
    
    # Get the initial node
    initial_node = api.navigator.current_node
    print(f"📍 Starting at: {initial_node.name}")
    
    # Get the children of the current node
    if hasattr(initial_node, 'children') and initial_node.children:
        print(f"\n📋 Children of {initial_node.name}:")
        for i, child in enumerate(initial_node.children):
            print(f"  {i+1}. {child.name}")
        
        # Try to drill down to the first child
        if initial_node.children:
            target_child = initial_node.children[0].name
            print(f"\n🔽 Drilling down to: {target_child}")
            
            success = api.navigator.go_down(target_child)
            if success:
                print(f"✅ Successfully drilled down to: {api.navigator.current_node.name}")
                
                # Check if the current node is actually the target
                if api.navigator.current_node.name == target_child:
                    print("✅ Current node matches target")
                else:
                    print(f"❌ Current node ({api.navigator.current_node.name}) does not match target ({target_child})")
            else:
                print(f"❌ Failed to drill down to: {target_child}")
    else:
        print(f"❌ Node {initial_node.name} has no children")

def test_bubble_up(api):
    """Test bubbling up in the Shadow Tree."""
    print("\n\n🔍 Testing Bubble Up")
    print("=" * 50)
    
    # Get the current node
    current_node = api.navigator.current_node
    print(f"📍 Starting at: {current_node.name}")
    
    # Check if we can bubble up
    if hasattr(current_node, 'parent') and current_node.parent:
        parent_name = current_node.parent.name
        print(f"👆 Parent node: {parent_name}")
        
        # Try to bubble up
        print("\n🔼 Bubbling up one level")
        success = api.navigator.go_up()
        if success:
            print(f"✅ Successfully bubbled up to: {api.navigator.current_node.name}")
            
            # Check if the current node is actually the parent
            if api.navigator.current_node.name == parent_name:
                print("✅ Current node matches parent")
            else:
                print(f"❌ Current node ({api.navigator.current_node.name}) does not match parent ({parent_name})")
        else:
            print("❌ Failed to bubble up")
    else:
        print(f"❌ Node {current_node.name} has no parent (already at root)")

def test_search(api):
    """Test searching in the Shadow Tree."""
    print("\n\n🔍 Testing Search")
    print("=" * 50)
    
    # Test search query
    query = "module"
    print(f"🔎 Searching for: '{query}'")
    
    results = api.search(query)
    if results:
        print(f"✅ Found {len(results)} results")
        print("\n📋 Top 5 results:")
        
        for i, (node, score) in enumerate(sorted(results[:5], key=lambda x: x[1], reverse=True)):
            path = []
            current = node
            while current:
                path.append(current.name)
                current = current.parent
            path_str = " > ".join(reversed(path))
            
            print(f"  {i+1}. {path_str} (score: {score:.2f})")
            print(f"     {node.summary if hasattr(node, 'summary') and node.summary else 'No summary'}")
    else:
        print(f"❌ No results found for '{query}'")

def fix_navigation_issues():
    """Fix any issues with the Shadow Tree navigation."""
    print("\n\n🔧 Fixing Navigation Issues")
    print("=" * 50)
    
    # Regenerate the Shadow Tree
    code_dir = Path(project_root) / "src"
    shadow_dir = Path(project_root) / "shadow_tree_output"
    
    print(f"\n🔄 Regenerating Shadow Tree for {code_dir}")
    generator = ShadowTreeGenerator()
    root = generator.generate_from_directory(code_dir, shadow_dir)
    
    print("✅ Shadow Tree regenerated successfully")
    
    # Test navigation after regeneration
    api = ShadowTreeAPI(str(code_dir), str(shadow_dir))
    test_navigation()

if __name__ == "__main__":
    # First test the current navigation
    test_navigation()
    
    # If there are issues, fix them
    fix_navigation_issues()
