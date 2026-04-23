import typer
from rich.console import Console
from rich.table import Table
from devkit.utils.gh import gh, gh_json

app = typer.Typer()
console = Console()


@app.command()
def issues(
    repo: str = typer.Option('', help='owner/repo (default: current repo)'),
    limit: int = typer.Option(15, help='Max number of issues'),
):
    """List open issues in a rich table."""
    args = ['issue', 'list', '--json', 'number,title,state,labels', '--limit', str(limit)]
    if repo:
        args += ['--repo', repo]
    data = gh_json(*args)

    table = Table(title='Open Issues', border_style='green')
    table.add_column('#', style='cyan', width=6)
    table.add_column('Title', min_width=30)
    table.add_column('Labels', width=20)

    for issue in data:
        labels = ', '.join(l['name'] for l in issue.get('labels', []))
        table.add_row(str(issue['number']), issue['title'], labels or '—')

    console.print(table)


@app.command()
def pr_summary(
    pr_number: int = typer.Argument(..., help='PR number to summarize'),
    repo: str = typer.Option('', help='owner/repo (default: current repo)'),
):
    """Show a PR title, body and changed files."""
    args = ['pr', 'view', str(pr_number), '--json', 'title,body,files']
    if repo:
        args += ['--repo', repo]
    data = gh_json(*args)

    console.print(f"\n[bold cyan]PR — {data['title']}[/bold cyan]\n")
    console.print(data.get('body') or '[dim]No description.[/dim]')

    table = Table(title='Changed Files', border_style='cyan')
    table.add_column('File', min_width=40)
    table.add_column('Additions', style='green', width=10)
    table.add_column('Deletions', style='red', width=10)

    for f in data.get('files', []):
        table.add_row(f['path'], str(f.get('additions', 0)), str(f.get('deletions', 0)))

    console.print(table)


@app.command()
def start_feature(
    name: str = typer.Argument(..., help='Feature name (kebab-case)'),
):
    """Create a new feature branch."""
    import subprocess
    branch = f'feature/{name}'
    subprocess.run(['git', 'checkout', '-b', branch], check=True)
    console.print(f'[green]✓[/green] Created branch: {branch}')


@app.command()
def open_pr(
    title: str = typer.Option(..., prompt=True, help='PR title'),
    body: str = typer.Option('', help='PR body'),
):
    """Create a pull request interactively."""
    url = gh('pr', 'create', '--title', title, '--body', body)
    console.print(f'[green]✓[/green] PR created: {url}')


@app.command()
def run_status(
    repo: str = typer.Option('', help='owner/repo (default: current repo)'),
):
    """Show latest CI run status per branch."""
    args = ['run', 'list', '--json', 'name,status,conclusion,headBranch', '--limit', '10']
    if repo:
        args += ['--repo', repo]
    data = gh_json(*args)

    table = Table(title='CI Runs', border_style='yellow')
    table.add_column('Branch', min_width=25)
    table.add_column('Name', min_width=20)
    table.add_column('Status', width=12)
    table.add_column('Result', width=12)

    for run in data:
        conclusion = run.get('conclusion') or '...'
        color = 'green' if conclusion == 'success' else 'red' if conclusion == 'failure' else 'yellow'
        table.add_row(
            run['headBranch'],
            run['name'],
            run['status'],
            f'[{color}]{conclusion}[/{color}]'
        )

    console.print(table)