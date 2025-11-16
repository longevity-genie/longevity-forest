from just_agents.data_classes import JustMCPServerParameters
from longevity_forest.config.mcp import BIOMART_MCP_CONFIG, OPENGENES_MCP_CONFIG, KNOWLEDGEBASE_MCP_CONFIG, BIO_MCP_CONFIG, OMNIPATH_MCP_CONFIG


# ============================================================================
# SLIM GENE ANALYSIS CONFIGS - Optimized for gene functional analysis
# ============================================================================
# These configurations are designed for the gene analysis prompt that requires:
# 1. Gene sequence & functional orthologs (BioMART)
# 2. Key known variants & functional outcomes (OpenGenes, UniProt)
# 3. Key interaction partners (STRING)
# 4. Active/functional sites (InterPro, UniProt)
# 5. Protein sequence modifications & functional changes (UniProt, PDB)
# 6. PDB codes for variants & complexes
#
# Tools selected based on: avoiding duplicates, discarding drug items,
# and limiting context bloat while maintaining functional coverage
# ============================================================================

# BioMART Slim: Gene sequence & orthologs lookup
BIOMART_MCP_SLIM_GENE_ANALYSIS = JustMCPServerParameters(
    mcp_client_config=BIOMART_MCP_CONFIG,
    only_include_tools=[
        "list_datasets",           # KEEP: Needed to identify available datasets
        "list_filters",            # KEEP: Filter by species, regions, attributes
        "get_data",                # KEEP: Retrieve ortholog sequences & IDs
        "get_translation",         # KEEP: Get protein translation from sequences
    ],
    exclude_tools=[]
)

# OpenGenes Slim: Variants & functional outcomes related to longevity
OPENGENES_MCP_SLIM_GENE_ANALYSIS = JustMCPServerParameters(
    mcp_client_config=OPENGENES_MCP_CONFIG,
    only_include_tools=[
        "opengenes_db_query",      # KEEP: Query known variants & functional info
        "opengenes_get_schema_info", # KEEP: Understand schema for proper queries
    ],
    exclude_tools=[]
)

# Knowledgebase Slim: UniProt, String, PDB, InterPro information
KNOWLEDGEBASE_MCP_SLIM_GENE_ANALYSIS = JustMCPServerParameters(
    mcp_client_config=KNOWLEDGEBASE_MCP_CONFIG,
    only_include_tools=[
        "bc_get_uniprot_id_by_protein_symbol",  # KEEP: Resolve gene symbol to UniProt ID
        "bc_get_uniprot_protein_info",          # KEEP: Protein features, domains, variants
        "bc_get_string_interactions",           # KEEP: Protein-protein interaction partners
        "bc_get_string_id",                     # KEEP: Resolve gene/protein to STRING ID
        "bc_search_interpro_entries",           # KEEP: Protein domains & functional sites
        "bc_get_interpro_entry",                # KEEP: Detailed domain/site information
        "bc_get_protein_domains",               # KEEP: Domain architecture & sequence intervals
        "bc_get_alphafold_info_by_protein_symbol", # KEEP: 3D structure predictions
        "bc_get_ensembl_id_from_gene_symbol",   # KEEP: Get Ensembl ID for orthologs
        "bc_search_google_scholar_publications", # KEEP: Find functional variant papers
        "bc_get_europepmc_articles",            # KEEP: Find functional variant papers
        "bc_search_studies",                    # KEEP: Find longevity/aging studies
    ],
    exclude_tools=[
        # DISCARD: Drug-related functions (not relevant to gene analysis)
        "bc_search_drugs_by_therapeutic_class",
        "bc_search_drugs_fda",
        "bc_get_drug_by_application_number",
        "bc_count_drugs_by_field",
        "bc_get_drug_label_info",
        "bc_get_available_pharmacologic_classes",
        "bc_get_generic_equivalents",
        "bc_get_drug_statistics",
        
        # DISCARD: Study/clinical recruitment (out of scope)
        "bc_get_recruiting_studies_by_location",
        "bc_get_studies_by_condition",
        "bc_get_studies_by_intervention",
        
        # DISCARD: Full text retrieval (context bloat, use abstracts instead)
        "bc_get_europepmc_fulltext",
        
        # DISCARD: Large outputs / network visualization (context bloat)
        "bc_get_string_network_image",
        "bc_get_antibody_list",
        "bc_get_antibody_information",
        
        # DISCARD: Non-relevant biological databases
        "bc_get_cell_ontology_terms",
        "bc_get_available_ontologies",
        "bc_get_go_terms_by_gene",
        "bc_get_panglaodb_marker_genes",
        "bc_get_panglaodb_options",
        "bc_get_term_details",
        "bc_get_term_hierarchical_children",
        "bc_search_ontology_terms",
        "bc_get_reactome_info_by_identifier",
        
        # DISCARD: Protein expression/proteomics (separate analysis scope)
        "bc_get_human_protein_atlas_info",
        
        # DISCARD: Preprint/bioRxiv (limit to peer-reviewed)
        "bc_get_recent_biorxiv_preprints",
        "bc_get_biorxiv_preprint_details",
        
        # DISCARD: Protein mass spec / antibody studies (not central)
        "bc_search_pride_projects",
        "bc_get_pride_project",
        "bc_search_pride_proteins",
        
        # DISCARD: Chemical/metabolite lookup (out of scope)
        "bc_get_chebi_terms_by_chemical",
        
        # DISCARD: Disease/phenotype mapping (use UniProt instead)
        "bc_get_efo_id_by_disease_name",
        
        # DISCARD: KEGG pathway (keep focused on protein features)
        "bc_get_kegg_id_by_gene_symbol",
        "bc_query_kegg",
        
        # DISCARD: Grant searching (not relevant)
        "bc_search_grants_gov",
        
        # DISCARD: Utility/schema functions
        "bc_get_open_targets_graphql_schema",
        "bc_get_open_targets_query_examples",
        
        # DISCARD: GraphQL queries (use simpler REST endpoints)
        "bc_query_open_targets_graphql",
        
        # DISCARD: String similarity (redundant with similarity scoring)
        "bc_get_string_similarity_scores",
    ]
)

# BIO Slim: PubMed/article fetching with variant information
BIO_MCP_SLIM_GENE_ANALYSIS = JustMCPServerParameters(
    mcp_client_config=BIO_MCP_CONFIG,
    only_include_tools=[
        "fetch",                   # KEEP: Generic fetch for PDB, web resources
        "variant_getter",          # KEEP: Retrieve known genetic variants
        "gene_getter",             # KEEP: Gene information & basic properties
        "article_searcher",        # KEEP: Article search in pubmed
    ],
    exclude_tools=[
        # DISCARD: Drug-related functions
        "drug_getter",
        "openfda_approval_searcher",
        "openfda_approval_getter",
        "openfda_adverse_searcher",
        "openfda_adverse_getter",
        "openfda_shortage_getter",
        "openfda_shortage_searcher",
        "openfda_device_getter",
        "openfda_device_searcher",
        "openfda_recall_getter",
        "openfda_recall_searcher",
        "openfda_label_searcher",
        "openfda_label_getter",
        
        # DISCARD: Clinical trial functions
        "trial_searcher",
        "trial_getter",
        "trial_locations_getter",
        "trial_outcomes_getter",
        "trial_protocol_getter",
        "trial_references_getter",
        
        # DISCARD: Disease & intervention (not central to gene analysis)
        "disease_getter",
        "nci_disease_searcher",
        "nci_intervention_getter",
        "nci_intervention_searcher",
        
        # DISCARD: Organizational search (not relevant)
        "nci_organization_searcher",
        "nci_organization_getter",
        
        # DISCARD: Biomarker search (separate analysis)
        "nci_biomarker_searcher",
        
        # DISCARD: Redundant search functions
        "search",
        
        # DISCARD: AI thinking (meta function)
        "think",
        
        # DISCARD: Variant searcher (use variant_getter instead, avoid duplicates)
        "variant_searcher",
    ]
)

# OmniPath Slim: Pathway & interaction information
OMNIPATH_MCP_SLIM_GENE_ANALYSIS = JustMCPServerParameters(
    mcp_client_config=OMNIPATH_MCP_CONFIG,
    only_include_tools=[
        "execute_sql_query_on_omnipath_db"  # KEEP: Query protein interactions & pathways
    ],
    exclude_tools=[]
)