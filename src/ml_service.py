import cv2
import numpy as np
import os

class FaceVerificationService:
    """
    Simpler Computer Vision implementation using OpenCV.
    Uses Histogram Comparison to check image similarity.
    """

    def verify_identity(self, live_photo_path, reference_photo_path):
        """
        Compares two images using Histogram Correlation.
        Returns: {'result': 'Match' or 'No Match', 'confidence': float}
        """
        try:
            
            if not os.path.exists(live_photo_path) or not os.path.exists(reference_photo_path):
                return {'result': 'Error: File not found', 'confidence': 0.0}

           
            img_live = cv2.imread(live_photo_path)
            img_ref = cv2.imread(reference_photo_path)

            if img_live is None or img_ref is None:
                return {'result': 'Error: Cannot read image', 'confidence': 0.0}

           
            height, width = img_ref.shape[:2]
            img_live_resized = cv2.resize(img_live, (width, height))

            
            hsv_live = cv2.cvtColor(img_live_resized, cv2.COLOR_BGR2HSV)
            hsv_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2HSV)

           
            hist_live = cv2.calcHist([hsv_live], [0, 1], None, [50, 60], [0, 180, 0, 256])
            hist_ref = cv2.calcHist([hsv_ref], [0, 1], None, [50, 60], [0, 180, 0, 256])

            
            cv2.normalize(hist_live, hist_live, 0, 1, cv2.NORM_MINMAX)
            cv2.normalize(hist_ref, hist_ref, 0, 1, cv2.NORM_MINMAX)

            
            similarity = cv2.compareHist(hist_live, hist_ref, cv2.HISTCMP_CORREL)

           
            confidence = round(similarity, 2)

          
            if confidence > 0.70:
                return {'result': 'Match', 'confidence': confidence}
            else:
                return {'result': 'No Match', 'confidence': confidence}

        except Exception as e:
            print(f"OpenCV Error: {e}")
            return {'result': 'Error', 'confidence': 0.0}
