from django.test import TestCase

class CertificateTestCase(TestCase):
    def test_certificate_generation(self):
        # Setup
        student = Profile.objects.create(...)
        event = Event.objects.create(...)
        
        # Generate Certificate
        certificate = Certificate.objects.create(event=event, participant=student)
        self.assertTrue(certificate)

    def test_aicte_point_limit(self):
        # Test for point limits
        student = Profile.objects.create(aicte_points=90)
        event = Event.objects.create(aicte_points=20)
        self.assertFalse(student.aicte_points + event.aicte_points <= 100)
