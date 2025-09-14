import sys
import os
import unittest
import numpy as np

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.ml_model import StudentPerformancePredictor

class TestStudentPerformancePredictor(unittest.TestCase):
    
    def setUp(self):
        """Set up a new predictor instance for each test"""
        self.predictor = StudentPerformancePredictor()
        # Ensure the model is trained
        if not self.predictor.is_trained:
            self.predictor.train()
    
    def test_model_initialization(self):
        """Test that the model initializes correctly"""
        self.assertIsNotNone(self.predictor.model)
        self.assertIsNotNone(self.predictor.scaler)
        self.assertTrue(self.predictor.is_trained)
    
    def test_prediction_within_bounds(self):
        """Test that predictions are within the expected range (0-100)"""
        # Test with various input combinations
        test_cases = [
            # attendance, study_hours, previous_grade
            (90, 8, 85),   # High values
            (50, 4, 60),   # Medium values
            (30, 2, 40),   # Low values
            (100, 10, 100), # Maximum values
            (0, 0, 0)       # Minimum values
        ]
        
        for attendance, study_hours, previous_grade in test_cases:
            prediction = self.predictor.predict(attendance, study_hours, previous_grade)
            self.assertGreaterEqual(prediction, 0)
            self.assertLessEqual(prediction, 100)
            print(f"Input: Attendance={attendance}, Study Hours={study_hours}, Previous Grade={previous_grade}")
            print(f"Prediction: {prediction:.2f}")
    
    def test_prediction_correlation(self):
        """Test that predictions correlate positively with input features"""
        # Base case
        base_attendance = 70
        base_study_hours = 5
        base_previous_grade = 75
        base_prediction = self.predictor.predict(base_attendance, base_study_hours, base_previous_grade)
        
        # Test increasing attendance
        higher_attendance_prediction = self.predictor.predict(base_attendance + 20, base_study_hours, base_previous_grade)
        self.assertGreater(higher_attendance_prediction, base_prediction)
        
        # Test increasing study hours
        higher_study_hours_prediction = self.predictor.predict(base_attendance, base_study_hours + 3, base_previous_grade)
        self.assertGreater(higher_study_hours_prediction, base_prediction)
        
        # Test increasing previous grade
        higher_previous_grade_prediction = self.predictor.predict(base_attendance, base_study_hours, base_previous_grade + 15)
        self.assertGreater(higher_previous_grade_prediction, base_prediction)
    
    def test_synthetic_data_generation(self):
        """Test that synthetic data is generated correctly"""
        data = self.predictor._generate_synthetic_data(n_samples=50)
        
        # Check data shape and columns
        self.assertEqual(len(data), 50)
        self.assertIn('attendance_percentage', data.columns)
        self.assertIn('study_hours', data.columns)
        self.assertIn('previous_grade', data.columns)
        self.assertIn('score', data.columns)
        
        # Check value ranges
        self.assertTrue(all(data['attendance_percentage'] >= 50))
        self.assertTrue(all(data['attendance_percentage'] <= 100))
        self.assertTrue(all(data['study_hours'] >= 1))
        self.assertTrue(all(data['study_hours'] <= 10))
        self.assertTrue(all(data['previous_grade'] >= 40))
        self.assertTrue(all(data['previous_grade'] <= 100))
        self.assertTrue(all(data['score'] >= 0))
        self.assertTrue(all(data['score'] <= 100))

if __name__ == '__main__':
    unittest.main()
