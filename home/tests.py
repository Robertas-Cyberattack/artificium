from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import ClientProject, Invoice, ProjectFile


class ArtificiumTests(TestCase):

    def setUp(self):
        self.client_user = User.objects.create_user(
            username='clientuser',
            email='client@test.com',
            password='testpass123'
        )

        self.other_client = User.objects.create_user(
            username='otherclient',
            email='other@test.com',
            password='testpass123'
        )

        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )

        self.project = ClientProject.objects.create(
            client=self.client_user,
            title='Test Project',
            description='Test description',
            price=100,
            invoice_number='INV-TEST-001',
            is_paid=True,
            status='paid',
            progress=100
        )

    def test_client_can_access_dashboard(self):
        self.client.login(username='clientuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_client_cannot_access_admin_dashboard(self):
        self.client.login(username='clientuser', password='testpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_can_access_admin_dashboard(self):
        self.client.login(username='adminuser', password='testpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_client_can_create_project(self):
        self.client.login(username='clientuser', password='testpass123')

        response = self.client.post(reverse('client_create_project'), {
            'title': 'New Client Project',
            'description': 'New project description',
            'client_notes': 'Client notes here'
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ClientProject.objects.filter(title='New Client Project').exists()
        )

    def test_client_cannot_edit_other_client_project(self):
        other_project = ClientProject.objects.create(
            client=self.other_client,
            title='Other Client Project',
            description='Private project',
            status='requested'
        )

        self.client.login(username='clientuser', password='testpass123')

        response = self.client.post(
            reverse('client_edit_project', args=[other_project.id]),
            {
                'title': 'Hacked Project',
                'description': 'Trying to edit',
                'client_notes': 'Not allowed'
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_invoice_download_creates_invoice(self):
        self.client.login(username='clientuser', password='testpass123')

        response = self.client.get(
            reverse('download_invoice', args=[self.project.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertTrue(
            Invoice.objects.filter(project=self.project).exists()
        )

    def test_client_can_upload_project_file(self):
        self.client.login(username='clientuser', password='testpass123')

        test_file = SimpleUploadedFile(
            'test_file.txt',
            b'This is a test file.',
            content_type='text/plain'
        )

        response = self.client.post(
            reverse('upload_project_file', args=[self.project.id]),
            {
                'title': 'Test Upload',
                'file': test_file
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            ProjectFile.objects.filter(
                project=self.project,
                title='Test Upload'
            ).exists()
        )

    def test_client_can_delete_project_file(self):
        project_file = ProjectFile.objects.create(
            project=self.project,
            title='Delete Me',
            file=SimpleUploadedFile(
                'delete_me.txt',
                b'Delete this file.',
                content_type='text/plain'
            ),
            uploaded_by=self.client_user
        )

        self.client.login(username='clientuser', password='testpass123')

        response = self.client.post(
            reverse('delete_project_file', args=[project_file.id])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            ProjectFile.objects.filter(id=project_file.id).exists()
        )