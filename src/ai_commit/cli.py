"""CLI entry point — three commands: msg, review, summary."""

from __future__ import annotations

import sys

import typer
from rich.console import Console

from ai_commit import git, llm, prompts

app = typer.Typer(
    name="ai-commit",
    help="AI-powered git commit messages, PR summaries & code review.",
    add_completion=False,
)
console = Console()


def _get_diff_or_exit(staged_only: bool) -> str:
    diff = git.get_staged_diff() if staged_only else git.get_diff()
    if not diff.strip():
        console.print(
            "[yellow]No diff found. Stage some changes first.[/yellow]"
        )
        raise typer.Exit(code=1)
    return diff


@app.command()
def msg(
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Print the prompt without calling the LLM."
    ),
    model: str = typer.Option(
        "gpt-4o-mini", "--model", "-m", help="OpenAI-compatible model name."
    ),
) -> None:
    """Generate a conventional commit message from the staged diff."""
    diff = _get_diff_or_exit(staged_only=True)
    prompt = prompts.build_commit_prompt(diff)

    if dry_run:
        console.print("[bold cyan]--- PROMPT (dry-run) ---[/bold cyan]")
        console.print(prompt)
        return

    console.print("[bold green]Generating commit message…[/bold green]")
    try:
        result = llm.call_llm(prompt, model=model)
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    console.print("\n[bold]Suggested commit message:[/bold]")
    console.print(result)


@app.command()
def review(
    base: str = typer.Option(
        "HEAD", "--base", "-b", help="Git ref to diff against."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Print the prompt without calling the LLM."
    ),
    model: str = typer.Option(
        "gpt-4o-mini", "--model", "-m", help="OpenAI-compatible model name."
    ),
) -> None:
    """Do a quick AI code review of the current diff."""
    diff = git.get_diff(base)
    if not diff.strip():
        console.print("[yellow]No diff found against base.[/yellow]")
        raise typer.Exit(code=1)

    prompt = prompts.build_review_prompt(diff)

    if dry_run:
        console.print("[bold cyan]--- PROMPT (dry-run) ---[/bold cyan]")
        console.print(prompt)
        return

    console.print("[bold green]Reviewing diff…[/bold green]")
    try:
        result = llm.call_llm(prompt, model=model)
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    console.print("\n[bold]Code review:[/bold]")
    console.print(result)


@app.command()
def summary(
    base: str = typer.Option(
        "HEAD", "--base", "-b", help="Git ref to diff against."
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", "-n", help="Print the prompt without calling the LLM."
    ),
    model: str = typer.Option(
        "gpt-4o-mini", "--model", "-m", help="OpenAI-compatible model name."
    ),
) -> None:
    """Summarise a diff or PR in bullet points."""
    diff = git.get_diff(base)
    if not diff.strip():
        console.print("[yellow]No diff found against base.[/yellow]")
        raise typer.Exit(code=1)

    prompt = prompts.build_summary_prompt(diff)

    if dry_run:
        console.print("[bold cyan]--- PROMPT (dry-run) ---[/bold cyan]")
        console.print(prompt)
        return

    console.print("[bold green]Summarising diff…[/bold green]")
    try:
        result = llm.call_llm(prompt, model=model)
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}", file=sys.stderr)
        raise typer.Exit(code=1) from exc

    console.print("\n[bold]Summary:[/bold]")
    console.print(result)


if __name__ == "__main__":
    app()
