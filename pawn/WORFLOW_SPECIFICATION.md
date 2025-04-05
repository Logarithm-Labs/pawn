# {Worflow} Template Prompt

Write an Worflow that implements an agentic graph using the langgraph-supervisor framework. This system should include three agents with the following responsibilities:

1. Task 1 (Example: Swap Tokens: An agent that swaps tokens on EVM chains.)
2. Task 2 (Example: Mint NFT: An agent that mints NFTs on EVM chains.)
3. Task 3 (Example: Transfer Tokens: An agent that handles token transfers on EVM chains.)

Rules:
- For tools, use GOAT tools (e.g., get_on_chain_tools).
- For creating the workflow, use langgraph_supervisor (e.g., create_supervisor).
- Use the base workflow structure as a base class and refer to the provided code for the expected format.

Below is the base workflow structure (do not change this structure):

--------------------------------------------------
import os
# other imports

class AgenticWorkflow:
    """
    A class to represent the agentic workflow based on langgraph supervisor library.
    """
    def __init__(self):
        """
        Initialize the workflow with agents
        """
        self._load_env()
        self._compile()

    def _load_env(self):
        """
        Internal function to load and initialize all environment variables, clients,
        accounts, and models.
        Example:

        def _load_env(self):
            import os

            load_dotenv()
            self.RPC_PROVIDER_URL = os.getenv("RPC_PROVIDER_URL")
            self.WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
            self.CROSSMINT_API_KEY = os.getenv("CROSSMINT_API_KEY")
            self.UNISWAP_API_KEY = os.getenv("UNISWAP_API_KEY")
        """
        raise NotImplementedError

    def _compile(self):
        """
        1. Define Model 
        2. Build all tools
        3. Create agents
        4. Create supervisor
        5. Compile the workflow

        Example:
        model = ChatOpenAI(model="gpt-4o")

        # Define NFT minting agent
        def mint_nft():
            """Mint NFT"""
            crossmint_factory = crossmint(self.CROSSMINT_API_KEY)
            tools = get_on_chain_tools(wallet=Web3EVMWalletClient(w3), plugins=[crossmint_factory["mint"]()])
            return tools

        nft_minting_agent = create_react_agent(
            model=model,
            tools=[mint_nft],
            name="nft_minting_expert",
            prompt="You are an NFT minting expert. Use the mint_nft tool to mint NFTs."
        )

        # Define token swapping agent
        def swap_tokens():
            """Swap tokens"""
            uniswap_api_key = self.UNISWAP_API_KEY
            uniswap_base_url = self.UNISWAP_BASE_URL or "https://trade-api.gateway.uniswap.org/v1"
            tools = get_on_chain_tools(
                wallet=Web3EVMWalletClient(w3),
                plugins=[
                    uniswap(options=UniswapPluginOptions(
                        api_key=uniswap_api_key,
                        base_url=uniswap_base_url
                    )),
                ],
            )
            return tools

        token_swapping_agent = create_react_agent(
            model=model,
            tools=[swap_tokens],
            name="token_swapping_expert",
            prompt="You are a token swapping expert. Use the swap_tokens tool to swap tokens."
        )

        # Create supervisor workflow
        workflow = create_supervisor(
            [nft_minting_agent, token_swapping_agent],
            model=model,
            prompt=(
                "You are a team supervisor managing an NFT minting expert and a token swapping expert. "
                "For NFT minting tasks, use nft_minting_agent. "
                "For token swapping tasks, use token_swapping_agent."
            )
        )
        self.workflow = workflow
        self.app = workflow.compile()
        """
        raise NotImplementedError

    def invoke(self, input_data):
        """
        Invoke the workflow with input data.
        """
        return self.app.invoke({
            "messages": [
                {
                    "role": "user",
                    "content": input_data
                }
            ]
        })
--------------------------------------------------

In your generated code, extend this base structure to implement the following agents:

Also, ensure that the supervisor is configured to integrate these three agents with a prompt that clearly delegates tasks.

Your final output should be only the complete Python code for Worflow that follows the above structure and incorporates the three agent functionalities as specified.
