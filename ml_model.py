import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os

class StudentPerformancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = os.path.join(os.path.dirname(__file__), 'performance_model.pkl')
        self.scaler_path = os.path.join(os.path.dirname(__file__), 'scaler.pkl')
        
        # Try to load existing model
        self.load_model()
    
    def load_model(self):
        """Load the model if it exists"""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            try:
                with open(self.model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(self.scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        return False
    
    def save_model(self):
        """Save the model to disk"""
        if self.model is not None:
            with open(self.model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(self.scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
            return True
        return False
    
    def train(self, data=None):
        """
        Train the model with provided data or generate synthetic data if none provided
        
        data: pandas DataFrame with columns ['attendance_percentage', 'study_hours', 'previous_grade', 'score']
        """
        if data is None or len(data) < 10:
            # Generate synthetic data for initial training if real data is insufficient
            data = self._generate_synthetic_data()
        
        X = data[['attendance_percentage', 'study_hours', 'previous_grade']]
        y = data['score']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model = LinearRegression()
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Save model
        self.save_model()
        
        return self.model
    
    def predict(self, attendance_percentage, study_hours, previous_grade):
        """Predict student score based on input features"""
        if not self.is_trained:
            self.train()
        
        # Prepare input data
        X = np.array([[attendance_percentage, study_hours, previous_grade]])
        
        # Scale input
        X_scaled = self.scaler.transform(X)
        
        # Make prediction
        prediction = self.model.predict(X_scaled)[0]
        
        # Ensure prediction is within reasonable bounds (0-100)
        prediction = max(0, min(100, prediction))
        
        return prediction
    
    def _generate_synthetic_data(self, n_samples=100):
        """Generate synthetic data for initial model training"""
        np.random.seed(42)
        
        # Generate random features
        attendance = np.random.uniform(50, 100, n_samples)
        study_hours = np.random.uniform(1, 10, n_samples)
        prev_grades = np.random.uniform(40, 100, n_samples)
        
        # Generate target with some noise
        # Formula: score = 0.3*attendance + 3*study_hours + 0.4*prev_grades + noise
        scores = 0.3 * attendance + 3 * study_hours + 0.4 * prev_grades + np.random.normal(0, 5, n_samples)
        
        # Ensure scores are within 0-100 range
        scores = np.clip(scores, 0, 100)
        
        # Create DataFrame
        df = pd.DataFrame({
            'attendance_percentage': attendance,
            'study_hours': study_hours,
            'previous_grade': prev_grades,
            'score': scores
        })
        
        return df


# Create an instance of the predictor
predictor = StudentPerformancePredictor()

# Ensure the model is trained
if not predictor.is_trained:
    predictor.train()
