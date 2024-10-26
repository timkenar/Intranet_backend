# License Module README

## Overview

The License Module is a Django application designed to manage user subscriptions and licenses efficiently. It allows the assignment of licenses to user groups, facilitating easier management of multiple users under different subscription plans.

## Features

- **User Group Management**: Create and manage groups of users to whom licenses can be assigned.
- **Subscription Plans**: Define various subscription plans with associated features and pricing.
- **License Management**: Assign licenses to user groups and track their validity and activation status.
- **Access Control**: Middleware to restrict access to applications based on user licenses.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   ```

2. **Install Requirements**:

   Ensure you have Django and other dependencies installed. You can use:

   ```bash
   pip install -r requirements.txt
   ```

3. **Add to Installed Apps**:

   Add the License module to your Django project’s `settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       'license',
   ]
   ```

4. **Run Migrations**:

   Create and apply the necessary database migrations:

   ```bash
   python manage.py makemigrations license
   python manage.py migrate
   ```

## Models

### UserGroup

Represents a group of users that can be assigned a license.

```python
class UserGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)
```

### Subscription

Defines subscription plans with features and pricing.

```python
class Subscription(models.Model):
    PLAN_CHOICES = [
        ('essential', 'Essential'),
        ('premium', 'Premium'),
        ('ultimate', 'Ultimate'),

    # List the applications that you want to include or restrict according to the license
      APPLICATIONS = [
        'intranet',
        'messenger',
        'resources',
        'meetings',
    ]



    ]
    name = models.CharField(max_length=255, choices=PLAN_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField()  # in days
    features = models.JSONField(default=list)
```

### License

Represents a license assigned to a user group linked to a subscription.

```python
class License(models.Model):
    user_group = models.ForeignKey(UserGroup, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
```

## Middleware

### Application Access Middleware

Controls access to applications based on user authentication and license status.

```python
def application_access_middleware(get_response):
    ...
```

## Admin Configuration

To manage the License module in the Django admin interface, register the models:

```python
from django.contrib import admin
from .models import UserGroup, Subscription, License

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration']

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ['user_group', 'subscription', 'start_date', 'end_date', 'is_active']
```

## Usage

1. **Create User Groups**: Use the Django admin to create user groups.
2. **Define Subscription Plans**: Create various subscription plans based on your requirements.
3. **Assign Licenses**: Assign licenses to user groups to enable access to features.
4. **Monitor Access**: The middleware will restrict access to applications based on the assigned licenses.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

For further assistance, please contact [chepkenertimothy@gmail.com].
