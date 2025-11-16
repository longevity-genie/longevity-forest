from just_agents.data_classes import JustMCPServerParameters

GGET_MCP_CONFIG = {
  "mcpServers": {
    "gget-mcp": {
      "type": "streamable-http",
      "url": "https://gget-mcp.longevity-genie.info/mcp"
    }
  }
}

BIO_MCP_CONFIG = {
  "mcpServers": {
    "bio-mcp": {
      "type": "streamable-http",
      "url": "https://bio-mcp.longevity-genie.info/mcp"
    }
  }
}

BIOTHINGS_MCP_CONFIG = {
  "mcpServers": {
    "biothings-mcp": {
      "type": "streamable-http",
      "url": "https://biothings-mcp.longevity-genie.info/mcp"
    }
  }
}

SYNERGY_AGE_MCP_CONFIG = {
  "mcpServers": {
    "synergy-age-mcp": {
      "type": "streamable-http",
      "url": "https://synergy-age-mcp.longevity-genie.info/mcp"
    }
  }
}

OPENGENES_MCP_CONFIG = {
  "mcpServers": {
    "opengenes-mcp": {
      "type": "streamable-http",
      "url": "https://opengenes-mcp.longevity-genie.info/mcp"
    }
  }
}

KNOWLEDGEBASE_MCP_CONFIG = {
  "mcpServers": {
    "knowledgebase-mcp": {
      "type": "streamable-http",
      "url": "https://knowledgebase-mcp.longevity-genie.info/mcp"
    }
  }
}

BIOMART_MCP_CONFIG = {
  "mcpServers": {
    "biomart-mcp": {
      "type": "streamable-http",
      "url": "https://biomart-mcp.longevity-genie.info/mcp"
    }
  }
}

ATOMICA_MCP_CONFIG = {
  "mcpServers": {
    "atomica-mcp": {
      "type": "streamable-http",
      "url": "https://atomica-mcp.longevity-genie.info/mcp"
    }
  }
}

OMNIPATH_MCP_CONFIG = {
  "mcpServers": {
    "omnipath-mcp": {
      "type": "streamable-http",
      "url": "https://explore.omnipathdb.org/api/mcp"
    }
  }
}

# JustMCPServerParameters wrappers for all MCP servers
GGET_MCP = JustMCPServerParameters(
    mcp_client_config=GGET_MCP_CONFIG,
    exclude_tools=[]
)

BIO_MCP = JustMCPServerParameters(
    mcp_client_config=BIO_MCP_CONFIG,
    exclude_tools=[]
)

BIOTHINGS_MCP = JustMCPServerParameters(
    mcp_client_config=BIOTHINGS_MCP_CONFIG,
    exclude_tools=[]
)

SYNERGY_AGE_MCP = JustMCPServerParameters(
    mcp_client_config=SYNERGY_AGE_MCP_CONFIG,
    exclude_tools=[]
)

OPENGENES_MCP = JustMCPServerParameters(
    mcp_client_config=OPENGENES_MCP_CONFIG,
    exclude_tools=[]
)

KNOWLEDGEBASE_MCP = JustMCPServerParameters(
    mcp_client_config=KNOWLEDGEBASE_MCP_CONFIG,
    exclude_tools=[]
)

BIOMART_MCP = JustMCPServerParameters(
    mcp_client_config=BIOMART_MCP_CONFIG,
    exclude_tools=[]
)

ATOMICA_MCP = JustMCPServerParameters(
    mcp_client_config=ATOMICA_MCP_CONFIG,
    exclude_tools=[]
)

OMNIPATH_MCP = JustMCPServerParameters(
    mcp_client_config=OMNIPATH_MCP_CONFIG,
    exclude_tools=[]
)

# Full configs with explicit tool lists

# BioMart: call_expert_agent + BioMart tools
BIOMART_MCP_FULL = JustMCPServerParameters(
    mcp_client_config=BIOMART_MCP_CONFIG,
    only_include_tools=[
        "get_data",
        "list_marts",
        "list_datasets",
        "list_all_attributes",
        "batch_translate",
        "get_translation",
        "list_common_attributes",
        "list_filters"
    ],
    exclude_tools=[]
)

# OmniPath: call_expert_agent + OmniPath tools
OMNIPATH_MCP_FULL = JustMCPServerParameters(
    mcp_client_config=OMNIPATH_MCP_CONFIG,
    only_include_tools=[
        "execute_sql_query_on_omnipath_db"
    ],
    exclude_tools=[]
)

# OpenGenes: call_expert_agent + OpenGenes tools
OPENGENES_MCP_FULL = JustMCPServerParameters(
    mcp_client_config=OPENGENES_MCP_CONFIG,
    only_include_tools=[
        "opengenes_db_query",
        "opengenes_get_schema_info",
        "opengenes_example_queries"
    ],
    exclude_tools=[]
)

# BIO (Biological data): call_expert_agent + BIO tools
BIO_MCP_FULL = JustMCPServerParameters(
    mcp_client_config=BIO_MCP_CONFIG,
    only_include_tools=[
        "nci_organization_searcher",
        "openfda_approval_searcher",
        "search",
        "article_getter",
        "alphagenome_predictor",
        "trial_references_getter",
        "article_searcher",
        "openfda_adverse_searcher",
        "gene_getter",
        "nci_disease_searcher",
        "openfda_shortage_getter",
        "think",
        "disease_getter",
        "nci_intervention_getter",
        "openfda_device_getter",
        "trial_locations_getter",
        "variant_getter",
        "nci_biomarker_searcher",
        "trial_searcher",
        "openfda_recall_getter",
        "trial_protocol_getter",
        "openfda_label_searcher",
        "nci_organization_getter",
        "openfda_recall_searcher",
        "trial_outcomes_getter",
        "nci_intervention_searcher",
        "drug_getter",
        "openfda_label_getter",
        "openfda_shortage_searcher",
        "variant_searcher",
        "openfda_approval_getter",
        "openfda_adverse_getter",
        "fetch",
        "trial_getter",
        "openfda_device_searcher"
    ],
    exclude_tools=[]
)

# Knowledgebase: call_expert_agent + Knowledgebase tools
KNOWLEDGEBASE_MCP_FULL = JustMCPServerParameters(
    mcp_client_config=KNOWLEDGEBASE_MCP_CONFIG,
    only_include_tools=[
        "bc_search_google_scholar_publications",
        "bc_get_uniprot_protein_info",
        "bc_get_term_details",
        "bc_search_drugs_by_therapeutic_class",
        "bc_search_interpro_entries",
        "bc_get_europepmc_articles",
        "bc_get_interpro_entry",
        "bc_query_open_targets_graphql",
        "bc_get_string_interactions",
        "bc_get_human_protein_atlas_info",
        "bc_get_string_similarity_scores",
        "bc_get_recent_biorxiv_preprints",
        "bc_get_cell_ontology_terms",
        "bc_get_available_ontologies",
        "bc_get_go_terms_by_gene",
        "bc_get_panglaodb_marker_genes",
        "bc_get_protein_domains",
        "bc_get_reactome_info_by_identifier",
        "bc_search_studies",
        "bc_get_ensembl_id_from_gene_symbol",
        "bc_get_alphafold_info_by_protein_symbol",
        "bc_get_string_network_image",
        "bc_get_study_details",
        "bc_search_drugs_fda",
        "bc_get_pride_project",
        "bc_get_recruiting_studies_by_location",
        "bc_get_europepmc_fulltext",
        "bc_get_open_targets_graphql_schema",
        "bc_get_uniprot_id_by_protein_symbol",
        "bc_search_ontology_terms",
        "bc_get_drug_by_application_number",
        "bc_count_drugs_by_field",
        "bc_search_pride_projects",
        "bc_get_efo_id_by_disease_name",
        "bc_get_biorxiv_preprint_details",
        "bc_get_term_hierarchical_children",
        "bc_search_pride_proteins",
        "bc_get_antibody_information",
        "bc_get_chebi_terms_by_chemical",
        "bc_get_studies_by_condition",
        "bc_get_available_pharmacologic_classes",
        "bc_get_drug_label_info",
        "bc_get_studies_by_intervention",
        "bc_get_kegg_id_by_gene_symbol",
        "bc_query_kegg",
        "bc_get_antibody_list",
        "bc_search_grants_gov",
        "bc_get_panglaodb_options",
        "bc_get_open_targets_query_examples",
        "bc_get_generic_equivalents",
        "bc_get_string_id",
        "bc_get_drug_statistics"
    ],
    exclude_tools=[]
)
