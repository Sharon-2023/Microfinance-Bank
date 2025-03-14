import cv2
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
from tensorflow.keras.models import load_model
import pytesseract
from PIL import Image
from datetime import datetime

class KYCVerificationEngine:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.document_verification_model = load_model('models/document_verification.h5')
        self.metrics = {
            'f1_score': 0,
            'accuracy': 0,
            'precision': 0,
            'recall': 0
        }
        
    def verify_document_authenticity(self, document_image):
        """Verify if the document is genuine and not tampered"""
        try:
            # Convert document to processable format
            img = Image.open(document_image)
            img_array = np.array(img)
            
            # Extract document features
            features = self.document_verification_model.predict(np.expand_dims(img_array, axis=0))
            
            # Check for signs of tampering
            tampering_score = self.check_tampering(img_array)
            
            # Verify document patterns and security features
            security_features_score = self.verify_security_features(img_array)
            
            return {
                'is_authentic': tampering_score > 0.8 and security_features_score > 0.8,
                'tampering_score': tampering_score,
                'security_score': security_features_score
            }
        except Exception as e:
            raise ValueError(f"Document verification failed: {str(e)}")

    def extract_document_info(self, document_image, document_type):
        """Extract and validate information from the document"""
        try:
            # OCR to extract text from document
            text = pytesseract.image_to_string(Image.open(document_image))
            
            # Extract relevant fields based on document type
            extracted_info = self.parse_document_text(text, document_type)
            
            return extracted_info
        except Exception as e:
            raise ValueError(f"Information extraction failed: {str(e)}")

    def verify_face_match(self, document_photo, live_photo, min_confidence=0.8):
        """Verify if the document photo matches the live photo using OpenCV"""
        try:
            # Read images
            doc_img = cv2.imdecode(np.fromstring(document_photo.read(), np.uint8), cv2.IMREAD_COLOR)
            live_img = cv2.imdecode(np.fromstring(live_photo.read(), np.uint8), cv2.IMREAD_COLOR)

            # Convert to grayscale
            doc_gray = cv2.cvtColor(doc_img, cv2.COLOR_BGR2GRAY)
            live_gray = cv2.cvtColor(live_img, cv2.COLOR_BGR2GRAY)

            # Detect faces
            doc_faces = self.face_cascade.detectMultiScale(doc_gray, 1.1, 4)
            live_faces = self.face_cascade.detectMultiScale(live_gray, 1.1, 4)

            if len(doc_faces) == 0 or len(live_faces) == 0:
                return {
                    'match': False,
                    'confidence': 0,
                    'error': 'No face detected in one or both images'
                }

            # Get the first face from each image
            doc_face = doc_faces[0]
            live_face = live_faces[0]

            # Extract face ROIs
            doc_face_roi = doc_gray[doc_face[1]:doc_face[1]+doc_face[3], doc_face[0]:doc_face[0]+doc_face[2]]
            live_face_roi = live_gray[live_face[1]:live_face[1]+live_face[3], live_face[0]:live_face[0]+live_face[2]]

            # Resize to same size
            doc_face_roi = cv2.resize(doc_face_roi, (128, 128))
            live_face_roi = cv2.resize(live_face_roi, (128, 128))

            # Compare faces using structural similarity
            similarity = self.compare_faces(doc_face_roi, live_face_roi)

            return {
                'match': similarity >= min_confidence,
                'confidence': similarity
            }

        except Exception as e:
            raise ValueError(f"Face verification failed: {str(e)}")

    def compare_faces(self, face1, face2):
        """Compare two face images using structural similarity"""
        try:
            # Use SSIM (Structural Similarity Index)
            score = cv2.matchTemplate(face1, face2, cv2.TM_CCOEFF_NORMED)[0][0]
            # Normalize score to 0-1 range
            similarity = (score + 1) / 2
            return similarity
        except Exception as e:
            raise ValueError(f"Face comparison failed: {str(e)}")

    def calculate_metrics(self, true_labels, predicted_labels):
        """Calculate verification performance metrics"""
        try:
            self.metrics['f1_score'] = f1_score(true_labels, predicted_labels, average='weighted')
            self.metrics['accuracy'] = accuracy_score(true_labels, predicted_labels)
            self.metrics['precision'] = precision_score(true_labels, predicted_labels, average='weighted')
            self.metrics['recall'] = recall_score(true_labels, predicted_labels, average='weighted')
            
            return self.metrics
        except Exception as e:
            raise ValueError(f"Metrics calculation failed: {str(e)}") 