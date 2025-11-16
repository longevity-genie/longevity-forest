from dotenv import load_dotenv
from pathlib import Path
import sys
import warnings
from typing import Optional, List
from datetime import datetime

import typer
from typer import Option, Argument
from eliot import start_action
from pycomfort.logging import to_nice_file, to_nice_stdout
from rich.console import Console

from just_agents.llm_options import LLMOptions
from just_agents.web.web_agent import WebAgent

from longevity_forest.core.helpers import save_result_to_markdown, validate_markdown_file, serialize_memory_to_yaml
from longevity_forest.config.llm import ANTHROPIC_CLAUDE_4_5_HAIKU
from longevity_forest.config.prompts import get_gene_analysis_prompt, get_insilico_knockout_prompt

# Fix encoding for Windows
if sys.platform == 'win32':
    # Force UTF-8 encoding for stdout/stderr
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')

# Create Typer app
app = typer.Typer(
    name="longevity_forest",
    help="Multi-agent bioinformatics research system for sequence-to-function analysis focusing on longevity",
    add_completion=False,
    no_args_is_help=True
)


def setup_warnings() -> None:
    """Suppress deprecation warnings from eliottree library."""
    warnings.filterwarnings("ignore", message="datetime.datetime.utcfromtimestamp.*", category=DeprecationWarning)
    warnings.filterwarnings("ignore", message="Passing `colorize` is deprecated.*", category=DeprecationWarning)


def setup_logging(log_dir: Path = Path("logs")) -> tuple[Path, Path]:
    """
    Setup Eliot logging with file and stdout destinations.
    
    Args:
        log_dir: Directory to store log files (default: logs/)
    
    Returns:
        Tuple of (json_log_path, rendered_log_path)
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique log file names with timestamp and random suffix
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    import random
    import string
    suffix = ''.join(random.choices(string.hexdigits.lower(), k=4))
    
    json_path = log_dir / f"{timestamp}_{suffix}.json.log"
    log_path = log_dir / f"{timestamp}_{suffix}.log"
    
    # Setup logging with both file and stdout
    to_nice_file(output_file=json_path, rendered_file=log_path)
    to_nice_stdout(output_file=json_path)
    
    return json_path, log_path


def load_agents(config_file: Path, debug: bool = False, enable_cache: bool = True) -> tuple[List[WebAgent], WebAgent]:
    """
    Load all agents from configuration file.
    
    Args:
        config_file: Path to the configuration YAML file
        debug: Whether to print debug information
        enable_cache: Whether to enable LLM prompt caching (default: True)
    
    Returns:
        Tuple of (list of all agents, main query agent)
    """
    with start_action(action_type="load_agents", config_file=str(config_file), debug=debug, enable_cache=enable_cache) as action:
        print("Loading agents...")
        
        # Original agents
        google_agent: WebAgent = WebAgent.from_yaml(
            section_name="google_agent",
            parent_section="agent_profiles",
            file_path=config_file
        )
        print("✓ Loaded google_agent (web search)")
        action.log(message_type="agent_loaded", agent="google_agent")
        
        # Literature search agent
        literature_agent: WebAgent = WebAgent.from_yaml(
            section_name="literature_agent",
            parent_section="agent_profiles",
            file_path=config_file
        )
        print("✓ Loaded literature_agent (articles, papers, clinical trials)")
        action.log(message_type="agent_loaded", agent="literature_agent")
        
        # Protein structure agent
        structure_agent: WebAgent = WebAgent.from_yaml(
            section_name="structure_agent",
            parent_section="agent_profiles",
            file_path=config_file
        )
        print("✓ Loaded structure_agent (structures, domains, interactions)")
        action.log(message_type="agent_loaded", agent="structure_agent")
        
        # BioMART query agent
        biomart_agent: WebAgent = WebAgent.from_yaml(
            section_name="biomart_agent",
            parent_section="agent_profiles",
            file_path=config_file
        )
        print("✓ Loaded biomart_agent (BioMART - genes, orthologs, sequences)")
        action.log(message_type="agent_loaded", agent="biomart_agent")
        
        # OpenGenes query agent
        opengenes_agent: WebAgent = WebAgent.from_yaml(
            section_name="opengenes_agent",
            parent_section="agent_profiles",
            file_path=config_file
        )
        print("✓ Loaded opengenes_agent (OpenGenes - longevity, aging)")
        action.log(message_type="agent_loaded", agent="opengenes_agent")
        
        # OmniPath query agent
        omnipath_agent: WebAgent = WebAgent.from_yaml(
            section_name="omnipath_agent",
            parent_section="agent_profiles",
            file_path=config_file
        )
        print("✓ Loaded omnipath_agent (OmniPath - pathways, interactions)")
        action.log(message_type="agent_loaded", agent="omnipath_agent")
        
        # Main query agent
        query_agent: WebAgent = WebAgent.from_yaml(
            section_name="query_agent",
            parent_section="agent_profiles",
            file_path=config_file
        )
        print("✓ Loaded query_agent (main orchestrator)")
        action.log(message_type="agent_loaded", agent="query_agent")
        
        agents = [
            google_agent,
            literature_agent,
            structure_agent,
            biomart_agent,
            opengenes_agent,
            omnipath_agent,
            query_agent
        ]
        
        # Configure result caching for query agent
        if not enable_cache and hasattr(query_agent, 'system_prompt'):
            # Remove caching instructions from system prompt if caching is disabled
            original_prompt = query_agent.system_prompt
            # Remove the caching-related instructions
            cache_instructions = """You always start your work by calling `grep_cache_only_queries` using search term, eg protein or gene name. 
      Note it works like grep, so it returns list of filenames that contain the exact search term.
      If you see relevant queries in the cache, form the list of respective filenames.
      YOU MUST ALWAYS CALL `read_results_by_filenames` tool to enrich your input from the cache before calling any other tools.
      YOU ARE EFFICIENT AND ONLY QUERY THE MISSING INFORMATION NEEDED TO FULFILL THE REQUEST, NOT THE INFORMATION THAT IS ALREADY IN THE CACHE.

      """
            if cache_instructions in original_prompt:
                query_agent.system_prompt = original_prompt.replace(cache_instructions, "")
                action.log(message_type="caching_disabled_prompt_modified")
        
        action.log(message_type="result_caching_configured", enable_cache=enable_cache)
        
        # Display tool distribution for debugging
        if debug:
            print("\nTool distribution across agents:")
            print("-" * 60)
            for agent in agents:
                tools = agent.list_tools() if hasattr(agent, 'list_tools') else []
                tool_count = len(tools) if isinstance(tools, list) else 0
                print(f"\n{agent.description if hasattr(agent, 'description') else 'Agent'}:")
                print(f"  Tools: {tool_count}")
                if isinstance(tools, list) and tools:
                    for tool in tools:
                        print(f"    - {tool}")
            print("-" * 60)
        
        action.log(message_type="agents_loaded", total_agents=len(agents))
        return agents, query_agent


def run_gene_analysis(
    query_agent: WebAgent,
    gene_name: str
) -> Optional[str]:
    """
    Run gene analysis for a given gene.
    
    Args:
        query_agent: The main query agent
        gene_name: Name of the gene to analyze
    
    Returns:
        The analysis result as a string, or None if failed
    """
    with start_action(action_type="run_gene_analysis", gene_name=gene_name) as action:
        console = Console()
        console.print("\n[bold cyan]Starting gene analysis for:[/bold cyan] [bold yellow]{gene_name}[/bold yellow]".format(gene_name=gene_name))
        console.print("[dim]" + "-" * 60 + "[/dim]")
        
        result = query_agent.query(
            query_input=get_gene_analysis_prompt(gene_name)
        )
        action.log(message_type="initial_query_complete", gene_name=gene_name)
        
        # Handle continuation if report is incomplete
        continuation_count = 0
        while "REPORT_END" not in result:
            continuation_count += 1
            print(f"REPORT_END marker not found, continuing the report generation from the last response")
            action.log(message_type="continuation_needed", continuation_number=continuation_count)
            
            continuation_result = query_agent.query(
                query_input="REPORT_END marker not found, continue the report generation from the last response"
            )
            
            if not continuation_result:
                action.log(message_type="continuation_failed", continuation_number=continuation_count)
                raise Exception("Continuation result is empty")
            
            result += continuation_result
            print(f"Continuation result added to the final result")
            action.log(message_type="continuation_added", continuation_number=continuation_count)

        print(f"REPORT_END marker found")
        action.log(message_type="analysis_complete", gene_name=gene_name, continuation_count=continuation_count)
        
        return result


@app.command()
def analyze_gene(
    gene_name: str = Argument("NRF2", help="Name of the gene to analyze (e.g., NRF2, TP53)"),
    config: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        help="Path to configuration YAML file (defaults to config/agents/web_search_delegated.yaml)"
    ),
    cache: bool = Option(
        True,
        "--cache/--no-cache",
        help="Enable or disable loading of cached interim results from data/interim/ (default: enabled)"
    ),
    debug: bool = Option(
        False,
        "--debug",
        "-d",
        help="Show debug information including tool distribution"
    ),
    show_history: bool = Option(
        True,
        "--show-history/--no-history",
        help="Display conversation history after analysis"
    ),
) -> None:
    """
    Analyze a gene using the multi-agent bioinformatics research system (default: NRF2).
    
    This command performs comprehensive gene analysis including:
    - Gene function and biological role
    - Protein structure and domains
    - Pathways and interactions
    - Literature and clinical trials
    - Longevity and aging associations
    """
    setup_warnings()
    load_dotenv()
    
    # Setup Eliot logging
    json_path, log_path = setup_logging()
    print(f"Logging initialized: {log_path}")
    
    # Display caching status in bold
    cache_status = "ENABLED" if cache else "DISABLED"
    print(f"\n\033[1mInterim Results Caching: {cache_status}\033[0m")
    if cache:
        print("  → Will load cached results from data/interim/ to avoid redundant queries")
    else:
        print("  → Will make fresh queries without loading cached results")
    print()
    
    with start_action(action_type="analyze_gene_command", gene_name=gene_name, cache_enabled=cache) as action:
        # Determine config file path
        if config is None:
            config = Path(__file__).parent / "config/agents/web_search_delegated.yaml"
        
        if not config.exists():
            action.log(message_type="config_not_found", config_path=str(config))
            typer.echo(f"Error: Configuration file not found: {config}", err=True)
            raise typer.Exit(1)
        
        action.log(message_type="config_loaded", config_path=str(config))
        
        # Load agents
        agents, query_agent = load_agents(config, debug=debug, enable_cache=cache)
        
        # Run analysis
        result = run_gene_analysis(query_agent, gene_name)
        
        # Save and validate results
        if result:
            result_str = str(result) if not isinstance(result, str) else result
            filepath = save_result_to_markdown(result_str, gene_name)
            action.log(message_type="result_saved", filepath=str(filepath))
            
            is_valid = validate_markdown_file(filepath)
            file_uri = filepath.resolve().as_uri()
            if is_valid:
                action.log(message_type="validation_success", filepath=str(filepath))
                typer.echo(f"\n✓ Query result successfully saved and validated: {filepath}")
                typer.echo(f"  Open report: {file_uri}")
            else:
                action.log(message_type="validation_warning", filepath=str(filepath))
                typer.echo(f"\n⚠ Query result saved but validation had issues: {filepath}")
                typer.echo(f"  Open report: {file_uri}")
        else:
            action.log(message_type="no_result", gene_name=gene_name)
            typer.echo("✗ No result returned from query agent", err=True)
            raise typer.Exit(1)
        
        # Display conversation history
        if show_history:
            print("\n" + "="*60)
            print("CONVERSATION HISTORY")
            print("="*60)
            for agent in agents:
                if hasattr(agent, 'memory'):
                    print(f"\n{agent.description if hasattr(agent, 'description') else 'Agent'}:")
                    agent.memory.pretty_print_all_messages()
            # Repeat report link after history for convenience
            print(f"\nOpen report: {file_uri}")


@app.command()
def analyze_genes(
    genes: List[str] = Argument(..., help="List of gene names to analyze (e.g., NRF2 TP53 FOXO3)"),
    config: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        help="Path to configuration YAML file (defaults to config/agents/web_search_delegated.yaml)"
    ),
    cache: bool = Option(
        True,
        "--cache/--no-cache",
        help="Enable or disable interim results caching (default: enabled)"
    ),
    debug: bool = Option(
        False,
        "--debug",
        "-d",
        help="Show debug information including tool distribution"
    ),
    show_history: bool = Option(
        False,
        "--show-history/--no-history",
        help="Display conversation history after each analysis"
    ),
) -> None:
    """
    Analyze multiple genes sequentially using the multi-agent bioinformatics research system.
    """
    setup_warnings()
    load_dotenv()
    
    # Setup Eliot logging
    json_path, log_path = setup_logging()
    print(f"Logging initialized: {log_path}")
    
    # Display caching status in bold
    cache_status = "ENABLED" if cache else "DISABLED"
    print(f"\n\033[1mInterim Results Caching: {cache_status}\033[0m")
    if cache:
        print("  → Will load cached results from data/interim/ to avoid redundant queries")
    else:
        print("  → Will make fresh queries without loading cached results")
    print()
    
    with start_action(action_type="analyze_genes_command", gene_count=len(genes), genes=genes, cache_enabled=cache) as action:
        # Determine config file path
        if config is None:
            config = Path(__file__).parent / "config/agents/web_search_delegated.yaml"
        
        if not config.exists():
            action.log(message_type="config_not_found", config_path=str(config))
            typer.echo(f"Error: Configuration file not found: {config}", err=True)
            raise typer.Exit(1)
        
        action.log(message_type="config_loaded", config_path=str(config))
        
        # Load agents once for all genes
        agents, query_agent = load_agents(config, debug=debug, enable_cache=cache)
        
        # Analyze each gene
        results = {}
        for gene_name in genes:
            with start_action(action_type="analyze_single_gene", gene_name=gene_name) as gene_action:
                result = run_gene_analysis(query_agent, gene_name)
                
                if result:
                    result_str = str(result) if not isinstance(result, str) else result
                    filepath = save_result_to_markdown(result_str, gene_name)
                    gene_action.log(message_type="result_saved", filepath=str(filepath))
                    
                    is_valid = validate_markdown_file(filepath)
                    file_uri = filepath.resolve().as_uri()
                    if is_valid:
                        gene_action.log(message_type="validation_success", filepath=str(filepath))
                        typer.echo(f"\n✓ {gene_name}: Query result successfully saved and validated: {filepath}")
                        typer.echo(f"  Open report: {file_uri}")
                        results[gene_name] = "success"
                    else:
                        gene_action.log(message_type="validation_warning", filepath=str(filepath))
                        typer.echo(f"\n⚠ {gene_name}: Query result saved but validation had issues: {filepath}")
                        typer.echo(f"  Open report: {file_uri}")
                        results[gene_name] = "warning"
                else:
                    gene_action.log(message_type="no_result", gene_name=gene_name)
                    typer.echo(f"✗ {gene_name}: No result returned from query agent", err=True)
                    results[gene_name] = "failed"
        
        # Display summary
        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)
        for gene_name, status in results.items():
            symbol = "✓" if status == "success" else "⚠" if status == "warning" else "✗"
            print(f"{symbol} {gene_name}: {status}")
        
        action.log(message_type="batch_analysis_complete", results=results)


@app.command()
def hunt_protein(
    target: str = Argument("KLF6", help="Gene name or protein sequence to target for degradation (e.g., KLF6, TP53, FOXO3)"),
    config: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        help="Path to protein hunter configuration YAML file (defaults to config/agents/protein_hunter.yaml)"
    ),
    debug: bool = Option(
        False,
        "--debug",
        "-d",
        help="Show debug information"
    ),
    show_history: bool = Option(
        True,
        "--show-history/--no-history",
        help="Display conversation history after design"
    ),
) -> None:
    """
    Design a degradation peptide for a target protein using protein hunter agent.
    
    This command will:
    1. Resolve the protein sequence from gene name (if gene provided)
    2. Design a high-affinity binder for the target protein
    3. Generate a degradation adaptor by fusing ubiquitin to the binder
    
    The resulting peptide will target the protein for degradation via the ubiquitin-proteasome system.
    """
    setup_warnings()
    load_dotenv()
    
    # Setup Eliot logging
    json_path, log_path = setup_logging()
    print(f"Logging initialized: {log_path}")
    
    with start_action(action_type="hunt_protein_command", target=target) as action:
        # Determine config file path
        if config is None:
            config = Path(__file__).parent / "config/agents/protein_hunter.yaml"
        
        if not config.exists():
            action.log(message_type="config_not_found", config_path=str(config))
            typer.echo(f"Error: Configuration file not found: {config}", err=True)
            raise typer.Exit(1)
        
        action.log(message_type="config_loaded", config_path=str(config))
        
        console = Console()
        console.print("\n[bold cyan]Protein Hunter: Designing degradation peptide for:[/bold cyan] [bold yellow]{target}[/bold yellow]".format(target=target))
        console.print("[dim]" + "-" * 60 + "[/dim]")
        
        # Load protein hunter agent
        print("Loading protein hunter agent...")
        protein_hunter_agent: WebAgent = WebAgent.from_yaml(
            section_name="protein_hunter",
            parent_section="agent_profiles",
            file_path=config
        )
        print("✓ Loaded protein_hunter agent")
        action.log(message_type="agent_loaded", agent="protein_hunter")
        
        # Construct the prompt for protein degradation design
        prompt = f"""Design a degradation peptide for the target: {target}

Your task:
1. If {target} is a gene name, first resolve it to a protein sequence using appropriate tools
2. Design a high-affinity protein binder for this target using Boltz or Chai design tools
3. Select the best binder from the results (look for high iPTM scores 0.9+ and good pLDDT scores)
4. Create a degradation adaptor by fusing ubiquitin to the C-terminus of the selected binder
5. Provide the final degradation peptide sequence in the format: BinderSequence + Linker + Ubiquitin

Use a flexible linker like GGSGGS between the binder and ubiquitin.

Please provide:
- The resolved target protein sequence
- Design metrics for the binder (iPTM, pLDDT, etc.)
- The final degradation peptide sequence
- Output file locations for structures

Generate a comprehensive report in markdown format."""

        console.print("\n[bold]Sending design request to protein hunter agent...[/bold]")
        console.print("[yellow]Note: Protein design is a long-running task (5-10 minutes per design)[/yellow]\n")
        
        result = protein_hunter_agent.query(query_input=prompt)
        action.log(message_type="design_complete", target=target)
        
        # Save and validate results
        if result:
            result_str = str(result) if not isinstance(result, str) else result
            # Use target name for filename
            safe_target = target.replace("/", "_").replace("\\", "_")
            filepath = save_result_to_markdown(result_str, f"degradation_peptide_{safe_target}")
            action.log(message_type="result_saved", filepath=str(filepath))
            
            is_valid = validate_markdown_file(filepath)
            file_uri = filepath.resolve().as_uri()
            if is_valid:
                action.log(message_type="validation_success", filepath=str(filepath))
                typer.echo(f"\n✓ Degradation peptide design successfully saved and validated: {filepath}")
                typer.echo(f"  Open report: {file_uri}")
            else:
                action.log(message_type="validation_warning", filepath=str(filepath))
                typer.echo(f"\n⚠ Degradation peptide design saved but validation had issues: {filepath}")
                typer.echo(f"  Open report: {file_uri}")
        else:
            action.log(message_type="no_result", target=target)
            typer.echo("✗ No result returned from protein hunter agent", err=True)
            raise typer.Exit(1)
        
        # Display conversation history
        if show_history:
            print("\n" + "="*60)
            print("CONVERSATION HISTORY")
            print("="*60)
            if hasattr(protein_hunter_agent, 'memory'):
                print(f"\n{protein_hunter_agent.description if hasattr(protein_hunter_agent, 'description') else 'Protein Hunter Agent'}:")
                protein_hunter_agent.memory.pretty_print_all_messages()
            # Repeat report link after history for convenience
            print(f"\nOpen report: {file_uri}")


@app.command()
def insilico_knockout(
    gene_name: str = Argument("KLF6", help="Gene symbol to knock out for in-silico analysis (e.g., KLF6, TP53, FOXO3)"),
    gene_sentence: Optional[str] = Option(
        None,
        "--gene-sentence",
        "-g",
        help="Optional gene expression sentence (space-separated gene names ordered by descending expression). If not provided, agent will construct one from OpenGenes."
    ),
    sex: Optional[str] = Option(
        None,
        "--sex",
        "-s",
        help="Optional sex metadata for improved prediction (male/female)"
    ),
    tissue: Optional[str] = Option(
        None,
        "--tissue",
        "-t",
        help="Optional tissue type (e.g., blood, brain, liver)"
    ),
    cell_type: Optional[str] = Option(
        None,
        "--cell-type",
        "-ct",
        help="Optional cell type (e.g., 'CD14-low, CD16-positive monocyte')"
    ),
    smoking_status: Optional[int] = Option(
        None,
        "--smoking-status",
        "-sm",
        help="Optional smoking status: 0 = non-smoker, 1 = smoker"
    ),
    config: Optional[Path] = Option(
        None,
        "--config",
        "-c",
        help="Path to in-silico knockout configuration YAML file (defaults to config/agents/insilico_knockout.yaml)"
    ),
    debug: bool = Option(
        False,
        "--debug",
        "-d",
        help="Show debug information"
    ),
    show_history: bool = Option(
        True,
        "--show-history/--no-history",
        help="Display conversation history after analysis"
    ),
) -> None:
    """
    Perform in-silico knockout analysis using cell2sentence4longevity model.
    
    This command will:
    1. Construct or use provided gene expression sentence
    2. Simulate gene knockout by removing the specified gene
    3. Compare biological age predictions before and after knockout
    4. Analyze the impact of the gene on aging
    
    ⚠️ WARNING: GPU-intensive workflow - requires H100 GPU and cell2sentence4longevity MCP server running.
    """
    setup_warnings()
    load_dotenv()
    
    # Setup Eliot logging
    json_path, log_path = setup_logging()
    print(f"Logging initialized: {log_path}")
    
    # GPU warning
    console = Console()
    console.print("\n[bold red]⚠️  WARNING: GPU-INTENSIVE WORKFLOW[/bold red]")
    console.print("[yellow]This command requires the cell2sentence4longevity MCP server with H100 GPU.[/yellow]")
    console.print("[yellow]Ensure the server is running at http://localhost:3002/mcp before proceeding.[/yellow]\n")
    
    with start_action(action_type="insilico_knockout_command", gene_name=gene_name) as action:
        # Determine config file path
        if config is None:
            config = Path(__file__).parent / "config/agents/insilico_knockout.yaml"
        
        if not config.exists():
            action.log(message_type="config_not_found", config_path=str(config))
            typer.echo(f"Error: Configuration file not found: {config}", err=True)
            raise typer.Exit(1)
        
        action.log(message_type="config_loaded", config_path=str(config))
        
        console.print(f"\n[bold cyan]In-silico Knockout Analysis for:[/bold cyan] [bold yellow]{gene_name}[/bold yellow]")
        console.print("[dim]" + "-" * 60 + "[/dim]")
        
        # Load insilico knockout agent
        print("Loading in-silico knockout agent...")
        
        # Import BaseAgentWithLogging from just_agents
        from just_agents.base_agent import BaseAgentWithLogging
        
        knockout_agent: BaseAgentWithLogging = BaseAgentWithLogging.from_yaml(
            section_name="insilico_knockout_agent",
            parent_section="agent_profiles",
            file_path=config
        )
        print("✓ Loaded insilico_knockout_agent")
        action.log(message_type="agent_loaded", agent="insilico_knockout_agent")
        
        # Generate the prompt
        prompt = get_insilico_knockout_prompt(
            gene_name=gene_name,
            gene_sentence=gene_sentence or "",
            sex=sex or "",
            tissue=tissue or "",
            cell_type=cell_type or "",
            smoking_status=smoking_status
        )
        
        # Log metadata if provided
        metadata = {}
        if gene_sentence:
            metadata["gene_sentence"] = gene_sentence
        if sex:
            metadata["sex"] = sex
        if tissue:
            metadata["tissue"] = tissue
        if cell_type:
            metadata["cell_type"] = cell_type
        if smoking_status is not None:
            metadata["smoking_status"] = smoking_status
        
        if metadata:
            action.log(message_type="metadata_provided", **metadata)
            console.print("\n[bold]Metadata provided:[/bold]")
            for key, value in metadata.items():
                console.print(f"  • {key}: {value}")
        
        console.print("\n[bold]Sending knockout analysis request...[/bold]")
        console.print("[yellow]Note: Age prediction requires GPU inference (may take 1-2 minutes)[/yellow]\n")
        
        result = knockout_agent.query(query_input=prompt)
        action.log(message_type="knockout_analysis_complete", gene_name=gene_name)
        
        # Save and validate results
        if result:
            result_str = str(result) if not isinstance(result, str) else result
            # Use gene name for filename
            safe_gene = gene_name.replace("/", "_").replace("\\", "_")
            filepath = save_result_to_markdown(result_str, f"insilico_knockout_{safe_gene}")
            action.log(message_type="result_saved", filepath=str(filepath))
            
            is_valid = validate_markdown_file(filepath)
            file_uri = filepath.resolve().as_uri()
            if is_valid:
                action.log(message_type="validation_success", filepath=str(filepath))
                typer.echo(f"\n✓ In-silico knockout analysis successfully saved and validated: {filepath}")
                typer.echo(f"  Open report: {file_uri}")
            else:
                action.log(message_type="validation_warning", filepath=str(filepath))
                typer.echo(f"\n⚠ In-silico knockout analysis saved but validation had issues: {filepath}")
                typer.echo(f"  Open report: {file_uri}")
        else:
            action.log(message_type="no_result", gene_name=gene_name)
            typer.echo("✗ No result returned from in-silico knockout agent", err=True)
            raise typer.Exit(1)
        
        # Display conversation history
        if show_history:
            print("\n" + "="*60)
            print("CONVERSATION HISTORY")
            print("="*60)
            if hasattr(knockout_agent, 'memory'):
                print(f"\n{knockout_agent.description if hasattr(knockout_agent, 'description') else 'In-silico Knockout Agent'}:")
                knockout_agent.memory.pretty_print_all_messages()
            # Repeat report link after history for convenience
            print(f"\nOpen report: {file_uri}")


def main() -> None:
    """Main entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()