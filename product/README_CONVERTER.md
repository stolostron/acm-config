# YAML to JSON Converter for Component Registry

⚠️ **TEMPORARY USE ONLY** ⚠️

This JSON file and converter are **temporary** and exist only to support a special case discussed in [this PR comment](https://github.com/stolostron/acm-config/pull/1#discussion_r2517798073).

**IMPORTANT**:
- This `product-manifest.json` file will be **removed in the future**
- **DO NOT use this JSON file** in other scripts or automation
- **ALWAYS use `component-registry.yaml`** as the source of truth for component configuration
- This converter is provided only for the specific transition period mentioned in the PR

---

This script converts the ACM/MCE component registry from YAML format to JSON format.

## Usage

```bash
python3 yaml_to_json.py
```

## Input Format (YAML)

The script reads from `component-registry.yaml` with the following structure:

```yaml
components:
  - name: "addon-manager"
    bundle: "mce-operator-bundle"
    repository: "https://github.com/stolostron/addon-framework"
    prodseccomponent: "pscomponent:multicluster-engine-addon-manager-container"
    jira_component: "Server Foundation"
```

## Output Format (JSON)

The script generates `product-manifest.json` with bundles as top-level keys:

```json
{
  "_WARNING": {
    "_notice": "TEMPORARY FILE - DO NOT USE",
    "_description": "This JSON file is TEMPORARY and will be removed in the future",
    "_reference": "https://github.com/stolostron/acm-config/pull/1#discussion_r2517798073",
    "_important": "DO NOT use this JSON file in scripts. ALWAYS use component-registry.yaml instead"
  },
  "acm-operator-bundle": {
    "acm_cli": {
      "prodseccomponent": "pscomponent:acm-cli-container",
      "component": "GRC",
      "repository": "https://github.com/stolostron/acm-cli"
    }
  }
}
```

**Note**: The `_WARNING` field is automatically added to the JSON output to remind users that this file is temporary and should not be used.

## Transformations

1. **Bundle grouping**: Components are grouped by their `bundle` field as top-level keys
2. **Name transformation**: Component names use underscores instead of hyphens (e.g., `acm-cli` → `acm_cli`)
3. **Field mapping**:
   - YAML `name` → JSON object key
   - YAML `prodseccomponent` → JSON `prodseccomponent`
   - YAML `jira_component` → JSON `component`
   - YAML `repository` → JSON `repository`
4. **No-bundle handling**: Components without a `bundle` field are placed in a `nobundle` group

## Dependencies

This script uses only Python standard library (no external dependencies required):
- `json` - for JSON output
- `re` - for regex parsing

## Output Statistics

After running, the script will display:
- Total number of bundles
- Total number of components converted

Example output:
```
Conversion complete!
Input: component-registry.yaml
Output: product-manifest.json
Total bundles: 7
Total components: 133
```

## Bundle Distribution

The current registry contains components across the following bundles:
- `acm-operator-bundle`: 53 components
- `mce-operator-bundle`: 38 components
- `nobundle`: 24 components (components without a bundle assignment)
- `submariner-operator-bundle`: 8 components
- `globalhub-operator-bundle`: 7 components
- `gatekeeper-operator-bundle`: 2 components
- `volsync-operator-bundle`: 1 component
