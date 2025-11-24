#!/usr/bin/env python3
"""
Compare prodseccomponent values between expected data and product-manifest.json.

This script identifies components where the prodseccomponent field differs
between the expected values (from the user's provided data) and the current
product-manifest.json file.

Usage:
    python3 compare_prodsec_components.py
"""

import json

# Expected prodseccomponent values for each component
# Format: prodseccomponent:namespace/component-name-rhel9 (or -rhel8)
EXPECTED_DATA = {
   "acm-operator-bundle": {
      "acm_cli": {
         "prodseccomponent": "pscomponent:rhacm2/acm-cli-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/acm-cli"
      },
      "acm_must_gather": {
         "prodseccomponent": "pscomponent:rhacm2/acm-must-gather-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/must-gather"
      },
      "cert_policy_controller": {
         "prodseccomponent": "pscomponent:rhacm2/cert-policy-controller-rhel9",
         "component": "GRC",
         "repository": "https://github.com/open-cluster-management/cert-policy-controller"
      },
      "cluster_backup_controller": {
         "prodseccomponent": "pscomponent:rhacm2/cluster-backup-operator-rhel9",
         "component": "Business Continuity",
         "repository": "https://github.com/open-cluster-management/cluster-backup-operator"
      },
      "cluster_permission": {
         "prodseccomponent": "pscomponent:rhacm2/acm-cluster-permission-rhel9",
         "component": "Application Lifecycle",
         "repository": "https://github.com/stolostron/cluster-permission"
      },
      "config_policy_controller": {
         "prodseccomponent": "pscomponent:rhacm2/config-policy-controller-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/config-policy-controller"
      },
      "console": {
         "prodseccomponent": "pscomponent:rhacm2/console-rhel9",
         "component": "Console",
         "repository": "https://github.com/stolostron/console"
      },
      "endpoint_monitoring_operator": {
         "prodseccomponent": "pscomponent:rhacm2/endpoint-monitoring-operator-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/multicluster-observability-operator"
      },
      "flightctl": {
         "prodseccomponent": "pscomponent:rhacm2/flightctl",
         "component": "Flight Control",
         "repository": "https://github.com/flightctl/flightctl"
      },
      "flightctl_api": {
         "prodseccomponent": "pscomponent:rhacm2/flightcontrol-api-rhel9",
         "component": "Flight Control",
         "repository": "https://github.com/flightctl/flightctl"
      },
      "flightctl_ocp_ui": {
         "prodseccomponent": "pscomponent:rhacm2/flightcontrol-ocp-ui-rhel9",
         "component": "Flight Control",
         "repository": "https://github.com/flightctl/flightctl-ui"
      },
      "flightctl_periodic": {
         "prodseccomponent": "pscomponent:rhacm2/flightcontrol-periodic-rhel9",
         "component": "Flight Control",
         "repository": "https://github.com/flightctl/flightctl"
      },
      "flightctl_ui": {
         "prodseccomponent": "pscomponent:rhacm2/flightcontrol-ui-rhel9",
         "component": "Flight Control",
         "repository": "https://github.com/flightctl/flightctl-ui"
      },
      "flightctl_worker": {
         "prodseccomponent": "pscomponent:rhacm2/flightcontrol-worker-rhel9",
         "component": "Flight Control",
         "repository": "https://github.com/flightctl/flightctl"
      },
      "governance_policy_addon_controller": {
         "prodseccomponent": "pscomponent:rhacm2/acm-governance-policy-addon-controller-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/governance-policy-addon-controller"
      },
      "governance_policy_framework_addon": {
         "prodseccomponent": "pscomponent:rhacm2/acm-governance-policy-framework-addon-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/governance-policy-framework-addon"
      },
      "governance_policy_propagator": {
         "prodseccomponent": "pscomponent:rhacm2/governance-policy-propagator-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/governance-policy-propagator"
      },
      "grafana": {
         "prodseccomponent": "pscomponent:rhacm2/acm-grafana-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/grafana"
      },
      "grafana_dashboard_loader": {
         "prodseccomponent": "pscomponent:rhacm2/grafana-dashboard-loader-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/grafana-dashboard-loader"
      },
      "insights_client": {
         "prodseccomponent": "pscomponent:rhacm2/insights-client-rhel9",
         "component": "Search",
         "repository": "https://github.com/stolostron/insights-client"
      },
      "insights_metrics": {
         "prodseccomponent": "pscomponent:rhacm2/insights-metrics-rhel9",
         "component": "Search",
         "repository": "https://github.com/stolostron/insights-metrics"
      },
      "klusterlet_addon_controller": {
         "prodseccomponent": "pscomponent:rhacm2/klusterlet-addon-controller-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/klusterlet-addon-controller"
      },
      "kube_rbac_proxy": {
         "prodseccomponent": "pscomponent:kube-rbac-proxy-container",
         "component": "Observability",
         "repository": "https://github.com/stolostron/kube-rbac-proxy"
      },
      "kube_rbac_proxy_rhel9": {
         "prodseccomponent": "pscomponent:rhacm2/kube-rbac-proxy-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/kube-rbac-proxy"
      },
      "kube_state_metrics": {
         "prodseccomponent": "pscomponent:rhacm2/kube-state-metrics-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/kube-state-metrics"
      },
      "memcached": {
         "prodseccomponent": "pscomponent:rhacm2/memcached-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/memcached"
      },
      "memcached_exporter": {
         "prodseccomponent": "pscomponent:rhacm2/memcached-exporter-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/memcached_exporter"
      },
      "metrics_collector": {
         "prodseccomponent": "pscomponent:rhacm2/multicluster-observability-operator-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/multicluster-observability-operator"
      },
      "multicloud_integrations": {
         "prodseccomponent": "pscomponent:rhacm2/multicloud-integrations-rhel9",
         "component": "Application Lifecycle",
         "repository": "https://github.com/stolostron/multicloud-integrations"
      },
      "multicluster_observability_addon": {
         "prodseccomponent": "pscomponent:rhacm2/acm-multicluster-observability-addon-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/multicluster-observability-addon"
      },
      "multicluster_observability_operator": {
         "prodseccomponent": "pscomponent:rhacm2/metrics-collector-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/multicluster-observability-operator"
      },
      "multicluster_operators_application": {
         "prodseccomponent": "pscomponent:rhacm2/multicluster-operators-application-rhel9",
         "component": "Application Lifecycle",
         "repository": "https://github.com/stolostron/multicloud-operators-application"
      },
      "multicluster_operators_channel": {
         "prodseccomponent": "pscomponent:rhacm2/multicluster-operators-channel-rhel9",
         "component": "Application Lifecycle",
         "repository": "https://github.com/stolostron/multicloud-operators-channel"
      },
      "multicluster_operators_subscription": {
         "prodseccomponent": "pscomponent:rhacm2/multicluster-operators-subscription-rhel9",
         "component": "Application Lifecycle",
         "repository": "https://github.com/stolostron/multicloud-operators-subscription"
      },
      "multiclusterhub_operator": {
         "prodseccomponent": "pscomponent:rhacm2/multiclusterhub-rhel9",
         "component": "Installer",
         "repository": "https://github.com/stolostron/multiclusterhub-operator"
      },
      "node_exporter": {
         "prodseccomponent": "pscomponent:rhacm2/node-exporter-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/node-exporter"
      },
      "observatorium": {
         "prodseccomponent": "pscomponent:rhacm2/observatorium-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/observatorium"
      },
      "observatorium_operator": {
         "prodseccomponent": "pscomponent:rhacm2/observatorium-operator-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/observatorium-operator"
      },
      "prometheus": {
         "prodseccomponent": "pscomponent:rhacm2/prometheus-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/prometheus"
      },
      "prometheus_alertmanager": {
         "prodseccomponent": "pscomponent:rhacm2/prometheus-alertmanager-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/prometheus-alertmanager"
      },
      "prometheus_config_reloader": {
         "prodseccomponent": "pscomponent:rhacm2/acm-prometheus-config-reloader-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/prometheus"
      },
      "prometheus_operator": {
         "prodseccomponent": "pscomponent:rhacm2/acm-prometheus-operator-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/prometheus-operator"
      },
      "rbac_query_proxy": {
         "prodseccomponent": "pscomponent:rbac-query-proxy-container",
         "component": "Observability",
         "repository": "https://github.com/stolostron/multicluster-observability-operator"
      },
      "search_collector": {
         "prodseccomponent": "pscomponent:rhacm2/search-collector-rhel9",
         "component": "Search",
         "repository": "https://github.com/stolostron/search-collector"
      },
      "search_indexer": {
         "prodseccomponent": "pscomponent:rhacm2/acm-search-indexer-rhel9",
         "component": "Search",
         "repository": "https://github.com/stolostron/search-indexer"
      },
      "search_v2_api": {
         "prodseccomponent": "pscomponent:rhacm2/acm-search-v2-api-rhel9",
         "component": "Search",
         "repository": "https://github.com/stolostron/search-v2-api"
      },
      "search_v2_operator": {
         "prodseccomponent": "pscomponent:rhacm2/acm-search-v2-rhel9",
         "component": "Search",
         "repository": "https://github.com/stolostron/search-v2-operator"
      },
      "siteconfig_operator": {
         "prodseccomponent": "pscomponent:rhacm2/acm-siteconfig-rhel9",
         "component": "SiteConfig Operator",
         "repository": "https://github.com/stolostron/siteconfig"
      },
      "submariner_addon": {
         "prodseccomponent": "pscomponent:rhacm2/submariner-addon-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/stolostron/submariner-addon"
      },
      "thanos": {
         "prodseccomponent": "pscomponent:rhacm2/thanos-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/thanos"
      },
      "thanos_receive_controller": {
         "prodseccomponent": "pscomponent:rhacm2/thanos-receive-controller-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/thanos-receive-controller"
      },
      "volsync_addon_controller": {
         "prodseccomponent": "pscomponent:rhacm2/volsync-addon-rhel9",
         "component": "Business Continuity",
         "repository": "https://github.com/stolostron/volsync-addon-controller"
      },
      "configmap_reloader": {
         "prodseccomponent": "",
         "component": "Observability",
         "repository": "https://github.com/openshift/configmap-reload"
      },
      "postgresql_13": {
         "prodseccomponent": "",
         "component": "Security",
         "repository": ""
      }
   },
   "mce-operator-bundle": {
      "addon_manager": {
         "prodseccomponent": "pscomponent:multicluster-engine/addon-manager-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/addon-framework"
      },
      "agent_service": {
         "prodseccomponent": "pscomponent:multicluster-engine/agent-service-rhel9",
         "component": "Infrastructure Operator",
         "repository": ""
      },
      "backplane_operator": {
         "prodseccomponent": "pscomponent:multicluster-engine/backplane-rhel9-operator",
         "component": "Installer",
         "repository": "https://github.com/stolostron/backplane-operator"
      },
      "backplane_operator_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/backplane-rhel8-operator",
         "component": "Installer",
         "repository": "https://github.com/stolostron/backplane-operator"
      },
      "backplane_must_gather": {
         "prodseccomponent": "pscomponent:multicluster-engine/must-gather-rhel9",
         "component": "Installer",
         "repository": "https://github.com/stolostron/backplane-must-gather"
      },
      "backplane_must_gather8": {
         "prodseccomponent": "pscomponent:multicluster-engine/must-gather-rhel8",
         "component": "Installer",
         "repository": "https://github.com/stolostron/backplane-must-gather"
      },
      "cluster_api": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-api-rhel9",
         "component": "Cluster Lifecycle",
         "repository": ""
      },
      "cluster_api_provider_assisted": {
         "prodseccomponent": "pscomponent:multicluster-engine-capoa-bootstrap-container",
         "component": "CAPOA",
         "repository": "https://github.com/openshift-assisted/cluster-api-provider-openshift-assisted"
      },
      "cluster_api_provider_agent": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-api-provider-agent-rhel9",
         "component": "HyperShift",
         "repository": "https://github.com/openshift/cluster-api-provider-agent"
      },
      "cluster_api_provider_azure": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-api-provider-azure-rhel9",
         "component": "HyperShift",
         "repository": "https://github.com/openshift/cluster-api-provider-azure"
      },
      "cluster_api_provider_kubevirt": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-api-provider-kubevirt-rhel9",
         "component": "HyperShift",
         "repository": "https://github.com/openshift/cluster-api-provider-kubevirt"
      },
      "clusterclaims_controller": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-claims-rhel9",
         "component": "Cluster Lifecycle",
         "repository": "https://github.com/stolostron/clusterclaims-controller"
      },
      "cluster_curator_controller": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-curator-rhel9",
         "component": "Cluster Lifecycle",
         "repository": "https://github.com/stolostron/cluster-curator-controller"
      },
      "cluster_image_set_controller": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-image-set-controller-rhel9",
         "component": "Cluster Lifecycle",
         "repository": "https://github.com/stolostron/cluster-image-set-controller"
      },
      "clusterlifecycle_state_metrics": {
         "prodseccomponent": "pscomponent:multicluster-engine/clusterlifecycle-state-metrics-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/clusterlifecycle-state-metrics"
      },
      "cluster_proxy_addon": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-proxy-addon-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/cluster-proxy-addon"
      },
      "cluster_proxy": {
         "prodseccomponent": "pscomponent:multicluster-engine/cluster-proxy-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/cluster-proxy"
      },
      "console_mce": {
         "prodseccomponent": "pscomponent:multicluster-engine/console-mce-rhel9",
         "component": "Console",
         "repository": "https://github.com/stolostron/console"
      },
      "discovery_operator": {
         "prodseccomponent": "pscomponent:multicluster-engine/discovery-operator-rhel9",
         "component": "Installer",
         "repository": "https://github.com/stolostron/discovery"
      },
      "hypershift_addon_operator": {
         "prodseccomponent": "pscomponent:multicluster-engine/hypershift-addon-rhel9-operator",
         "component": "HyperShift",
         "repository": "https://github.com/stolostron/hypershift-addon-operator"
      },
      "hypershift_addon_operator_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/hypershift-addon-rhel8-operator",
         "component": "HyperShift",
         "repository": "https://github.com/stolostron/hypershift-addon-operator"
      },
      "hypershift_cli": {
         "prodseccomponent": "pscomponent:multicluster-engine/hypershift-cli-rhel9",
         "component": "HyperShift",
         "repository": "https://github.com/openshift/hypershift"
      },
      "hypershift_cli8": {
         "prodseccomponent": "pscomponent:multicluster-engine/hypershift-cli-rhel8",
         "component": "HyperShift",
         "repository": "https://github.com/openshift/hypershift"
      },
      "hypershift_operator": {
         "prodseccomponent": "pscomponent:multicluster-engine/hypershift-operator-rhel9",
         "component": "HyperShift",
         "repository": "https://github.com/openshift/hypershift"
      },
      "image_based_install_operator": {
         "prodseccomponent": "pscomponent:multicluster-engine/image-based-install-rhel9",
         "component": "Image Based Install Operator",
         "repository": "https://github.com/openshift/image-based-install-operator"
      },
      "kube_rbac_proxy_mce": {
         "prodseccomponent": "pscomponent:multicluster-engine/kube-rbac-proxy-mce-rhel9",
         "component": "Observability",
         "repository": "https://github.com/stolostron/kube-rbac-proxy"
      },
      "kube_rbac_proxy_mce_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/kube-rbac-proxy-mce-rhel8",
         "component": "Observability",
         "repository": "https://github.com/stolostron/kube-rbac-proxy"
      },
      "managedcluster_import_controller": {
         "prodseccomponent": "pscomponent:multicluster-engine/managedcluster-import-controller-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/managedcluster-import-controller"
      },
      "managed_serviceaccount": {
         "prodseccomponent": "pscomponent:multicluster-engine/managed-serviceaccount-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/managed-serviceaccount"
      },
      "multicloud_manager": {
         "prodseccomponent": "pscomponent:multicluster-engine/multicloud-manager-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/multicloud-operators-foundation"
      },
      "openshift_hive": {
         "prodseccomponent": "pscomponent:multicluster-engine/hive-rhel9",
         "component": "Hive",
         "repository": "https://github.com/openshift/hive"
      },
      "provider_credential_controller": {
         "prodseccomponent": "pscomponent:multicluster-engine/provider-credential-controller-rhel9",
         "component": "Cluster Lifecycle",
         "repository": "https://github.com/stolostron/provider-credential-controller"
      },
      "provider_credential_controller_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/provider-credential-controller-rhel8",
         "component": "Cluster Lifecycle",
         "repository": "https://github.com/stolostron/provider-credential-controller"
      },
      "placement": {
         "prodseccomponent": "pscomponent:multicluster-engine/placement-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/ocm"
      },
      "registration": {
         "prodseccomponent": "pscomponent:multicluster-engine/registration-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/ocm"
      },
      "registration_operator": {
         "prodseccomponent": "pscomponent:multicluster-engine/registration-operator-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/ocm"
      },
      "work": {
         "prodseccomponent": "pscomponent:multicluster-engine/work-rhel9",
         "component": "Server Foundation",
         "repository": "https://github.com/stolostron/ocm"
      },
      "assisted_image_service": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-installer-reporter-rhel9",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-image-service"
      },
      "assisted_installer": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-installer-rhel9",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-installer"
      },
      "assisted_installer_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-installer-rhel8",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-installer"
      },
      "assisted_installer_agent": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-installer-agent-rhel9",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-installer-agent"
      },
      "assisted_installer_agent_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-installer-agent-rhel8",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-installer-agent"
      },
      "assisted_installer_controller": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-installer-controller-rhel9",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-installer"
      },
      "assisted_service_8": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-service-8-rhel9",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-service"
      },
      "assisted_service_8_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-service-8-rhel8",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-service"
      },
      "assisted_service_9": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-service-9-rhel9",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-service"
      },
      "assisted_service_9_rhel8": {
         "prodseccomponent": "pscomponent:multicluster-engine/assisted-service-9-rhel8",
         "component": "Infrastructure Operator",
         "repository": "https://github.com/openshift/assisted-service"
      },
      "ose_cluster_api_rhel9": {
         "prodseccomponent": "",
         "component": "Cluster Lifecycle",
         "repository": "https://github.com/kubernetes-sigs/cluster-api"
      },
      "ose_aws_cluster_api_controllers_rhel9": {
         "prodseccomponent": "",
         "component": "Cluster Lifecycle",
         "repository": "https://github.com/kubernetes-sigs/cluster-api-provider-aws"
      },
      "postgresql_12": {
         "prodseccomponent": "",
         "component": "Security",
         "repository": ""
      }
   },
   "gatekeeper-operator-bundle": {
      "gatekeeper": {
         "prodseccomponent": "pscomponent:rhacm2/gatekeeper-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/gatekeeper"
      },
      "gatekeeper-operator": {
         "prodseccomponent": "pscomponent:rhacm2/gatekeeper-operator-rhel9",
         "component": "GRC",
         "repository": "https://github.com/stolostron/gatekeeper-operator"
      }
   },
   "volsync-operator-bundle": {
      "volsync": {
         "prodseccomponent": "pscomponent:rhacm2/volsync-rhel9",
         "component": "Business Continuity",
         "repository": "https://github.com/backube/volsync"
      }
   },
   "submariner-operator-bundle": {
      "submariner-route-agent": {
         "prodseccomponent": "",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/submariner"
      },
      "lighthouse-agent": {
         "prodseccomponent": "pscomponent:rhacm2/lighthouse-agent-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/lighthouse"
      },
      "lighthouse-coredns": {
         "prodseccomponent": "pscomponent:rhacm2/lighthouse-agent-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/lighthouse"
      },
      "nettest": {
         "prodseccomponent": "pscomponent:rhacm2/nettest-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/submariner"
      },
      "submariner-globalnet": {
         "prodseccomponent": "pscomponent:rhacm2/submariner-gateway-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/submariner"
      },
      "submariner-operator": {
         "prodseccomponent": "pscomponent:rhacm2/submariner-operator-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/submariner-operator"
      },
      "submariner-gateway": {
         "prodseccomponent": "pscomponent:rhacm2/submariner-gateway-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/submariner"
      },
      "subctl": {
         "prodseccomponent": "pscomponent:rhacm2/subctl-rhel9",
         "component": "Multicluster Networking",
         "repository": "https://github.com/submariner-io/submariner"
      }
   },
   "globalhub-operator-bundle": {
      "globalhub-operator": {
         "prodseccomponent": "pscomponent:multicluster-globalhub/multicluster-globalhub-operator-rhel9",
         "component": "Global Hub",
         "repository": "https://github.com/stolostron/multicluster-global-hub"
      },
      "globalhub-manager": {
         "prodseccomponent": "pscomponent:multicluster-globalhub/multicluster-globalhub-manager-rhel9",
         "component": "Global Hub",
         "repository": "https://github.com/stolostron/multicluster-global-hub"
      },
      "globalhub-agent": {
         "prodseccomponent": "pscomponent:multicluster-globalhub/multicluster-globalhub-agent-rhel9",
         "component": "Global Hub",
         "repository": "https://github.com/stolostron/multicluster-global-hub"
      },
      "globalhub-postgres-exporter": {
         "prodseccomponent": "pscomponent:multicluster-globalhub/multicluster-globalhub-postgres-exporter-rhel9",
         "component": "Global Hub",
         "repository": ""
      },
      "globalhub-grafana": {
         "prodseccomponent": "pscomponent:multicluster-globalhub/multicluster-globalhub-grafana-rhel9",
         "component": "Global Hub",
         "repository": ""
      },
      "globalhub-kessel-inventory-api": {
         "prodseccomponent": "pscomponent:multicluster-globalhub/multicluster-globalhub-kessel-inventory-api-rhel9",
         "component": "Global Hub",
         "repository": ""
      },
      "postgresql_13": {
         "prodseccomponent": "",
         "component": "Security",
         "repository": ""
      }
   }
}


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
