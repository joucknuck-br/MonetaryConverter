import django
django.setup()

from django.test import TestCase

from django.contrib.auth.models import User

from backend.models import CurrencyRate, Conversion


class UserCreateAPIViewTests(TestCase):

    def test_valid_data(self):
        data = {
            'username': 'username',
            'password': 'password',
            'email': 'email@example.com',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }
        response = self.client.post('/api/users/', data=data)
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username='username')
        self.assertEqual(user.email, 'email@example.com')
        self.assertEqual(user.first_name, 'First Name')
        self.assertEqual(user.last_name, 'Last Name')

    def test_invalid_data(self):
        data = {
            'username': 'invalid-username',
            'password': 'invalid-password',
            'email': 'invalid-email',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }
        response = self.client.post('/api/users/', data=data)
        self.assertEqual(response.status_code, 400)


class LoginViewTests(TestCase):

    def test_valid_data(self):
        User.objects.create_user('username', 'password')
        data = {
            'username': 'username',
            'password': 'password'
        }
        response = self.client.post('/api/login/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_data(self):
        data = {
            'username': 'invalid-username',
            'password': 'invalid-password'
        }
        response = self.client.post('/api/login/', data=data)
        self.assertEqual(response.status_code, 401)


class LogoutViewTests(TestCase):

    def test_valid_data(self):
        user = User.objects.create_user('username', 'password')
        self.client.force_login(user)
        response = self.client.post('/api/logout/', data={})
        self.assertEqual(response.status_code, 200)

    def test_invalid_data(self):
        response = self.client.post('/api/logout/', data={})
        self.assertEqual(response.status_code, 400)


class GetAllRatesTests(TestCase):

    def test_empty_data(self):
        response = self.client.get('/api/rates/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'rates': []
        })

    def test_valid_data(self):
        CurrencyRate.objects.create(currency='USD', rate='1.0000')
        CurrencyRate.objects.create(currency='BRL', rate='5.0000')
        response = self.client.get('/api/rates/')
        self.assertEqual(response.status_code, 200)


class GetObjectRateTests(TestCase):

    def test_currency_not_found(self):
        response = self.client.get('/api/rates/INVALID/')
        self.assertEqual(response.status_code, 404)

    def test_valid_currency(self):
        CurrencyRate.objects.create(currency='USD', rate='1.0000')
        response = self.client.get('/api/rates/USD/')
        self.assertEqual(response.status_code, 200)


class PostConversionTests(TestCase):

    def test_invalid_data(self):
        response = self.client.post('/api/convert/', data={})
        self.assertEqual(response.status_code, 400)

    def test_valid_data(self):
        CurrencyRate.objects.create(currency='USD', rate='1.0000')
        CurrencyRate.objects.create(currency='BRL', rate='5.0000')
        data = {
            'from_currency': 'USD',
            'to_currency': 'BRL',
            'amount': '100.00'
        }
        response = self.client.post('/api/convert/', data=data)
        self.assertEqual(response.status_code, 200)
        conversion = Conversion.objects.get(from_currency='USD', to_currency='BRL', amount='100.00')
        self.assertEqual(conversion.converted_amount, '500.00')


class GetAllConversionsTests(TestCase):

    def test_empty_data(self):
        response = self.client.get('/api/conversions/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'conversions': []
        })

    def test_valid_data(self):
        Conversion.objects.create(
            from_currency='USD',
            to_currency='BRL',
            amount='100.00',
            converted_amount='500.00',
            created_at='2023-02-28 18:48:10.000000'
        )
        response = self.client.get('/api/conversions/')
        self.assertEqual(response.status_code, 200)