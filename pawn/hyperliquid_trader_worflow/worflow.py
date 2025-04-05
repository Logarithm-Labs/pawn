from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

from pawn.agentic_worlflow import AgenticWorkflow
from pawn.hyperliquid_trader_worflow.tools import GetCryptoPriceUSD, GetHyperliquidKlines


class HyperliquidWorkflow(AgenticWorkflow):

    def __init__(self, openai_model: str = "gpt-4o"):
        self._openai_model = openai_model
        super().__init__()

    def _load_env(self):
        pass

    def _compile(self):
        # Initialize LlamaFeed client to fetch crypto events.
        model = ChatOpenAI(model=self._openai_model)

        market_data_fetcher = create_react_agent(
            model=model,
            tools=[GetCryptoPriceUSD(), GetHyperliquidKlines()],
            name="market_data_fetcher",
            prompt=(
                "You are a market data expert. You can use the first tool to fetch the current price of any cryptocurrency in USD "
                "and the second tool to fetch 1h klines for a given symbol. "
            )
        )

        # Agent 2: Hacks Agent - Retrieves hack events.
        def make_trade(symbol: str, amount: float):
            """Make a trade on the Hyperliquid exchange."""
            # mocked
            print(f"Making trade: {symbol} for {amount} units.")

        trader = create_react_agent(
            model=model,
            tools=[make_trade],
            name="trader",
            prompt="You are trader on Hyperliquid that can execute trades."
        )

        # Create supervisor workflow with the three agents.
        workflow = create_supervisor(
            agents=[trader, market_data_fetcher],
            model=model,
            prompt=(
                "You are a team supervisor managing 2 experts: "
                "for data fetching requests use market_data_fetcher "
                "for trading requests use trader "
            )
        )
        self.workflow = workflow
        self.app = workflow.compile()
