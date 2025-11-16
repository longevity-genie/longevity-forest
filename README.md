# LongevityForest AI Scientist Agent

An advanced multi-agent bioinformatics research system that analyzes protein structures, sequences, and functional outcomes to establish clear relationships between genetic variations and their biological implications, particularly focusing on longevity and aging.

## 🧬 What Is This?

This project implements a **delegated multi-agent architecture** where specialized AI agents work together to perform comprehensive bioinformatics research. Instead of a single monolithic agent, the system orchestrates 7 specialized agents, each with domain-specific expertise and access to dedicated biological databases.

**Key Capability**: Perform exhaustive gene analysis that integrates:
- Genomic sequences and orthologs (BioMART)
- Protein 3D structures and domains (AlphaFold, PDB, InterPro)
- Protein-protein interactions (STRING, OmniPath)
- Scientific literature and clinical trials (PubMed, EuropePMC)
- Longevity and aging data (OpenGenes)
- Functional variants and their effects (web search + databases)

**Output**: Comprehensive markdown reports with full source attribution, structured in WikiCrow format for scientific clarity.

## 🏗️ Architecture

See [HLA.md](./HLA.md) for a detailed high-level architecture document.

### Quick Overview

```
Query Agent (Orchestrator)
├── Google Agent (web search)
├── Literature Agent (PubMed, clinical trials)
├── Structure Agent (3D structures, domains)
├── BioMART Agent (genomic sequences)
├── OpenGenes Agent (longevity/aging)
└── OmniPath Agent (pathways, interactions)
```

**Key Benefit**: Delegated architecture reduces prompt context by **73-88%** compared to monolithic agents, improving accuracy and reducing costs.

## 🚀 Quick Start

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

# Create .env file with your API keys
cp .env.example .env
# Edit .env with your credentials:
# - ANTHROPIC_API_KEY
# - Other database credentials as needed
```

### Running Gene Analysis

```bash
# Analyze a specific gene
uv run longevity_forest

# The default gene is NRF2, modify src/longevity_forest/main.py to change:
# gene_name: str = "NRF2"  # Change this line
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

## 📊 Features

- **Multi-Source Data Integration**: Combines data from 6+ specialized databases
- **Scientific Rigor**: All claims backed by citations with PubMed IDs and DOIs
- **Specialized Agents**: Task-specific prompts and tools for accuracy
- **Conversation Memory**: Full conversation history for transparency and debugging
- **Scalable Architecture**: Easy to add new specialist agents or databases
- **Context Efficiency**: Optimized token usage through delegation
- **Continuation Handling**: Automatically continues incomplete report generation
- **Intermediate Caching**: Results cached in `data/interim/` for analysis

## 🔧 Configuration

### Main Configuration Files

- **`config/agents/web_search_delegated.yaml`**: Agent profiles and tool mappings (primary)
- **`config/agents/web_search_full.yaml`**: Alternative monolithic configuration
- **`config/llm.py`**: LLM settings (Anthropic Claude 4.5 Haiku)
- **`config/prompts.py`**: System prompts for each agent
- **`config/mcp.py`**: Database connections (BioMART, OpenGenes, etc.)

### Customizing Gene Analysis

Edit the analysis prompt in `config/prompts.py`:

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

Then modify `main.py` to use a different gene:

```python
gene_name: str = "TP53"  # or any other gene
```

## 📁 Project Structure

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
└── .env                         # Environment variables (API keys)
```

## 💾 Data Flow

1. **Input**: Gene name (e.g., "NRF2")
2. **Orchestration**: Query Agent delegates to 6 specialists
3. **Collection**: Each agent queries its specialized databases
4. **Integration**: Query Agent synthesizes findings
5. **Output**: Markdown report with full citations

## 🔍 Example: NRF2 Analysis

```bash
# Run default NRF2 analysis
uv run longevity_forest
```

**This performs**:
- BioMART lookup: Human ENSG00000116236, mouse/rat orthologs
- Literature search: ~500+ papers on NRF2 function and variants
- OpenGenes query: NRF2 association with longevity and aging
- Structure analysis: Domains, AlphaFold confidence, PDB codes
- OmniPath query: Antioxidant response elements, pathway context
- Integration: Cross-referenced findings with source attribution

**Output**: `data/output/NRF2_TIMESTAMP.md` with complete analysis

## 📦 Dependencies

- **[just-agents](https://github.com/longgpt/just_agents)** >= 0.8.7: Multi-agent framework
- **[typer](https://typer.tiangolo.com/)**: CLI framework (future CLI support)
- **[python-dotenv](https://python-dotenv.readthedocs.io/)**: Environment configuration
- **[win-unicode-console](https://github.com/Ekopalypse/win_unicode_console/)**: Windows UTF-8 support

See `pyproject.toml` for complete dependency list.

## 🔑 Environment Setup

Create a `.env` file in the project root:

```env
# Anthropic API
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Database credentials
# BIOMART_API_KEY=...
# OPENGENES_API_KEY=...
# OMNIPATH_API_KEY=...
```

Load with:
```python
from dotenv import load_dotenv
load_dotenv()
```

## 📖 Advanced Usage

### Running with Detailed Logging

Logs are automatically saved to `logs/` directory:
```
logs/
├── TIMESTAMP_XXXX.log       # Text logs
└── TIMESTAMP_XXXX.json.log  # JSON formatted logs
```

To enable debug output, edit `main.py`:
```python
if True:  # Set to True for tool distribution debug
    print("\nTool distribution across agents:")
    # ... debugging output ...
```

### Intermediate Results

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

### Extending with New Agents

1. Add agent profile to `config/agents/web_search_delegated.yaml`
2. Define system prompt in `config/prompts.py`
3. Configure tools/MCPs in `config/mcp.py`
4. Query Agent will automatically delegate to new agent

## 🧪 Testing & Validation

All results are validated before completion:

```python
if is_valid:
    print(f"✓ Query result successfully saved and validated: {filepath}")
else:
    print(f"⚠ Query result saved but validation had issues: {filepath}")
```

Validation checks:
- Markdown syntax integrity
- UTF-8 encoding correctness
- File write success

## 🎯 Use Cases

- **Gene Function Analysis**: Understand sequence-to-function relationships
- **Variant Impact Assessment**: Predict effects of genetic variants
- **Longevity Research**: Identify aging-related genes and pathways
- **Drug Target Validation**: Analyze protein targets and interactions
- **Literature Mining**: Comprehensive scientific research synthesis
- **Structural Bioinformatics**: Integrate sequence and 3D structure data

## ⚙️ Performance

- **Context Efficiency**: 73-88% reduction vs monolithic agents
- **Token Usage**: ~3-5K tokens per gene analysis (vs 10-15K for monolithic)
- **Execution Time**: 2-10 minutes depending on complexity and source availability
- **Reliability**: Automatic continuation for incomplete responses
- **Accuracy**: Cross-source validation reduces hallucinations

## 🐛 Troubleshooting

### "Agent with shortname X not found"
- Verify agent is defined in `config/agents/web_search_delegated.yaml`
- Check agent is loaded in `main.py` agents list

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

## 📚 References

- [just-agents Documentation](https://github.com/longgpt/just_agents)
- [Model Context Protocols (MCP)](https://modelcontextprotocol.io/)
- [BioMART](https://www.ensembl.org/biomart/)
- [OpenGenes](https://www.opengenes.org/)
- [OmniPath](https://omnipathdb.org/)
- [InterPro](https://www.ebi.ac.uk/interpro/)
- [STRING Database](https://string-db.org/)

## 📄 Architecture Documentation

For detailed information about the system architecture, see [HLA.md](./HLA.md) which covers:
- Complete agent descriptions
- Data flow diagrams
- Tool mappings
- Extension points
- Performance analysis

## 🤝 Contributing

To extend this system:

1. **Add new agent**: Modify `config/agents/web_search_delegated.yaml` + add prompt
2. **Add new database**: Create MCP in `config/mcp.py`
3. **Modify analysis prompt**: Edit `config/prompts.py` functions
4. **Change output format**: Modify report generation in agents

## 📝 License

See LICENSE file for details.

## 🔬 Scientific Use

This tool is designed for research purposes. When publishing results:
- Always cite original sources (automatically done)
- Verify findings against literature
- Use as a research assistant, not sole authority
- Document all assumptions and limitations

---

**Questions?** See [HLA.md](./HLA.md) for architecture details or review `config/prompts.py` for agent behavior customization.
