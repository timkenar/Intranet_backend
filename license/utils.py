from .models import License

# license/utils.py

def assign_subscription_to_group(group, subscription):
    if group.users.count() > subscription.max_users:
        raise ValueError("Group exceeds maximum user limit for this subscription.")

    group.tenant.subscription_set.create(
        name=subscription.name,
        price=subscription.price,
        duration=subscription.duration,
        features=subscription.features,
        max_users=subscription.max_users,
        allowed_apps=subscription.allowed_apps,
    )


def can_access_app(user, app_name):
    try:
        license = License.objects.get(user=user)
        return app_name in license.subscription.allowed_apps
    except License.DoesNotExist:
        return False  # No license means no access
