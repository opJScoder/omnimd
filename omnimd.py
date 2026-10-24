#!/usr/bin/env python3
import os
import sys
import ollama
import questionary
from rich.console import Console
from rich.panel import Panel

# Initialize standard styling console
console = Console()
MODEL_NAME = "qwen2.5-coder:1.5b"  # Fast, highly performant local model for laptops

def print_banner():
    """Renders a beautiful ASCII art title banner."""
    banner = """
 █▀█ █▀▄▀█ █▄░█ █▀█ █▀▄
 █▄█ █░▀░█ █░▀█ █▄█ █▄▀  v1.0.0
    """
    console.print(banner, style="bold cyan")
    console.print("⚡ [dim]Flash-speed codebase documentation engine[/dim]\n")

def get_codebase_context(directory):
    """
    Recursively scans the local directory structure.
    Extracts code to build context while ignoring heavy dependency/build boilerplate.
    """
    context = ""
    exclude_dirs = {
        '.git', '__pycache__', 'venv', '.venv', 
        'node_modules', 'dist', 'build', '.next', 'out'
    }
    valid_extensions = {
        '.py', '.js', '.jsx', '.ts', '.tsx', 
        'html', '.css', '.go', '.rs', '.java', '.cpp'
    }

    for root, dirs, files in os.walk(directory):
        # In-place modification to skip ignored folders
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if os.path.splitext(file)[1] in valid_extensions:
                file_path = os.path.join(root, file)
                try:
                    relative_path = os.path.relpath(file_path, directory)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        context += f"\n--- File: {relative_path} ---\n"
                        context += f.read() + "\n"
                except Exception:
                    pass
    return context

def generate_doc(file_name, codebase, existing_content=None):
    """
    Interacts with the local Ollama LLM execution engine.
    Supports either fresh generation or smart context updating.
    """
    if existing_content:
        prompt = f"""
        You are OmniMD, a fast documentation engineer. The developer has updated their codebase.
        Your task is to update the existing {file_name} file to reflect these recent changes.
        
        CRITICAL RULES:
        1. Maintain the existing formatting layout and keep custom descriptions written by the dev.
        2. Focus on modifying or adding details only for newly added modules, functions, or dependencies.
        3. Return ONLY valid markdown content. No conversational fluff.

        [Original Document Content]:
        {existing_content}

        [Updated Codebase Context]:
        {codebase}
        """
        status_msg = f"[bold yellow]🔄 Updating {file_name} with smart sync..."
    else:
        prompt = f"""
        You are OmniMD. Generate a brand new, highly professional {file_name} file for this project codebase.
        Return ONLY valid markdown content. No conversational fluff or meta-commentary.

        [Codebase Context]:
        {codebase}
        """
        status_msg = f"[bold green]✨ Crafting a fresh {file_name}..."

    with console.status(status_msg, spinner="dots"):
        try:
            response = ollama.chat(model=MODEL_NAME, messages=[
                {'role': 'user', 'content': prompt}
            ])
            return response['message']['content']
        except Exception:
            console.print(f"\n[red]❌ Local LLM Error:[/red] Make sure Ollama is running and `{MODEL_NAME}` is downloaded.")
            sys.exit(1)

def main():
    print_banner()
    
    current_dir = os.getcwd()
    console.print(f"🔍 Analyzing workspace: [bold white]{current_dir}[/bold white]")
    
    # 1. Extract local code artifacts
    codebase = get_codebase_context(current_dir)
    if not codebase.strip():
        console.print("[red]❌ Aborting: No supported programming files found in this folder.[/red]")
        sys.exit(1)

    # 2. Check for target documentation tracking
    targets = ["README.md", "skills.md"]
    existing_docs = {t: os.path.exists(os.path.join(current_dir, t)) for t in targets}
    any_exists = any(existing_docs.values())
    
    is_update = False
    
    # Simple, automated single-command logic check
    if any_exists:
        console.print("\n[yellow]⚠️  Existing markdown documentation detected in this directory.[/yellow]")
        action = questionary.select(
            "How would you like OmniMD to proceed?",
            choices=[
                "🔄 Smart Sync (Intelligently update based on code shifts)",
                "📝 Overwrite (Discard existing files and start entirely fresh)",
                "❌ Cancel operation"
            ]
        ).ask()
        
        if not action or "Cancel" in action:
            console.print("[dim]Operation stopped safely. No files were modified.[/dim]")
            sys.exit(0)
        
        is_update = "Smart Sync" in action

    # 3. Code processing loop
    files_processed = []
    
    for file_name in targets:
        file_path = os.path.join(current_dir, file_name)
        existing_content = None
        
        # Read file contents only if performing a smart update sync
        if is_update and os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                existing_content = f.read()

        # Request generation mapping from local engine
        md_output = generate_doc(file_name, codebase, existing_content)
        
        # Commit back onto disk securely
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_output)
        
        size_kb = len(md_output.encode('utf-8')) / 1024
        files_processed.append(f"📄 Processed: [bold white]{file_name}[/bold white] ({size_kb:.2f} KB)")

    # 4. Success summary output panel
    console.print("\n")
    success_text = "\n".join(files_processed)
    console.print(Panel(
        success_text,
        title="[bold green]🎉 OmniMD Action Complete[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))

if __name__ == "__main__":
    main()
