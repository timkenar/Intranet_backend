from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Resource
from .serializers import ResourceSerializer, CreateResourceSerializer, NestedFolderSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]


    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def nested_folders(self, request):
        """
        Return the folder hierarchy starting from root folders.
        """
        root_folders = Resource.objects.filter(parent=None, resource_type='folder')
        serializer = NestedFolderSerializer(root_folders, many=True)
        return Response(serializer.data)
    
    def get_queryset(self):
        # Return resources owned by the user or their children
        return Resource.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the owner of the resource
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def children(self, request, pk=None):
        """
        List all subfolders and files within a specific folder.
        """
        resource = self.get_object()
        if resource.resource_type != 'folder':
            return Response({"detail": "This resource is not a folder."}, status=400)

        children = resource.children.all()
        serializer = ResourceSerializer(children, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def rename(self, request, pk=None):
        """
        Rename a resource (folder or file).
        """
        resource = self.get_object()
        new_name = request.data.get('name')
        if not new_name:
            return Response({"detail": "New name is required."}, status=400)

        # Check for duplicate names within the same parent folder
        if resource.parent and resource.parent.children.filter(name=new_name).exists():
            return Response({"detail": "A resource with this name already exists in the parent folder."}, status=400)

        resource.name = new_name
        resource.save()
        return Response({"detail": "Resource renamed successfully.", "new_name": resource.name})