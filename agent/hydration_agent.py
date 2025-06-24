from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq
from agent.tools import get_tools

def run_agent(user_input: str, api_key: str, goal_ml: int) -> str:
    """
    Executes a hydration assistant agent using LangChain + Groq LLaMA model.

    Parameters:
    - user_input: The question asked by the user.
    - api_key: Groq API key for LLaMA model access.
    - goal_ml: User's daily hydration goal to personalize response.

    Returns:
    - A string response from the agent.
    """
    try:
        # Initialize the LLM with Groq
        llm = ChatGroq(api_key=api_key, model_name="llama3-70b-8192")

        # Load hydration tools with goal
        tools = get_tools(goal_ml)

        # Initialize the LangChain agent
        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

        # Run the agent with the user's question
        return agent.run(user_input)

    except Exception as e:
        return f"[Agent Error] {str(e)}"
