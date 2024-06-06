from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, Request
from .serializers import RequestSerializer, CustomUserSerializer
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from .paginations import ResultsPagination
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(ratelimit(key="user_or_ip", rate="3/m"))
    def post(self, request, receiver_id):
        try:
            receiver = CustomUser.objects.get(pk=receiver_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if receiver == request.user:
            return Response(
                {"error": "Cannot send request to yourself"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if Request.objects.filter(sender=request.user, receiver=receiver).exists():
            return Response(
                {"error": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST
            )

        request_obj = Request.objects.create(sender=request.user, receiver=receiver)

        request.user.update_friend_count()

        serializer = RequestSerializer(request_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = Request.objects.get(pk=request_id)
        except Request.DoesNotExist:
            return Response(
                {"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if friend_request.receiver != request.user:
            return Response(
                {"error": "You cannot accept this request"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Add users to each other's friend lists and update friend counts
        friend_request.sender.friends.add(friend_request.receiver)
        friend_request.sender.update_friend_count()  # Call update_friend_count method

        friend_request.receiver.friends.add(friend_request.sender)
        friend_request.receiver.update_friend_count()  # Call update_friend_count method

        friend_request.delete()  # Delete the accepted request

        return Response(
            {"message": "Friend request accepted"}, status=status.HTTP_200_OK
        )


class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id):
        try:
            friend_request = Request.objects.get(pk=request_id)
        except Request.DoesNotExist:
            return Response(
                {"error": "Request not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if friend_request.receiver != request.user:
            return Response(
                {"error": "You cannot reject this request"},
                status=status.HTTP_403_FORBIDDEN,
            )

        friend_request.delete()  # Simply delete the rejected request

        return Response(
            {"message": "Friend request rejected"}, status=status.HTTP_200_OK
        )


class ListFriends(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        user = CustomUser.objects.filter(id=request_id).first()
        if user:
            print(user.friends.all())
            serialized_data = CustomUserSerializer(user.friends.all(), many=True)
            return Response(
                {"friends": serialized_data.data}, status=status.HTTP_200_OK
            )


class ListPendingRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, request_id):
        requests = Request.objects.filter(sender__id=request_id)
        if requests:
            serialized_data = RequestSerializer(requests, many=True)
            return Response(
                {"Pending Requests": serialized_data.data}, status=status.HTTP_200_OK
            )
        return Response({"Pending Requests": {}}, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = ResultsPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "first_name", "last_name"]

    @action(detail=False, methods=["get"])
    def search(self, request):
        search_term = request.query_params.get("search", None)

        if search_term is None:
            return Response({"error": "Missing search term"})

        try:
            exact_match = CustomUser.objects.get(email=search_term)
            return Response(CustomUserSerializer(exact_match).data)
        except CustomUser.DoesNotExist:
            pass

        queryset = self.get_queryset().filter(
            Q(email__icontains=search_term)
            | Q(first_name__icontains=search_term)
            | Q(last_name__icontains=search_term)
        )
        page = self.paginate_queryset(queryset)
        serialized_data = CustomUserSerializer(page, many=True).data
        return self.get_paginated_response(serialized_data)


@login_required(login_url="login/")
def dashboard(request):
    return render(request, "dashboard.html")
