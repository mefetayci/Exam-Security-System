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
            # 1. Dosyaların var olup olmadığını kontrol et
            if not os.path.exists(live_photo_path) or not os.path.exists(reference_photo_path):
                return {'result': 'Error: File not found', 'confidence': 0.0}

            # 2. Resimleri Yükle
            img_live = cv2.imread(live_photo_path)
            img_ref = cv2.imread(reference_photo_path)

            if img_live is None or img_ref is None:
                return {'result': 'Error: Cannot read image', 'confidence': 0.0}

            # 3. Görüntüleri aynı boyuta getir (Karşılaştırma için şart)
            # Referans resmin boyutunu alıp canlı resmi ona uyduruyoruz
            height, width = img_ref.shape[:2]
            img_live_resized = cv2.resize(img_live, (width, height))

            # 4. Görüntüleri HSV formatına çevir (Renk analizi için daha iyi)
            hsv_live = cv2.cvtColor(img_live_resized, cv2.COLOR_BGR2HSV)
            hsv_ref = cv2.cvtColor(img_ref, cv2.COLOR_BGR2HSV)

            # 5. Histogram Hesapla
            # H (Hue) ve S (Saturation) kanallarını kullanıyoruz
            hist_live = cv2.calcHist([hsv_live], [0, 1], None, [50, 60], [0, 180, 0, 256])
            hist_ref = cv2.calcHist([hsv_ref], [0, 1], None, [50, 60], [0, 180, 0, 256])

            # Histogramları normalize et (0 ile 1 arasına sıkıştır)
            cv2.normalize(hist_live, hist_live, 0, 1, cv2.NORM_MINMAX)
            cv2.normalize(hist_ref, hist_ref, 0, 1, cv2.NORM_MINMAX)

            # 6. Karşılaştır (Korelasyon Yöntemi)
            # 1.0 = Birebir aynı, 0.0 = Hiç benzemiyor
            similarity = cv2.compareHist(hist_live, hist_ref, cv2.HISTCMP_CORREL)

            # Güven Skoru (Yüzdelik)
            confidence = round(similarity, 2)

            # Eşik Değer (Threshold): 0.70 ve üzeri benzer kabul edilsin
            # (Demo olduğu için biraz esnek tutuyoruz)
            if confidence > 0.70:
                return {'result': 'Match', 'confidence': confidence}
            else:
                return {'result': 'No Match', 'confidence': confidence}

        except Exception as e:
            print(f"OpenCV Error: {e}")
            return {'result': 'Error', 'confidence': 0.0}