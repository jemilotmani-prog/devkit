import subprocess
import typer
from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule
from devkit.utils.gh import gh, gh_json

app = typer.Typer()
console = Console()


@app.command('feature-start')
def feature_start(
    name: str = typer.Argument(..., help='Feature name (kebab-case)'),
    issue: int = typer.Option(None, help='Issue number to link'),
):
    """Start a new feature: branch + draft PR + AI scaffold."""
    console.print(Rule('[bold]Starting Feature[/bold]'))

    # 1. Créer la branche
    branch = f'feature/{name}'
    subprocess.run(['git', 'checkout', '-b', branch], check=True)
    console.print(f'[green]✓[/green] Created branch: {branch}')

    # 2. Pusher la branche
    subprocess.run(['git', 'push', '-u', 'origin', branch], check=True)
    console.print(f'[green]✓[/green] Branch pushed to origin')

    # 3. Créer le PR (sans --draft car branche vide)
    pr_title = name.replace('-', ' ').title()
    body = f'Closes #{issue}' if issue else 'Work in progress'
    try:
        pr_url = gh('pr', 'create', '--title', pr_title, '--body', body)
        console.print(f'[green]✓[/green] PR created: {pr_url}')
    except Exception:
        console.print(f'[yellow]⚠[/yellow] PR creation skipped — push commits first')

    # 4. AI scaffold si issue fournie
    if issue:
        issue_data = gh_json('issue', 'view', str(issue), '--json', 'title,body')
        prompt = f'Je commence à travailler sur: {issue_data["title"]}\nSuggère un plan étape par étape.'
        result = subprocess.run(
            ['gh', 'copilot', '-p', prompt],
            capture_output=True, text=True
        )
        console.print(Panel(
            result.stdout or result.stderr,
            title='[cyan]AI Implementation Plan[/cyan]',
            border_style='cyan'
        ))

    console.print(Rule('[green]Ready to code![/green]'))