from datetime import datetime
from pathlib import Path
import yaml
from just_agents.base_memory import BaseMemory

def save_result_to_markdown(result: str, gene_name: str) -> Path:
    """Save query result to a markdown file.
    
    Args:
        result: The query result string
        gene_name: The gene name for naming the file
        
    Returns:
        Path to the saved markdown file
    """
    output_dir = Path("data/output")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{gene_name}_{timestamp}.md"
    filepath = output_dir / filename
    
    filepath.write_text(result, encoding="utf-8")
    file_uri = filepath.resolve().as_uri()
    print(f"✓ Query result saved to: {filepath}")
    print(f"  Open report: {file_uri}")
    
    return filepath


def serialize_memory_to_yaml(agent_name: str, user_query: str, memory: BaseMemory) -> Path:
    """Serialize agent memory to a YAML file in results/interim folder.
    
    Args:
        agent_name: Name of the agent
        user_query: The query sent to the agent
        memory: The BaseMemory object to serialize
        
    Returns:
        Path to the saved YAML file
    """
    output_dir = Path("data/interim")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent_name}_{timestamp}.yaml"
    filepath = output_dir / filename
    
    # Serialize memory using Pydantic 2+ method
    memory_data = memory.model_dump()
    
    # Create the data structure with query and memory
    data: dict = {
        "agent_name": agent_name,
        "timestamp": datetime.now().isoformat(),
        "query": user_query,
        "memory": memory_data,
    }
    
    # Write to YAML
    filepath.write_text(yaml.dump(data, default_flow_style=False), encoding="utf-8")
    print(f"✓ Memory serialized to: {filepath}")
    
    return filepath

def serialize_content(agent_name: str, user_query: str, content: str) -> Path:
    """Serialize agent memory to a YAML file in results/interim folder.
    
    Args:
        agent_name: Name of the agent
        user_query: The query sent to the agent
        content: The content to serialize
        
    Returns:
        Path to the saved YAML file
    """
    output_dir = Path("data/interim")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{agent_name}_{timestamp}_result.txt"
    filepath = output_dir / filename
    
    filepath.write_text("============ Agent query ==============\n"+user_query+"\n============ Result ==============\n"+content, encoding="utf-8")
    print(f"✓ Content serialized to: {filepath}")
    
    return filepath


def validate_markdown_file(filepath: Path) -> bool:
    """Validate markdown file structure and syntax.
    
    Args:
        filepath: Path to the markdown file to validate
        
    Returns:
        True if valid, False otherwise
    """
    try:
        content = filepath.read_text(encoding="utf-8")
        
        # Check basic structure
        if not content.strip():
            print("✗ Validation failed: File is empty")
            return False
        
        # Check for common markdown elements
        has_headers: bool = "#" in content
        has_links: bool = "[" in content and "]" in content
        has_code_blocks: bool = "```" in content
        
        # Check for balanced markdown syntax
        validation_issues: list[str] = []
        
        # Check balanced brackets
        if "[" in content:
            open_brackets = content.count("[")
            close_brackets = content.count("]")
            if open_brackets != close_brackets:
                validation_issues.append(f"Unbalanced brackets: {open_brackets} [ vs {close_brackets} ]")
        
        # Check balanced code blocks
        code_block_count = content.count("```")
        if code_block_count % 2 != 0:
            validation_issues.append(f"Unbalanced code blocks: {code_block_count} (should be even)")
        
        # Report findings
        print("\n📋 Markdown Validation Report:")
        print(f"   ✓ File size: {len(content)} characters")
        print(f"   {'✓' if has_headers else '⚠'} Headers detected: {has_headers}")
        print(f"   {'✓' if has_links else '⚠'} Links/references detected: {has_links}")
        print(f"   {'✓' if has_code_blocks else '⚠'} Code blocks detected: {has_code_blocks}")
        
        if validation_issues:
            print("\n   ⚠ Issues found:")
            for issue in validation_issues:
                print(f"      - {issue}")
            return False
        else:
            print("\n   ✓ All syntax checks passed!")
            return True
            
    except Exception as e:
        print(f"✗ Validation error: {e}")
        return False
