from django.urls import path

from .views import GroupsAPIView, GroupAPIView, FullGroupAPIView, ParticipantGroupAPIView, \
    DeleteParticipantGroupAPIView, TossAPIView, RecipientAPIView

urlpatterns = [
    path("groups/", GroupsAPIView.as_view()),
    path("group/", GroupAPIView.as_view()),
    path("group/<int:id>", FullGroupAPIView.as_view()),
    path("group/<int:id>/participant", ParticipantGroupAPIView.as_view()),
    path("group/<int:id>/participant/<int:par_id>", DeleteParticipantGroupAPIView.as_view()),
    path("group/<int:id>/toss", TossAPIView.as_view()),
    path("group/<int:id>/participant/<int:par_id>/recipient", RecipientAPIView.as_view())
]