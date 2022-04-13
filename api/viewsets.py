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
            pontuacao = l.findChildren('th')
            text = (filhas[0].text).replace('\n', '')
            pos = text.split('º')
            name = pos[1].split(' -')[0]
            obj.append({
                'name': name.replace('0', ''),
                'pos': pos[0],
                'pts': pontuacao[0].text,
                'v': filhas[2].text,
                'e': filhas[3].text,
                'd': filhas[4].text,
                'img': filhas[0].img['src']
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


class RoundsViewSet(APIView):

    def get(self, request):
        qp = int(request.GET.get('rodada', 1))
        html = urlopen("https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a")
        bs = BeautifulSoup(html, "html.parser")

        linhas = bs.find_all('aside', {'class': 'aside-rodadas'})
        rounds = linhas[0].findChildren('ul')
        ronda = rounds[qp - 1].find_all('li')
        obj = []


        for r in ronda:
            sigla = r.findChildren('span', attrs={'class': 'time-sigla'})
            divs = r.findChildren('div')[0].findChildren('div')
            desc = r.findChildren('span', attrs={'class': 'partida-desc'})
            try:
                descricao = {
                    'data': desc[0].text.split('\r\n')[1].strip(),
                    'local': desc[1].text.split('\r\n')[1].strip().split('\n')[0].strip()
                }
            except:
                descricao = {
                    'data': 'Sem definição',
                    'local': 'Sem definição'
                }

            try:
                placar = r.findChildren(
                    'strong', attrs={'class': 'partida-horario'}
                )[0].text.split('\r\n')[0].strip().replace('\n', '')
                if not placar:
                    placar = '- x -'
            except:
                placar = '- x -'
            obj.append({
                'data': descricao['data'] if descricao else 'Sem definição',
                'local': descricao['local'] if descricao else 'Sem definição',
                'home': {
                    'nick': sigla[0].text,
                    'img': divs[1].img['src']
                },
                'away': {
                    'nick': sigla[1].text,
                    'img': divs[2].img['src']
                },
                'score': placar
            })


        return Response(obj)