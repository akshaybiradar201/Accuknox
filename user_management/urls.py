from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import (
    dashboard,
    UserViewSet,
    SendFriendRequestView,
    ListPendingRequests,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    ListFriends,
)

urlpatterns = [
    path(
        "friends/send-request/<int:receiver_id>/",
        SendFriendRequestView.as_view(),
        name="send-friend-request",
    ),
    path(
        "friends/accept-request/<int:request_id>/",
        AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "friends/reject-request/<int:request_id>/",
        RejectFriendRequestView.as_view(),
        name="reject-friend-request",
    ),
    path("listfriends/<int:request_id>/", ListFriends.as_view(), name="friend-list"),
    path(
        "listpendingrequests/<int:request_id>/",
        ListPendingRequests.as_view(),
        name="request-list",
    ),
    path("searchusers/", UserViewSet.as_view({"get": "list"}), name="search-user"),
    path("", include("django.contrib.auth.urls")),
    path(
        "", dashboard, name="dashboard"
    ),
]
