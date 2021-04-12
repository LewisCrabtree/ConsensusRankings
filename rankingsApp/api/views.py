from rest_framework import generics
from rankingsApp.api.serializers import *
from rankingsApp.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework import filters
from rest_framework.response import Response
import random
from rest_framework import status
from django.http import Http404
from django.urls import path
from rankingsApp import rankingsEngine

Valid_Positions = ['QB', 'RB', 'WR', 'TE']


class PlayersList(APIView):
    """
    List all Players
    """
    def get(self, request):
        position = request.GET.get('position')
        players = Player.objects.all().order_by('-Rating', 'Name')
        if position in Valid_Positions:
            players = players.filter(Position=position)
            print(position)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    """
    Create new player
    """
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlayersView(APIView):
    """
    internal method to get player
    """
    def get_object(self, pk):
        try:
            return Player.objects.get(id=pk)
        except Player.DoesNotExist:
            raise Http404

    """
    Get single matchup from id
    """
    def get(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        players = self.get_object(pk=pid)
        serializer = PlayerSerializer(players, many=False)
        return Response(serializer.data)

    """
    List all matchups
    """
    def put(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        serializer = PlayerSerializer(player, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all matchups
    """
    def patch(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        serializer = PlayerSerializer(player, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all matchups
    """
    def delete(self, request, *args, **kwargs):
        pid = self.kwargs['pk']
        player = self.get_object(pk=pid)
        player.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class MatchupsList(APIView):

    """
    List all matchups
    """
    def get(self, request):
        position = request.GET.get('position')
        nextMatchup = self.GetNextMatchup(position)
        serializer = MatchupSerializer(nextMatchup, many=False)
        return Response(serializer.data)


    """
    Insert matchup
    """
    def post(self, request):
        serializer = MatchupSerializer(data=request.data)
        if serializer.is_valid():
            self.EvaluateMatchup(serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Used for Getting the next matchup in get()
    """
    def GetNextMatchup(self, position):
        players = Player.objects.all()
        if position not in Valid_Positions:
            position = random.choice(Valid_Positions)
        players = players.filter(Position=position)
        players = players.order_by('-Rating', 'Name')
        index1 = math.floor(abs(random.uniform(0,1) - random.uniform(0,1)) * (1 + players.count() - 10))
        index2 = math.floor(abs(random.uniform(0,1) - random.uniform(0,1)) * (1 + players.count() - 10))
        if index1 == index2:
            if index1 == 0:
                index1 += 1
            else:
                index1 -= 1
        nextMatchup = Matchup(PlayerOne=players[index1], PlayerTwo=players[index2])
        return nextMatchup
    
    """
    Update the ratings of the winner and loser
    """
    def EvaluateMatchup(self, matchup):
        print(matchup)
        if matchup['PlayerOne'] == None or matchup['PlayerTwo'] == None or matchup['Winner'] == None:
            return
    
        player1 = Player.objects.get(id=matchup['PlayerOne']['id'])
        player2 = Player.objects.get(id=matchup['PlayerTwo']['id'])

        rePlayer1 = rankingsEngine.Player(player1.id, player1.Rating, player1.Deviation, player1.Volatility)
        rePlayer2 = rankingsEngine.Player(player2.id, player2.Rating, player2.Deviation, player2.Volatility)

        if matchup['PlayerOne']['id'] == matchup['Winner']['id']:
            rePlayer1.update_player([rePlayer2.rating], [rePlayer2.rd], [1])
            rePlayer2.update_player([rePlayer1.rating], [rePlayer1.rd], [0])
        elif matchup['PlayerTwo']['id'] == matchup['Winner']['id']:
            rePlayer1.update_player([rePlayer2.rating], [rePlayer2.rd], [0])
            rePlayer2.update_player([rePlayer1.rating], [rePlayer1.rd], [1])
        
        player1.Rating = rePlayer1.rating
        player1.Deviation = rePlayer1.rd
        player1.Volatility = rePlayer1.vol

        player2.Rating = rePlayer2.rating
        player2.Deviation = rePlayer2.rd
        player2.Volatility = rePlayer2.vol

        player1.save()
        player2.save()

class MatchupsView(APIView):

    """
    internal method to get single matchup by id
    """
    def get_object(self, pk):
        try:
            return Matchup.objects.get(id=pk)
        except Matchup.DoesNotExist:
            raise Http404

    """
    Get single matchup by id
    """
    def get(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        serializer = MatchupSerializer(matchup, many=False)
        print(serializer.data)
        return Response(serializer.data)

    """
    update a matchup
    """
    def put(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        serializer = PlayerSerializer(matchup, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Partial Update a matchup (eg. change winner)
    """
    def patch(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        serializer = PlayerSerializer(self.kwargs['pk'], data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Delete matchup by id
    """
    def delete(self, request, *args, **kwargs):
        matchup = self.get_object(self.kwargs['pk'])
        matchup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)