## 1. Clone the Repo

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

## 2. Setup the virtual environment

# Using venv

# OR using conda

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Create the Django Project and App

```bash
django-admin startproject adminportal
cd adminportal
python manage.py startapp authentication
```

## 5. Configure PostgreSQL Database

Replace the default SQLite configuration in adminportal/settings.py with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'admin_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 6. Set Up the Database in pgAdmin

Create a database named: admin_db

Create a new user: your_db_user

Set password: your_db_password

Under Privileges, enable almost all

Under Role Membership, assign postgres

Run this query in Query Tool:

```sql
GRANT ALL PRIVILEGES ON DATABASE admin_db TO your_db_user;
```

## 7. Update Installed Apps in settings.py

```python
'authentication',
'rest_framework',
'rest_framework_simplejwt',
```

## 8. Define Custom User Model

In authentication/models.py:

```python
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AdminUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

class AdminUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    # Add other fields as needed

    USERNAME_FIELD = 'username'
    objects = AdminUserManager()
```

Also register it in authentication/admin.py AND settings.py

```python
AUTH_USER_MODEL = 'authentication.AdminUser'
```

## 9. Run Migrations and Create Admin User

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py shell
```

and in python shell

```python
from authentication.models import AdminUser
AdminUser.objects.create_user(username='admin', password='adminpass')
exit()
```

## 10. Configure JWT in settings.py

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
}
```

## 11. Create the Login View

In authentication/views.py:

```python
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

class AdminTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
```

Create authentication/urls.py:

```python
from django.urls import path
from .views import AdminTokenObtainPairView

urlpatterns = [
    path('login/', AdminTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
```

Update adminportal/urls.py:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
]
```

## 12. Run the Server

```bash
python manage.py runserver
```

## 13. Test Authentication

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "adminpass"}'
```

### ✅ What Has Been Achieved

- Custom Admin Authentication

- API-Based Login

- Secure Authentication

- Session Management

- Session Timeout

- Encryption in Transit
