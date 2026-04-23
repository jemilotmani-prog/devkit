import subprocess
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from devkit.utils.gh import gh, gh_json

app = typer.Typer()
console = Console()


@app.command()
def explain(
    command: str = typer.Argument(..., help='Shell command to explain'),
):
    """Ask Copilot CLI to explain a shell command."""
    result = subprocess.run(
        ['gh', 'copilot', '-p', f'explain this command: {command}'],
        capture_output=True, text=True
    )
    console.print(Panel(
        result.stdout or result.stderr,
        title='[purple]Copilot Explanation[/purple]',
        border_style='purple'
    ))


@app.command()
def suggest(
    task: str = typer.Argument(..., help='Task to accomplish'),
):
    """Ask Copilot CLI to suggest a command."""
    result = subprocess.run(
        ['gh', 'copilot', '-p', task],
        capture_output=True, text=True
    )
    console.print(Panel(
        result.stdout or result.stderr,
        title='[purple]Copilot Suggestion[/purple]',
        border_style='purple'
    ))


@app.command()
def review(
    pr_number: int = typer.Argument(..., help='PR number to review'),
):
    """AI-powered code review of a pull request."""
    with Progress(SpinnerColumn(), TextColumn('{task.description}')) as progress:
        t = progress.add_task('Fetching PR diff...')
        diff = gh('pr', 'diff', str(pr_number))
        pr_info = gh_json('pr', 'view', str(pr_number), '--json', 'title,body')

        progress.update(t, description='Running AI review...')
        prompt = f'Review this PR titled "{pr_info["title"]}":\n\n{diff[:4000]}'

        result = subprocess.run(
            ['gh', 'copilot', '-p', prompt],
            capture_output=True, text=True
        )

    console.print(Panel(
        result.stdout or result.stderr,
        title=f'[cyan]AI Review — PR #{pr_number}[/cyan]',
        border_style='cyan'
    ))


@app.command()
def commit():
    """Generate a commit message from staged changes using AI."""
    diff = subprocess.check_output(['git', 'diff', '--staged'], text=True)

    if not diff.strip():
        console.print('[yellow]No staged changes.[/yellow]')
        raise typer.Exit()

    prompt = f'Write a conventional commit message for these staged changes:\n\n{diff[:3000]}'
    result = subprocess.run(
        ['gh', 'copilot', '-p', prompt],
        capture_output=True, text=True
    )

    suggested = result.stdout.strip()
    console.print(Panel(suggested, title='[green]Suggested Commit Message[/green]'))

    use_it = Confirm.ask('Use this message?')
    if use_it:
        message = Prompt.ask('Edit if needed', default=suggested)
        subprocess.run(['git', 'commit', '-m', message])
    else:
        manual = Prompt.ask('Enter your message')
        subprocess.run(['git', 'commit', '-m', manual])