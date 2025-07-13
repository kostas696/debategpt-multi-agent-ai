from state.debate_state import DebateState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def print_debate_transcript(state: DebateState):
    """
    Nicely formats and prints the debate history using Rich markdown.
    """

    console.rule(f"[bold blue] Debate Topic: {state.topic} [/bold blue]")

    for i, message in enumerate(state.history):
        if isinstance(message, HumanMessage):
            role = "Human Prompt"
            color = "cyan"
        elif isinstance(message, AIMessage):
            role = "AI Response"
            color = "green"
        elif isinstance(message, SystemMessage):
            role = "System"
            color = "magenta"
        else:
            role = "Unknown"
            color = "white"

        console.print(f"[bold {color}]Turn {i+1} - {role}[/bold {color}]")
        console.print(Markdown(message.content))
        console.print()

    if state.verdict:
        console.rule("[bold red]Final Verdict[/bold red]")
        console.print(Markdown(state.verdict), style="bold yellow")

    if state.error:
        console.rule("[bold red]Error Encountered[/bold red]")
        console.print(state.error, style="bold red")