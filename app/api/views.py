import random

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_409_CONFLICT

from rest_framework.views import APIView

from .models import Group, ParticipantGroup, Participant
from .serializers import GroupSerializer, ParticipantSerializer


# Create your views here.
class GroupsAPIView(APIView):
    def get(self, request):
        groups = Group.objects.all()
        gs = GroupSerializer(groups, many=True)
        return Response(gs.data, status=HTTP_200_OK)


class GroupAPIView(APIView):
    def post(self, request):
        gs = GroupSerializer(data=request.data)
        if gs.is_valid():
            gs.save()
            return Response(gs.data['id'], status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class GettingGroups:
    def get_objects(self, **kwargs):
        return Group.objects.filter(id=kwargs.get("id"))


class FullGroupAPIView(APIView, GettingGroups):
    def get(self, request, **kwargs):
        groups = self.get_objects(**kwargs)
        if groups:
            group = groups[0]
            participants_id = ParticipantGroup.objects.filter(group=group.id).values("participant")
            participants = Participant.objects.filter(id__in=participants_id)
            result = GroupSerializer(group).data
            participants_list = []
            for elem in participants:
                participant = Participant.objects.filter(id=elem.recipient).first()
                cur_dict = {
                    "id": elem.id,
                    "name": elem.name,
                    "wish": elem.wish,
                }
                if participant is not None:
                    cur_dict["recipient"] = ParticipantSerializer(participant).data
                participants_list.append(cur_dict)
            result["participants"] = participants_list
            return Response(result, status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        groups = self.get_objects(**kwargs)
        if groups and request.data.get("name") is not None:
            group = groups[0]
            group.name = request.data.get("name")
            group.description = request.data.get("description")
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        groups = self.get_objects(**kwargs)
        if groups:
            group = groups[0]
            group.delete()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class ParticipantGroupAPIView(APIView, GettingGroups):
    def post(self, request, **kwargs):
        groups = self.get_objects(**kwargs)
        if groups:
            group = groups[0]
            ps = ParticipantSerializer(data=request.data)
            print(1)
            if ps.is_valid():
                ps.save()
                ParticipantGroup.objects.create(participant_id=ps.data["id"], group=group)
            else:
                return Response(status=HTTP_400_BAD_REQUEST)
            return Response(ps.data.get("id"), status=HTTP_201_CREATED)
        return Response(status=HTTP_400_BAD_REQUEST)


class DeleteParticipantGroupAPIView(APIView):
    def delete(self, request, **kwargs):
        cols = ParticipantGroup.objects.filter(participant_id=kwargs.get("par_id"),
                                               group_id=kwargs.get("id"))
        print(cols)
        if cols:
            cols[0].delete()
            return Response(status=HTTP_200_OK)
        return Response(status=HTTP_400_BAD_REQUEST)


class TossAPIView(APIView, GettingGroups):
    def post(self, request, **kwargs):
        groups = self.get_objects(**kwargs)
        if groups:
            group = groups[0]
            participants = [i for i in ParticipantGroup.objects.filter(group=group)]
            if len(participants) >= 3:
                participants_for_choosing = [i for i in participants]
                for participant in participants:
                    cur_id = random.choice(participants_for_choosing)
                    while cur_id == participant:
                        cur_id = random.choice(participants_for_choosing)
                    participant.recipient = cur_id
                    participant.save()
                    del participants_for_choosing[participants_for_choosing.index(cur_id)]
                return Response(status=HTTP_200_OK)
            return Response(status=HTTP_409_CONFLICT)
        return Response(status=HTTP_400_BAD_REQUEST)


class RecipientAPIView(APIView):
    def get(self, request, **kwargs):
        participants = Participant.objects.filter(id=kwargs.get("par_id"))
        if participants:
            participant = participants[0]
            if participant.recipient is None:
                return Response({}, status=HTTP_200_OK)
            else:
                Response(ParticipantSerializer(participant.recipient), status=HTTP_200_OK)

        return Response(status=HTTP_400_BAD_REQUEST)
