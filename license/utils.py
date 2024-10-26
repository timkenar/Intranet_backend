# license/utils.py

from .models import License

def assign_subscription_to_group(group, subscription):
    if group.users.count() > subscription.max_users:
        raise ValueError("Group exceeds maximum user limit for this subscription.")

    # Assuming you still want to create licenses for groups
    for user in group.users.all():
        License.objects.create(
            user=user,
            subscription=subscription,
            end_date=timezone.now() + timezone.timedelta(days=subscription.duration),
        )

def can_access_app(user, app_name):
    # Check if the user has a license that allows access to the specified app
    try:
        license = License.objects.get(user=user)
        return app_name in license.subscription.allowed_apps
    except License.DoesNotExist:
        return False  # No license means no access

def can_access_group_apps(group, app_name):
    # Check if any user in the group has access to the specified app.
    for user in group.user_set.all():
        if can_access_app(user, app_name):
            return True
    return False


def has_access(user, group, app_name):
    """Check if either the user or any user in the group has access to the app."""
    # Check the individual user's access
    if can_access_app(user, app_name):
        return True
    # Check the group's access
    if can_access_group_apps(group, app_name):
            return True
    return False

# from .models import License

# # license/utils.py

# def assign_subscription_to_group(group, subscription):
#     if group.users.count() > subscription.max_users:
#         raise ValueError("Group exceeds maximum user limit for this subscription.")

#     group.tenant.subscription_set.create(
#         name=subscription.name,
#         price=subscription.price,
#         duration=subscription.duration,
#         features=subscription.features,
#         max_users=subscription.max_users,
#         allowed_apps=subscription.allowed_apps,
#     )


# def can_access_app(user, app_name):
#     try:
#         license = License.objects.get(user=user)
#         return app_name in license.subscription.allowed_apps
#     except License.DoesNotExist:
#         return False  # No license means no access
