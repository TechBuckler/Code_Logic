#!/usr/bin/env python
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase


# Simple Shadow Tree Generator
# This version doesn't rely on NLTK for natural language processing

import os
import json
import ast
import argparse

class ShadowNode:
    """A node in the shadow tree."""
    
    def __init__(self, name, path, code_path=None, parent=None):
        self.name = name
        self.path = Path(path)
        self.code_path = code_path
        self.parent = parent
        self.children = []
        self.summary = ""
        self.description = ""
        self.keywords = []
        
    def add_child(self, child):
        """Add a child node."""
        self.children.append(child)
        
    def to_dict(self):
        """Convert the node to a dictionary."""
        return {
            'name': self.name,
            'path': str(self.path),
            'code_path': str(self.code_path) if self.code_path else None,
            'summary': self.summary,
            'description': self.description,
            'keywords': self.keywords,
            'children': [child.to_dict() for child in self.children]
        }

class SimpleShadowTreeGenerator:
    """Generates a natural language shadow tree from a code tree."""
    
    def __init__(self):
        self.root = None
        self.files_processed = 0
        self.dirs_processed = 0
        
    def generate_from_directory(self, code_dir, output_dir=None):
        """Generate a shadow tree from a code directory."""
        code_dir = Path(code_dir)
        print(f"\n🌳 Generating Shadow Tree for {code_dir}")
        print(f"📂 Output directory: {output_dir}\n")
        
        # Create root node
        self.root = ShadowNode(code_dir.name, Path(output_dir) if output_dir else code_dir)
        print(f"🌱 Created root node: {self.root.name}")
        
        # Process the directory
        print(f"\n📊 Processing directory structure...")
        self._process_directory(code_dir, self.root)
        print(f"✅ Processed {self.files_processed} files and {self.dirs_processed} directories")
        
        # Generate natural language descriptions
        print(f"\n🔍 Generating natural language descriptions...")
        self._generate_descriptions(self.root)
        print(f"✅ Generated descriptions for all nodes")
        
        # Save the shadow tree
        if output_dir:
            print(f"\n💾 Saving shadow tree to {output_dir}...")
            output_dir = Path(output_dir)
            os.makedirs(output_dir, exist_ok=True)
            self._save_shadow_tree(output_dir)
            print(f"✅ Shadow tree saved successfully")
        
        print(f"\n🎉 Shadow Tree generation complete!")
        return self.root
    
    def _process_directory(self, directory, parent_node):
        """Process a directory and add it to the shadow tree."""
        self.dirs_processed += 1
        print(f"  📁 Processing directory: {directory.name}")
        
        # Process Python files
        for item in directory.iterdir():
            if item.is_file() and item.name.endswith('.py') and not item.name.startswith('__'):
                # Create a shadow node for the file
                shadow_path = parent_node.path / item.name.replace('.py', '_shadow.md')
                node = ShadowNode(item.name, shadow_path, item, parent_node)
                parent_node.add_child(node)
                
                # Extract information from the file
                self._process_file(item, node)
                self.files_processed += 1
                if self.files_processed % 10 == 0:
                    print(f"    📄 Processed {self.files_processed} files so far...")
        
        # Process subdirectories
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith('__'):
                # Create a shadow node for the directory
                shadow_path = parent_node.path / item.name
                node = ShadowNode(item.name, shadow_path, item, parent_node)
                parent_node.add_child(node)
                
                # Process the subdirectory
                self._process_directory(item, node)
    
    def _process_file(self, file_path, node):
        """Process a Python file and extract information."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract docstring
            try:
                tree = ast.parse(content)
                docstring = ast.get_docstring(tree)
                if docstring:
                    node.description = docstring
                    node.summary = docstring.split('\n')[0]
                    
                    # Extract keywords from docstring
                    words = [w.lower() for w in docstring.split() if len(w) > 3]
                    node.keywords = list(set(words))[:10]
            except Exception:
                pass
        except Exception:
            pass
    
    def _generate_descriptions(self, node):
        """Generate natural language descriptions for nodes without docstrings."""
        if not node.summary and node.code_path and node.code_path.is_file():
            try:
                print(f"  📝 Generating description for: {node.name}")
                with open(node.code_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract function and class names
                names = []
                try:
                    tree = ast.parse(content)
                    for item in ast.walk(tree):
                        if isinstance(item, ast.FunctionDef):
                            names.append(item.name)
                        elif isinstance(item, ast.ClassDef):
                            names.append(item.name)
                except Exception as e:
                    print(f"    ⚠️ Error parsing {node.name}: {str(e)}")
                    
                # Generate summary from names
                if names:
                    readable_names = [self._make_readable(name) for name in names]
                    node.summary = f"Contains {', '.join(readable_names[:3])}"
                    if len(names) > 3:
                        node.summary += f" and {len(names) - 3} more"
                    print(f"    ✨ Created summary with {len(names)} components")
                else:
                    # Fall back to filename
                    node.summary = f"Python module {self._make_readable(node.name.replace('.py', ''))}"
                    print(f"    📄 Created basic module summary")
            except Exception as e:
                print(f"    ❌ Error generating description for {node.name}: {str(e)}")
                node.summary = f"Python module {node.name}"
        
        # Process children
        for child in node.children:
            self._generate_descriptions(child)
    
    def _make_readable(self, name):
        """Convert a snake_case or camelCase name to a readable string."""
        # Handle snake_case
        if '_' in name:
            words = name.split('_')
            return ' '.join(word.capitalize() for word in words)
        
        # Handle camelCase
        result = name[0].upper()
        for char in name[1:]:
            if char.isupper():
                result += ' ' + char
            else:
                result += char
        return result
    
    def _save_shadow_tree(self, output_dir):
        """Save the shadow tree to files."""
        # Create the output directory
        os.makedirs(output_dir, exist_ok=True)
        print(f"  💾 Creating output directory: {output_dir}")
        
        # Save the tree structure as JSON
        tree_path = output_dir / "shadow_tree.json"
        with open(tree_path, 'w', encoding='utf-8') as f:
            json.dump(self.root.to_dict(), f, indent=2)
        print(f"  💾 Saved shadow tree JSON to: {tree_path}")
        
        # Save individual node descriptions
        print(f"  💾 Saving individual node descriptions...")
        self._save_node(self.root, output_dir)
        print(f"  ✅ All node descriptions saved successfully")
    
    def _save_node(self, node, base_dir):
        """Save a node to a file."""
        try:
            # Create the node directory
            node_dir = base_dir / node.name.replace('.py', '')
            os.makedirs(node_dir, exist_ok=True)
            
            # Save the node description
            desc_path = node_dir / "description.md"
            with open(desc_path, 'w', encoding='utf-8') as f:
                f.write(f"# {node.name}\n\n")
                f.write(f"{node.summary}\n\n")
                
                if node.description:
                    f.write("## Description\n\n")
                    f.write(f"{node.description}\n\n")
                
                if node.keywords:
                    f.write("## Keywords\n\n")
                    f.write(", ".join(node.keywords) + "\n\n")
                
                if node.code_path:
                    f.write("## Code Path\n\n")
                    f.write(f"`{node.code_path}`\n\n")
                
                if node.children:
                    f.write("## Children\n\n")
                    for child in node.children:
                        f.write(f"- [{child.name}](./{child.name.replace('.py', '')}/description.md): {child.summary}\n")
            
            # Save children
            for child in node.children:
                self._save_node(child, node_dir)
        except Exception as e:
            print(f"    ❌ Error saving node {node.name}: {str(e)}")

class ShadowTreeNavigator:
    """Navigate the shadow tree."""
    
    def __init__(self, root_node):
        self.root = root_node
        self.current_node = root_node
        
    def bubble_up(self, levels=1):
        """Bubble up to a higher level in the tree."""
        node = self.current_node
        for _ in range(levels):
            if node.parent:
                node = node.parent
            else:
                break
        self.current_node = node
        return self.current_node
    
    def drill_down(self, child_name):
        """Drill down to a child node."""
        for child in self.current_node.children:
            if child.name == child_name:
                self.current_node = child
                return self.current_node
        return None
    
    def get_path_to_root(self):
        """Get the path from the current node to the root."""
        path = []
        node = self.current_node
        while node:
            path.append(node)
            node = node.parent
        return list(reversed(path))
    
    def search(self, query):
        """Search for nodes matching the query."""
        results = []
        self._search_node(self.root, query.lower(), results)
        return results
    
    def _search_node(self, node, query, results):
        """Search a node and its children for the query."""
        # Check if the query is in the node name, summary, or description
        score = 0
        if query in node.name.lower():
            score += 3
        if query in node.summary.lower():
            score += 2
        if query in node.description.lower():
            score += 1
        
        # Check if the query is in the keywords
        for keyword in node.keywords:
            if query in keyword.lower():
                score += 1
        
        if score > 0:
            results.append((node, score))
        
        # Search children
        for child in node.children:
            self._search_node(child, query, results)

def generate_html_visualization(root_node, output_path):
    """Generate an HTML visualization of the shadow tree."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shadow Tree Visualization</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .tree-node { margin-left: 20px; }
            .node-name { cursor: pointer; font-weight: bold; }
            .node-summary { color: #666; }
            .node-children { display: none; }
            .expanded .node-children { display: block; }
            .node-path { color: #999; font-size: 0.8em; }
            .search-box { margin-bottom: 20px; }
            .search-results { margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>Shadow Tree Visualization</h1>
        
        <div class="search-box">
            <input type="text" id="search-input" placeholder="Search the shadow tree...">
            <button onclick="searchTree()">Search</button>
            <div class="search-results" id="search-results"></div>
        </div>
        
        <div id="tree-root">
    """
    
    html += _generate_node_html(root_node)
    
    html += """
        </div>
        
        <script>
            function toggleNode(nodeId) {
                const node = document.getElementById(nodeId);
                node.classList.toggle('expanded');
            }
            
            function searchTree() {
                const query = document.getElementById('search-input').value.toLowerCase();
                const results = document.getElementById('search-results');
                results.innerHTML = '';
                
                if (!query) return;
                
                const nodes = document.querySelectorAll('.tree-node');
                let matchCount = 0;
                
                nodes.forEach(node => {
                    const nodeName = node.querySelector('.node-name').textContent.toLowerCase();
                    const nodeSummary = node.querySelector('.node-summary').textContent.toLowerCase();
                    
                    if (nodeName.includes(query) || nodeSummary.includes(query)) {
                        const nodeId = node.id;
                        const path = getNodePath(node);
                        
                        const resultItem = document.createElement('div');
                        resultItem.innerHTML = `<a href="#${nodeId}" onclick="expandToNode('${nodeId}')">${path}</a>`;
                        results.appendChild(resultItem);
                        
                        matchCount++;
                    }
                });
                
                if (matchCount === 0) {
                    results.innerHTML = 'No results found.';
                }
            }
            
            function getNodePath(node) {
                const path = [];
                let current = node;
                
                while (current && current.classList.contains('tree-node')) {
                    const nodeName = current.querySelector('.node-name').textContent;
                    path.unshift(nodeName);
                    current = current.parentElement.closest('.tree-node');
                }
                
                return path.join(' > ');
            }
            
            function expandToNode(nodeId) {
                const node = document.getElementById(nodeId);
                let current = node.parentElement.closest('.tree-node');
                
                while (current) {
                    current.classList.add('expanded');
                    current = current.parentElement.closest('.tree-node');
                }
                
                node.classList.add('expanded');
                node.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        </script>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

def _generate_node_html(node, node_id=None):
    """Generate HTML for a node and its children."""
    if node_id is None:
        node_id = f"node-{node.name.replace('.', '-').replace(' ', '-')}"
    
    html = f"""
    <div class="tree-node" id="{node_id}">
        <div class="node-header">
            <span class="node-name" onclick="toggleNode('{node_id}')">{node.name}</span>
            <span class="node-summary"> - {node.summary}</span>
        </div>
        <div class="node-children">
    """
    
    if node.description:
        html += f"""
        <div class="node-description">
            <p>{node.description}</p>
        </div>
        """
    
    if node.code_path:
        html += f"""
        <div class="node-path">
            <p>Code path: {node.code_path}</p>
        </div>
        """
    
    for i, child in enumerate(node.children):
        child_id = f"{node_id}-child-{i}"
        html += _generate_node_html(child, child_id)
    
    html += """
        </div>
    </div>
    """
    
    return html

def main():
    parser = argparse.ArgumentParser(description='Generate and navigate a shadow tree for a code directory.')
    parser.add_argument('--generate', action='store_true', help='Generate a shadow tree')
    parser.add_argument('--visualize', action='store_true', help='Visualize the shadow tree')
    parser.add_argument('--search', type=str, help='Search the shadow tree')
    parser.add_argument('--code-dir', type=str, default='src', help='Code directory')
    parser.add_argument('--shadow-dir', type=str, default='shadow', help='Shadow directory')
    parser.add_argument('--format', type=str, default='html', choices=['html', 'md', 'json'], help='Visualization format')
    
    args = parser.parse_args()
    
    if args.generate:
        generator = SimpleShadowTreeGenerator()
        root = generator.generate_from_directory(args.code_dir, args.shadow_dir)
        
        if args.visualize:
            if args.format == 'html':
                output_path = Path(args.shadow_dir) / 'shadow_tree.html'
                generate_html_visualization(root, output_path)
                print(f"\n🌐 HTML visualization saved to {output_path}")
    
    elif args.visualize:
        # Load the shadow tree from the JSON file
        tree_path = Path(args.shadow_dir) / 'shadow_tree.json'
        if not tree_path.exists():
            print(f"Error: Shadow tree not found at {tree_path}")
            return
        
        with open(tree_path, 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
        
        # Create a shadow tree from the JSON data
        root = _create_node_from_dict(tree_data)
        
        if args.format == 'html':
            output_path = Path(args.shadow_dir) / 'shadow_tree.html'
            generate_html_visualization(root, output_path)
            print(f"\n🌐 HTML visualization saved to {output_path}")
    
    elif args.search:
        # Load the shadow tree from the JSON file
        tree_path = Path(args.shadow_dir) / 'shadow_tree.json'
        if not tree_path.exists():
            print(f"Error: Shadow tree not found at {tree_path}")
            return
        
        with open(tree_path, 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
        
        # Create a shadow tree from the JSON data
        root = _create_node_from_dict(tree_data)
        
        # Search the shadow tree
        navigator = ShadowTreeNavigator(root)
        results = navigator.search(args.search)
        
        # Sort results by score
        results.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n🔍 Search results for '{args.search}':")
        for node, score in results[:10]:
            path = []
            current = node
            while current:
                path.append(current.name)
                current = current.parent
            path = ' > '.join(reversed(path))
            
            print(f"  - {path}")
            print(f"    {node.summary}")
            print()

def _create_node_from_dict(data, parent=None):
    """Create a shadow node from a dictionary."""
    node = ShadowNode(data['name'], data['path'], data['code_path'], parent)
    node.summary = data['summary']
    node.description = data['description']
    node.keywords = data['keywords']
    
    for child_data in data['children']:
        child = _create_node_from_dict(child_data, node)
        node.add_child(child)
    
    return node

if __name__ == '__main__':
    main()
