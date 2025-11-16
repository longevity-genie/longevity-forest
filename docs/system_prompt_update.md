# System Prompt Updates for In-Silico Knockout Agent

## Changes Made

Updated the `insilico_knockout_agent` system prompt to be more focused and concise, emphasizing MCP results over general biological discussion.

## Key Changes

### 1. **Primary Focus Shift**
- **Before**: "Write detailed, exhaustive and accurate reports about age predictions, gene knockout effects, and their implications for aging biology"
- **After**: "Your primary task is to execute MCP tool calls, report the numerical results, and provide focused interpretation of the delta age"

### 2. **Delta Age Prominence**
Added explicit instruction to make delta age the star:
- Display delta age **first and prominently**
- It's the most important metric
- Results summary leads with delta age

### 3. **Report Structure**
Defined a clear, concise structure:

```
1. Results Summary (MCP outputs front and center)
   - Delta Age: [VALUE] years - [DIRECTION]
   - Original Age, Knockout Age, Model

2. Experimental Setup (table format)
   - Gene, sentences, metadata

3. Interpretation (brief, 2-3 paragraphs max)
   - What delta age tells us
   - Keep it focused on the knockout results
```

### 4. **Explicit DO NOTs**
Added clear constraints:
- ❌ No lengthy background sections about the gene
- ❌ No extensive literature reviews
- ❌ No detailed molecular mechanisms (unless directly explaining delta age)
- ❌ No multiple subsections with general biological information

### 5. **Explicit DOs**
Added clear requirements:
- ✅ Make delta age the star of the report
- ✅ Present MCP results clearly in tables
- ✅ Keep interpretation focused on knockout experiment results
- ✅ Be concise and data-driven

### 6. **Length Constraint**
- Added: "Keep total report length under 200 lines unless results warrant more detail"
- Previous report was 218 lines with extensive biological background
- Target: ~100-150 lines focused on MCP results

## Expected Report Format

### Old Format (218 lines):
```markdown
# Executive Summary
## Experimental Design
### Metadata
### Gene Expression Sentences
## Results
### Age Prediction Comparison
### Key Findings
## Biological Interpretation
### Direction of Effect
### Biological Context of KLF6
### Position in Expression Ranking
## Mechanistic Insights (extensive)
## Clinical and Research Implications
## Comparison with Other Aging Genes
## Conclusions
## Recommendations
## References and Gene Information
```

### New Format (target ~100-150 lines):
```markdown
# In-Silico Knockout: [GENE]

## Results Summary (MCP)
- **Delta Age**: -5.0 years (PRO-AGING)
- Original Age: 34.0 years
- Knockout Age: 29.0 years
- Model: C2S-Scale-Gemma-2-27B-age-prediction-fullft

## Experimental Setup
[Table with gene, sentences, metadata]

## Interpretation
[2-3 concise paragraphs explaining what the delta age means]
```

## Comparison

| Aspect | Before | After |
|--------|--------|-------|
| **Primary Focus** | General aging biology | MCP results & delta age |
| **Report Length** | 218 lines | Target: 100-150 lines |
| **Gene Background** | Extensive (50+ lines) | Minimal (only for context) |
| **Delta Age** | Buried in results | First and prominent |
| **Interpretation** | Multiple detailed sections | 2-3 concise paragraphs |
| **Mechanisms** | Detailed discussion | Only if explaining delta |

## Benefits

1. **Faster to read**: Users get key metrics immediately
2. **MCP-focused**: Emphasizes the actual model predictions
3. **Delta age prominent**: The most important metric is front-and-center
4. **Less noise**: Removes general gene biology that users can look up elsewhere
5. **Action-oriented**: Focuses on what the knockout experiment tells us

## Testing

To test the new format, run:
```bash
uv run forest insilico-knockout KLF6
```

The new report should:
- Lead with delta age prominently
- Be significantly shorter (~100-150 lines)
- Focus on MCP results
- Have minimal general biological discussion

