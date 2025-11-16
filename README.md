![LongevityForest Logo](images/longevity_forest.jpg)

# LongevityForest AI Scientist Agent

LongevityForest is a multi-agent bioinformatics system for analysing protein structures, sequences, and functional outcomes in the context of longevity and ageing.

## LongevityForest science agents ecosystem

The LongevityForest science agents ecosystem is a set of tools for studying genes and proteins that influence lifespan. It currently includes:

- **[longevity_forest](https://github.com/longevity-genie/longevity_forest)** (this repository): multi-agent gene analysis system with specialised bioinformatics agents
- **[protein_hunter_mcp](https://github.com/longevity-genie/protein_hunter_mcp)**: MCP server for protein structure analysis and protein target selection
- **[cell2sequence4longevity-mcp](https://github.com/longevity-genie/cell2sequence4longevity-mcp)**: MCP server connecting cellular phenotypes to sequence-level changes in longevity research

Used together, these tools link cellular observations, sequence analysis, and protein structure analysis across multiple biological scales.

## What is this?

This repository provides a delegated multi-agent architecture. Instead of a single monolithic agent, the system orchestrates seven specialised agents, each focused on specific databases or data sources.

The system can analyse a gene by integrating:
- Genomic sequences and orthologs (BioMART)
- Protein 3D structures and domains (AlphaFold, PDB, InterPro)
- Protein-protein interactions (STRING, OmniPath)
- Scientific literature and clinical trials (PubMed, EuropePMC)
- Longevity and aging data (OpenGenes)
- Functional variants and their effects (web search + databases)

The output is a markdown report with source attribution, structured in WikiCrow format.


### Quick overview

```
Query Agent (Orchestrator)
├── Google Agent (web search)
├── Literature Agent (PubMed, clinical trials)
├── Structure Agent (3D structures, domains)
├── BioMART Agent (genomic sequences)
├── OpenGenes Agent (longevity/aging)
└── OmniPath Agent (pathways, interactions)
```

## Quick start

### Prerequisites

- Python 3.12+
- `uv` package manager ([install uv](https://docs.astral.sh/uv/))
- Environment variables configured (see Setup section)

### Installation

```bash
# Clone the repository
git clone https://github.com/longevity-genie/longevity_forest
cd longevity_forest

# Install dependencies with uv
uv sync

# Copy .env.template to .env and fill in your API keys
cp .env.template .env

# Edit .env with your API keys:
# - ANTHROPIC_API_KEY (required) - Used by literature, structure, biomart, and query agents
# - GEMINI_API_KEY (required) - Used by google, opengenes, and omnipath agents
# - Google Cloud credentials (optional - for Vertex AI)
# - Other database credentials as needed
```

### Running gene analysis

```bash
# Analyze a specific gene (default: NRF2)
uv run longevity_forest analyze-gene

# Analyze a specific gene by name
uv run longevity_forest analyze-gene TP53

# Analyze multiple genes
uv run longevity_forest analyze-genes NRF2 TP53 FOXO3

# Available options:
# --config, -c: Path to configuration YAML file
# --cache/--no-cache: Enable/disable cached interim results (default: enabled)
# --debug, -d: Show debug information including tool distribution
# --show-history/--no-history: Display conversation history (default: enabled for single gene)
```

### Output

Results are saved to `data/output/` with format: `GENENAME_TIMESTAMP.md`

Example output structure:
```
# NRF2 - Sequence to Function Analysis

## 1. Sequences & Orthologs
## 2. Key Variants
## 3. Functional Domains
## 4. Interaction Network
## 5. Structural Modifications
## 6. References
```

## Features

- Multi-source data integration from several specialised biological databases
- Results backed by citations with PubMed IDs and DOIs
- Task-specific agents and prompts for different parts of the analysis
- Conversation history stored for transparency and debugging
- Architecture that makes it straightforward to add new agents or databases
- Reduced context size through delegation between agents
- Automatic continuation when a report is incomplete
- Intermediate results cached in `data/interim/` for later inspection

## Configuration

### Main configuration files

- **`src/longevity_forest/config/agents/web_search_delegated.yaml`**: Agent profiles and tool mappings (primary)
- **`src/longevity_forest/config/agents/web_search_full.yaml`**: Alternative monolithic configuration
- **`src/longevity_forest/config/llm.py`**: LLM settings (Anthropic Claude 4.5 Haiku)
- **`src/longevity_forest/config/prompts.py`**: System prompts for each agent
- **`src/longevity_forest/config/mcp.py`**: Database connections (BioMART, OpenGenes, etc.)

### Customising gene analysis

To analyze a different gene, use the CLI command:

```bash
uv run longevity_forest analyze-gene GENE_NAME
```

To customize the analysis prompt, edit `src/longevity_forest/config/prompts.py`:

```python
def get_gene_analysis_prompt(gene_name: str) -> str:
    return f"""For the gene {gene_name} retrieve or identify:
    1) Known gene sequences & functional orthologs
    2) Key variants with longevity implications
    3) Interaction partners
    4) Active/functional sites
    5) Sequence modifications and effects
    6) PDB structures
    """
```

## Project structure

```
longevity_forest/
├── README.md                    # This file
├── pyproject.toml               # Project metadata & dependencies
├── src/
│   └── longevity_forest/       # Main package
│       ├── __init__.py
│       ├── main.py             # Entry point (CLI via entry point)
│       ├── config/
│       │   ├── llm.py           # LLM configuration
│       │   ├── prompts.py       # Agent system prompts
│       │   ├── mcp.py           # Database MCPs (Model Context Protocols)
│       │   ├── gene_analysis_mcp.py # Slim MCPs for gene analysis
│       │   └── agents/
│       │       ├── web_search_delegated.yaml # Delegated architecture config
│       │       └── web_search_full.yaml # Monolithic architecture config (legacy)
│       └── core/
│           ├── helpers.py       # Utility functions (save, validate, serialize)
│           └── experts.py       # Agent delegation logic
├── data/
│   ├── input/                   # Input data files
│   ├── interim/                 # Intermediate cache (YAML & text outputs)
│   ├── output/                  # Final markdown reports (*.md)
│   └── example/                 # Example outputs
├── logs/                        # Execution logs (JSON + text)
├── .env                         # Environment variables (API keys) - create from .env.template
└── .env.template                # Template for environment variables with all required keys
```

## Data flow

1. **Input**: Gene name (e.g., "NRF2")
2. **Orchestration**: Query Agent delegates to 6 specialists
3. **Collection**: Each agent queries its specialized databases
4. **Integration**: Query Agent synthesizes findings
5. **Output**: Markdown report with full citations

## Example: NRF2 analysis

```bash
# Run default NRF2 analysis
uv run longevity_forest analyze-gene NRF2

# Or use the default (NRF2)
uv run longevity_forest analyze-gene
```

The default NRF2 analysis performs:
- BioMART lookup: Human ENSG00000116236, mouse/rat orthologs
- Literature search: ~500+ papers on NRF2 function and variants
- OpenGenes query: NRF2 association with longevity and aging
- Structure analysis: Domains, AlphaFold confidence, PDB codes
- OmniPath query: Antioxidant response elements, pathway context
- Integration: Cross-referenced findings with source attribution

The output is saved to `data/output/NRF2_TIMESTAMP.md`.

## Dependencies

- **[just-agents](https://github.com/longgpt/just_agents)** >= 0.8.8: Multi-agent framework
- **[typer](https://typer.tiangolo.com/)**: CLI framework
- **[python-dotenv](https://python-dotenv.readthedocs.io/)**: Environment configuration
- **[win-unicode-console](https://github.com/Ekopalypse/win_unicode_console/)**: Windows UTF-8 support

See `pyproject.toml` for complete dependency list.

## Environment setup

This project uses two LLM providers: **Anthropic (Claude)** and **Google Gemini**. Different agents use different models:

- **Anthropic Claude**: Used by literature_agent, structure_agent, biomart_agent (Haiku), and query_agent (Sonnet)
- **Google Gemini**: Used by google_agent, opengenes_agent, and omnipath_agent (Gemini 2.5 Pro)

1. Copy the template file:
```bash
cp .env.template .env
```

2. Edit `.env` and add your API keys. You need:
   - **ANTHROPIC_API_KEY** (required) - For Claude models
   - **GEMINI_API_KEY** (required) - For Gemini models
   
   Optional:
   - Google Cloud credentials (GOOGLE_CLOUD_PROJECT, GOOGLE_API_KEY, etc.) - For Vertex AI usage

See `.env.template` for the complete list of configuration options.

The environment variables are automatically loaded when running the CLI:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Advanced usage

### Running with detailed logging

Logs are automatically saved to `logs/` directory:
```
logs/
├── TIMESTAMP_XXXX.log       # Text logs
└── TIMESTAMP_XXXX.json.log  # JSON formatted logs
```

To enable debug output, use the `--debug` flag:

```bash
uv run longevity_forest analyze-gene NRF2 --debug
```

This will show tool distribution across agents and other debugging information.

### Intermediate results

Cached intermediate results are stored in `data/interim/`:
```
interim/
├── *_result.txt    # Agent output text
└── *.yaml          # Agent memory (YAML serialized)
```

Use helper functions to inspect:
```python
from longevity_forest.core.helpers import serialize_memory_to_yaml, serialize_content
```

### Extending with new agents

1. Add agent profile to `config/agents/web_search_delegated.yaml`
2. Define system prompt in `config/prompts.py`
3. Configure tools/MCPs in `config/mcp.py`
4. Query Agent will automatically delegate to new agent

## Testing and validation

All results are validated before completion:

```python
if is_valid:
    print(f"✓ Query result successfully saved and validated: {filepath}")
else:
    print(f"⚠ Query result saved but validation had issues: {filepath}")
```

Validation checks include:
- Markdown syntax integrity
- UTF-8 encoding correctness
- File write success

## Use cases

- Gene function analysis: sequence-to-function relationships
- Variant impact assessment for genetic variants
- Longevity research: ageing-related genes and pathways
- Drug target analysis for protein targets and interactions
- Literature mining and research synthesis
- Structural bioinformatics combining sequence and 3D structure data

## Performance

- Context efficiency: 73–88% reduction compared to monolithic agents
- Token usage: roughly 3–5K tokens per gene analysis (vs 10–15K for monolithic setups)
- Execution time: typically 2–10 minutes depending on sources and gene complexity
- Automatic continuation for incomplete responses
- Cross-source validation to reduce hallucinations

## Troubleshooting

### "Agent with shortname X not found"
- Verify agent is defined in `src/longevity_forest/config/agents/web_search_delegated.yaml`
- Check agent is loaded in `src/longevity_forest/main.py` agents list

### "API rate limit exceeded"
- Wait before re-running
- Use cached intermediate results
- Consider parallel vs sequential agent calls

### "REPORT_END marker not found"
- System automatically continues generation
- Check logs in `logs/` directory for details
- Increase continuation attempts if needed

### UTF-8 Encoding Issues (Windows)
- System automatically reconfigures stdout/stderr to UTF-8
- Verify Windows locale settings support Unicode

## References

- [just-agents Documentation](https://github.com/longgpt/just_agents)
- [Model Context Protocols (MCP)](https://modelcontextprotocol.io/)
- [BioMART](https://www.ensembl.org/biomart/)
- [OpenGenes](https://www.opengenes.org/)
- [OmniPath](https://omnipathdb.org/)
- [InterPro](https://www.ebi.ac.uk/interpro/)
- [STRING Database](https://string-db.org/)

## Architecture documentation

For detailed information about the system architecture, see the agent configuration files:
- Agent profiles: `src/longevity_forest/config/agents/web_search_delegated.yaml`
- Agent prompts: `src/longevity_forest/config/prompts.py`
- MCP configurations: `src/longevity_forest/config/mcp.py`
- Tool mappings: `src/longevity_forest/config/GENE_ANALYSIS_TOOL_MAPPING.md`

## Contributing

To extend this system:

1. **Add new agent**: Modify `src/longevity_forest/config/agents/web_search_delegated.yaml` + add prompt
2. **Add new database**: Create MCP in `src/longevity_forest/config/mcp.py`
3. **Modify analysis prompt**: Edit `src/longevity_forest/config/prompts.py` functions
4. **Change output format**: Modify report generation in agents

## License

See LICENSE file for details.

## Scientific use

When publishing results based on this system:
- cite the original data sources
- verify important findings against the underlying literature
- treat the agent outputs as assistance for expert analysis, not a substitute for it

For agent behaviour configuration, see `src/longevity_forest/config/prompts.py`. For tool mappings, see `src/longevity_forest/config/GENE_ANALYSIS_TOOL_MAPPING.md`.
