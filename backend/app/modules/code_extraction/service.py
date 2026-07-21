import time
from pathlib import Path
from loguru import logger
from app.core.settings import settings
from app.modules.code_extraction.validator import CodeExtractionValidator
from app.modules.code_extraction.detector import CodeDetector
from app.modules.code_extraction.generator import CodeGenerator
from app.modules.code_extraction.merger import CodeMerger
from app.modules.code_extraction.syntax_validator import SyntaxValidator
from app.modules.code_extraction.formatter import CodeFormatter
from app.modules.code_extraction.metadata import MetadataGenerator
from app.modules.code_extraction.schemas import CodeResponse
from app.modules.code_extraction.exceptions import CodeExtractionError

class CodeExtractionService:
    """Orchestrates the AI Code Extraction pipeline."""
    
    @staticmethod
    def ensure_directories(job_id: str) -> dict:
        base_path = Path(settings.PROCESSED_DIR) / job_id / "code"
        source_dir = base_path / "source"
        snippets_dir = base_path / "snippets"
        
        base_path.mkdir(parents=True, exist_ok=True)
        source_dir.mkdir(parents=True, exist_ok=True)
        snippets_dir.mkdir(parents=True, exist_ok=True)
        
        return {
            "base": base_path,
            "json": base_path / "code.json",
            "markdown": base_path / "code.md",
            "source": source_dir,
            "snippets": snippets_dir,
            "metadata": base_path / "metadata.json"
        }

    @staticmethod
    def process_job(job_id: str) -> CodeResponse:
        logger.info(f"Starting Code Extraction Pipeline for job {job_id}")
        start_time = time.time()
        
        try:
            job_dir = Path(settings.PROCESSED_DIR) / job_id
            chunks_path = job_dir / "chunks" / "chunks.json"
            
            # 1. Validate
            CodeExtractionValidator.validate(str(chunks_path))
            
            # 2. Setup Directories
            dirs = CodeExtractionService.ensure_directories(job_id)
            
            # 3. Generate Intermediate Snippets
            snippets = CodeGenerator.extract_chunk_code(job_id)
            
            # 4. Merge Snippets into Final Files
            code_json, tokens = CodeMerger.merge(job_id, snippets)
            
            # 5. Validate Syntax
            all_valid = True
            for file in code_json.files:
                is_valid = SyntaxValidator.validate(file.code, code_json.language)
                if not is_valid:
                    all_valid = False
            
            # 6. Format Outputs
            if code_json.files:
                CodeFormatter.format(code_json, dirs)
            else:
                logger.info(f"No code generated for job {job_id}. Skipping formatting.")
            
            # 7. Generate Metadata
            processing_time = time.time() - start_time
            metadata = MetadataGenerator.generate(
                job_id=job_id,
                num_chunks=len(snippets),
                num_files=len(code_json.files),
                syntax_valid=all_valid,
                tokens=tokens,
                processing_time=processing_time
            )
            
            with open(dirs["metadata"], "w", encoding="utf-8") as f:
                f.write(metadata.model_dump_json(indent=2))
                
            logger.info(f"Successfully extracted code for job {job_id}")
            
            return CodeResponse(
                success=True,
                job_id=job_id,
                message="Code extraction completed.",
                data={"metadata": metadata.model_dump()}
            )
            
        except Exception as e:
            logger.error(f"Code extraction failed for job {job_id}: {str(e)}")
            raise CodeExtractionError(details={"error": str(e)})
