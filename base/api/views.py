# from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSeriallizers

@api_view(['GET'])
def getRoutes(request):
    routes=[
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms:id'
    ]
    return Response(routes)
    # return JsonResponse(routes,safe=False)



@api_view(['GET'])
def getRooms(request):
    rooms= Room.objects.all()
    seriallizers =RoomSeriallizers(rooms,many=True)
    return Response(seriallizers.data)
    
@api_view(['GET'])
def getRoom(request,pk):
    rooms= Room.objects.get(id=pk)
    seriallizers =RoomSeriallizers(rooms,many=False)
    return Response(seriallizers.data)