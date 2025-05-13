#!/usr/bin/env python
"""
Shadow Tree Module

This module integrates the Shadow Tree system with the unified UI,
allowing for natural language navigation of the codebase.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# Import the shadow tree
sys.path.append(os.path.dirname(parent_dir))
    ShadowTreeGenerator,
    ShadowTreeNavigator,
    ShadowNode,
    ShadowTreeAPI
)

class ShadowTreeModule:
    """Module for integrating the Shadow Tree with the unified UI."""
    
    def __init__(self):
        self.name = "Shadow Tree Module"
        self.description = "Natural language navigation of the codebase"
        self.shadow_dir = Path(os.path.dirname(parent_dir)) / "shadow_tree_output"
        self.code_dir = Path(parent_dir)
        self.navigator = None
        self.current_path = []
        self.active = False
    
    def initialize(self):
        """Initialize the module."""
        self._load_or_generate_tree()
        self.active = True
        return True
    
    def _load_or_generate_tree(self):
        """Load the shadow tree if it exists, or generate it if not."""
        # Ensure shadow directory exists
        os.makedirs(self.shadow_dir, exist_ok=True)
        
        # Path to shadow tree JSON
        tree_path = self.shadow_dir / "shadow_tree.json"
        
        # Check if we need to generate the tree
        force_generate = not tree_path.exists()
        
        if force_generate:
            print(f"Shadow tree not found at {tree_path}, generating new tree...")
            try:
                # Generate the tree
                generator = ShadowTreeGenerator()
                generator.generate_from_directory(self.code_dir, self.shadow_dir)
                print(f"Generated new Shadow Tree in {self.shadow_dir}")
            except Exception as e:
                print(f"Error generating Shadow Tree: {e}")
                return False
        
        # Now load the tree
        try:
            self.api = ShadowTreeAPI(str(self.code_dir), str(self.shadow_dir))
            print(f"Loaded Shadow Tree API for {self.code_dir}")
            
            # Get the navigator from the API
            self.navigator = self.api.navigator
            
            # Verify the navigator and tree are valid
            if not self.navigator or not self.navigator.tree:
                print("Warning: Navigator or tree is None, attempting to regenerate...")
                # Force regeneration
                generator = ShadowTreeGenerator()
                generator.generate_from_directory(self.code_dir, self.shadow_dir)
                # Reload the navigator
                self.api = ShadowTreeAPI(str(self.code_dir), str(self.shadow_dir))
                self.navigator = self.api.navigator
                
                if not self.navigator or not self.navigator.tree:
                    print("Error: Still could not load Shadow Tree after regeneration")
                    return False
            
            print(f"Successfully loaded Shadow Tree with root: {self.navigator.tree.name}")
            return True
                
        except Exception as e:
            print(f"Error initializing Shadow Tree: {e}")
            return False
    
    def can_process(self, command):
        """Check if this module can process the given command."""
        shadow_commands = [
            "shadow", "tree", "navigate", "explore", "search", "find",
            "bubble", "drill", "up", "down", "code", "structure"
        ]
        
        command_words = command.lower().split()
        return any(cmd in command_words for cmd in shadow_commands)
    
    def process(self, command):
        """Process a command related to the Shadow Tree."""
        if not self.active:
            success = self.initialize()
            if not success:
                return "Failed to initialize Shadow Tree. Please check logs for details."
        
        if not self.navigator or not self.navigator.tree:
            return "Shadow Tree not properly initialized. Please try again."
        
        command = command.lower()
        
        try:
            # Handle search commands
            if "search" in command or "find" in command:
                query = command.replace("search", "").replace("find", "").strip()
                return self._search(query)
            
            # Handle navigation commands
            if "bubble" in command or "up" in command:
                levels = 1
                if "2" in command or "two" in command:
                    levels = 2
                elif "3" in command or "three" in command:
                    levels = 3
                return self._bubble_up(levels)
            
            if "drill" in command or "down" in command:
                parts = command.split()
                target = None
                for i, part in enumerate(parts):
                    if part in ["to", "into", "down"]:
                        if i + 1 < len(parts):
                            target = parts[i + 1]
                            break
                
                if target:
                    return self._drill_down(target)
                else:
                    return "Please specify a target to drill down to."
            
            # Show current location
            if "where" in command or "location" in command:
                return self._show_current_location()
            
            # Show children
            if "children" in command or "list" in command:
                return self._show_children()
            
            # Regenerate tree
            if "regenerate" in command or "rebuild" in command:
                return self._regenerate_tree()
            
            # Default to showing help
            return self.get_help()
        except Exception as e:
            return f"Error processing command: {str(e)}"
    
    def _search(self, query):
        """Search the shadow tree for the given query."""
        if not query:
            return "Please provide a search term."
        
        results = self.navigator.search(query)
        
        if not results:
            return f"No results found for '{query}'."
        
        # Sort results by score
        results.sort(key=lambda x: x[1], reverse=True)
        
        output = f"🔍 Search results for '{query}':\n\n"
        
        for node, score in results[:10]:
            path = []
            current = node
            while current:
                path.append(current.name)
                current = current.parent
            path_str = " > ".join(reversed(path))
            
            output += f"- {path_str}\n"
            output += f"  {node.summary}\n\n"
        
        return output
    
    def _bubble_up(self, levels=1):
        """Bubble up to a higher level in the tree."""
        if not self.navigator or not self.navigator.current_node:
            return "Cannot bubble up: Shadow Tree not properly initialized."
            
        try:
            success = False
            for _ in range(levels):
                if self.navigator.go_up():
                    success = True
                else:
                    break
                    
            if success:
                self.current_path = self.navigator.get_path_to_root()
                output = f"📂 Bubbled up {levels} level{'s' if levels > 1 else ''}.\n\n"
                output += self._format_node_info(self.navigator.current_node)
                return output
            else:
                return f"Could not bubble up {levels} levels. Already at top level."
        except Exception as e:
            return f"Error bubbling up: {str(e)}"
    
    def _drill_down(self, target):
        """Drill down to a child node."""
        if not self.navigator or not self.navigator.current_node:
            return "Cannot drill down: Shadow Tree not properly initialized."
            
        try:
            # Use the go_down method which now handles partial matches
            if self.navigator.go_down(target):
                self.current_path = self.navigator.get_path_to_root()
                output = f"📂 Drilled down to {self.navigator.current_node.name}.\n\n"
                output += self._format_node_info(self.navigator.current_node)
                return output
            else:
                return f"Could not find a child matching '{target}'.\n\n" + self._show_children()
        except Exception as e:
            return f"Error drilling down: {str(e)}"
    
    def _show_children(self):
        """Show the children of the current node."""
        if not self.navigator or not self.navigator.current_node:
            return "Cannot show children: Shadow Tree not properly initialized."
            
        try:
            node = self.navigator.current_node
            
            if not hasattr(node, 'children') or not node.children:
                return f"{node.name} has no children."
            
            output = f"📂 Children of {node.name}:\n\n"
            
            for child in node.children:
                output += f"- {child.name}\n"
                summary = child.summary if hasattr(child, 'summary') and child.summary else "No summary available"
                output += f"  {summary}\n\n"
            
            return output
        except Exception as e:
            return f"Error showing children: {str(e)}"
    
    def _show_current_location(self):
        """Show the current location in the shadow tree."""
        if not self.navigator or not self.navigator.current_node:
            return "Shadow Tree not properly initialized or no current location."
            
        node = self.navigator.current_node
        try:
            self.current_path = self.navigator.get_path_to_root()
            
            output = "📍 Current location:\n"
            if self.current_path:
                output += " > ".join(n.name for n in self.current_path) + "\n\n"
            else:
                output += "Root\n\n"
                
            output += self._format_node_info(node)
            
            return output
        except Exception as e:
            return f"Error showing current location: {str(e)}"
    
    def _format_node_info(self, node):
        """Format information about a node."""
        if not node:
            return "No node information available."
            
        output = f"# {node.name}\n\n"
        
        if hasattr(node, 'summary') and node.summary:
            output += f"{node.summary}\n\n"
        
        if hasattr(node, 'description') and node.description:
            output += f"## Description\n\n{node.description}\n\n"
        
        if hasattr(node, 'code_path') and node.code_path:
            output += f"## Code Path\n\n`{node.code_path}`\n\n"
        
        if hasattr(node, 'children') and node.children:
            output += f"## Children\n\n"
            for child in node.children:
                child_summary = child.summary if hasattr(child, 'summary') and child.summary else "No summary available"
                output += f"- {child.name}: {child_summary}\n"
        
        return output
    
    def get_help(self):
        """Get help information for this module."""
        return """
        Shadow Tree Module - Natural Language Navigation
        
        Commands:
        - search/find [query]: Search the codebase for components matching the query
        - bubble up [levels]: Move up in the hierarchy (default: 1 level)
        - drill down [component]: Move down to a specific component
        - show children: Show all children of the current component
        
        Examples:
        - "search optimizer"
        - "bubble up 2 levels"
        - "drill down to optimizer"
        """

    def _regenerate_tree(self):
        """Regenerate the shadow tree."""
        try:
            print("Regenerating Shadow Tree...")
            # Ensure shadow directory exists
            os.makedirs(self.shadow_dir, exist_ok=True)
            
            # Generate the tree
            generator = ShadowTreeGenerator()
            generator.generate_from_directory(self.code_dir, self.shadow_dir)
            
            # Reload the API and navigator
            self.api = ShadowTreeAPI(str(self.code_dir), str(self.shadow_dir))
            self.navigator = self.api.navigator
            
            if self.navigator and self.navigator.tree:
                return f"✅ Successfully regenerated Shadow Tree with root: {self.navigator.tree.name}"
            else:
                return "❌ Failed to regenerate Shadow Tree: Navigator or tree is None"
        except Exception as e:
            return f"❌ Error regenerating Shadow Tree: {str(e)}"

# For testing
if __name__ == "__main__":
    module = ShadowTreeModule()
    module.initialize()
    
    # Test search
    print(module.process("search optimizer"))
    
    # Test navigation
    print(module.process("drill down to optimizer"))
    print(module.process("bubble up"))
