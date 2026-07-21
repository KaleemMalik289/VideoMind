import json
from pathlib import Path
from app.modules.summary.schemas import SummaryJSON

class SummaryFormatter:
    """Writes the generated JSON summary into specific Markdown files."""
    
    @staticmethod
    def format(summary: SummaryJSON, dirs: dict) -> None:
        # Save JSON
        with open(dirs["json"], "w", encoding="utf-8") as f:
            f.write(summary.model_dump_json(indent=2))
            
        # Save Executive Summary
        with open(dirs["executive"], "w", encoding="utf-8") as f:
            f.write("# Executive Summary\n\n")
            f.write(summary.executive_summary)
            f.write("\n")
            
        # Save Detailed Summary
        with open(dirs["detailed"], "w", encoding="utf-8") as f:
            f.write("# Detailed Summary\n\n")
            f.write(summary.detailed_summary)
            f.write("\n")
            
        # Save Bullet Summary
        with open(dirs["bullet"], "w", encoding="utf-8") as f:
            f.write("# Key Takeaways\n\n")
            for bullet in summary.bullet_summary:
                f.write(f"- {bullet}\n")
            f.write("\n")
