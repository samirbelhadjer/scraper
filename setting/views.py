from rest_framework.response import Response
from rest_framework import status, serializers, generics
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from .models import Setting, Contact


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = [
            'phone_number',
            'email',
            'address',
            'google_map_link',
            'content',
            'logo',
            'colored_logo',
            'title',
        ]




@swagger_auto_schema(method='GET',)
@api_view(["GET"])
def AboutUsView(request):
    """
    Returns content for about us and contact us page
    """
    info = Setting.objects.all().first()
    info = AboutUsSerializer(info)
    return Response(info.data, status=status.HTTP_200_OK)



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            'email',
            'subject',
            'name',
            'message',
        ]


class ContactView(generics.GenericAPIView):
    serializer_class = ContactSerializer
    def post(self, request):
        """
        Post a contact form
        """
        try:
            data = ContactSerializer(data=request.data)
            if data.is_valid():
                data.save()
                return Response({"details":"contact sent"}, status=status.HTTP_200_OK)
            return Response({"details":"incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"details":"incorrect data"}, status=status.HTTP_400_BAD_REQUEST)
    