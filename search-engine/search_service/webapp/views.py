from django.shortcuts import render
from rest_framework.decorators import api_view
# Create your views here.




@api_view(['GET'])
def webapp_home(request):
    """
    webapp home
    """
    print("hitesh")
    if request.method == 'GET':
        return render(request,'home/index.html')