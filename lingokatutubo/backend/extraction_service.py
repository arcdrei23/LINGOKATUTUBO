"""
Text extraction service for digital PDFs and DOCX files
"""

import fitz  # PyMuPDF
from docx import Document
from typing import List, Dict, Any
from models import TextSegment


class ExtractionService:
    """Extracts text and layout information from digital documents"""
    
    @staticmethod
    def extract_pdf_text_and_layout(pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract text and layout information from a digital PDF
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of pages, each with text blocks and their positions
        """
        pages_data = []
        
        try:
            doc = fitz.open(pdf_path)
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_height = page.rect.height
                page_width = page.rect.width
                
                # Extract text with bounding boxes
                text_dict = page.get_text("dict")
                blocks = text_dict.get("blocks", [])
                
                page_data = {
                    "page": page_num,
                    "width": page_width,
                    "height": page_height,
                    "blocks": []
                }
                
                for block in blocks:
                    if block["type"] == 0:  # Text block
                        block_bbox = block.get("bbox")
                        block_lines = block.get("lines", [])
                        
                        block_data = {
                            "type": "text",
                            "bbox": block_bbox,
                            "lines": []
                        }
                        
                        for line in block_lines:
                            line_bbox = line.get("bbox")
                            line_text = ""
                            spans = line.get("spans", [])
                            
                            for span in spans:
                                line_text += span.get("text", "")
                            
                            if line_text.strip():
                                block_data["lines"].append({
                                    "text": line_text,
                                    "bbox": line_bbox,
                                    "font": spans[0].get("font", "") if spans else ""
                                })
                        
                        if block_data["lines"]:
                            page_data["blocks"].append(block_data)
                    
                    elif block["type"] == 1:  # Image block
                        page_data["blocks"].append({
                            "type": "image",
                            "bbox": block.get("bbox")
                        })
                
                pages_data.append(page_data)
            
            doc.close()
        
        except Exception as e:
            print(f"[Extraction] Error extracting PDF: {e}")
        
        return pages_data
    
    @staticmethod
    def extract_docx_text_and_layout(docx_path: str) -> List[Dict[str, Any]]:
        """
        Extract text from DOCX file
        
        DOCX doesn't have concept of "pages" but we'll return paragraphs with metadata
        
        Args:
            docx_path: Path to DOCX file
        
        Returns:
            List of pages with text blocks
        """
        pages_data = []
        
        try:
            doc = Document(docx_path)
            
            # Group into pages (rough estimate based on paragraph count)
            page_data = {
                "page": 0,
                "width": 612,  # Standard letter width in points
                "height": 792,  # Standard letter height in points
                "blocks": []
            }
            
            for para in doc.paragraphs:
                text = para.text.strip()
                if not text:
                    continue
                
                # Detect heading style
                is_heading = para.style.name.startswith("Heading")
                
                block_data = {
                    "type": "text",
                    "bbox": [50, len(page_data["blocks"]) * 20, 562, len(page_data["blocks"]) * 20 + 20],
                    "lines": [{
                        "text": text,
                        "bbox": [50, len(page_data["blocks"]) * 20, 562, len(page_data["blocks"]) * 20 + 20],
                        "font": para.style.font.name if para.style.font else "Calibri",
                        "is_heading": is_heading
                    }]
                }
                
                page_data["blocks"].append(block_data)
            
            pages_data.append(page_data)
        
        except Exception as e:
            print(f"[Extraction] Error extracting DOCX: {e}")
        
        return pages_data
    
    @staticmethod
    def extract_text_from_layout(pages_data: List[Dict[str, Any]]) -> List[TextSegment]:
        """
        Convert layout data to TextSegment list
        
        Args:
            pages_data: Output from extract_pdf_text_and_layout
        
        Returns:
            List of TextSegment objects
        """
        segments = []
        
        for page_data in pages_data:
            page_num = page_data.get("page", 0)
            blocks = page_data.get("blocks", [])
            
            for block in blocks:
                if block.get("type") != "text":
                    continue
                
                block_bbox = block.get("bbox")
                lines = block.get("lines", [])
                
                for line in lines:
                    text = line.get("text", "").strip()
                    if not text:
                        continue
                    
                    segment = TextSegment(
                        content=text,
                        page=page_num,
                        bbox=line.get("bbox", block_bbox),
                        font_info={"font": line.get("font", "")},
                        is_heading=line.get("is_heading", False),
                        is_list_item=text[0].isdigit() or text.startswith(("•", "-", "*"))
                    )
                    segments.append(segment)
        
        return segments


# Global instance
_extraction_service = ExtractionService()


def get_extraction_service() -> ExtractionService:
    """Get the extraction service"""
    return _extraction_service

