# Precompiled Agents Workflows Network (P.A.W.N. ♟️)

Precompiled Agents Workflows Network is a multi-package project that provides prebuilt agent workflows for blockchain and crypto agents. PAWN workflows are implemented using [Langgraph Supervisor](https://github.com/langchain-ai/langgraph-supervisor-py), ensuring maximum composability for agent systems. PAWN also allows seamless integration with various agent frameworks, such as [GOAT](https://github.com/goat-sdk/goat/tree/main#%EF%B8%8F-supported-tools-and-frameworks).

---

## How to Install?

You can install the base package along with only the dependencies you need. For example:

- **Basic installation:**
```bash
pip install pawn-ai
```
- **Installation with a specific submodule (e.g., llamafeed_worflow):**
```bash
  pip install pawn-ai[llamafeed_worflow]
```
- **Installation with multiple submodules:**
```bash
  pip install pawn-ai[goat_evm_workflow,goat_solana_workflow]
```
The extras allow you to install only the dependencies relevant to the submodules you intend to use.

---

## Integration

PAWN offers several integration options for incorporating agent workflows into your system:

### 1. Integrating with an Existing Supervisor-Based System

If you already have a supervisor-based agent system, you can attach PAWN's precompiled workflows directly.
![Supervisor-based system with PAWN worflows](docs/sb.png)

For example:
```python
from pawn.llamafeed_workflow import LlamaFeedWorkflow

team1 = ...
team2 = LlamaFeedWorkflow()

custom_workflow = create_supervisor(
    agents=[team1, team2.workflow],
    model=model,
    prompt=(
        "You are a team supervisor managing three teams:"
        ...
    )
)
```
This approach allows you to seamlessly integrate PAWN's workflows as additional tools in your existing system. See more [here](https://github.com/langchain-ai/langgraph-supervisor-py?tab=readme-ov-file#multi-level-hierarchies).

---

### 2. Using the Workflow as a Tool (Agent as a Tool Pattern)

PAWN workflows can also be used as tools within your agent's framework. This approach follows the "agent as a tool" pattern described in the [LangGraph documentation](https://langchain-ai.github.io/langgraph/concepts/multi_agent/#supervisor-tool-calling).
![Workflow as a tool](docs/tool.png)
For example using [OpenAI Agents SDK](https://github.com/openai/openai-agents-python):

```python
import asyncio

from agents import Agent, Runner, function_tool
from pawn.hyperliquid_trader_workflow import HyperliquidWorkflow


@function_tool
def get_price(symbol: str) -> float:
    workflow: HyperliquidWorkflow = HyperliquidWorkflow()
    response = workflow.invoke(f'What is the price of {symbol}?')
    ...
    return result


agent = Agent(
    name="Price Fetcher",
    instructions="You are a helpful agent that can fetch price of crypto.",
    tools=[get_price],
)


async def main():
    result = await Runner.run(agent, input="What's the price of bitcoin?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

This integration leverages PAWN's workflows as modular tools that can be called by your agent system when needed.

---

### 3. Running the Workflow as a Standalone FastAPI or fastMCP Server

You can also run a PAWN workflow as an independent service using FastAPI (or a similar framework like fastMCP). This allows you to deploy the workflow as a RESTful API. For example, using FastAPI:
![Independent Service](docs/fast.png)

```python
from fastapi import FastAPI
from pawn.goat_evm_workflow import EVMAgenticWorkflow

app = FastAPI()
workflow = EVMAgenticWorkflow()

@app.post("/invoke")
def invoke_workflow(payload: dict):
    return workflow.invoke(payload)
```

This will launch a standalone server where you can access the workflow via HTTP.

---

## Contributing

Contributions are welcome! Please ensure that your changes are well-documented and include examples.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.
