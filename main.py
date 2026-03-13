import os
import argparse
from crewai import Crew, Process
from dotenv import load_dotenv

from tools import (
    validate_violity_url,
    parse_violity_lot,
    search_web,
    get_current_date,
    save_report,
    analyze_coin_images,
)

from helpers import (
    load_agents_config,
    load_task_config,
    build_agent,
    build_task,
)

# Load environment variables
load_dotenv()

# Verify API key
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")


def parse_args():
    parser = argparse.ArgumentParser(description="NumismAItic - auction coin lot evaluation")
    parser.add_argument(
        "--url",
        required=True,
        help="Auction lot URL to analyze",
    )
    parser.add_argument(
        "--output",
        default="report.md",
        help="Output report filename",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    url = args.url
    report_path = args.output

    # Load config
    agents_cfg = load_agents_config("config/agents.yaml")
    tasks_cfg = load_task_config("config/agent_task.yaml")

    # Сreate agents
    url_validator = build_agent(agents_cfg["url_validator"], tools=[validate_violity_url, search_web])

    data_retriever = build_agent(agents_cfg["data_retriever"], tools=[search_web, parse_violity_lot])

    appraiser = build_agent(agents_cfg["appraiser"], tools=[search_web, save_report, analyze_coin_images])

    history_researcher = build_agent(agents_cfg["history_researcher"], tools=[search_web])

    finansists = build_agent(agents_cfg["financial_analyst"], tools=[search_web, get_current_date])

    # Task creation
    validate_auction_task = build_task(
        task_config=tasks_cfg["validate_auction"], task_agent=url_validator, context_list=[]
    )

    retrieve_coins_lot = build_task(
        task_config=tasks_cfg["retrieve_coins_lot"], task_agent=data_retriever, context_list=[validate_auction_task]
    )

    estimation_task = build_task(
        task_config=tasks_cfg["estimation_task"], task_agent=appraiser, context_list=[retrieve_coins_lot]
    )

    sell_history = build_task(
        task_config=tasks_cfg["sell_history"],
        task_agent=history_researcher,
        context_list=[retrieve_coins_lot, estimation_task],
    )

    price_normalization = build_task(
        task_config=tasks_cfg["price_normalization"],
        task_agent=finansists,
        context_list=[retrieve_coins_lot, sell_history],
    )

    final_report = build_task(
        task_config=tasks_cfg["final_report"],
        task_agent=appraiser,
        context_list=[retrieve_coins_lot, estimation_task, sell_history, price_normalization],
    )

    # Create the crew
    crew = Crew(
        agents=[url_validator, data_retriever, appraiser, history_researcher, finansists],
        tasks=[
            validate_auction_task,
            retrieve_coins_lot,
            estimation_task,
            sell_history,
            price_normalization,
            final_report,
        ],
        process=Process.sequential,
        verbose=True,
        tracing=False,
        memory=False,
    )

    # Run the crew
    crew.kickoff(inputs={"url": url, "report_path": report_path})


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nRun aborted")
    except Exception as e:
        print(f"\nCritical error: {e}")
        import traceback

        traceback.print_exc()
