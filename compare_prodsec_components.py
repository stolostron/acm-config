#!/usr/bin/env python3
"""
Compare prodseccomponent values between expected data and product-manifest.json.

This script identifies components where the prodseccomponent field differs
between the expected values (from the user's provided data) and the current
product-manifest.json file.

Usage:
    1. Populate EXPECTED_DATA below with your JSON data
    2. Run: python3 compare_prodsec_components.py

Example EXPECTED_DATA format:
    EXPECTED_DATA = {
       "acm-operator-bundle": {
          "acm_cli": {
             "prodseccomponent": "pscomponent:rhacm2/acm-cli-rhel9",
             "component": "GRC",
             "repository": "https://github.com/stolostron/acm-cli"
          },
          ...
       },
       "mce-operator-bundle": {
          ...
       }
    }
"""

import json

# Expected prodseccomponent values for each component
# Populate this with your expected JSON data
# Format: prodseccomponent:namespace/component-name-rhel9 (or -rhel8)
EXPECTED_DATA = {}


def main():
    """Compare prodseccomponent values and report differences."""
    # Read current file
    with open('product/product-manifest.json', 'r') as f:
        current_data = json.load(f)

    # Compare and find differences
    print("=== Components with Different Prodsec Components ===\n")

    differences_found = False

    for bundle_name, bundle_components in EXPECTED_DATA.items():
        if bundle_name not in current_data:
            continue

        for component_name, component_info in bundle_components.items():
            # Handle both underscore and hyphen versions
            component_name_alt = component_name.replace('_', '-') if '_' in component_name else component_name.replace('-', '_')

            current_component = current_data[bundle_name].get(component_name) or current_data[bundle_name].get(component_name_alt)

            if current_component:
                expected_prodsec = component_info.get('prodseccomponent', '')
                current_prodsec = current_component.get('prodseccomponent', '')

                if expected_prodsec != current_prodsec:
                    differences_found = True
                    print(f"{bundle_name} / {component_name}:")
                    print(f"  Current:  {current_prodsec}")
                    print(f"  Expected: {expected_prodsec}")
                    print()

    if not differences_found:
        print("No differences found. All prodsec components match expected values!")


if __name__ == '__main__':
    main()
