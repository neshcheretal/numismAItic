import yaml
from pathlib import Path
from models import AgentConfig, TaskConfig, SearchConfig
from typing import Optional, List, Dict, Any
from crewai import Agent, Task



def read_yaml_mapping(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if data is None:
        return {}

    if not isinstance(data, dict):
        raise ValueError(f"Expected top-level YAML mapping in {path}")

    return data

def load_agents_config(path: str | Path) -> Dict[str, AgentConfig]:
    raw = read_yaml_mapping(path)
    return {name: AgentConfig(**cfg) for name, cfg in raw.items()}


def load_task_config(path: str | Path) -> Dict[str, TaskConfig]:
    raw = read_yaml_mapping(path)
    return {name: TaskConfig(**cfg) for name, cfg in raw.items()}


def load_main_config(path: str | Path) -> SearchConfig:
    raw = read_yaml_mapping(path)
    return SearchConfig(**raw["sell_history_search"])




def build_agent(agent_config: AgentConfig, tools: List):
    return Agent(
        role=agent_config.role,
        goal=agent_config.goal,
        backstory=agent_config.backstory,
        tools=tools,
        verbose=agent_config.verbose,
        allow_delegation=agent_config.allow_delegation,
        llm=agent_config.llm,
    )


def build_task(task_config: TaskConfig, task_agent: Agent, context_list: List[Task]):
    return Task(
        description=task_config.description,
        expected_output=task_config.expected_output,
        agent=task_agent,
        context=context_list,
    )
