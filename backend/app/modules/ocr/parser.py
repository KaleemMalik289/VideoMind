from app.modules.ocr.schemas import OCRDetection

class OutputParser:
    """Sorts OCR detections to preserve natural human reading order."""
    
    @staticmethod
    def sort_reading_order(detections: list[OCRDetection]) -> list[OCRDetection]:
        """
        Sorts detections top-to-bottom, left-to-right.
        Groups lines based on the y-coordinate.
        """
        if not detections:
            return []
            
        # Calculate a center point or use top-left corner for sorting
        def get_y_coord(det: OCRDetection):
            # Use top-left y coordinate
            return det.bounding_box[0][1]
            
        def get_x_coord(det: OCRDetection):
            return det.bounding_box[0][0]
            
        # Sort vertically first
        vertical_sorted = sorted(detections, key=get_y_coord)
        
        # Group into lines if Y difference is small (e.g., within 10-15 pixels)
        lines = []
        current_line = []
        current_y = None
        
        # Dynamic threshold based on box height could be better, but fixed pixel is okay for MVP
        Y_TOLERANCE = 15.0 
        
        for det in vertical_sorted:
            y = get_y_coord(det)
            if current_y is None:
                current_y = y
                current_line.append(det)
            else:
                if abs(y - current_y) <= Y_TOLERANCE:
                    current_line.append(det)
                else:
                    lines.append(current_line)
                    current_line = [det]
                    current_y = y
                    
        if current_line:
            lines.append(current_line)
            
        # Sort each line horizontally (left-to-right)
        final_sorted = []
        for line in lines:
            sorted_line = sorted(line, key=get_x_coord)
            final_sorted.extend(sorted_line)
            
        return final_sorted
