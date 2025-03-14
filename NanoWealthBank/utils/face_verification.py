import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import time
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

class FaceVerifier:
    def __init__(self):
        # Initialize the FaceAnalysis model with FaceNet512
        self.model = FaceAnalysis(
            name='webface_r50',  # Using FaceNet512 model
            allowed_modules=['detection', 'recognition'],
            providers=['CPUExecutionProvider']
        )
        # Larger detection size for better accuracy with high-res images
        self.model.prepare(ctx_id=0, det_size=(640, 640))
        # Initialize metrics history
        self.verification_history = {
            'true_labels': [],
            'predicted_labels': [],
            'similarity_scores': []
        }
        
    def get_face_embedding(self, img):
        """Extract face embedding from image using FaceNet512"""
        try:
            # Ensure image is in RGB format
            if len(img.shape) == 2:  # If grayscale
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif img.shape[2] == 4:  # If RGBA
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            
            # Get face detection and embedding
            faces = self.model.get(img)
            
            if not faces:
                return None, "⚠️ No face detected in the image"
                
            if len(faces) > 1:
                return None, "⚠️ Multiple faces detected - please provide an image with a single face"
                
            # Return the 512-dimensional embedding of the first face
            return faces[0].embedding, None
            
        except Exception as e:
            return None, f"❌ Error in face detection: {str(e)}"
    
    def verify_faces(self, doc_image, live_image, threshold=0.6, is_genuine_pair=None):
        """
        Compare document face with live face
        Returns: (match_result, detailed_message, metrics)
        """
        try:
            # Get embeddings for both images
            doc_embedding, doc_error = self.get_face_embedding(doc_image)
            if doc_error:
                return False, f"Document Image: {doc_error}", None
                
            live_embedding, live_error = self.get_face_embedding(live_image)
            if live_error:
                return False, f"Live Image: {live_error}", None
                
            # Normalize embeddings
            doc_embedding = doc_embedding / np.linalg.norm(doc_embedding)
            live_embedding = live_embedding / np.linalg.norm(live_embedding)
            
            # Calculate cosine similarity
            similarity = float(np.dot(doc_embedding, live_embedding))
            
            # Determine match
            is_match = similarity > threshold
            
            # Update verification history if ground truth is provided
            if is_genuine_pair is not None:
                self.verification_history['true_labels'].append(int(is_genuine_pair))
                self.verification_history['predicted_labels'].append(int(is_match))
                self.verification_history['similarity_scores'].append(similarity)
            
            # Calculate metrics
            metrics = self.calculate_metrics() if len(self.verification_history['true_labels']) > 0 else None
            
            # Prepare detailed message
            if is_match:
                message = (
                    "✅ MATCH FOUND!\n"
                    f"Similarity Score: {similarity:.2%}\n"
                    "Face in the document matches with the live face capture."
                )
            else:
                message = (
                    "❌ NO MATCH!\n"
                    f"Similarity Score: {similarity:.2%}\n"
                    "Face in the document does not match with the live face capture."
                )
            
            # Add metrics to message if available
            if metrics:
                message += f"\n\nVerification Metrics:\n"
                message += f"F1-Score: {metrics['f1_score']:.2%}\n"
                message += f"Accuracy: {metrics['accuracy']:.2%}\n"
                message += f"Precision: {metrics['precision']:.2%}\n"
                message += f"Recall: {metrics['recall']:.2%}"
            
            return is_match, message, metrics
            
        except Exception as e:
            return False, f"❌ Error during verification: {str(e)}", None
    
    def calculate_metrics(self):
        """Calculate verification metrics based on historical data"""
        try:
            if len(self.verification_history['true_labels']) < 2:
                return None
                
            true_labels = np.array(self.verification_history['true_labels'])
            pred_labels = np.array(self.verification_history['predicted_labels'])
            
            metrics = {
                'accuracy': float(accuracy_score(true_labels, pred_labels)),
                'precision': float(precision_score(true_labels, pred_labels, zero_division=0)),
                'recall': float(recall_score(true_labels, pred_labels, zero_division=0)),
                'f1_score': float(f1_score(true_labels, pred_labels, zero_division=0)),
                'total_comparisons': len(true_labels),
                'false_positives': sum((pred_labels == 1) & (true_labels == 0)),
                'false_negatives': sum((pred_labels == 0) & (true_labels == 1)),
                'average_similarity': float(np.mean(self.verification_history['similarity_scores']))
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating metrics: {str(e)}")
            return None
    
    def get_metrics_summary(self):
        """Get a formatted summary of the verification metrics"""
        metrics = self.calculate_metrics()
        if not metrics:
            return "Insufficient data for metrics calculation"
            
        summary = (
            f"Face Verification Metrics:\n"
            f"------------------------\n"
            f"Accuracy: {metrics['accuracy']:.2%}\n"
            f"Precision: {metrics['precision']:.2%}\n"
            f"Recall: {metrics['recall']:.2%}\n"
            f"F1-Score: {metrics['f1_score']:.2%}\n"
            f"------------------------\n"
            f"Total Comparisons: {metrics['total_comparisons']}\n"
            f"False Positives: {metrics['false_positives']}\n"
            f"False Negatives: {metrics['false_negatives']}\n"
            f"Average Similarity: {metrics['average_similarity']:.3f}"
        )
        return summary
    
    def reset_metrics(self):
        """Reset the verification history and metrics"""
        self.verification_history = {
            'true_labels': [],
            'predicted_labels': [],
            'similarity_scores': []
        }
    
    def preprocess_image(self, img):
        """Preprocess image for better face detection"""
        try:
            # Convert to RGB if needed
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
            elif img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
                
            # Resize if image is too large
            max_size = 1920
            height, width = img.shape[:2]
            if height > max_size or width > max_size:
                scale = max_size / max(height, width)
                new_size = (int(width * scale), int(height * scale))
                img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)
                
            # Enhance contrast if needed
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
            l, a, b = cv2.split(lab)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            l = clahe.apply(l)
            enhanced = cv2.merge([l, a, b])
            img = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
            
            return img, None
            
        except Exception as e:
            return None, f"Error preprocessing image: {str(e)}"