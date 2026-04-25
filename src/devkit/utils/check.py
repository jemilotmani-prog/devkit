import shutil
from rich.console import Console

console = Console(stderr=True)

REQUIRED_TOOLS = {
    'gh': 'Install from https://cli.github.com',
    'fzf': 'winget install junegunn.fzf',
    'bat': 'winget install sharkdp.bat',
    'delta': 'winget install dandavison.delta',
}

def check_tools():
    missing = {t: hint for t, hint in REQUIRED_TOOLS.items() if not shutil.which(t)}
    if missing:
        console.print('[red]Missing required tools:[/red]')
        for tool, hint in missing.items():
            console.print(f'  [cyan]{tool}[/cyan] — {hint}')
        raise SystemExit(1)