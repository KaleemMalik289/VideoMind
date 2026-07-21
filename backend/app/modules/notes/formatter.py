import json
from pathlib import Path
from app.modules.notes.schemas import NotesJSON

class NotesFormatter:
    """Writes the generated JSON notes into a structured Markdown file."""
    
    @staticmethod
    def format(notes: NotesJSON, dirs: dict) -> None:
        # Save JSON
        with open(dirs["json"], "w", encoding="utf-8") as f:
            f.write(notes.model_dump_json(indent=2))
            
        # Save Markdown
        with open(dirs["markdown"], "w", encoding="utf-8") as f:
            f.write(f"# {notes.title}\n\n")
            f.write(f"{notes.introduction}\n\n")
            
            for section in notes.sections:
                f.write(f"## {section.title}\n\n")
                
                if section.definitions:
                    f.write("### Definitions\n")
                    for d in section.definitions:
                        f.write(f"- {d}\n")
                    f.write("\n")
                    
                if section.formulas:
                    f.write("### Important Formulas\n")
                    for form in section.formulas:
                        f.write(f"- {form}\n")
                    f.write("\n")
                    
                if section.content:
                    f.write("### Key Points\n")
                    for bullet in section.content:
                        f.write(f"- {bullet}\n")
                    f.write("\n")
                    
                if section.examples:
                    f.write("### Examples\n")
                    for ex in section.examples:
                        f.write(f"- {ex}\n")
                    f.write("\n")
            
            if notes.conclusions:
                f.write("## Conclusions\n\n")
                for c in notes.conclusions:
                    f.write(f"- {c}\n")
                f.write("\n")
