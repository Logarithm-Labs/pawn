# SolanaAgenticWorkflow Template Prompt

Write a Workflow that implements an agentic graph using the langgraph-supervisor framework. This system should include four agents with the following responsibilities:

1. Swap Tokens – An agent that swaps tokens on Solana using the Jupiter aggregator plugin.
2. Transfer Tokens – An agent that sends and receives tokens on Solana using the SPL token plugin.
3. Mint NFT – An agent that mints NFTs on Solana using the Crossmint plugin.
4. Deposit Yield – An agent that deposits USDC for yield on Solana (placeholder functionality)

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

Extend the above base structure to implement the following agents with the specified responsibilities:

Agent 1: Swap Token Agent
  - Function: swap_tokens()
  - Responsibility: Swap tokens on Solana using GOAT tools and the Jupiter aggregator plugin.
  - Prompt: Describe its role as a token swapping expert.

Agent 2: Transfer Tokens Agent
  - Function: send_receive_tokens()
  - Responsibility: Send and receive tokens on Solana using GOAT tools and the SPL token plugin.
  - Prompt: Describe its role as a token transfer expert.

Agent 3: Mint NFT Agent
  - Function: mint_nft()
  - Responsibility: Mint NFTs on Solana using GOAT tools and the Crossmint plugin.
  - Prompt: Describe its role as an NFT minting expert.

Agent 4: Deposit Yield Agent
  - Function: deposit_usdc_yield()
  - Responsibility: Deposit USDC for yield on Solana using GOAT tools with a placeholder tool (to be replaced with actual logic later).
  - Prompt: Describe its role as an expert in USDC yield deposit.

Also, ensure that the supervisor is configured to integrate these four agents with a prompt that clearly delegates tasks for token swapping, token transferring, NFT minting, and yield deposit operations.

Your final output should be only the complete Python code for the Workflow that follows the above structure and incorporates the four agent functionalities as specified.
