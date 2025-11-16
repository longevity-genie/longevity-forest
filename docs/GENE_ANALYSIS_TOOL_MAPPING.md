# Gene Analysis Tool Mapping & SLIM Configuration

## Prompt Requirements Analysis

The gene analysis prompt requires gathering 6 categories of information:

1. **Gene sequence & functional orthologs** - Query BioMART for ortholog IDs
2. **Key variants & functional outcomes** - OpenGenes database + functional impact
3. **Interaction partners** - STRING database protein interactions
4. **Functional sites** - Active/functional domains and sites
5. **Sequence modifications** - Protein intervals with functional changes
6. **PDB codes** - 3D structures for variants and complexes

---

## MCP Tool Selection Matrix

### 5 Available MCPs:
1. **BioMART MCP** - Gene sequence, orthologs, attributes
2. **OpenGenes MCP** - Variant data, longevity-related genes
3. **Knowledgebase MCP** - UniProt, STRING, InterPro, PDB, literature
4. **BIO MCP** - PubMed, variants, gene info, general fetching
5. **OmniPath MCP** - Protein interactions, pathways

---

## BIOMART MCP Slim Configuration

### Tools Selected (4/8):
| Tool | Reason |
|------|--------|
| `list_datasets` | ✅ KEEP - Identify available species/assemblies |
| `list_filters` | ✅ KEEP - Filter by species, genomic regions |
| `get_data` | ✅ KEEP - Retrieve ortholog sequences & gene IDs |
| `get_translation` | ✅ KEEP - Get protein sequences from genes |

### Tools Excluded (0):
None - BioMART full config already lean

---

## OPENGENES MCP Slim Configuration

### Tools Selected (2/3):
| Tool | Reason |
|------|--------|
| `opengenes_db_query` | ✅ KEEP - Query variants & functional info |
| `opengenes_get_schema_info` | ✅ KEEP - Understand database schema |

### Tools Excluded (1):
| Tool | Reason |
|------|--------|
| `opengenes_example_queries` | Utility only - use schema + query directly |

---

## KNOWLEDGEBASE MCP Slim Configuration

### Tools Selected (12/57):
Core protein & variant information:
- `bc_get_uniprot_id_by_protein_symbol` - ✅ Resolve gene to UniProt ID
- `bc_get_uniprot_protein_info` - ✅ Protein features, domains, variants
- `bc_get_string_interactions` - ✅ PPIs with confidence scores
- `bc_get_string_id` - ✅ Resolve gene to STRING ID
- `bc_search_interpro_entries` - ✅ Find protein domains/functional sites
- `bc_get_interpro_entry` - ✅ Detailed site information
- `bc_get_protein_domains` - ✅ Domain architecture & exact sequence intervals
- `bc_get_alphafold_info_by_protein_symbol` - ✅ 3D structure predictions
- `bc_get_ensembl_id_from_gene_symbol` - ✅ Get Ensembl ID for orthologs

Literature & studies:
- `bc_search_google_scholar_publications` - ✅ Functional variant papers
- `bc_get_europepmc_articles` - ✅ Functional variant papers
- `bc_search_studies` - ✅ Longevity/aging studies

### Tools Excluded (46):

**Drug-related (8)** - Out of scope:
- ~~`bc_search_drugs_by_therapeutic_class`~~
- ~~`bc_search_drugs_fda`~~
- ~~`bc_get_drug_by_application_number`~~
- ~~`bc_count_drugs_by_field`~~
- ~~`bc_get_drug_label_info`~~
- ~~`bc_get_available_pharmacologic_classes`~~
- ~~`bc_get_generic_equivalents`~~
- ~~`bc_get_drug_statistics`~~

**Clinical/Recruitment (3)** - Out of scope:
- ~~`bc_get_recruiting_studies_by_location`~~
- ~~`bc_get_studies_by_condition`~~
- ~~`bc_get_studies_by_intervention`~~

**Context bloat - Large outputs (3)**:
- ~~`bc_get_europepmc_fulltext`~~ (Use abstracts)
- ~~`bc_get_string_network_image`~~ (Use data, not visualization)
- ~~`bc_get_antibody_list`~~, ~~`bc_get_antibody_information`~~

**Non-essential biology (8)** - Separate scope:
- ~~`bc_get_cell_ontology_terms`~~, ~~`bc_get_available_ontologies`~~
- ~~`bc_get_go_terms_by_gene`~~, ~~`bc_get_panglaodb_marker_genes`~~
- ~~`bc_get_term_details`~~, ~~`bc_get_term_hierarchical_children`~~
- ~~`bc_search_ontology_terms`~~, ~~`bc_get_reactome_info_by_identifier`~~

**Expression/Proteomics (1)** - Separate scope:
- ~~`bc_get_human_protein_atlas_info`~~

**Preprints (2)** - Use peer-reviewed only:
- ~~`bc_get_recent_biorxiv_preprints`~~
- ~~`bc_get_biorxiv_preprint_details`~~

**Mass spectrometry (3)** - Not central:
- ~~`bc_search_pride_projects`~~
- ~~`bc_get_pride_project`~~
- ~~`bc_search_pride_proteins`~~

**Chemistry (1)** - Out of scope:
- ~~`bc_get_chebi_terms_by_chemical`~~

**Disease mapping (1)** - Use UniProt:
- ~~`bc_get_efo_id_by_disease_name`~~

**Metabolic pathways (2)** - Keep protein-focused:
- ~~`bc_get_kegg_id_by_gene_symbol`~~
- ~~`bc_query_kegg`~~

**Grant searching (1)** - Not relevant:
- ~~`bc_search_grants_gov`~~

**Utility/Schema (2)** - Not needed:
- ~~`bc_get_open_targets_graphql_schema`~~
- ~~`bc_get_open_targets_query_examples`~~

**GraphQL (1)** - Use REST endpoints:
- ~~`bc_query_open_targets_graphql`~~

**Redundant scoring (1)**:
- ~~`bc_get_string_similarity_scores`~~ (Use `bc_get_string_interactions`)

---

## BIO MCP Slim Configuration

### Tools Selected (4/37):
| Tool | Reason |
|------|--------|
| `fetch` | ✅ KEEP - Generic fetch for PDB, web resources |
| `variant_getter` | ✅ KEEP - Genetic variants & their info |
| `gene_getter` | ✅ KEEP - Gene properties & basic info |
| `article_searcher` | ✅ KEEP - PubMed article search for variant literature |

### Tools Excluded (34):

**Drug-related (11)** - Out of scope:
- ~~`drug_getter`~~, ~~`openfda_approval_searcher`~~, ~~`openfda_approval_getter`~~
- ~~`openfda_adverse_searcher`~~, ~~`openfda_adverse_getter`~~
- ~~`openfda_shortage_getter`~~, ~~`openfda_shortage_searcher`~~
- ~~`openfda_device_getter`~~, ~~`openfda_device_searcher`~~
- ~~`openfda_recall_getter`~~, ~~`openfda_recall_searcher`~~
- ~~`openfda_label_searcher`~~, ~~`openfda_label_getter`~~

**Clinical trials (6)** - Out of scope:
- ~~`trial_searcher`~~, ~~`trial_getter`~~
- ~~`trial_locations_getter`~~, ~~`trial_outcomes_getter`~~
- ~~`trial_protocol_getter`~~, ~~`trial_references_getter`~~

**Disease/Intervention (4)** - Not central:
- ~~`disease_getter`~~, ~~`nci_disease_searcher`~~
- ~~`nci_intervention_getter`~~, ~~`nci_intervention_searcher`~~

**Organizational (2)** - Not relevant:
- ~~`nci_organization_searcher`~~, ~~`nci_organization_getter`~~

**Biomarker (1)** - Separate scope:
- ~~`nci_biomarker_searcher`~~

**Redundant search (2)**:
- ~~`article_searcher`~~ (Use Knowledgebase)
- ~~`search`~~ (Too generic)

**Meta function (1)**:
- ~~`think`~~ (AI reasoning - not a data tool)

**Duplicate (1)**:
- ~~`variant_searcher`~~ (Use `variant_getter`)

---

## OMNIPATH MCP Slim Configuration

### Tools Selected (1/1):
| Tool | Reason |
|------|--------|
| `execute_sql_query_on_omnipath_db` | ✅ KEEP - Query protein interactions & pathways |

### Tools Excluded (0):
None - OmniPath config is already single tool

---

## Summary Statistics

### Kept vs Discarded
- **Total functions across 5 MCPs**: 106 (full config)
- **Selected for SLIM**: 24
- **Reduction**: 77.4% context reduction
- **Selectivity**: 22.6% of original

### By MCP:
| MCP | Full | Selected | Reduction |
|-----|------|----------|-----------|
| BioMART | 8 | 4 | 50% |
| OpenGenes | 3 | 2 | 33% |
| Knowledgebase | 57 | 12 | 79% |
| BIO | 37 | 4 | 89% |
| OmniPath | 1 | 1 | 0% |
| **TOTAL** | **106** | **23** | **78%** |

### Discards by Category
- **Drugs**: 8 functions (not in gene analysis scope)
- **Clinical/Trials**: 10 functions (separate analysis domain)
- **Context bloat**: 5 functions (large outputs)
- **Non-essential**: 17 functions (biology outside scope)
- **Duplicates**: 3 functions (use primary instead)
- **Utility**: 2 functions (meta/schema only)
- **Expression/Proteomics**: 1 function (separate scope)

---

## Usage

### Import in main.py:

```python
from longevity_forest.config.mcp import (
    BIOMART_MCP_SLIM_GENE_ANALYSIS,
    OPENGENES_MCP_SLIM_GENE_ANALYSIS,
    KNOWLEDGEBASE_MCP_SLIM_GENE_ANALYSIS,
    BIO_MCP_SLIM_GENE_ANALYSIS,
    OMNIPATH_MCP_SLIM_GENE_ANALYSIS
)

gene_analysis_agent: BaseAgentWithLogging = BaseAgentWithLogging(
    name="gene_analysis_agent",
    description="Agent specialized in gene structure-to-function analysis",
    system_prompt=BASE_SCIENTIST_PROMPT,
    llm_options=agent_llm_options,
    tools=[
        call_expert_agent,
        BIOMART_MCP_SLIM_GENE_ANALYSIS,
        OPENGENES_MCP_SLIM_GENE_ANALYSIS,
        KNOWLEDGEBASE_MCP_SLIM_GENE_ANALYSIS,
        BIO_MCP_SLIM_GENE_ANALYSIS,
        OMNIPATH_MCP_SLIM_GENE_ANALYSIS,
    ]
)
```

---

## Key Design Decisions

1. **Avoided drug functions**: All drug-related tools (FDA, classes, etc.) excluded as they're outside gene analysis scope
2. **Removed clinical trial functions**: Recruitment, outcomes, protocols not relevant to gene structure-function
3. **Limited output size**: Excluded full-text retrieval, network images, large lists
4. **Removed duplicates**: Kept primary tools (e.g., `variant_getter` over `variant_searcher`)
5. **Focused on protein info**: Kept UniProt, STRING, InterPro, AlphaFold for comprehensive protein analysis
6. **Domain architecture coverage**: Added `bc_get_protein_domains` for exact sequence intervals and functional site mapping (critical for task #5)
7. **Literature search**: Kept peer-reviewed article search (Scholar, EuropePMC) plus studies, added `article_searcher` for PubMed variant searches
8. **Maintained core functions**: All required functions from user list included
9. **Orthologs via BioMART**: Enabled via `get_data` + `get_translation` + Ensembl ID lookup

---

## Next Steps

1. **Test SLIM configs** with gene analysis queries
2. **Monitor context usage** to verify 80% reduction
3. **Validate output quality** for functional insights
4. **Add tool calls** if specific functions are needed
5. **Profile performance** of slim vs full configurations

