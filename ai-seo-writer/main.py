import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Append current directory to sys.path to ensure imports work if run from outside
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.input.handler import InputHandler
from app.ai.provider import GeminiProvider
from app.research.engine import ResearchEngine
from app.planner.planner import ContentPlanner
from app.seo.writer import SEOWriter
from app.exporter.file_exporter import FileExporter

def main():
    console = Console()
    console.print(Panel.fit("[bold cyan]Dawen AI SEO Writer[/bold cyan]", border_style="cyan"))

    # Argument Parsing
    parser = argparse.ArgumentParser(description="Generate SEO-optimized articles using AI.")
    parser.add_argument("keyword", nargs="?", help="The focus keyword for the article")
    args = parser.parse_args()

    # Interactive mode if no keyword provided
    keyword = args.keyword
    if not keyword:
        keyword = console.input("[bold green]Enter keyword:[/bold green] ")

    try:
        # Step 1: Input Processing
        console.print(f"\n[bold]1. Processing Keyword:[/bold] {keyword}")
        clean_keyword = InputHandler.process(keyword)
        
        # Initialize Components
        # We do this here to catch config errors early
        ai_provider = GeminiProvider()
        researcher = ResearchEngine()
        planner = ContentPlanner(ai_provider)
        writer = SEOWriter(ai_provider)
        exporter = FileExporter()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            
            # Step 2: Research
            task1 = progress.add_task(description="[cyan]Researching topic on the web...[/cyan]", total=None)
            research_data = researcher.search(clean_keyword)
            progress.remove_task(task1)
            console.print(f"   [green]✓[/green] Found {len(research_data['sources'])} sources.")

            # Step 3: Planning
            task2 = progress.add_task(description="[cyan]Generating content plan...[/cyan]", total=None)
            plan = planner.create_plan(clean_keyword, research_data)
            progress.remove_task(task2)
            console.print(f"   [green]✓[/green] Plan created: [bold]{plan.get('main_topic')}[/bold]")
            
            # Step 4: Writing
            task3 = progress.add_task(description="[cyan]Writing full article (this may take a minute)...[/cyan]", total=None)
            content = writer.write_article(plan, research_data)
            progress.remove_task(task3)
            console.print(f"   [green]✓[/green] Article generated ({len(content.split())} words approx).")

        # Step 5: Export
        filepath = exporter.save_article(clean_keyword, content)
        console.print(Panel(f"SUCCESS!\nArticle saved to: [underline]{filepath}[/underline]", style="bold green"))

    except ValueError as ve:
        console.print(f"[bold red]Validation Error:[/bold red] {ve}")
    except Exception as e:
        console.print(f"[bold red]System Error:[/bold red] {e}")

if __name__ == "__main__":
    import os
    main()
