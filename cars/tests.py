from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Car, Review


def make_admin():
    return User.objects.create_superuser('admin_test', 'a@test.com', 'pass123')


def make_customer():
    return User.objects.create_user('customer_test', 'c@test.com', 'pass123')


def make_car(**kwargs):
    defaults = dict(make='BMW', model='3 Series', year=2022,
                    price=32000, mileage=15000, fuel_type='petrol',
                    color='White', status='available')
    defaults.update(kwargs)
    return Car.objects.create(**defaults)


class AuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = make_admin()
        self.customer = make_customer()

    def test_login_page_loads(self):
        r = self.client.get(reverse('login'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Mapps Cars')

    def test_admin_login_redirects_to_admin_panel(self):
        self.client.login(username='admin_test', password='pass123')
        r = self.client.get(reverse('dashboard'))
        self.assertRedirects(r, reverse('admin_panel'))

    def test_customer_login_redirects_to_showroom(self):
        self.client.login(username='customer_test', password='pass123')
        r = self.client.get(reverse('dashboard'))
        self.assertRedirects(r, reverse('showroom'))

    def test_invalid_login_shows_error(self):
        r = self.client.post(reverse('login'), {'username': 'bad', 'password': 'bad'})
        self.assertEqual(r.status_code, 200)

    def test_unauthenticated_redirects_to_login(self):
        r = self.client.get(reverse('showroom'))
        self.assertEqual(r.status_code, 302)
        self.assertIn('/login/', r['Location'])

    def test_logout_redirects_to_login(self):
        self.client.login(username='customer_test', password='pass123')
        r = self.client.get(reverse('logout'))
        self.assertRedirects(r, reverse('login'))


class AdminViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = make_admin()
        self.client.login(username='admin_test', password='pass123')
        self.car = make_car()

    def test_admin_panel_loads(self):
        r = self.client.get(reverse('admin_panel'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Dashboard')

    def test_manage_cars_lists_cars(self):
        r = self.client.get(reverse('manage_cars'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'BMW')

    def test_add_car(self):
        data = dict(make='Audi', model='A4', year=2021, price=28000,
                    mileage=20000, fuel_type='diesel', color='Black',
                    status='available', description='')
        r = self.client.post(reverse('add_car'), data)
        self.assertRedirects(r, reverse('manage_cars'))
        self.assertTrue(Car.objects.filter(make='Audi').exists())

    def test_edit_car(self):
        r = self.client.post(reverse('edit_car', args=[self.car.pk]), {
            'make': 'BMW', 'model': '5 Series', 'year': 2022,
            'price': 40000, 'mileage': 15000, 'fuel_type': 'petrol',
            'color': 'Black', 'status': 'available', 'description': '',
        })
        self.assertRedirects(r, reverse('manage_cars'))
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, '5 Series')

    def test_delete_car_get_shows_confirm(self):
        r = self.client.get(reverse('delete_car', args=[self.car.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Delete Vehicle')

    def test_delete_car_post_removes_car(self):
        self.client.post(reverse('delete_car', args=[self.car.pk]))
        self.assertFalse(Car.objects.filter(pk=self.car.pk).exists())

    def test_manage_reviews_loads(self):
        r = self.client.get(reverse('manage_reviews'))
        self.assertEqual(r.status_code, 200)

    def test_add_comment_to_review(self):
        review = Review.objects.create(
            customer_name='Jane', customer_email='j@test.com',
            title='Great!', review_text='Loved it.', rating=5,
        )
        r = self.client.post(reverse('add_comment', args=[review.pk]), {
            'admin_comment': 'Thank you, Jane!',
            'is_approved': True,
        })
        self.assertRedirects(r, reverse('manage_reviews'))
        review.refresh_from_db()
        self.assertEqual(review.admin_comment, 'Thank you, Jane!')
        self.assertTrue(review.is_approved)


class CustomerViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = make_customer()
        self.client.login(username='customer_test', password='pass123')
        make_car()

    def test_showroom_loads(self):
        r = self.client.get(reverse('showroom'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'BMW')

    def test_review_form_loads(self):
        r = self.client.get(reverse('review'))
        self.assertEqual(r.status_code, 200)

    def test_submit_review(self):
        r = self.client.post(reverse('review'), {
            'customer_name': 'John Smith',
            'customer_email': 'john@test.com',
            'car': '',
            'rating': 5,
            'title': 'Brilliant experience',
            'review_text': 'Really happy with everything.',
        })
        self.assertRedirects(r, reverse('review_success'))
        self.assertTrue(Review.objects.filter(customer_name='John Smith').exists())

    def test_review_success_page(self):
        r = self.client.get(reverse('review_success'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Thank You')

    def test_customer_cannot_access_admin_panel(self):
        r = self.client.get(reverse('admin_panel'))
        self.assertEqual(r.status_code, 302)

    def test_customer_cannot_add_car(self):
        r = self.client.get(reverse('add_car'))
        self.assertEqual(r.status_code, 302)


class ModelTests(TestCase):
    def test_car_str(self):
        car = make_car()
        self.assertEqual(str(car), '2022 BMW 3 Series')

    def test_review_str(self):
        review = Review.objects.create(
            customer_name='Alice', customer_email='a@test.com',
            title='Excellent', review_text='Loved it.', rating=5,
        )
        self.assertIn('Alice', str(review))

    def test_car_status_choices(self):
        car = make_car(status='sold')
        self.assertEqual(car.get_status_display(), 'Sold')

    def test_review_defaults_not_approved(self):
        review = Review.objects.create(
            customer_name='Bob', customer_email='b@test.com',
            title='Good', review_text='Nice.', rating=4,
        )
        self.assertFalse(review.is_approved)
