import sys
from collections import deque

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)
from rich.prompt import Prompt

from extractors import extract
from parsers.get_tree import get_tree
from repository.load import load_source
from storage.retreiver import ask_repo, rewrite_query
from storage.vec_db import getCollection

console = Console()

HISTORY_LIMIT = 5


# Get repo and check if it already exits
def ingest_repo(url: str):
    with console.status("[bold green]Cloning repository...", spinner="dots"):
        repo, trees = get_tree(url)

    repo_name = repo.root.split("/")[-1]
    collection = getCollection(repo_name)

    if collection.count() > 0:
        console.print(
            f"[yellow]'{repo_name}' already indexed ({collection.count()} chunks). "
            f"Skipping ingestion.[/yellow]"
        )
        return repo_name

    files = list(repo.files.items())

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[green]Ingesting files...", total=len(files))

        for path, node in files:
            ids, documents, metadatas = [], [], []

            source = load_source(path, repo.root)
            tree = trees.get(path)
            node = extract(node, tree, source)

            for c in node.chunks:
                doc_id = f"{path}::{c.name}::{c.start_line}"
                ids.append(doc_id)
                documents.append(
                    f"File: {c.path}\n"
                    f"Type: {c.kind}\n"
                    f"Name: {c.name}\n\n"
                    f"Imports:\n{', '.join(node.imports or [])}\n\n"
                    f"Code:\n{c.content}"
                )
                metadatas.append(
                    {
                        "name": c.name,
                        "kind": c.kind,
                        "path": c.path,
                        "start_line": c.start_line,
                        "end_line": c.end_line,
                        "exported": c.exported,
                        "language": c.language,
                    }
                )

            if documents:
                collection.add(ids=ids, documents=documents, metadatas=metadatas)

            progress.advance(task)

    console.print(
        f"[green]✓ Indexed {collection.count()} chunks from {len(files)} files[/green]"
    )
    return repo_name


def format_history(history: deque) -> str:
    if not history:
        return ""
    lines = []
    for q, a in history:
        lines.append(f"User: {q}\nAssistant: {a}")
    return "\n\n".join(lines)


def chat_loop(repo_name: str):
    history: deque = deque(maxlen=HISTORY_LIMIT)

    console.print(
        Panel(
            f"[bold green]{repo_name}[/bold green] is ready.\n"
            "[dim]Ask anything about the codebase. Type [bold]exit[/bold] to quit.[/dim]",
            title="[bold]RepoScan[/bold]",
            border_style="green",
        )
    )

    while True:
        try:
            question = Prompt.ask("\n[bold cyan]You[/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        question = question.strip()

        if not question:
            continue

        if question.lower() in ("exit", "quit", "q"):
            console.print("[dim]Goodbye.[/dim]")
            break

        with console.status("[bold yellow]Thinking...", spinner="dots"):
            search_query = rewrite_query(question)
            answer = ask_repo(
                repo_name=repo_name,
                question=question,
                search_query=search_query,
                history=format_history(history),
            )

        if not answer:
            console.print("[red]No answer returned.[/red]")
            continue

        console.print("\n[bold magenta]Assistant[/bold magenta]")
        console.print(Panel(Markdown(answer), border_style="magenta", padding=(1, 2)))

        history.append((question, answer))


def main():
    console.print(
        Panel(
            "[bold]RepoScan[/bold]\n"
            "[dim]Local AI-powered repository explorer · Ollama + ChromaDB[/dim]",
            border_style="blue",
            padding=(1, 4),
        )
    )

    url = Prompt.ask("[bold cyan]GitHub Repository URL[/bold cyan]")

    if not url.strip():
        console.print("[red]No URL provided. Exiting.[/red]")
        sys.exit(1)

    try:
        repo_name = ingest_repo(url.strip())
        chat_loop(repo_name)
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted.[/dim]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise


if __name__ == "__main__":
    main()
