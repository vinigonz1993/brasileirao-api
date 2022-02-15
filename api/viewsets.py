from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import mixins
from urllib.request import urlopen
from bs4 import BeautifulSoup


class TeamsViewSet(APIView):

    def get(self, request):
        html = urlopen(f"https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/{request.GET.get('year', '')}")
        bs = BeautifulSoup(html, "html.parser")

        linhas = bs.find_all('tr', {'class': 'expand-trigger'})
        obj = []

        for l in linhas:
            filhas = l.findChildren('td')
            text = (filhas[0].text).replace('\n', '')
            pos = text.split('º')
            obj.append({
                'name': pos[1].split(' -')[0],
                'pos': pos[0],
                'pts': filhas[1].text,
                'v': filhas[1].text,
                'e': filhas[2].text,
                'd': filhas[3].text
            })

        return Response(obj)


class SeasonsViewSet(APIView):

    def get(self, request):
        html = urlopen("https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a")
        bs = BeautifulSoup(html, "html.parser")

        linhas = bs.find_all('select', {'id': 'years'})
        obj = []

        for l in linhas:
            filhas = l.findChildren('option')
            for f in filhas:
                obj.append({
                    'year': f.text
                })


        return Response(obj)