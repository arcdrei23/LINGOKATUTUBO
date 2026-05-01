"""
PDF reconstruction service - rebuilds PDF with translated text while preserving layout
"""

import fitz  # PyMuPDF
import os
from typing import List, Dict, Any, Optional
from translation_dataset import get_translation_dataset


class ReconstructionService:
    """Rebuilds PDFs with translated text while preserving original layout"""
    
    @staticmethod
    def reconstruct_pdf(
        input_pdf_path: str,
        layout_data: List[Dict[str, Any]],
        translations: Dict[str, Dict[str, str]],
        output_path: str
    ) -> bool:
        """
        Reconstruct a PDF with translated text
        
        Args:
            input_pdf_path: Path to original PDF
            layout_data: Layout information from extraction
            translations: Dict mapping block_id -> {"original", "translated"}
            output_path: Path to save new PDF
        
        Returns:
            True if successful
        """
        try:
            doc = fitz.open(input_pdf_path)
            
            # Process each page
            for page_num, page_layout in enumerate(layout_data):
                if page_num >= doc.page_count:
                    break
                
                page = doc[page_num]
                blocks = page_layout.get("blocks", [])
                
                # Remove old text blocks and replace with translated ones
                # This is a simplified approach - removes all text and re-adds translated
                
                for block_index, block in enumerate(blocks):
                    if block.get("type") != "text":
                        continue

                    block_bbox = block.get("bbox")

                    # Draw white rectangle over original text to cover it
                    if block_bbox:
                        x0, y0, x1, y1 = block_bbox
                        rect = fitz.Rect(x0, y0, x1, y1)
                        page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                
                # Add translated text
                for block in blocks:
                    if block.get("type") != "text":
                        continue
                    
                    block_bbox = block.get("bbox")
                    lines = block.get("lines", [])
                    
                    for line in lines:
                        original_text = line.get("text", "")
                        lookup_key = f"{page_num}_{block_index}"
                        translated_text = translations.get(lookup_key, {}).get("translated", original_text)
                        line_bbox = line.get("bbox")
                        
                        if line_bbox and translated_text:
                            x0, y0, x1, y1 = line_bbox
                            
                            # Add translated text at original position
                            # Use smaller font to fit if translation is longer
                            try:
                                page.insert_text(
                                    (x0, y0 + 10),  # Adjust y to match baseline
                                    translated_text,
                                    fontsize=11,
                                    color=(0, 0, 0)
                                )
                            except Exception as e:
                                print(f"[Reconstruction] Error inserting text: {e}")
            
            # Save output PDF
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            doc.save(output_path)
            doc.close()
            
            return True
        
        except Exception as e:
            print(f"[Reconstruction] Error reconstructing PDF: {e}")
            return False
    
    @staticmethod
    def create_bilingual_pdf(
        original_pdf_path: str,
        translated_pdf_path: str,
        output_path: str
    ) -> bool:
        """
        Create a bilingual PDF with original and translated pages side-by-side or alternating
        
        Args:
            original_pdf_path: Path to original PDF
            translated_pdf_path: Path to translated PDF
            output_path: Path to save combined PDF
        
        Returns:
            True if successful
        """
        try:
            original_doc = fitz.open(original_pdf_path)
            translated_doc = fitz.open(translated_pdf_path)
            output_doc = fitz.open()
            
            page_count = min(original_doc.page_count, translated_doc.page_count)
            
            # Alternate pages: original, translated, original, translated...
            for i in range(page_count):
                # Add original page
                orig_page = original_doc[i]
                output_doc.insert_pdf(original_doc, from_page=i, to_page=i)
                
                # Add translated page
                if i < translated_doc.page_count:
                    output_doc.insert_pdf(translated_doc, from_page=i, to_page=i)
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            output_doc.save(output_path)
            output_doc.close()
            original_doc.close()
            translated_doc.close()
            
            return True
        
        except Exception as e:
            print(f"[Reconstruction] Error creating bilingual PDF: {e}")
            return False
    
    @staticmethod
    def create_preview_images(
        pdf_path: str,
        output_dir: str,
        max_pages: int = 3,
        dpi: int = 150
    ) -> List[str]:
        """
        Create preview images from PDF pages
        
        Args:
            pdf_path: Path to PDF
            output_dir: Directory to save preview images
            max_pages: Maximum pages to preview
            dpi: DPI for rendering
        
        Returns:
            List of image file paths
        """
        image_paths = []
        
        try:
            doc = fitz.open(pdf_path)
            os.makedirs(output_dir, exist_ok=True)
            
            for page_num in range(min(max_pages, doc.page_count)):
                page = doc[page_num]
                
                # Render to image
                mat = fitz.Matrix(dpi / 72, dpi / 72)
                pix = page.get_pixmap(matrix=mat)
                
                image_path = os.path.join(output_dir, f"preview_page_{page_num}.png")
                pix.save(image_path)
                image_paths.append(image_path)
            
            doc.close()
        
        except Exception as e:
            print(f"[Reconstruction] Error creating preview images: {e}")
        
        return image_paths


# Global instance
_reconstruction_service = ReconstructionService()


def get_reconstruction_service() -> ReconstructionService:
    """Get the reconstruction service"""
    return _reconstruction_service

