#!/usr/bin/env python3
"""
CLI interface for the Lost Pet Identifier system.
"""

import click
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from lost_pet_identifier import LostPetIdentifier

console = Console()


@click.group()
@click.option(
    '--db-path',
    default='./data/faiss_index',
    help='Path to vector database index'
)
@click.option(
    '--ollama-url',
    default='http://localhost:11434',
    help='Ollama API base URL'
)
@click.option(
    '--ollama-model',
    default='llama2',
    help='Ollama model name'
)
@click.pass_context
def cli(ctx, db_path, ollama_url, ollama_model):
    """Lost Pet Identifier - Multimodal AI System for Pet Recovery."""
    ctx.ensure_object(dict)
    ctx.obj['db_path'] = db_path
    ctx.obj['ollama_url'] = ollama_url
    ctx.obj['ollama_model'] = ollama_model
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else '.', exist_ok=True)


@cli.command()
@click.option('--image', '-i', type=click.Path(exists=True), help='Path to pet image')
@click.option('--description', '-d', type=str, help='Text description of the pet')
@click.option('--location', '-l', type=str, help='Location where pet was found')
@click.option('--date', type=str, help='Date when pet was found')
@click.pass_context
def add_found(ctx, image, description, location, date):
    """Add a found pet to the database."""
    if not image and not description:
        console.print("[red]Error: At least one of --image or --description is required[/red]")
        return
    
    console.print("[cyan]Initializing Lost Pet Identifier...[/cyan]")
    identifier = LostPetIdentifier(
        vector_db_path=ctx.obj['db_path'],
        ollama_url=ctx.obj['ollama_url'],
        ollama_model=ctx.obj['ollama_model']
    )
    
    console.print("[cyan]Processing found pet...[/cyan]")
    try:
        idx = identifier.add_found_pet(
            image_path=image,
            description=description,
            location=location,
            date=date
        )
        console.print(f"[green]Successfully added found pet (index: {idx})[/green]")
        console.print(f"[dim]Database now contains {identifier.get_database_size()} pets[/dim]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


@cli.command()
@click.option('--image', '-i', type=click.Path(exists=True), help='Path to lost pet image')
@click.option('--description', '-d', type=str, help='Text description of the lost pet')
@click.option('--top-k', '-k', default=5, type=int, help='Number of top results to return')
@click.pass_context
def search(ctx, image, description, top_k):
    """Search for a lost pet in the database."""
    if not image and not description:
        console.print("[red]Error: At least one of --image or --description is required[/red]")
        return
    
    console.print("[cyan]Initializing Lost Pet Identifier...[/cyan]")
    identifier = LostPetIdentifier(
        vector_db_path=ctx.obj['db_path'],
        ollama_url=ctx.obj['ollama_url'],
        ollama_model=ctx.obj['ollama_model']
    )
    
    if identifier.get_database_size() == 0:
        console.print("[yellow]Warning: Database is empty. Add some found pets first.[/yellow]")
        return
    
    console.print("[cyan]Searching for matches...[/cyan]")
    try:
        results_dict = identifier.search_lost_pet(
            image_path=image,
            description=description,
            k=top_k,
            include_explanation=True
        )
        
        results = results_dict['results']
        explanation = results_dict.get('explanation')
        
        if not results:
            console.print("[yellow]No matches found.[/yellow]")
            return
        
        # Display results
        console.print("\n[bold cyan]Search Results:[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Rank", style="dim", width=6)
        table.add_column("Similarity", justify="right", width=10)
        table.add_column("Description", width=40)
        table.add_column("Location", width=20)
        table.add_column("Image", width=30)
        
        for i, result in enumerate(results, 1):
            similarity = result['similarity_score']
            desc = result.get('description', 'No description')[:40]
            location = result.get('location', 'N/A')[:20]
            img_path = result.get('image_path', 'N/A')
            if img_path and len(img_path) > 30:
                img_path = "..." + img_path[-27:]
            
            # Color code similarity
            if similarity > 0.7:
                sim_color = "green"
            elif similarity > 0.5:
                sim_color = "yellow"
            else:
                sim_color = "red"
            
            table.add_row(
                str(i),
                f"[{sim_color}]{similarity:.3f}[/{sim_color}]",
                desc,
                location,
                img_path
            )
        
        console.print(table)
        
        # Display explanation
        if explanation:
            console.print("\n[bold cyan]Explanation:[/bold cyan]")
            console.print(Panel(explanation, border_style="blue"))
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise


@cli.command()
@click.pass_context
def stats(ctx):
    """Show database statistics."""
    identifier = LostPetIdentifier(
        vector_db_path=ctx.obj['db_path'],
        ollama_url=ctx.obj['ollama_url'],
        ollama_model=ctx.obj['ollama_model']
    )
    
    size = identifier.get_database_size()
    console.print(f"[cyan]Database contains {size} pets[/cyan]")
    
    if size > 0:
        console.print("[dim]Use 'search' command to find matches[/dim]")


@cli.command()
@click.confirmation_option(prompt='Are you sure you want to clear the database?')
@click.pass_context
def clear(ctx):
    """Clear all entries from the database."""
    identifier = LostPetIdentifier(
        vector_db_path=ctx.obj['db_path'],
        ollama_url=ctx.obj['ollama_url'],
        ollama_model=ctx.obj['ollama_model']
    )
    
    identifier.clear_database()
    console.print("[green]Database cleared[/green]")


if __name__ == '__main__':
    cli()

