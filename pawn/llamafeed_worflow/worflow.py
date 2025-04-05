from datetime import datetime

from langchain_openai import ChatOpenAI
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

from pawn.agentic_worlflow import AgenticWorkflow
from pawn.llamafeed_worflow.llamafeed import LlamaFeed


class LlamaFeedWorkflow(AgenticWorkflow):

    def __init__(self, openai_model: str = "gpt-4o"):
        self._openai_model = openai_model
        super().__init__()

    def _load_env(self):
        pass

    def _compile(self):
        # Initialize LlamaFeed client to fetch crypto events.
        client = LlamaFeed()
        model = ChatOpenAI(model=self._openai_model)

        # Agent 1: NewsReader Agent - Groups news and tweets tools.
        def get_news(since_datetime: datetime):
            """Retrieve crypto news since the given datetime."""
            since_timestamp = since_datetime.timestamp()
            return client.get_news(since_timestamp=since_timestamp)

        def get_tweets(since_datetime: datetime):
            """Retrieve crypto tweets since the given datetime."""
            since_timestamp = since_datetime.timestamp()
            return client.get_tweets(since_timestamp=since_timestamp)

        news_reader_agent = create_react_agent(
            model=model,
            tools=[get_news, get_tweets],
            name="newsreader_expert",
            prompt=(
                "You are a newsreader expert. Use the first tool to fetch crypto news and "
                "the second tool to fetch crypto tweets."
            )
        )

        # Agent 2: Hacks Agent - Retrieves hack events.
        def get_hacks(since_datetime: datetime):
            """Retrieve crypto hack events since the given datetime."""
            since_timestamp = since_datetime.timestamp()
            return client.get_hacks(since_timestamp=since_timestamp)

        hacks_agent = create_react_agent(
            model=model,
            tools=[get_hacks],
            name="hacks_expert",
            prompt="You are a security analyst. Use the get_hacks tool to fetch recent crypto hack events."
        )

        # Agent 3: Finance Agent - Groups unlocks and raises tools.
        def get_unlocks(since_datetime: datetime):
            """Retrieve crypto unlock events since the given datetime."""
            since_timestamp = since_datetime.timestamp()
            return client.get_unlocks(since_timestamp=since_timestamp)

        def get_raises(since_datetime: datetime):
            """Retrieve crypto raise events since the given datetime."""
            since_timestamp = since_datetime.timestamp()
            return client.get_raises(since_timestamp=since_timestamp)

        finance_agent = create_react_agent(
            model=model,
            tools=[get_unlocks, get_raises],
            name="finance_expert",
            prompt=(
                "You are a financial expert. Use the first tool to fetch unlock events and "
                "the second tool to fetch raise events."
            )
        )

        # Create supervisor workflow with the three agents.
        workflow = create_supervisor(
            agents=[news_reader_agent, hacks_agent, finance_agent],
            model=model,
            prompt=(
                "You are a team supervisor managing three experts: "
                "for news and tweets, use newsreader_expert; "
                "for hack events, use hacks_expert; "
                "for financial events (unlocks and raises), use finance_expert."
            )
        )
        self.workflow = workflow
        self.app = workflow.compile()
