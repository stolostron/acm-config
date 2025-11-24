# ACM Config

ACM/MCE metadata repository containing:
- Component registry and ownership mapping
- Team member information
- Development workflow metadata

Used by automation tools and AI assistants.

## Claude Code Plugin Marketplace

This repository provides a Claude Code plugin marketplace for ACM/MCE team tools and workflows.

### Using the Marketplace

Add this marketplace to your Claude Code installation:

```bash
# Using GitHub (recommended)
/plugin marketplace add stolostron/acm-config

# Using Git URL
/plugin marketplace add https://github.com/stolostron/acm-config.git

# Using local path (for development)
/plugin marketplace add /Users/zxue/workspaces/acm-config
```

Once added, install plugins from this marketplace:

```bash
# Install the product plugin
/plugin install product@acm-config-plugins

# Browse all available plugins
/plugin
```

### For Team Members

To automatically load this marketplace in team projects, add to your `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "acm-config-plugins": {
      "source": {
        "source": "github",
        "repo": "stolostron/acm-config"
      }
    }
  }
}
```

### Marketplace Structure

The marketplace configuration is located at `.claude-plugin/marketplace.json` and contains:
- **name**: Marketplace identifier
- **owner**: Maintainer contact information
- **plugins**: Array of plugin definitions with name, source, and description

For more details on plugin marketplaces, see the [Claude Code Plugin Marketplace documentation](https://docs.claude.ai/claude-code/plugins-marketplaces).
