# license/middleware.py

from django.http import JsonResponse
from .utils import has_access, can_access_app

def application_access_middleware(get_response):
    def middleware(request):
        app_name = request.path.split('/')[2]  # Extract application name
        
        if app_name in ['intranet', 'messenger', 'resources', 'meetings']:
            if request.user.is_authenticated:
                user_groups = request.user.groups.all()
                
                # Check if the user has access or if any group they belong to has access
                if any(has_access(request.user, group, app_name) for group in user_groups):
                    response = get_response(request)
                    return response
                else:
                    return JsonResponse({"detail": "Access to this application is restricted."}, status=403)
            else:
                return JsonResponse({"detail": "Authentication required."}, status=401)

        response = get_response(request)
        return response

    return middleware


# # license/middleware.py

# from django.http import JsonResponse
# from .utils import can_access_app

# def application_access_middleware(get_response):
#     def middleware(request):
#         app_name = request.path.split('/')[2]  # Extract application name
        
#         if app_name in ['intranet', 'messenger', 'resources', 'meetings']:
#             if request.user.is_authenticated:
#                 # Check if user belongs to a group with access
#                 user_groups = request.user.groups.all()
#                 if any(can_access_app(group.tenant, app_name) for group in user_groups):
#                     response = get_response(request)
#                     return response
#                 else:
#                     return JsonResponse({"detail": "Access to this application is restricted."}, status=403)
#             else:
#                 return JsonResponse({"detail": "Authentication required."}, status=401)

#         response = get_response(request)
#         return response

#     return middleware
