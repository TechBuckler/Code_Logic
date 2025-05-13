#!/usr/bin/env python
"""
Summarize Codebase

This script quickly summarizes all files in the codebase and identifies
interesting or previously unknown components.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import sys
import time

# Add project root to path for imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import our existing tools
try:
except ImportError as e:
    print(f"Error importing tools: {e}")
    print("Make sure you've run the reorganization scripts first.")
    sys.exit(1)

def summarize_codebase():
    """Quickly summarize all files in the codebase."""
    print("\n📊 Summarizing Codebase")
    print("=" * 80)
    
    # Find all Python files
    python_files = []
    for root, _, files in os.walk(project_root):
        # Skip certain directories
        if any(skip in root for skip in ['.git', '__pycache__', '.vscode', '.idea']):
            continue
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files to summarize")
    
    # Collect statistics
    stats = {
        "total_files": len(python_files),
        "total_loc": 0,
        "total_functions": 0,
        "total_classes": 0,
        "total_imports": 0,
        "avg_complexity": 0,
        "max_complexity": 0,
        "max_complexity_file": "",
        "largest_file": "",
        "largest_file_loc": 0,
        "most_functions_file": "",
        "most_functions_count": 0,
        "most_classes_file": "",
        "most_classes_count": 0,
        "most_complex_function": "",
        "most_complex_function_score": 0,
        "most_complex_function_file": ""
    }
    
    # Collect module information
    modules = defaultdict(list)
    keywords = Counter()
    imports = Counter()
    interesting_files = []
    
    # Process each file
    start_time = time.time()
    for i, file_path in enumerate(python_files):
        rel_path = os.path.relpath(file_path, project_root)
        
        try:
            # Analyze the file
            file_info = analyze_file(file_path)
            
            # Update statistics
            stats["total_loc"] += file_info["metrics"]["loc"]
            stats["total_functions"] += file_info["metrics"]["functions"]
            stats["total_classes"] += file_info["metrics"]["classes"]
            stats["total_imports"] += file_info["metrics"]["imports"]
            stats["avg_complexity"] += file_info["metrics"]["complexity"]
            
            # Check for largest file
            if file_info["metrics"]["loc"] > stats["largest_file_loc"]:
                stats["largest_file_loc"] = file_info["metrics"]["loc"]
                stats["largest_file"] = rel_path
            
            # Check for most functions
            if file_info["metrics"]["functions"] > stats["most_functions_count"]:
                stats["most_functions_count"] = file_info["metrics"]["functions"]
                stats["most_functions_file"] = rel_path
            
            # Check for most classes
            if file_info["metrics"]["classes"] > stats["most_classes_count"]:
                stats["most_classes_count"] = file_info["metrics"]["classes"]
                stats["most_classes_file"] = rel_path
            
            # Check for most complex file
            if file_info["metrics"]["complexity"] > stats["max_complexity"]:
                stats["max_complexity"] = file_info["metrics"]["complexity"]
                stats["max_complexity_file"] = rel_path
            
            # Check for most complex function
            for func in file_info["semantics"]["functions"]:
                if func.get("complexity", 0) > stats["most_complex_function_score"]:
                    stats["most_complex_function_score"] = func.get("complexity", 0)
                    stats["most_complex_function"] = func["name"]
                    stats["most_complex_function_file"] = rel_path
            
            # Collect module information
            module_path = os.path.dirname(rel_path).replace("\\", "/")
            if not module_path:
                module_path = "root"
            modules[module_path].append({
                "name": os.path.basename(file_path),
                "loc": file_info["metrics"]["loc"],
                "functions": file_info["metrics"]["functions"],
                "classes": file_info["metrics"]["classes"],
                "complexity": file_info["metrics"]["complexity"]
            })
            
            # Collect keywords
            for keyword in file_info["semantics"]["keywords"]:
                keywords[keyword] += 1
            
            # Collect imports
            for imp in file_info["semantics"]["imports"]:
                imports[imp["module"]] += 1
            
            # Check for interesting files
            is_interesting = False
            interesting_reason = []
            
            # Files with high complexity
            if file_info["metrics"]["complexity"] > 15:
                is_interesting = True
                interesting_reason.append("high complexity")
            
            # Files with many functions
            if file_info["metrics"]["functions"] > 10:
                is_interesting = True
                interesting_reason.append("many functions")
            
            # Files with many classes
            if file_info["metrics"]["classes"] > 3:
                is_interesting = True
                interesting_reason.append("many classes")
            
            # Files with unusual imports or keywords
            unusual_imports = [imp["module"] for imp in file_info["semantics"]["imports"] 
                              if "nltk" in imp["module"] or "sklearn" in imp["module"] or "networkx" in imp["module"]]
            if unusual_imports:
                is_interesting = True
                interesting_reason.append(f"unusual imports: {', '.join(unusual_imports)}")
            
            # Files with interesting docstrings
            if file_info["semantics"]["docstring"] and any(term in file_info["semantics"]["docstring"].lower() 
                                                         for term in ["algorithm", "optimization", "neural", "ai", "ml"]):
                is_interesting = True
                interesting_reason.append("AI/ML-related docstring")
            
            if is_interesting:
                interesting_files.append({
                    "path": rel_path,
                    "reasons": interesting_reason,
                    "loc": file_info["metrics"]["loc"],
                    "docstring": file_info["semantics"]["docstring"] or "No docstring"
                })
            
            # Progress indicator
            if (i + 1) % 20 == 0 or i == len(python_files) - 1:
                print(f"Processed {i + 1}/{len(python_files)} files...")
                
        except Exception as e:
            print(f"Error analyzing {rel_path}: {str(e)}")
    
    # Calculate averages
    stats["avg_complexity"] /= stats["total_files"]
    
    # Generate summary report
    summary_path = os.path.join(project_root, "codebase_summary.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("# Codebase Summary\n\n")
        f.write(f"**Generated on:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Overall statistics
        f.write("## Overall Statistics\n\n")
        f.write(f"- **Total Files:** {stats['total_files']}\n")
        f.write(f"- **Total Lines of Code:** {stats['total_loc']}\n")
        f.write(f"- **Total Functions:** {stats['total_functions']}\n")
        f.write(f"- **Total Classes:** {stats['total_classes']}\n")
        f.write(f"- **Total Imports:** {stats['total_imports']}\n")
        f.write(f"- **Average Complexity:** {stats['avg_complexity']:.2f}\n")
        f.write(f"- **Maximum Complexity:** {stats['max_complexity']} (in `{stats['max_complexity_file']}`)\n\n")
        
        # Notable files
        f.write("## Notable Files\n\n")
        f.write(f"- **Largest File:** `{stats['largest_file']}` ({stats['largest_file_loc']} lines)\n")
        f.write(f"- **Most Functions:** `{stats['most_functions_file']}` ({stats['most_functions_count']} functions)\n")
        f.write(f"- **Most Classes:** `{stats['most_classes_file']}` ({stats['most_classes_count']} classes)\n")
        f.write(f"- **Most Complex Function:** `{stats['most_complex_function']}` in `{stats['most_complex_function_file']}` (complexity: {stats['most_complex_function_score']})\n\n")
        
        # Module breakdown
        f.write("## Module Breakdown\n\n")
        for module, files in sorted(modules.items()):
            module_loc = sum(file["loc"] for file in files)
            module_functions = sum(file["functions"] for file in files)
            module_classes = sum(file["classes"] for file in files)
            
            f.write(f"### {module}/\n\n")
            f.write(f"- **Files:** {len(files)}\n")
            f.write(f"- **Lines of Code:** {module_loc}\n")
            f.write(f"- **Functions:** {module_functions}\n")
            f.write(f"- **Classes:** {module_classes}\n\n")
            
            # List files in the module
            f.write("| File | LOC | Functions | Classes | Complexity |\n")
            f.write("|------|-----|-----------|---------|------------|\n")
            for file in sorted(files, key=lambda x: x["loc"], reverse=True):
                f.write(f"| {file['name']} | {file['loc']} | {file['functions']} | {file['classes']} | {file['complexity']} |\n")
            f.write("\n")
        
        # Top keywords
        f.write("## Top Keywords\n\n")
        for keyword, count in keywords.most_common(20):
            f.write(f"- **{keyword}:** {count}\n")
        f.write("\n")
        
        # Top imports
        f.write("## Top Imports\n\n")
        for imp, count in imports.most_common(20):
            f.write(f"- **{imp}:** {count}\n")
        f.write("\n")
        
        # Interesting files
        f.write("## Interesting Files\n\n")
        for file in sorted(interesting_files, key=lambda x: x["loc"], reverse=True):
            f.write(f"### {file['path']}\n\n")
            f.write(f"**Lines:** {file['loc']}\n\n")
            f.write(f"**Interesting because:** {', '.join(file['reasons'])}\n\n")
            
            # Add a short excerpt from the docstring
            docstring = file['docstring']
            if len(docstring) > 200:
                docstring = docstring[:200] + "..."
            f.write(f"**Description:**\n> {docstring}\n\n")
    
    print(f"\n✅ Summary generated in {summary_path}")
    print(f"Total analysis time: {time.time() - start_time:.2f}s")
    
    return summary_path

def main():
    """Main function."""
    summary_path = summarize_codebase()
    
    # Print the summary
    with open(summary_path, "r", encoding="utf-8") as f:
        print("\n" + "=" * 80)
        print(f.read())

if __name__ == "__main__":
    main()
