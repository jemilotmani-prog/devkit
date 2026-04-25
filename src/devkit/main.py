import typer
from rich.console import Console
from rich.panel import Panel
from devkit.commands import github, ai, workflow
from devkit.utils.check import check_tools

app = typer.Typer(
    name='devkit',
    help='AI-powered developer toolkit',
    rich_markup_mode='rich',
)

console = Console()

# Register sub-apps
app.add_typer(github.app, name='gh', help='GitHub operations')
app.add_typer(ai.app, name='ai', help='AI tools (Copilot)')
app.add_typer(workflow.app, name='workflow', help='End-to-end dev workflows')

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    check_tools() 
    if ctx.invoked_subcommand is None:
        console.print(Panel(
            'Welcome to [bold cyan]devkit[/bold cyan] — AI-powered developer toolkit',
            border_style='cyan'
        ))
        console.print(ctx.get_help())

if __name__ == '__main__':
    app()