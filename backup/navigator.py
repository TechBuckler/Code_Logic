"""
Shadow Tree Generator

Creates a natural language shadow tree that mirrors the code structure,
allowing intuitive navigation through the fractal codebase.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import core.ast
import re
import nltk

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions

# Set NLTK data path to use local directory
nltk.data.path.insert(0, './nltk_data')
print(f"NLTK data path set to: {nltk.data.path}")

# Try to download NLTK data if not already present
try:
    nltk.data.find('tokenizers/punkt')
    print("NLTK punkt tokenizer found")
except LookupError:
    print("Downloading NLTK punkt tokenizer...")
    nltk.download('punkt', download_dir='./nltk_data', quiet=True)
    print("Downloaded NLTK punkt tokenizer successfully")
    
try:
    nltk.data.find('corpora/wordnet')
    print("NLTK WordNet found")
except LookupError:
    print("Downloading NLTK WordNet...")
    nltk.download('wordnet', download_dir='./nltk_data', quiet=True)
    print("Downloaded NLTK WordNet successfully")

try:
    from nltk.tokenize import word_tokenize
    from nltk.corpus import wordnet
    from nltk.stem import WordNetLemmatizer
    print("NLTK components imported successfully")
except Exception as e:
    print(f"Error importing NLTK components: {str(e)}")
    # Provide fallback implementations if NLTK fails
    def word_tokenize(text):
        return text.lower().split()
    
    class WordNetLemmatizer:
        def lemmatize(self, word):
            return word

# Constants
MAX_SUMMARY_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 250
BUBBLE_UP_LEVELS = 3  # Default number of levels to bubble up

class ShadowNode:
    """A node in the shadow tree."""
    
    def __init__(self, name, path, code_path=None, parent=None):
        self.name = name
        self.path = path
        self.code_path = code_path  # Path to the corresponding code file
        self.parent = parent
        self.children = []
        self.summary = ""
        self.description = ""
        self.keywords = []
        self.level = 0 if parent is None else parent.level + 1
        
    def add_child(self, child):
        """Add a child node to this node."""
        self.children.append(child)
        child.parent = self
        
    def to_dict(self):
        """Convert the node to a dictionary."""
        return {
            "name": self.name,
            "path": str(self.path),
            "code_path": str(self.code_path) if self.code_path else None,
            "level": self.level,
            "summary": self.summary,
            "description": self.description,
            "keywords": self.keywords,
            "children": [child.to_dict() for child in self.children]
        }
        
    def __str__(self):
        return f"ShadowNode({self.name}, level={self.level}, children={len(self.children)})"


class ShadowTreeGenerator:
    """Generates a natural language shadow tree from a code tree."""
    
    def __init__(self):
        self.root = None
        self.lemmatizer = WordNetLemmatizer()
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
            # Read file using utility function
            content = read_file(file_path, encoding='utf-8')
                
            # Extract docstring if present
            tree = ast.parse(content)
            docstring = ast.get_docstring(tree)
            
            if docstring:
                node.description = docstring.strip()
                node.summary = self._summarize_text(docstring)
                
            # Extract keywords from the content
            node.keywords = self._extract_keywords(content)
            
            # Set the code path
            node.code_path = file_path
            
            self.files_processed += 1
        except Exception as e:
            print(f"Error processing file {file_path}: {str(e)}")
    
    def _generate_descriptions(self, node):
        """Generate natural language descriptions for nodes without docstrings."""
        if not node.summary and node.code_path and node.code_path.is_file():
            # Generate a summary based on the file content
            try:
                print(f"  📝 Generating description for: {node.name}")
                content = read_file(node.code_path, encoding='utf-8')
                    
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
    
    def _summarize_text(self, text):
        """Summarize a text to a short description."""
        # Remove newlines and extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Get the first sentence or a truncated version
        sentences = nltk.sent_tokenize(text)
        if sentences:
            summary = sentences[0]
            if len(summary) > MAX_SUMMARY_LENGTH:
                summary = summary[:MAX_SUMMARY_LENGTH] + "..."
            return summary
        
        return ""
    
    def _extract_keywords(self, content):
        """Extract keywords from content."""
        if not content:
            return []
            
        # Clean the text using utility function
        content = normalize_string(content)
        
        # Tokenize
        tokens = word_tokenize(content)
        
        # Remove stopwords (common words)
        stopwords = set(['the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 
                         'in', 'on', 'at', 'to', 'for', 'with', 'by', 'about', 'as', 'of',
                         'from', 'into', 'during', 'until', 'while', 'throughout', 'through',
                         'this', 'that', 'these', 'those', 'it', 'its', 'they', 'them', 'their',
                         'he', 'him', 'his', 'she', 'her', 'hers', 'we', 'us', 'our', 'you', 'your'])
        tokens = [t for t in tokens if t not in stopwords and len(t) > 2]
        
        # Lemmatize (convert to base form)
        lemmatized = [self.lemmatizer.lemmatize(t) for t in tokens]
        
        # Count frequencies
        freq = {}
        for token in lemmatized:
            if token in freq:
                freq[token] += 1
            else:
                freq[token] = 1
                
        # Get top keywords
        keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return [k for k, v in keywords]
    
    def _make_readable(self, name):
        """Convert a code name to a readable string."""
        # Split by underscores and camelCase
        words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', name.replace('_', ' '))
        
        # Capitalize first letter of each word
        words = [word.lower() for word in words]
        
        # Join with spaces
        return ' '.join(words)
    
    def _save_shadow_tree(self, output_dir):
        """Save the shadow tree to files."""
        if output_dir is None:
            return
            
        output_dir = Path(output_dir)
        ensure_dir(output_dir)
        
        # Save the tree structure as JSON
        tree_json = self.root.to_dict()
        save_json(output_dir / "shadow_tree.json", tree_json)
            
        # Save individual node files
        self._save_node(self.root, output_dir)
    
    def _save_node(self, node, base_dir):
        """Save a node to a file."""
        # Create node directory
        node_dir = base_dir / node.path
        ensure_dir(node_dir)
        
        # Save node info
        node_info = {
            "name": node.name,
            "path": str(node.path),
            "code_path": str(node.code_path) if node.code_path else None,
            "summary": node.summary,
            "description": node.description,
            "keywords": node.keywords,
            "level": node.level,
            "children": [child.name for child in node.children]
        }
        
        save_json(node_dir / "node.json", node_info)
            
        # Save node description as markdown
        markdown = f"# {node.name}\n\n"
        if node.summary:
            markdown += f"{node.summary}\n\n"
        if node.description:
            markdown += f"{node.description}\n\n"
        if node.keywords:
            markdown += f"**Keywords**: {', '.join(node.keywords)}\n\n"
        if node.children:
            markdown += f"## Children\n\n"
            for child in node.children:
                markdown += f"- {child.name}\n"
                
        write_file(node_dir / "README.md", markdown)
            
        # Save children
        for child in node.children:
            self._save_node(child, base_dir)


class ShadowTreeNavigator:
    """Navigates the shadow tree."""
    
    def __init__(self, shadow_tree_path):
        """Initialize with the path to the shadow tree JSON file."""
        self.shadow_tree_path = Path(shadow_tree_path)
        self.tree = None
        self.current_node = None
        self.history = [None]  # Initialize history with None
        self._load_tree()
        if self.tree:
            self.current_node = self.tree
            self.history[0] = self.tree  # Update history with root node
        print(f"Shadow Tree Navigator initialized with root node: {self.tree.name if self.tree else None}")
        
    def _load_tree(self):
        """Load the shadow tree from JSON."""
        try:
            # Check if the file exists
            if not os.path.exists(self.shadow_tree_path):
                print(f"Error: Shadow tree file not found at {self.shadow_tree_path}")
                return False
                
            # Load the JSON file using utility function
            tree_dict = load_json(self.shadow_tree_path)
                
            # Convert the dictionary to a tree of ShadowNodes
            self.tree = self._dict_to_node(tree_dict)
            
            # Set the current node to the root
            self.current_node = self.tree
            
            # Print debug info
            print(f"Loaded shadow tree with {len(self.tree.children)} top-level nodes")
            print(f"Current node: {self.current_node.name}")
            
            return True
        except Exception as e:
            print(f"Error loading shadow tree: {str(e)}")
            return False
    

    def _dict_to_node(self, node_dict, parent=None):
        """Convert a dictionary to a ShadowNode."""
        try:
            # Create the node with proper path handling
            node = ShadowNode(
                name=node_dict["name"],
                path=Path(node_dict["path"]) if isinstance(node_dict["path"], str) else node_dict["path"],
                code_path=Path(node_dict["code_path"]) if node_dict["code_path"] and isinstance(node_dict["code_path"], str) else node_dict["code_path"],
                parent=parent
            )
            
            # Set properties with error handling
            node.summary = node_dict.get("summary", "")
            node.description = node_dict.get("description", "")
            node.keywords = node_dict.get("keywords", [])
            node.level = node_dict.get("level", 0 if parent is None else parent.level + 1)
            
            # Process children with error handling
            for child_dict in node_dict.get("children", []):
                child = self._dict_to_node(child_dict, node)
                if child:  # Only add child if successfully created
                    node.add_child(child)
                
            return node
        except Exception as e:
            print(f"Error converting dict to node: {str(e)}")
            return None

    def go_up(self):
        """Go up one level in the shadow tree."""
        if not self.current_node:
            print("Cannot go up: No current node")
            return False
            
        if not hasattr(self.current_node, 'parent') or not self.current_node.parent:
            print(f"Cannot go up: Node {self.current_node.name} has no parent (already at root)")
            return False
            
        # Move up to parent
        self.current_node = self.current_node.parent
        self.history.append(self.current_node)
        print(f"Moved up to: {self.current_node.name}")
        return True

    def go_down(self, name):
        """Go down to a child node."""
        if not self.current_node:
            print("Cannot go down: No current node")
            return False
            
        if not hasattr(self.current_node, 'children') or not self.current_node.children:
            print(f"Cannot go down: Node {self.current_node.name} has no children")
            return False
        
        # Debug information
        print(f"Attempting to go down to '{name}' from '{self.current_node.name}'")
        print(f"Available children: {[child.name for child in self.current_node.children]}")
        
        # First try exact match
        for child in self.current_node.children:
            if child.name == name:
                print(f"Found exact match: {child.name}")
                self.current_node = child
                self.history.append(self.current_node)
                return True
        
        # If no exact match, try partial match
        for child in self.current_node.children:
            if name.lower() in child.name.lower():
                print(f"Found partial name match: {child.name}")
                self.current_node = child
                self.history.append(self.current_node)
                return True
        
        # If no match found, try matching with summary or description
        for child in self.current_node.children:
            if hasattr(child, 'summary') and child.summary and name.lower() in child.summary.lower():
                print(f"Found match in summary: {child.name}")
                self.current_node = child
                self.history.append(self.current_node)
                return True
            
            if hasattr(child, 'description') and child.description and name.lower() in child.description.lower():
                print(f"Found match in description: {child.name}")
                self.current_node = child
                self.history.append(self.current_node)
                return True
        
        print(f"No matching child found for '{name}'")
        return False
        
    def go_to_path(self, path):
        """Go to a specific path in the shadow tree."""
        if not self.tree:
            print("Cannot navigate: Tree is not loaded")
            return False
            
        # Start from root
        current = self.tree
        
        # Split the path
        if isinstance(path, str):
            path_parts = path.split("/")
        else:
            path_parts = path
        
        print(f"Navigating to path: {path_parts}")
        
        # Navigate through the path
        for part in path_parts:
            found = False
            if not hasattr(current, 'children') or not current.children:
                print(f"Cannot navigate further: Node {current.name} has no children")
                return False
                
            for child in current.children:
                if child.name == part:
                    current = child
                    found = True
                    print(f"Found path component: {part}")
                    break
            
            if not found:
                print(f"Path component not found: {part}")
                return False
        
        # Set the current node
        self.current_node = current
        self.history.append(self.current_node)
        print(f"Successfully navigated to: {current.name}")
        return True

    def search(self, query):
        """Search the shadow tree for nodes matching the query."""
        results = []
        
        # Tokenize and lowercase the query
        query_tokens = set(word_tokenize(query.lower()))
        
        # Search function
        def search_node(node):
            # Check if query matches node name
            if query.lower() in node.name.lower():
                results.append((node, 1.0))  # Perfect match in name
                
            # Check if query matches summary
            elif query.lower() in node.summary.lower():
                results.append((node, 0.8))  # Good match in summary
                
            # Check if query matches description
            elif query.lower() in node.description.lower():
                results.append((node, 0.6))  # Decent match in description
                
            # Check if query tokens match keywords
            else:
                keyword_tokens = set(node.keywords)
                overlap = query_tokens.intersection(keyword_tokens)
                if overlap:
                    score = len(overlap) / len(query_tokens)
                    results.append((node, score * 0.5))  # Partial match in keywords
            
            # Search children
            for child in node.children:
                search_node(child)
        
        # Start search from root
        search_node(self.tree)
        
        # Sort by score
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results

    def get_current_view(self):
        """Get the current view of the shadow tree."""
        return {
            "current": self.current_node.to_dict(),
            "parent": self.current_node.parent.to_dict() if self.current_node.parent else None,
            "children": [child.to_dict() for child in self.current_node.children],
            "siblings": [child.to_dict() for child in self.current_node.parent.children] if self.current_node.parent else []
        }
    
    def get_bubble_up_view(self, levels=BUBBLE_UP_LEVELS):
        """Get a bubble-up view of the shadow tree."""
        # Start with current node
        nodes = [self.current_node]
        
        # Add ancestors
        current = self.current_node
        for _ in range(levels):
            if current.parent:
                current = current.parent
                nodes.append(current)
            else:
                break
        
        # Add descendants
        def add_descendants(node, level):
            if level <= 0:
                return
            for child in node.children:
                nodes.append(child)
                add_descendants(child, level - 1)
        
        add_descendants(self.current_node, levels)
        
        # Convert to dictionaries
        return [node.to_dict() for node in nodes]
    
    def get_path_to_root(self):
        """Get the path from current node to root."""
        if not self.current_node:
            print("Cannot get path: No current node")
            return []
        
        path = []
        current = self.current_node
        
        try:
            while current:
                path.append(current)
                current = current.parent if hasattr(current, 'parent') else None
            
            return list(reversed(path))
        except Exception as e:
            print(f"Error getting path to root: {str(e)}")
            return [self.current_node] if self.current_node else []
class ShadowTreeVisualizer:
    """Visualizes the shadow tree."""
    
    def __init__(self, shadow_tree):
        """Initialize with a shadow tree."""
        self.tree = shadow_tree
        
    def generate_markdown(self, output_path, max_depth=None):
        """Generate a markdown representation of the shadow tree."""
        output_path = Path(output_path)
        
        # Create the output directory
        os.makedirs(output_path.parent, exist_ok=True)
        
        # Generate markdown
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# {self.tree.name} Shadow Tree\n\n")
            
            # Write tree structure
            f.write("## Tree Structure\n\n")
            self._write_node_markdown(f, self.tree, 0, max_depth)
            
            # Write node details
            f.write("\n## Node Details\n\n")
            self._write_node_details(f, self.tree)
        
        return output_path
    
    def _write_node_markdown(self, file, node, level, max_depth):
        """Write a node to the markdown file."""
        if max_depth is not None and level > max_depth:
            return
            
        indent = "  " * level
        file.write(f"{indent}- **{node.name}**: {node.summary}\n")
        
        for child in node.children:
            self._write_node_markdown(file, child, level + 1, max_depth)
    
    def _write_node_details(self, file, node):
        """Write node details to the markdown file."""
        file.write(f"### {node.name}\n\n")
        file.write(f"{node.summary}\n\n")
        
        if node.description:
            file.write(f"**Description**: {node.description}\n\n")
        
        if node.keywords:
            file.write(f"**Keywords**: {', '.join(node.keywords)}\n\n")
        
        if node.code_path:
            file.write(f"**Code Path**: `{node.code_path}`\n\n")
        
        # Write children recursively
        for child in node.children:
            self._write_node_details(file, child)
    
    def generate_html(self, output_path, max_depth=None):
        """Generate an HTML visualization of the shadow tree."""
        output_path = Path(output_path)
        
        # Create the output directory
        os.makedirs(output_path.parent, exist_ok=True)
        
        # Generate HTML
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>{self.tree.name} Shadow Tree</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; }}
        .tree {{ margin-left: 20px; }}
        .node {{ margin: 5px 0; }}
        .node-name {{ font-weight: bold; cursor: pointer; }}
        .node-summary {{ color: #666; }}
        .node-details {{ margin-left: 20px; display: none; }}
        .expanded .node-details {{ display: block; }}
        .toggle {{ display: inline-block; width: 20px; text-align: center; }}
    </style>
    <script>
        function toggleNode(id) {{
            const node = document.getElementById(id);
            node.classList.toggle('expanded');
            
            const toggle = node.querySelector('.toggle');
            toggle.textContent = node.classList.contains('expanded') ? '-' : '+';
        }}
    </script>
</head>
<body>
    <h1>{self.tree.name} Shadow Tree</h1>
    
    <div class="tree">
""")
            
            # Write tree structure
            self._write_node_html(f, self.tree, 0, max_depth)
            
            f.write("""
    </div>
</body>
</html>
""")
        
        return output_path
    
    def _write_node_html(self, file, node, level, max_depth, node_id=0):
        """Write a node to the HTML file."""
        if max_depth is not None and level > max_depth:
            return node_id + 1
            
        current_id = node_id
        
        file.write(f"""
        <div class="node" id="node-{current_id}">
            <div class="node-header">
                <span class="toggle" onclick="toggleNode('node-{current_id}')">+</span>
                <span class="node-name" onclick="toggleNode('node-{current_id}')">{node.name}</span>
                <span class="node-summary">{node.summary}</span>
            </div>
            <div class="node-details">
""")
        
        if node.description:
            file.write(f"                <p><strong>Description:</strong> {node.description}</p>\n")
        
        if node.keywords:
            file.write(f"                <p><strong>Keywords:</strong> {', '.join(node.keywords)}</p>\n")
        
        if node.code_path:
            file.write(f"                <p><strong>Code Path:</strong> <code>{node.code_path}</code></p>\n")
        
        if node.children:
            file.write("                <div class=\"children\">\n")
            
            next_id = current_id + 1
            for child in node.children:
                next_id = self._write_node_html(file, child, level + 1, max_depth, next_id)
            
            file.write("                </div>\n")
        
        file.write("""
            </div>
        </div>
""")
        
        return next_id


class ShadowTreeAPI:
    """API for interacting with the shadow tree."""
    
    def __init__(self, code_dir, shadow_dir=None):
        """Initialize the API."""
        self.code_dir = Path(code_dir)
        self.shadow_dir = Path(shadow_dir) if shadow_dir else self.code_dir / "shadow_tree"
        
        # Create shadow directory if it doesn't exist
        os.makedirs(self.shadow_dir, exist_ok=True)
        
        # Path to shadow tree JSON
        self.shadow_tree_path = self.shadow_dir / "shadow_tree.json"
        
        # Check if shadow tree exists
        if not self.shadow_tree_path.exists():
            print(f"Shadow tree not found at {self.shadow_tree_path}, generating new tree...")
            # Generate shadow tree
            try:
                generator = ShadowTreeGenerator()
                generator.generate_from_directory(self.code_dir, self.shadow_dir)
                print(f"Generated new Shadow Tree in {self.shadow_dir}")
            except Exception as e:
                print(f"Error generating Shadow Tree: {str(e)}")
        
        # Load navigator
        self.navigator = ShadowTreeNavigator(self.shadow_tree_path)
        
        # Verify navigator is working
        if not self.navigator or not self.navigator.tree:
            print("Warning: Navigator or tree is None, attempting to regenerate...")
            try:
                # Force regeneration
                generator = ShadowTreeGenerator()
                generator.generate_from_directory(self.code_dir, self.shadow_dir)
                # Reload the navigator
                self.navigator = ShadowTreeNavigator(self.shadow_tree_path)
                
                if not self.navigator or not self.navigator.tree:
                    print("Error: Still could not load Shadow Tree after regeneration")
            except Exception as e:
                print(f"Error regenerating Shadow Tree: {str(e)}")
    
    def regenerate(self):
        """Regenerate the shadow tree."""
        generator = ShadowTreeGenerator()
        generator.generate_from_directory(self.code_dir, self.shadow_dir)
        
        # Reload navigator
        self.navigator = ShadowTreeNavigator(self.shadow_tree_path)
    
    def get_current_view(self):
        """Get the current view of the shadow tree."""
        return self.navigator.get_current_view()
    
    def get_bubble_up_view(self, levels=BUBBLE_UP_LEVELS):
        """Get a bubble-up view of the shadow tree."""
        return self.navigator.get_bubble_up_view(levels)
    
    def search(self, query):
        """Search the shadow tree."""
        return self.navigator.search(query)
    
    def navigate(self, path=None, up=False, down=None):
        """Navigate the shadow tree."""
        if path:
            return self.navigator.go_to_path(path)
        elif up:
            return self.navigator.go_up()
        elif down:
            return self.navigator.go_down(down)
        else:
            return False
    
    def visualize(self, format="html", max_depth=None):
        """Visualize the shadow tree."""
        visualizer = ShadowTreeVisualizer(self.navigator.tree)
        
        if format == "html":
            return visualizer.generate_html(self.shadow_dir / "shadow_tree.html", max_depth)
        else:
            return visualizer.generate_markdown(self.shadow_dir / "shadow_tree.md", max_depth)
    
    def get_code_path(self):
        """Get the code path for the current node."""
        return self.navigator.current_node.code_path
    
    def get_shadow_path(self):
        """Get the shadow path for the current node."""
        return self.navigator.current_node.path


def main():
    """Main function for the shadow tree."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Shadow Tree Generator')
    parser.add_argument('--generate', action='store_true', help='Generate a shadow tree')
    parser.add_argument('--visualize', action='store_true', help='Visualize the shadow tree')
    parser.add_argument('--search', type=str, help='Search the shadow tree')
    parser.add_argument('--code-dir', type=str, default='.', help='Code directory')
    parser.add_argument('--shadow-dir', type=str, help='Shadow directory')
    parser.add_argument('--format', type=str, default='html', choices=['html', 'markdown'], help='Visualization format')
    parser.add_argument('--max-depth', type=int, help='Maximum depth for visualization')
    parser.add_argument('--bubble-levels', type=int, default=BUBBLE_UP_LEVELS, help='Number of levels to bubble up')
    
    args = parser.parse_args()
    
    # Create API
    api = ShadowTreeAPI(args.code_dir, args.shadow_dir)
    
    if args.generate:
        api.regenerate()
        print(f"Generated shadow tree in {api.shadow_dir}")
    
    if args.visualize:
        output_path = api.visualize(args.format, args.max_depth)
        print(f"Visualized shadow tree to {output_path}")
    
    if args.search:
        results = api.search(args.search)
        print(f"Search results for '{args.search}':")
        for node, score in results[:10]:  # Show top 10 results
            print(f"- {node.name} (score: {score:.2f}): {node.summary}")


if __name__ == "__main__":
    main()
