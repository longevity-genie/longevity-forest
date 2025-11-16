# In-Silico Knockout Implementation

This document describes the implementation of the `insilico-knockout` command for the Longevity Forest project.

## Overview

The `insilico-knockout` command performs in-silico gene knockout experiments using the Cell2Sentence4Longevity model to predict biological age changes when genes are removed from expression profiles.

## Components

### 1. Agent Configuration (`src/longevity_forest/config/agents/insilico_knockout.yaml`)

The agent is configured as a `BaseAgentWithLogging` with:
- **Model**: Claude Sonnet 4.5 (temperature: 0.0 for reproducibility)
- **System Prompt**: Detailed instructions on performing knockout experiments and interpreting results
- **MCP Tools**:
  - `predict_age`: Basic age prediction from gene sentences
  - `predict_age_with_metadata`: Age prediction with demographic/biological metadata
  - `insilico_knockout`: Complete knockout workflow (handles both predictions automatically)

The agent is specialized in:
- Analyzing gene expression effects on biological age
- Performing knockout experiments
- Interpreting delta age (age change after knockout)
- Considering biological context (tissue, cell type, sex, smoking status)

### 2. Prompt Generator (`src/longevity_forest/config/prompts.py`)

**Function**: `get_insilico_knockout_prompt()`

**Parameters**:
- `gene_name` (str): Gene to knock out (e.g., "KLF6")
- `gene_sentence` (str, optional): Pre-constructed gene expression sentence
- `sex` (str, optional): "male" or "female"
- `tissue` (str, optional): e.g., "blood", "brain", "liver"
- `cell_type` (str, optional): e.g., "CD14-low, CD16-positive monocyte"
- `smoking_status` (int, optional): 0 = non-smoker, 1 = smoker

**Generated Prompt Structure**:
1. Instructions to construct or use gene expression sentence
2. Knockout simulation steps
3. Metadata inclusion (if provided)
4. Analysis and interpretation guidelines
5. Report format specifications

The prompt ensures:
- Gene sentences include aging-related genes from OpenGenes
- Metadata is used when available for improved predictions
- Results include delta age with biological interpretation
- Output is in markdown format with tables

### 3. CLI Command (`src/longevity_forest/main.py`)

**Command**: `insilico_knockout`

**Default Gene**: KLF6

**Options**:
- `--gene-sentence, -g`: Custom gene expression sentence
- `--sex, -s`: Sex metadata (male/female)
- `--tissue, -t`: Tissue type
- `--cell-type, -ct`: Cell type
- `--smoking-status, -sm`: Smoking status (0 or 1)
- `--config, -c`: Custom config file path
- `--debug, -d`: Debug mode
- `--show-history/--no-history`: Toggle conversation history display

**Workflow**:
1. Setup logging with Eliot
2. Display GPU warning (requires H100 + MCP server)
3. Load in-silico knockout agent from YAML config
4. Generate prompt with user-provided parameters
5. Execute knockout analysis through agent
6. Save results to markdown file
7. Display conversation history (optional)

**Output**: Results saved to `data/output/insilico_knockout_GENENAME_TIMESTAMP.md`

## Usage Examples

### Basic Usage (Default: KLF6)

```bash
uv run forest insilico-knockout
```

### Specific Gene

```bash
uv run forest insilico-knockout TP53
```

### With Metadata

```bash
uv run forest insilico-knockout KLF6 \
  --sex female \
  --tissue blood \
  --cell-type "CD14-low, CD16-positive monocyte" \
  --smoking-status 0
```

### With Custom Gene Sentence

```bash
uv run forest insilico-knockout KLF6 \
  --gene-sentence "MT-CO1 FTL EEF1A1 HLA-B LST1 KLF6 S100A4 HLA-C"
```

## Prerequisites

The Cell2Sentence4Longevity MCP server must be running:

```bash
# In the cell2sentence4longevity-mcp directory
uv run cell2sentence4longevity-mcp-run --host 0.0.0.0 --port 3002
```

**Hardware Requirements**:
- H100 GPU (or equivalent)
- Sufficient VRAM for model inference

## Delta Age Interpretation

The knockout analysis produces a **delta age** metric that indicates the gene's impact:

| Delta Age | Interpretation | Biological Meaning |
|-----------|----------------|-------------------|
| **Positive** | Gene knockout increases predicted age | Gene may be **protective/anti-aging** |
| **Negative** | Gene knockout decreases predicted age | Gene may be **pro-aging** |
| **Near-zero** | Gene knockout has minimal effect | Gene has minimal impact on age prediction in this context |

## Agent Behavior

The agent is instructed to:

1. **Gene Sentence Construction**: If not provided, construct a typical aging-related gene expression sentence from OpenGenes that includes the target gene

2. **Knockout Simulation**: Use the `insilico_knockout` MCP tool to:
   - Predict age with full gene sentence
   - Remove target gene from sentence
   - Predict age with knockout sentence
   - Calculate delta age

3. **Metadata Integration**: Include provided metadata (sex, tissue, cell type, smoking status) to improve prediction accuracy

4. **Result Interpretation**: 
   - Report delta age with direction and magnitude
   - Discuss biological significance of the target gene
   - Consider gene position in expression ranking
   - Reference known biological functions

5. **Report Generation**: Output markdown report with:
   - Comparison table (original vs knockout)
   - Delta age calculation
   - Biological context
   - Gene expression sentences
   - All metadata used

## Files Modified

1. **`src/longevity_forest/config/prompts.py`**
   - Added `get_insilico_knockout_prompt()` function

2. **`src/longevity_forest/main.py`**
   - Added import for `get_insilico_knockout_prompt`
   - Added `insilico_knockout()` command function
   - Follows same pattern as `hunt_protein` command

3. **`README.md`**
   - Updated in-silico knockout section with complete documentation
   - Added usage examples
   - Added interpretation guidelines

## Integration with MCP

The agent uses the Cell2Sentence4Longevity MCP server with three available tools:

1. **predict_age**: Basic age prediction
   ```python
   predict_age(gene_sentence="MT-CO1 FTL EEF1A1 HLA-B ...")
   ```

2. **predict_age_with_metadata**: Age prediction with metadata
   ```python
   predict_age_with_metadata(
       gene_sentence="MT-CO1 FTL ...",
       sex="female",
       tissue="blood",
       cell_type="CD14-low, CD16-positive monocyte",
       smoking_status=0
   )
   ```

3. **insilico_knockout**: Complete knockout workflow (recommended)
   ```python
   insilico_knockout(
       gene_sentence="MT-CO1 FTL KLF6 ...",
       sex="female",
       tissue="blood"
   )
   ```

The `insilico_knockout` tool automatically:
- Removes the first gene (highest expressed) from the sentence
- Performs both predictions (original and knockout)
- Calculates delta age
- Returns complete comparison

## Design Decisions

1. **Default Gene: KLF6** - A well-studied aging-related gene, same as `hunt-protein` default

2. **BaseAgentWithLogging** - Same agent type as `protein_hunter` for consistency

3. **Metadata Optional** - All metadata parameters are optional to allow flexible usage

4. **Direct Tool Call** - Prompt recommends using `insilico_knockout` tool directly rather than separate predictions for efficiency

5. **Markdown Output** - Consistent with other commands (`analyze-gene`, `hunt-protein`)

6. **GPU Warning** - Prominent warnings about GPU requirements and MCP server dependency

## Error Handling

The command includes:
- Config file validation
- Agent loading verification
- Result validation
- Eliot logging for all operations
- Clear error messages

## Future Enhancements

Potential improvements:
1. Batch knockout analysis (multiple genes)
2. Integration with OpenGenes for automatic gene sentence construction
3. Visualization of delta age distributions
4. Statistical significance testing
5. Comparison with experimental knockout data

## Testing

To test the implementation:

```bash
# Check command registration
uv run forest --help

# Check command help
uv run forest insilico-knockout --help

# Test with default gene (requires MCP server)
uv run forest insilico-knockout

# Test with metadata
uv run forest insilico-knockout KLF6 \
  --sex female \
  --tissue blood \
  --smoking-status 0
```

## Related Documentation

- [Cell2Sentence4Longevity MCP README](../../cell2sentence4longevity-mcp/README.md)
- [Longevity Forest README](../README.md)
- [Protein Hunter Implementation](../src/longevity_forest/config/agents/protein_hunter.yaml)

