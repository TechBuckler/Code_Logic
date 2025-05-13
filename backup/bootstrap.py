"""
Bootstrap - Self-generating architecture system

This module analyzes the existing codebase and transforms it into the new
hierarchical architecture. It serves as the entry point for the self-bootstrapping
process.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase



import os
import json
import shutil
# Import the hierarchical core

class BootstrapModule(HierarchicalModule):
    """
    Module for bootstrapping the new architecture
    """
    def __init__(self, module_id: str, parent=None):
        super().__init__(module_id=module_id, parent=parent)
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.src_dir = os.path.join(self.project_root, "src")
        self.output_dir = os.path.join(self.project_root, "src_new")
        self.analysis_results = None
        self.module_map = {}  # old_module_name -> new_module_info
        
    def initialize(self) -> bool:
        """Initialize the bootstrap module"""
        try:
            # Subscribe to events
            self.event_bus.subscribe("analysis_complete", self._on_analysis_complete)
            self.event_bus.subscribe("generation_complete", self._on_generation_complete)
            self.event_bus.subscribe("transformation_complete", self._on_transformation_complete)
            
            # Create output directory if it doesn't exist
            os.makedirs(self.output_dir, exist_ok=True)
            
            return True
        except Exception as e:
            self.error = e
            return False
    
    def process(self, command: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Process bootstrap commands
        
        Args:
            command: The command to process
            context: Additional context
            
        Returns:
            Command result
        """
        if command == "analyze":
            return self.analyze_codebase()
        elif command == "generate":
            return self.generate_architecture()
        elif command == "transform":
            return self.transform_codebase()
        elif command == "bootstrap":
            # Run the full bootstrap process
            analysis = self.analyze_codebase()
            if "error" in analysis:
                return analysis
                
            generation = self.generate_architecture()
            if "error" in generation:
                return generation
                
            transformation = self.transform_codebase()
            if "error" in transformation:
                return transformation
                
            return {
                "status": "success",
                "message": "Bootstrap process completed successfully",
                "analysis": analysis,
                "generation": generation,
                "transformation": transformation
            }
        else:
            return {
                "error": f"Unknown command: {command}"
            }
    
    def analyze_codebase(self) -> Dict[str, Any]:
        """
        Analyze the existing codebase to identify modules and their relationships
        
        Returns:
            Analysis results
        """
        try:
            print("Analyzing codebase...")
            
            # Analyze all Python files in the src directory
            self.analysis_results = CodeAnalyzer.analyze_directory(self.src_dir)
            
            # Find existing modules
            modules = []
            for file_result in self.analysis_results:
                # Skip files with errors
                if "error" in file_result:
                    print(f"Skipping file with error: {file_result['file_path']} - {file_result['error']}")
                    continue
                    
                for class_info in file_result["classes"]:
                    if class_info.get("is_module", False):
                        modules.append({
                            "file_path": file_result["file_path"],
                            "class_name": class_info["name"],
                            "methods": class_info["methods"]
                        })
            
            # Identify module relationships
            module_relationships = self._identify_module_relationships(modules)
            
            # Publish analysis complete event
            self.event_bus.publish("analysis_complete", {
                "modules": modules,
                "relationships": module_relationships
            })
            
            print(f"Analysis complete. Found {len(modules)} modules.")
            
            return {
                "status": "success",
                "modules": modules,
                "relationships": module_relationships
            }
        except Exception as e:
            print(f"Error analyzing codebase: {e}")
            return {
                "error": f"Error analyzing codebase: {e}"
            }
    
    def generate_architecture(self) -> Dict[str, Any]:
        """
        Generate the new architecture based on analysis results
        
        Returns:
            Generation results
        """
        try:
            if not self.analysis_results:
                return {
                    "error": "No analysis results available. Run analyze_codebase first."
                }
                
            print("Generating new architecture...")
            
            # Debug: Print module information
            print("\nDEBUG: Module Information")
            modules = []
            for file_result in self.analysis_results:
                if "error" in file_result:
                    continue
                    
                for class_info in file_result.get("classes", []):
                    if class_info.get("is_module", False):
                        module_info = {
                            "file_path": file_result["file_path"],
                            "class_name": class_info.get("name"),
                            "methods": class_info.get("methods", [])
                        }
                        modules.append(module_info)
                        print(f"  Module: {module_info['class_name']} in {module_info['file_path']}")
            
            print(f"\nFound {len(modules)} modules for generation.\n")
            
            # Create core directory structure
            core_dir = os.path.join(self.output_dir, "core")
            modules_dir = os.path.join(self.output_dir, "modules")
            ui_dir = os.path.join(self.output_dir, "ui")
            
            os.makedirs(core_dir, exist_ok=True)
            os.makedirs(modules_dir, exist_ok=True)
            os.makedirs(ui_dir, exist_ok=True)
            
            # Copy the hierarchical core
            shutil.copy(
                os.path.join(self.src_dir, "core", "hierarchical_core.py"),
                os.path.join(core_dir, "hierarchical_core.py")
            )
            
            # Generate module hierarchy
            module_hierarchy = self._generate_module_hierarchy()
            
            # Generate module files
            generated_modules = []
            for module_info in module_hierarchy:
                module_path = self._generate_module_file(module_info)
                generated_modules.append({
                    "name": module_info["name"],
                    "path": module_path,
                    "parent": module_info.get("parent")
                })
            
            # Generate module registry
            registry_path = self._generate_registry()
            
            # Publish generation complete event
            self.event_bus.publish("generation_complete", {
                "modules": generated_modules,
                "registry": registry_path
            })
            
            print(f"Generation complete. Generated {len(generated_modules)} modules.")
            
            return {
                "status": "success",
                "modules": generated_modules,
                "registry": registry_path
            }
        except Exception as e:
            print(f"Error generating architecture: {e}")
            return {
                "error": f"Error generating architecture: {e}"
            }
    
    def transform_codebase(self) -> Dict[str, Any]:
        """
        Transform the existing codebase to use the new architecture
        
        Returns:
            Transformation results
        """
        try:
            if not self.module_map:
                return {
                    "error": "No module map available. Run generate_architecture first."
                }
                
            print("Transforming codebase...")
            
            # Transform module implementations
            transformed_modules = []
            for old_name, new_info in self.module_map.items():
                transformed_path = self._transform_module(old_name, new_info)
                transformed_modules.append({
                    "old_name": old_name,
                    "new_name": new_info["name"],
                    "path": transformed_path
                })
            
            # Generate new entry point
            entry_point_path = self._generate_entry_point()
            
            # Publish transformation complete event
            self.event_bus.publish("transformation_complete", {
                "modules": transformed_modules,
                "entry_point": entry_point_path
            })
            
            print(f"Transformation complete. Transformed {len(transformed_modules)} modules.")
            
            return {
                "status": "success",
                "modules": transformed_modules,
                "entry_point": entry_point_path
            }
        except Exception as e:
            print(f"Error transforming codebase: {e}")
            return {
                "error": f"Error transforming codebase: {e}"
            }
    
    def _identify_module_relationships(self, modules: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Identify relationships between modules
        
        Args:
            modules: List of module information
            
        Returns:
            Dictionary mapping module names to lists of related module names
        """
        relationships = {}
        
        # Simple approach: check for module name mentions in file content
        for module in modules:
            module_name = module["class_name"]
            relationships[module_name] = []
            
            # Check other module files for references to this module
            for other_module in modules:
                if other_module["class_name"] == module_name:
                    continue
                    
                with open(other_module["file_path"], 'r') as f:
                    content = f.read()
                    
                if module_name in content:
                    relationships[module_name].append(other_module["class_name"])
        
        return relationships
    
    def _generate_module_hierarchy(self) -> List[Dict[str, Any]]:
        """
        Generate the module hierarchy based on analysis results
        
        Returns:
            List of module information for the new hierarchy
        """
        print("\nGenerating module hierarchy...")
        
        # Extract modules from analysis results
        modules = []
        for file_result in self.analysis_results:
            # Skip files with errors
            if "error" in file_result:
                print(f"Skipping file with error: {file_result['file_path']}")
                continue
                
            for class_info in file_result.get("classes", []):
                # Debug: Print class info
                print(f"Processing class: {class_info}")
                
                if class_info.get("is_module", False):
                    module_info = {
                        "file_path": file_result["file_path"],
                        "class_name": class_info.get("name"),
                        "methods": class_info.get("methods", [])
                    }
                    
                    # Verify class_name is not None
                    if module_info["class_name"] is None:
                        print(f"WARNING: Found module with None class_name in {file_result['file_path']}")
                        continue
                        
                    modules.append(module_info)
        
        # Group modules by functionality
        analysis_modules = [m for m in modules if "analysis" in m["class_name"].lower()]
        optimization_modules = [m for m in modules if "optimization" in m["class_name"].lower()]
        project_modules = [m for m in modules if "project" in m["class_name"].lower() or "explorer" in m["class_name"].lower()]
        ui_modules = [m for m in modules if "ui" in m["class_name"].lower()]
        other_modules = [m for m in modules if m not in analysis_modules + optimization_modules + project_modules + ui_modules]
        
        # Create module hierarchy
        hierarchy = []
        
        # Core modules
        analysis_core = {
            "name": "AnalysisCoreModule",
            "parent": None,
            "children": []
        }
        hierarchy.append(analysis_core)
        
        optimization_core = {
            "name": "OptimizationCoreModule",
            "parent": None,
            "children": []
        }
        hierarchy.append(optimization_core)
        
        project_core = {
            "name": "ProjectCoreModule",
            "parent": None,
            "children": []
        }
        hierarchy.append(project_core)
        
        ui_core = {
            "name": "UICoreModule",
            "parent": None,
            "children": []
        }
        hierarchy.append(ui_core)
        
        # Map old modules to new hierarchy
        for module in analysis_modules:
            # Ensure class_name is not None
            if module.get("class_name") is None:
                print(f"Skipping module with no class name: {module}")
                continue
                
            child = {
                "name": module["class_name"],
                "parent": "AnalysisCoreModule",
                "original": module
            }
            analysis_core["children"].append(child)
            hierarchy.append(child)
            self.module_map[module["class_name"]] = child
        
        for module in optimization_modules:
            # Ensure class_name is not None
            if module.get("class_name") is None:
                print(f"Skipping module with no class name: {module}")
                continue
                
            child = {
                "name": module["class_name"],
                "parent": "OptimizationCoreModule",
                "original": module
            }
            optimization_core["children"].append(child)
            hierarchy.append(child)
            self.module_map[module["class_name"]] = child
        
        for module in project_modules:
            # Ensure class_name is not None
            if module.get("class_name") is None:
                print(f"Skipping module with no class name: {module}")
                continue
                
            child = {
                "name": module["class_name"],
                "parent": "ProjectCoreModule",
                "original": module
            }
            project_core["children"].append(child)
            hierarchy.append(child)
            self.module_map[module["class_name"]] = child
        
        for module in ui_modules:
            # Ensure class_name is not None
            if module.get("class_name") is None:
                print(f"Skipping module with no class name: {module}")
                continue
                
            child = {
                "name": module["class_name"],
                "parent": "UICoreModule",
                "original": module
            }
            ui_core["children"].append(child)
            hierarchy.append(child)
            self.module_map[module["class_name"]] = child
        
        for module in other_modules:
            # Ensure class_name is not None
            if module.get("class_name") is None:
                print(f"Skipping module with no class name: {module}")
                continue
                
            # Determine best parent based on name
            name = module["class_name"].lower()
            if "parser" in name or "analyzer" in name:
                parent = "AnalysisCoreModule"
            elif "optimizer" in name or "performance" in name:
                parent = "OptimizationCoreModule"
            elif "file" in name or "project" in name:
                parent = "ProjectCoreModule"
            elif "ui" in name or "view" in name:
                parent = "UICoreModule"
            else:
                parent = None
                
            child = {
                "name": module["class_name"],
                "parent": parent,
                "original": module
            }
            
            if parent:
                for p in hierarchy:
                    if p["name"] == parent:
                        p["children"].append(child)
                        break
            
            hierarchy.append(child)
            self.module_map[module["class_name"]] = child
        
        return hierarchy
    
    def _generate_module_file(self, module_info: Dict[str, Any]) -> str:
        """
        Generate a module file
        
        Args:
            module_info: Module information
            
        Returns:
            Path to the generated file
        """
        module_name = module_info["name"]
        parent_name = module_info.get("parent", "HierarchicalModule")
        
        # Determine output path
        if parent_name in ["AnalysisCoreModule", "OptimizationCoreModule", "ProjectCoreModule"]:
            # Core module
            output_dir = os.path.join(self.output_dir, "modules", parent_name.replace("Module", "").lower())
        elif parent_name == "UICoreModule":
            # UI module
            output_dir = os.path.join(self.output_dir, "ui")
        else:
            # Other module
            output_dir = os.path.join(self.output_dir, "modules")
        
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{module_name.lower()}.py")
        
        # Generate imports
        imports = [
            "import os",
            "import sys",
            "from typing import Dict, List, Any, Optional"
        ]
        
        # Add parent import
        if parent_name == "HierarchicalModule":
            imports.append("from core.hierarchical_core import HierarchicalModule")
        else:
            if parent_name in ["AnalysisCoreModule", "OptimizationCoreModule", "ProjectCoreModule"]:
                parent_path = f"src.modules.{parent_name.replace('Module', '').lower()}.{parent_name.lower()}"
            elif parent_name == "UICoreModule":
                parent_path = f"src.ui.{parent_name.lower()}"
            else:
                parent_path = f"src.modules.{parent_name.lower()}"
                
            imports.append(f"from {parent_path} import {parent_name}")
        
        # Generate module class
        ModuleGenerator.generate_module_file(
            module_name, output_path, parent_name, imports
        )
        
        return output_path
    
    def _generate_registry(self) -> str:
        """
        Generate the module registry
        
        Returns:
            Path to the generated registry file
        """
        output_path = os.path.join(self.output_dir, "core", "registry.py")
        
        with open(output_path, 'w') as f:
            f.write("""\"\"\"
Module Registry - Central registry for all modules in the system
\"\"\"

import os
import sys
from typing import Dict, List, Any, Optional

from core.hierarchical_core import ModuleRegistry, HierarchicalModule

# Import core modules
from modules.analysis.analysiscoremodule import AnalysisCoreModule
from modules.optimization.optimizationcoremodule import OptimizationCoreModule
from modules.project.projectcoremodule import ProjectCoreModule
from ui.uicoremodule import UICoreModule

def initialize_registry():
    \"\"\"
    Initialize the module registry with all modules
    
    Returns:
        Initialized module registry
    \"\"\"
    registry = ModuleRegistry()
    
    # Create core modules
    analysis_core = AnalysisCoreModule(module_id="analysis_core")
    optimization_core = OptimizationCoreModule(module_id="optimization_core")
    project_core = ProjectCoreModule(module_id="project_core")
    ui_core = UICoreModule(module_id="ui_core")
    
    # Register core modules
    registry.register_module(analysis_core)
    registry.register_module(optimization_core)
    registry.register_module(project_core)
    registry.register_module(ui_core)
    
    # Initialize all modules
    registry.initialize_all()
    
    return registry
""")
        
        return output_path
    
    def _transform_module(self, old_name: str, new_info: Dict[str, Any]) -> str:
        """
        Transform an existing module to use the new architecture
        
        Args:
            old_name: Name of the old module
            new_info: Information about the new module
            
        Returns:
            Path to the transformed module file
        """
        # For now, just copy the original file as a reference
        if "original" in new_info:
            original = new_info["original"]
            original_path = original["file_path"]
            
            # Determine output path
            parent_name = new_info.get("parent", "HierarchicalModule")
            
            if parent_name in ["AnalysisCoreModule", "OptimizationCoreModule", "ProjectCoreModule"]:
                # Core module
                output_dir = os.path.join(self.output_dir, "modules", parent_name.replace("Module", "").lower(), "original")
            elif parent_name == "UICoreModule":
                # UI module
                output_dir = os.path.join(self.output_dir, "ui", "original")
            else:
                # Other module
                output_dir = os.path.join(self.output_dir, "modules", "original")
            
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, os.path.basename(original_path))
            
            # Copy the original file
            shutil.copy(original_path, output_path)
            
            return output_path
        else:
            return ""
    
    def _generate_entry_point(self) -> str:
        """
        Generate the new entry point
        
        Returns:
            Path to the generated entry point file
        """
        output_path = os.path.join(self.output_dir, "main.py")
        
        with open(output_path, 'w') as f:
            f.write("""\"\"\"
Main entry point for the hierarchical system
\"\"\"

import os
import sys
import streamlit as st

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the module registry
from core.registry import initialize_registry

def main():
    \"\"\"Main entry point\"\"\"
    # Initialize the registry
    registry = initialize_registry()
    
    # Set up the UI
    st.title("Logic Tool - Hierarchical Edition")
    
    # Get the UI core module
    ui_core = registry.get_module("ui_core")
    
    # Render the UI
    ui_core.process({"command": "render"})
    
    # Clean up on exit
    import atexit
    atexit.register(lambda: registry.shutdown_all())

if __name__ == "__main__":
    main()
""")
        
        return output_path
    
    def _on_analysis_complete(self, event):
        """Handle analysis complete event"""
        print("Analysis complete event received")
    
    def _on_generation_complete(self, event):
        """Handle generation complete event"""
        print("Generation complete event received")
    
    def _on_transformation_complete(self, event):
        """Handle transformation complete event"""
        print("Transformation complete event received")

def run_bootstrap():
    """Run the bootstrap process"""
    # Create registry
    registry = ModuleRegistry()
    
    # Create bootstrap module
    bootstrap = BootstrapModule(module_id="bootstrap")
    
    # Register and initialize
    registry.register_module(bootstrap)
    registry.initialize_all()
    
    # Run the bootstrap process
    result = bootstrap.process("bootstrap")
    
    print(json.dumps(result, indent=2))
    
    return result

if __name__ == "__main__":
    run_bootstrap()
