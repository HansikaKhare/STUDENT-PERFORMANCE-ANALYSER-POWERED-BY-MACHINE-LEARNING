import sys
import os
import unittest
from flask import url_for

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.models.models import db, User, StudentInfo, Subject, PerformanceData

class TestRoutes(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and application context"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create database tables
        db.create_all()
        
        # Create test users
        self._create_test_users()
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def _create_test_users(self):
        """Create test users for testing"""
        # Create a student user
        student_user = User(username='test_student', email='student@test.com', role='student')
        student_user.set_password('password123')
        db.session.add(student_user)
        
        # Create student info
        student_info = StudentInfo(
            user_id=1,
            student_id='S12345',
            first_name='Test',
            last_name='Student',
            year_of_study=2
        )
        db.session.add(student_info)
        
        # Create a faculty user
        faculty_user = User(username='test_faculty', email='faculty@test.com', role='faculty')
        faculty_user.set_password('password123')
        db.session.add(faculty_user)
        
        db.session.commit()
    
    def test_index_route(self):
        """Test the index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_login_route(self):
        """Test the login route"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        
        # Test login with valid credentials
        response = self.client.post('/auth/login', data={
            'username': 'test_student',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
        
        # Test login with invalid credentials
        response = self.client.get('/auth/logout', follow_redirects=True)
        response = self.client.post('/auth/login', data={
            'username': 'test_student',
            'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_student_dashboard(self):
        """Test the student dashboard route"""
        # Login as student
        self.client.post('/auth/login', data={
            'username': 'test_student',
            'password': 'password123'
        })
        
        # Access student dashboard
        response = self.client.get('/student/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Student Dashboard', response.data)
    
    def test_faculty_dashboard(self):
        """Test the faculty dashboard route"""
        # Login as faculty
        self.client.post('/auth/login', data={
            'username': 'test_faculty',
            'password': 'password123'
        })
        
        # Access faculty dashboard
        response = self.client.get('/faculty/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Faculty Dashboard', response.data)
    
    def test_add_subject(self):
        """Test adding a subject"""
        # Login as student
        self.client.post('/auth/login', data={
            'username': 'test_student',
            'password': 'password123'
        })
        
        # Add a subject
        response = self.client.post('/student/add-subject', data={
            'name': 'Test Subject',
            'submit': 'Add Subject'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Subject', response.data)
        
        # Verify subject was added to database
        subject = Subject.query.filter_by(name='Test Subject').first()
        self.assertIsNotNone(subject)
        self.assertEqual(subject.name, 'Test Subject')
    
    def test_subject_performance_prediction(self):
        """Test performance prediction for a subject"""
        # Login as student
        self.client.post('/auth/login', data={
            'username': 'test_student',
            'password': 'password123'
        })
        
        # Add a subject
        self.client.post('/student/add-subject', data={
            'name': 'Math',
            'submit': 'Add Subject'
        })
        
        subject = Subject.query.filter_by(name='Math').first()
        
        # Add performance data and get prediction
        response = self.client.post(f'/student/subject/{subject.id}', data={
            'attendance_percentage': 85,
            'study_hours': 7,
            'previous_grade': 78,
            'submit': 'Predict Score'
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Predicted Score', response.data)
        
        # Verify performance data was added to database
        performance = PerformanceData.query.filter_by(subject_id=subject.id).first()
        self.assertIsNotNone(performance)
        self.assertEqual(performance.attendance_percentage, 85)
        self.assertEqual(performance.study_hours, 7)
        self.assertEqual(performance.previous_grade, 78)
        self.assertIsNotNone(performance.predicted_score)

if __name__ == '__main__':
    unittest.main()
