from just_agents.just_bus import JustLogBus
from just_agents.base_agent import BaseAgent
from just_agents.base_memory import BaseMemory
from just_agents.just_locator import JustAgentsLocator
from typing import Optional
from pathlib import Path
from datetime import datetime
from longevity_forest.core.helpers import serialize_memory_to_yaml, serialize_content
from just_agents.data_classes import Message



def call_expert_agent(agent_name: str, user_query: str, agent_codename: Optional[str] = None, call_the_first_instance: bool = True) -> str:
    """
    Call the expert agent with the given name.

    Args:
        agent_name: The name of the agent to call
        user_query: The query to pass to the agent
        agent_codename: The unique codename of the agent instance to select if multiple instances of the same agent are found
        call_the_first_instance: Whether to call the first instance of the agent, true by default
        
    Returns:
        The response from the agent or the error message
    """
    locator = JustAgentsLocator()
    log_bus = JustLogBus()

    agents = locator.get_agents_by_shortname(agent_name, bounding_class=BaseAgent)
    if not agents:
        return f"Agent with shortname {agent_name} not found"
    
    agent = agents[0]

    if len(agents) > 1 and not call_the_first_instance:
        codenames = locator.get_codenames_by_shortname(agent_name, bounding_class=BaseAgent)
        log_bus.debug(f"Multiple agents with shortname {agent_name} found",
                        source="call_expert_agent",
                        action="agent_locator.get_agents_by_shortname",
                        codenames=codenames,
                        agent_name=agent_name,
                        call_the_first_instance=call_the_first_instance,
                        agent_codename=agent_codename)

        if agent_codename is None:
            return f"Multiple agents with shortname {agent_name} found, codenames: {str(codenames)}"
        
        if agent_codename not in codenames:
            return f"Agent with codename {agent_codename} not found, existing codenames: {str(codenames)}"
        
        agent = locator.get_agent_by_codename(agent_codename)
    
    response = agent.query(user_query)
    memory: BaseMemory = agent.memory
    memory.pretty_print_message(memory.last_message)
    
    # Serialize memory to YAML with query
    serialize_memory_to_yaml(agent_name, user_query, memory)
    serialize_content(agent_name, user_query, response)

    return f"Agent {agent_name} response: {response}"


def write_md_result(content: str) -> str:
    """Save markdown report to results directory.
    
    Args:
        content: Markdown content to save
    
    Returns:
        Success/failure message with file path
    """
    try:
        output_dir = Path("data/output")
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"report_{timestamp}.md"
        filepath.write_text(content, encoding="utf-8")
        file_uri = filepath.resolve().as_uri()
        return f"✓ Report saved: {filepath}\n  Open report: {file_uri}"
    except Exception as e:
        return f"✗ Failed to save: {str(e)}"




def grep_cache_full(search_term: str) -> list[dict[str, str]]:
    """Search cached result files for a search term and return filename, query, and result.
    
    Args:
        search_term: Term to search for in result files (case-insensitive)
    
    Returns:
        List of dictionaries with 'filename', 'query', and 'result' fields
    """
    results = []
    interim_dir = Path("data/interim")
    
    if not interim_dir.exists():
        return results
    
    # Find all _result.txt files
    result_files = list(interim_dir.glob("*_result.txt"))
    
    for filepath in result_files:
        try:
            content = filepath.read_text(encoding="utf-8")
            
            # Case-insensitive search
            if search_term.lower() not in content.lower():
                continue
            
            # Extract query and result sections
            query = ""
            result = ""
            
            if "============ Agent query ==============" in content:
                lines = content.split("\n")
                in_query_section = False
                in_result_section = False
                query_lines = []
                result_lines = []
                
                for line in lines:
                    if "============ Agent query ==============" in line:
                        in_query_section = True
                        in_result_section = False
                        continue
                    elif "============ Result ==============" in line:
                        in_query_section = False
                        in_result_section = True
                        continue
                    
                    if in_query_section:
                        query_lines.append(line)
                    elif in_result_section:
                        result_lines.append(line)
                
                query = "\n".join(query_lines).strip()
                result = "\n".join(result_lines).strip()
            
            results.append({
                "filename": filepath.name,
                "query": query,
                "result": result
            })
            
        except Exception as e:
            # Skip files that can't be read
            continue
    
    return results

def grep_cache_only_queries(search_term: str) -> list[dict[str, str]]:
    """Search cached result files for a search term and return filename and query.
    
    Args:
        search_term: Term to search for in result files (case-insensitive)
    
    Returns:
        List of dictionaries with 'filename' and 'query' fields
    """
    print(f"[DEBUG] grep_cache_only_queries called with search_term: {search_term}")
    full_results = grep_cache_full(search_term)
    print(f"[DEBUG] grep_cache_full returned {len(full_results)} results")
    # Remove 'result' field and keep only 'filename' and 'query'
    results = []
    for item in full_results:
        if item["query"] is not None:
            item.pop("result", None)
            results.append(item)
    print(f"[DEBUG] Filtered to {len(results)} results with non-None queries")
    print(f"[DEBUG] grep_cache_only_queries returning: {results}")
    return results

def read_results_by_filenames(filenames: list[str]) -> str:
    """Read result from a file by filename.
    
    Args:
        filename: Name of the file to read
    
    Returns:
        Content of the file
    """
    print(f"[DEBUG] read_results_by_filenames called with {len(filenames)} filenames")
    print(f"[DEBUG] Filenames: {filenames}")
    contents = []
    for filename in filenames:
        filepath = Path("data/interim") / filename
        print(f"[DEBUG] Checking filepath: {filepath}")
        if not filepath.exists():
            print(f"[DEBUG] File does not exist: {filepath}")
            continue
        print(f"[DEBUG] Reading file: {filepath}")
        contents.append(filepath.read_text(encoding="utf-8"))
    print(f"[DEBUG] Successfully read {len(contents)} files")
    result = "\n".join(contents)
    print(f"[DEBUG] read_results_by_filenames returning {len(result)} characters")
    return result








