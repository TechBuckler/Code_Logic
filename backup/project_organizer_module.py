"""
Project Organizer Module

This module handles project organization, file naming conventions, and project structure.
It can analyze the current project structure, suggest improvements, and apply changes.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import re
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.append(project_root)

# Import utility functions


class ProjectOrganizerModule:
    """Module for organizing project files and enforcing naming conventions."""
    
    def __init__(self):
        self.name = "project_organizer"
        self.description = "Organizes project files and enforces naming conventions"
        self.dependencies = []
        self.active = True
        
    def initialize(self):
        """Initialize the module."""
        pass
        
        # Define naming patterns
        self.patterns = {
            "python_files": r"^[a-z][a-z0-9_]*\.py$",
            "entry_points": r"^(run|analyze|generate)_[a-z][a-z0-9_]*\.py$",
            "generated_files": r"^[a-z][a-z0-9_]*_(optimized|generated|transformed)\.py$",
            "utility_scripts": r"^[a-z][a-z0-9_]*\.(py|sh|bat)$"
        }
        
        # Define ideal directory structure
        self.ideal_structure = {
            "docs": ["README.md", "implementation_plan.md"],
            "src": {
                "core": [],
                "modules": [],
                "ui": [],
                "utils": []
            },
            "templates": [],
            "examples": [],
            "tests": [],
            "scripts": {
                "cleanup": [],
                "runners": []
            },
            "output": {
                "optimized": [],
                "logs": []
            },
            "cache": []
        }
    
    def can_process(self, data):
        """Check if this module can process the given data."""
        return isinstance(data, str) and (data == "analyze_project" or data == "reorganize_project")
    
    def process(self, command, context=None):
        """Process the command."""
        if command == "analyze_project":
            return self.analyze_project(context.get("project_root", os.getcwd()))
        elif command == "reorganize_project":
            return self.reorganize_project(context.get("project_root", os.getcwd()))
        return {"error": "Unknown command"}
    
    def analyze_project(self, project_root):
        """Analyze the current project structure and suggest improvements."""
        results = {
            "structure_issues": [],
            "naming_issues": [],
            "suggestions": []
        }
        
        # Check if directories exist
        for directory in self.ideal_structure.keys():
            dir_path = join_paths(project_root, directory)
            if not os.path.exists(dir_path):
                results["structure_issues"].append(f"Missing directory: {directory}")
                results["suggestions"].append(f"Create directory: {directory}")
        
        # Check file naming conventions
        for root, _, files in os.walk(project_root):
            rel_path = get_relative_path(root, project_root)
            
            # Determine which pattern to use based on directory
            pattern_key = "python_files"  # Default
            if "scripts" in rel_path:
                pattern_key = "utility_scripts"
            elif "output/optimized" in rel_path:
                pattern_key = "generated_files"
            
            for file in files:
                if file.endswith('.py'):
                    if not re.match(self.patterns[pattern_key], file):
                        results["naming_issues"].append(f"File {os.path.join(rel_path, file)} does not follow the {pattern_key} naming convention")
                        
                        # Suggest a better name
                        better_name = self._suggest_better_name(file, pattern_key)
                        if better_name:
                            results["suggestions"].append(f"Rename {file} to {better_name}")
        
        # Check for files in the wrong location
        for root, _, files in os.walk(project_root):
            rel_path = os.path.relpath(root, project_root)
            
            for file in files:
                if file.endswith('_optimized.py') and "output/optimized" not in rel_path:
                    results["structure_issues"].append(f"Optimized file {file} should be in output/optimized/")
                    results["suggestions"].append(f"Move {file} to output/optimized/")
                
                if file == "streamlit_output.txt" and "output/logs" not in rel_path:
                    results["structure_issues"].append(f"Log file {file} should be in output/logs/")
                    results["suggestions"].append(f"Move {file} to output/logs/")
        
        return results
    
    def reorganize_project(self, project_root):
        """Reorganize the project according to the ideal structure."""
        results = {
            "created_dirs": [],
            "moved_files": [],
            "renamed_files": []
        }
        
        # Create missing directories
        for directory, subdirs in self.ideal_structure.items():
            dir_path = os.path.join(project_root, directory)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                results["created_dirs"].append(directory)
            
            # Create subdirectories if they're dictionaries
            if isinstance(subdirs, dict):
                for subdir in subdirs.keys():
                    subdir_path = os.path.join(dir_path, subdir)
                    if not os.path.exists(subdir_path):
                        os.makedirs(subdir_path)
                        results["created_dirs"].append(f"{directory}/{subdir}")
        
        # Move files to appropriate directories
        self._move_files(project_root, results)
        
        # Rename files according to conventions
        self._rename_files(project_root, results)
        
        return results
    
    def _move_files(self, project_root, results):
        """Move files to their appropriate directories."""
        # Move documentation files
        for doc_file in ["README.md", "plan_1.md"]:
            src_path = os.path.join(project_root, doc_file)
            if os.path.exists(src_path):
                dest_name = "implementation_plan.md" if doc_file == "plan_1.md" else doc_file
                dest_path = os.path.join(project_root, "docs", dest_name)
                ensure_dir(os.path.dirname(dest_path))
                copy_file(src_path, dest_path)  # Copy instead of move to avoid breaking things
                results["moved_files"].append(f"{doc_file} -> docs/{dest_name}")
        
        # Move optimized files
        for file in os.listdir(project_root):
            if file.endswith('_optimized.py'):
                src_path = os.path.join(project_root, file)
                dest_path = os.path.join(project_root, "output", "optimized", file)
                ensure_dir(os.path.dirname(dest_path))
                copy_file(src_path, dest_path)  # Copy instead of move to avoid breaking things
                results["moved_files"].append(f"{file} -> output/optimized/{file}")
        
        # Move log files
        if os.path.exists(os.path.join(project_root, "streamlit_output.txt")):
            src_path = os.path.join(project_root, "streamlit_output.txt")
            dest_path = os.path.join(project_root, "output", "logs", "streamlit_output.txt")
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            shutil.copy2(src_path, dest_path)  # Copy instead of move to avoid breaking things
            results["moved_files"].append(f"streamlit_output.txt -> output/logs/streamlit_output.txt")
        
        # Move cleanup scripts
        for file in ["cleanup_files.py", "cleanup_final.py"]:
            src_path = os.path.join(project_root, file)
            if os.path.exists(src_path):
                dest_path = os.path.join(project_root, "scripts", "cleanup", file)
                ensure_dir(os.path.dirname(dest_path))
                copy_file(src_path, dest_path)  # Copy instead of move to avoid breaking things
                results["moved_files"].append(f"{file} -> scripts/cleanup/{file}")
        
        # Move runner scripts
        for file in ["run_safe.bat", "safe_runner.py"]:
            src_path = os.path.join(project_root, file)
            if os.path.exists(src_path):
                dest_path = os.path.join(project_root, "scripts", "runners", file)
                ensure_dir(os.path.dirname(dest_path))
                copy_file(src_path, dest_path)  # Copy instead of move to avoid breaking things
                results["moved_files"].append(f"{file} -> scripts/runners/{file}")
    
    def _rename_files(self, project_root, results):
        """Rename files according to naming conventions."""
        # Rename entry points
        if os.path.exists(os.path.join(project_root, "run_app.py")):
            src_path = os.path.join(project_root, "run_app.py")
            dest_path = os.path.join(project_root, "run_ui.py")
            shutil.copy2(src_path, dest_path)  # Copy instead of move to avoid breaking things
            results["renamed_files"].append(f"run_app.py -> run_ui.py")
        
        if os.path.exists(os.path.join(project_root, "logic_tool.py")):
            src_path = os.path.join(project_root, "logic_tool.py")
            dest_path = os.path.join(project_root, "run_cli.py")
            shutil.copy2(src_path, dest_path)  # Copy instead of move to avoid breaking things
            results["renamed_files"].append(f"logic_tool.py -> run_cli.py")
    
    def _suggest_better_name(self, filename, pattern_key):
        """Suggest a better name for a file based on the pattern."""
        name, ext = os.path.splitext(filename)
        
        # Convert camelCase to snake_case using utility function
        name_snake = camel_to_snake(name)
        
        if pattern_key == "python_files":
            return f"{name_snake}{ext}"
        elif pattern_key == "entry_points":
            if not name.startswith(("run_", "analyze_", "generate_")):
                if "run" in name.lower():
                    return f"run_{name_snake}{ext}"
                elif "analyze" in name.lower():
                    return f"analyze_{name_snake}{ext}"
                else:
                    return f"run_{name_snake}{ext}"
        elif pattern_key == "generated_files":
            if not name.endswith(("_optimized", "_generated", "_transformed")):
                return f"{name_snake}_optimized{ext}"
        
        return None
