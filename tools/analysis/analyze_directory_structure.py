#!/usr/bin/env python3
"""
Analyze the directory structure of the codebase to evaluate balance.
This script will measure depth, breadth, and file distribution.
"""
# Fix imports for reorganized codebase
import utils.import_utils


# Fix imports for reorganized codebase


import os
import json
from collections import defaultdict

# Define the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


def count_files_and_dirs(path):
    """Count the number of files and directories in a path."""
    files = 0
    dirs = 0

    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            dirs += 1
        else:
            files += 1

    return files, dirs


def analyze_directory_structure():
    """Analyze the directory structure and return statistics."""
    results = {
        "total_files": 0,
        "total_dirs": 0,
        "max_depth": 0,
        "dirs_by_depth": defaultdict(int),
        "files_by_depth": defaultdict(int),
        "dir_contents": {},
        "files_by_extension": defaultdict(int),
        "dirs_with_most_files": [],
        "dirs_with_most_subdirs": [],
        "empty_dirs": [],
        "depth_distribution": {},
        "breadth_distribution": {},
    }

    # Walk through the directory structure
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip __pycache__ directories
        if "__pycache__" in root:
            continue

        # Calculate depth relative to project root
        rel_path = os.path.relpath(root, PROJECT_ROOT)
        if rel_path == ".":
            depth = 0
        else:
            depth = len(rel_path.split(os.sep))

        # Update max depth
        results["max_depth"] = max(results["max_depth"], depth)

        # Count files and directories at this depth
        results["dirs_by_depth"][depth] += len(dirs)
        results["files_by_depth"][depth] += len(files)

        # Count total files and directories
        results["total_dirs"] += len(dirs)
        results["total_files"] += len(files)

        # Store directory contents
        dir_name = os.path.basename(root) if depth > 0 else "root"
        results["dir_contents"][rel_path] = {
            "files": len(files),
            "dirs": len(dirs),
            "depth": depth,
            "path": rel_path,
        }

        # Count files by extension
        for file in files:
            _, ext = os.path.splitext(file)
            if ext:
                results["files_by_extension"][ext] += 1
            else:
                results["files_by_extension"]["no_extension"] += 1

        # Check for empty directories
        if len(dirs) == 0 and len(files) == 0:
            results["empty_dirs"].append(rel_path)

    # Calculate depth distribution
    total_nodes = results["total_dirs"] + results["total_files"]
    for depth in range(results["max_depth"] + 1):
        dirs_at_depth = results["dirs_by_depth"][depth]
        files_at_depth = results["files_by_depth"][depth]
        nodes_at_depth = dirs_at_depth + files_at_depth
        results["depth_distribution"][depth] = {
            "dirs": dirs_at_depth,
            "files": files_at_depth,
            "total": nodes_at_depth,
            "percentage": round(nodes_at_depth / total_nodes * 100, 2)
            if total_nodes > 0
            else 0,
        }

    # Find directories with most files and subdirectories
    dir_list = list(results["dir_contents"].values())
    dir_list.sort(key=lambda x: x["files"], reverse=True)
    results["dirs_with_most_files"] = dir_list[:10]

    dir_list.sort(key=lambda x: x["dirs"], reverse=True)
    results["dirs_with_most_subdirs"] = dir_list[:10]

    # Calculate breadth distribution (number of items per directory)
    breadth_counts = defaultdict(int)
    for dir_info in results["dir_contents"].values():
        total_items = dir_info["files"] + dir_info["dirs"]
        breadth_counts[total_items] += 1

    results["breadth_distribution"] = {
        str(k): v for k, v in sorted(breadth_counts.items())
    }

    return results


def generate_report(results):
    """Generate a human-readable report from the analysis results."""
    report = []

    report.append("# Directory Structure Analysis")
    report.append("")
    report.append(f"Total files: {results['total_files']}")
    report.append(f"Total directories: {results['total_dirs']}")
    report.append(f"Maximum directory depth: {results['max_depth']}")
    report.append("")

    report.append("## Depth Distribution")
    report.append("")
    report.append("| Depth | Directories | Files | Total | Percentage |")
    report.append("|-------|-------------|-------|-------|------------|")
    for depth, data in results["depth_distribution"].items():
        report.append(
            f"| {depth} | {data['dirs']} | {data['files']} | {data['total']} | {data['percentage']}% |"
        )
    report.append("")

    report.append("## Breadth Analysis")
    report.append("")
    report.append("Number of directories by item count:")
    report.append("")
    for items, count in sorted(
        [(int(k), v) for k, v in results["breadth_distribution"].items()]
    ):
        report.append(f"- {count} directories contain {items} items")
    report.append("")

    report.append("## Top Directories by File Count")
    report.append("")
    report.append("| Directory | Files | Subdirectories | Depth |")
    report.append("|-----------|-------|----------------|-------|")
    for dir_info in results["dirs_with_most_files"][:10]:
        report.append(
            f"| {dir_info['path']} | {dir_info['files']} | {dir_info['dirs']} | {dir_info['depth']} |"
        )
    report.append("")

    report.append("## Top Directories by Subdirectory Count")
    report.append("")
    report.append("| Directory | Subdirectories | Files | Depth |")
    report.append("|-----------|----------------|-------|-------|")
    for dir_info in results["dirs_with_most_subdirs"][:10]:
        report.append(
            f"| {dir_info['path']} | {dir_info['dirs']} | {dir_info['files']} | {dir_info['depth']} |"
        )
    report.append("")

    report.append("## Files by Extension")
    report.append("")
    report.append("| Extension | Count | Percentage |")
    report.append("|-----------|-------|------------|")
    for ext, count in sorted(
        results["files_by_extension"].items(), key=lambda x: x[1], reverse=True
    ):
        percentage = (
            round(count / results["total_files"] * 100, 2)
            if results["total_files"] > 0
            else 0
        )
        report.append(f"| {ext} | {count} | {percentage}% |")
    report.append("")

    if results["empty_dirs"]:
        report.append("## Empty Directories")
        report.append("")
        for empty_dir in results["empty_dirs"]:
            report.append(f"- {empty_dir}")
        report.append("")

    report.append("## Balance Analysis")
    report.append("")

    # Calculate balance metrics
    breadth_values = [
        int(k) for k, v in results["breadth_distribution"].items() for _ in range(v)
    ]
    if breadth_values:
        avg_breadth = sum(breadth_values) / len(breadth_values)
        min_breadth = min(breadth_values)
        max_breadth = max(breadth_values)

        report.append(f"Average items per directory: {avg_breadth:.2f}")
        report.append(f"Minimum items per directory: {min_breadth}")
        report.append(f"Maximum items per directory: {max_breadth}")

        # Calculate balance score (lower is better)
        if max_breadth > 0:
            balance_ratio = (
                max_breadth / avg_breadth if avg_breadth > 0 else float("inf")
            )
            depth_ratio = results["max_depth"] / 3  # Ideal max depth is around 3

            balance_score = (balance_ratio + depth_ratio) / 2

            if balance_score < 2:
                balance_rating = "Excellent"
            elif balance_score < 3:
                balance_rating = "Good"
            elif balance_score < 5:
                balance_rating = "Fair"
            else:
                balance_rating = "Poor"

            report.append(f"Balance score: {balance_score:.2f} ({balance_rating})")

            # Recommendations
            report.append("")
            report.append("## Recommendations")
            report.append("")

            if max_breadth > 20:
                report.append(
                    "- Consider splitting directories with more than 20 items"
                )

            if results["max_depth"] > 5:
                report.append(
                    "- Consider flattening directory structure in areas deeper than 5 levels"
                )

            if min_breadth < 2 and len(results["dir_contents"]) > 10:
                report.append("- Consider merging directories with very few items")

    return "\n".join(report)


def main():
    """Main function to analyze directory structure and generate report."""
    print("Analyzing directory structure...")

    # Analyze directory structure
    results = analyze_directory_structure()

    # Generate report
    report = generate_report(results)

    # Write report to file
    report_path = os.path.join(PROJECT_ROOT, "directory_structure_report.md")
    with open(report_path, "w") as f:
        f.write(report)

    # Write raw data to JSON for further analysis
    json_path = os.path.join(PROJECT_ROOT, "directory_structure_data.json")
    with open(json_path, "w") as f:
        # Convert defaultdicts to regular dicts for JSON serialization
        serializable_results = json.loads(
            json.dumps(
                results,
                default=lambda x: dict(x) if isinstance(x, defaultdict) else str(x),
            )
        )
        json.dump(serializable_results, f, indent=2)

    print(f"Analysis complete. Report written to {report_path}")
    print(f"Raw data written to {json_path}")

    # Print summary
    print("\nSummary:")
    print(f"Total files: {results['total_files']}")
    print(f"Total directories: {results['total_dirs']}")
    print(f"Maximum directory depth: {results['max_depth']}")

    # Calculate balance metrics
    breadth_values = [
        int(k) for k, v in results["breadth_distribution"].items() for _ in range(v)
    ]
    if breadth_values:
        avg_breadth = sum(breadth_values) / len(breadth_values)
        min_breadth = min(breadth_values)
        max_breadth = max(breadth_values)

        print(f"Average items per directory: {avg_breadth:.2f}")
        print(f"Minimum items per directory: {min_breadth}")
        print(f"Maximum items per directory: {max_breadth}")


if __name__ == "__main__":
    main()
