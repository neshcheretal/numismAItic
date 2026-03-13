import yaml
from pathlib import Path
from models import AgentConfig, TaskConfig
from typing import Optional, List, Dict
from crewai import Agent, Task


def load_agents_config(path: str | Path) -> Dict[str, AgentConfig]:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return {name: AgentConfig(**cfg) for name, cfg in raw.items()}


def load_task_config(path: str | Path) -> Dict[str, AgentConfig]:
    with open(path, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)

    return {name: TaskConfig(**cfg) for name, cfg in raw.items()}


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
