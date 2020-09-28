from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Message
from .permissions import IsAuthenticated
from .serializers import MessageSerializer
from .pagination import CustomPagination
from .tasks import send_message


class SingleMessageView(RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, pk):
        try:
            message = Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return message

    def get(self, request, pk):
        # Get a message
        message = self.get_queryset(pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        # Mark message as read
        message = self.get_queryset(pk)
        if request.user == message.author:
            message.mark_read()
            return Response({'status': 'MARK AS READ'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'UNAUTHORIZED'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        # Delete a message
        message = self.get_queryset(pk)
        if request.user == message.author:
            message.delete()
            content = {
                'status': 'NO CONTENT'
            }
            return Response(content, status=status.HTTP_204_NO_CONTENT)
        else:
            content = {
                'status': 'UNAUTHORIZED'
            }
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)


class MessagesView(ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        messages = Message.objects.all()
        return messages

    def get(self, request):
        # Get all messages
        messages = self.get_queryset()
        paginate_queryset = self.paginate_queryset(messages)
        serializer = self.serializer_class(paginate_queryset, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        # Create a new message
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            mes = serializer.save(author=request.user)
            send_message.delay(mes.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
