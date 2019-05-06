from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SearchService



@api_view(['GET'])
def search_index(request):
    """
    search index 
    """
    if request.method == 'GET':
        return Response(SearchService.query(request.query_params))