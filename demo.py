#!/usr/bin/env python3
"""
Demo script showing how to use the Lost Pet Identifier system.
"""

import os
import sys

# Set OpenMP environment variable to avoid conflicts on macOS
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'

from lost_pet_identifier import LostPetIdentifier
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    console.print("[bold cyan]Lost Pet Identifier - Demo[/bold cyan]\n")
    
    # Initialize the system
    console.print("[yellow]Initializing system...[/yellow]")
    identifier = LostPetIdentifier(
        vector_db_path="./data/faiss_index",
        ollama_url="http://localhost:11434",
        ollama_model="llama2"
    )
    console.print("[green]System initialized[/green]\n")
    
    # Demo: Add some found pets
    console.print("[bold]Step 1: Adding Found Pets[/bold]\n")
    
    found_pets = [
        {
            "description": "Small brown dog with floppy ears, friendly, found near Bukit Timah",
            "location": "Bukit Timah",
            "date": "2024-01-15"
        },
        {
            "description": "Black and white cat, medium size, shy, found near Orchard Road",
            "location": "Orchard Road",
            "date": "2024-01-16"
        },
        {
            "description": "Golden retriever, large, friendly, found near Marina Bay",
            "location": "Marina Bay",
            "date": "2024-01-17"
        },
        {
            "description": "Small brown dog with pointy ears, energetic",
            "location": "Sentosa",
            "date": "2024-01-18"
        }
    ]
    
    for i, pet in enumerate(found_pets, 1):
        console.print(f"Adding found pet {i}...")
        idx = identifier.add_found_pet(
            description=pet["description"],
            location=pet["location"],
            date=pet["date"]
        )
        console.print(f"[green]Added (index: {idx})[/green]")
    
    console.print(f"\n[cyan]Database now contains {identifier.get_database_size()} pets[/cyan]\n")
    
    # Demo: Search for lost pets
    console.print("[bold]Step 2: Searching for Lost Pets[/bold]\n")
    
    search_queries = [
        {
            "description": "Brown dog, friendly, last seen near Bukit Timah",
            "title": "Lost: Brown Dog"
        },
        {
            "description": "Bird heard nearby, audio available",
            "title": "Lost: Bird (Audio-Enabled)",
            "audio_path": None
        },
        {
            "description": "Small dog with floppy ears",
            "title": "Lost: Small Dog"
        },
        {
            "description": "Black and white cat",
            "title": "Lost: Cat"
        }
    ]
    
    for query in search_queries:
        console.print(f"[bold]{query['title']}[/bold]")
        console.print(f"Query: \"{query['description']}\"\n")
        
        results = identifier.search_lost_pet(
            audio_path=query.get("audio_path"),
            description=query['description'],
            k=3,
            include_explanation=True
        )
        
        if results['results']:
            console.print("[cyan]Top Matches:[/cyan]")
            for i, result in enumerate(results['results'], 1):
                similarity = result['similarity_score']
                desc = result.get('description', 'No description')
                location = result.get('location', 'N/A')
                
                # Color code similarity
                if similarity > 0.7:
                    sim_color = "green"
                elif similarity > 0.5:
                    sim_color = "yellow"
                else:
                    sim_color = "red"
                
                console.print(
                    f"  {i}. [{sim_color}]Similarity: {similarity:.3f}[/{sim_color}] - "
                    f"{desc[:50]}... ({location})"
                )
            
            if results.get('explanation'):
                console.print("\n[dim]Explanation:[/dim]")
                console.print(Panel(results['explanation'], border_style="blue"))
        else:
            console.print("[yellow]No matches found[/yellow]")
        
        console.print("\n" + "="*60 + "\n")
    
    console.print("[green]Demo completed![/green]")
    console.print("\n[dim]To use with images, provide --image path/to/image.jpg[/dim]")
    console.print("[dim]To use with Ollama, ensure it's running: ollama serve[/dim]")

if __name__ == "__main__":
    main()

