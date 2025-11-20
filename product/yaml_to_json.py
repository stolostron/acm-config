#!/usr/bin/env python3
"""
Convert component-registry.yaml to JSON format.

⚠️ TEMPORARY USE ONLY ⚠️

This JSON file and converter are TEMPORARY and exist only to support a special case
discussed in https://github.com/stolostron/acm-config/pull/1#discussion_r2517798073

IMPORTANT:
- This product-manifest.json file will be REMOVED in the future
- DO NOT use this JSON file in other scripts or automation
- ALWAYS use component-registry.yaml as the source of truth for component configuration
- This converter is provided only for the specific transition period mentioned in the PR

This script reads the YAML component registry and converts it to a JSON structure
where components are grouped by bundle and indexed by name.
"""

import json
import re


def parse_yaml_component(lines, start_idx):
    """
    Parse a single component entry from YAML lines.

    Args:
        lines: List of all lines from the YAML file
        start_idx: Starting index for this component

    Returns:
        Tuple of (component_dict, next_index)
    """
    component = {}
    idx = start_idx

    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        # Stop at next component or end of file
        if stripped.startswith('- name:') and idx > start_idx:
            break

        # Parse key-value pairs
        if ':' in line and not stripped.startswith('#'):
            # Get indentation level
            indent = len(line) - len(line.lstrip())

            # Only process if it's at component level (indentation ~2-4)
            if indent >= 2:
                # Match key: value or key: "value"
                match = re.match(r'\s*-?\s*(\w+):\s*"?([^"\n]*)"?\s*$', line)
                if match:
                    key = match.group(1)
                    value = match.group(2).strip('"').strip()
                    if value:  # Only add non-empty values
                        component[key] = value

        idx += 1

    return component, idx


def convert_yaml_to_json(yaml_file, json_file):
    """
    Convert YAML component registry to JSON format.

    Args:
        yaml_file: Path to the input YAML file
        json_file: Path to the output JSON file
    """
    # Read YAML file
    with open(yaml_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Create the output structure with warning metadata
    result = {
        "_WARNING": {
            "_notice": "TEMPORARY FILE - DO NOT USE",
            "_description": "This JSON file is TEMPORARY and will be removed in the future",
            "_reference": "https://github.com/stolostron/acm-config/pull/1#discussion_r2517798073",
            "_important": "DO NOT use this JSON file in scripts. ALWAYS use component-registry.yaml instead"
        }
    }
    idx = 0

    # Process each component
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()

        # Look for component entries
        if stripped.startswith('- name:'):
            component, idx = parse_yaml_component(lines, idx)

            name = component.get('name')
            bundle = component.get('bundle', 'nobundle')  # Use 'nobundle' if no bundle specified
            prodseccomponent = component.get('prodseccomponent')
            jira_component = component.get('jira_component')
            repository = component.get('repository')

            # Skip components without a name
            if not name:
                continue

            # Initialize bundle if not exists
            if bundle not in result:
                result[bundle] = {}

            # Create component entry
            component_entry = {}

            if prodseccomponent:
                component_entry['prodseccomponent'] = prodseccomponent

            if jira_component:
                component_entry['component'] = jira_component

            if repository:
                component_entry['repository'] = repository

            # Only add if there's at least one field
            if component_entry:
                # Replace hyphens with underscores in component name for JSON key
                json_key = name.replace('-', '_')
                result[bundle][json_key] = component_entry
        else:
            idx += 1

    # Write JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

    print(f"Conversion complete!")
    print(f"Input: {yaml_file}")
    print(f"Output: {json_file}")
    # Exclude _WARNING from bundle count
    bundle_count = len([k for k in result.keys() if not k.startswith('_')])
    print(f"Total bundles: {bundle_count}")
    # Exclude _WARNING from component count
    total_components = sum(len(v) for k, v in result.items() if not k.startswith('_'))
    print(f"Total components: {total_components}")


if __name__ == '__main__':
    yaml_file = 'component-registry.yaml'
    json_file = 'product-manifest.json'

    convert_yaml_to_json(yaml_file, json_file)
