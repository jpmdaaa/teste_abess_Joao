from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import datetime, timedelta
import requests
import logging
from .models import Cotacao
from .serializers import CotacaoSerializer

logger = logging.getLogger(__name__)

class CotacaoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cotacao.objects.all()
    serializer_class = CotacaoSerializer

    @action(detail=False, methods=['get'])
    def buscar(self, request):
        moeda = request.query_params.get('moeda', 'BRL').upper()
        dias = int(request.query_params.get('dias', 5))
        
        # Verifica se a moeda é válida
        moedas_validas = ['BRL', 'EUR', 'JPY']
        if moeda not in moedas_validas:
            return Response(
                {'error': f'Moeda inválida. Use uma das seguintes: {", ".join(moedas_validas)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se ja existe dados no banco os parametros solicitados
        data_inicio = datetime.now().date() - timedelta(days=dias)
        cotacoes_existentes = Cotacao.objects.filter(
            moeda=moeda,
            data__gte=data_inicio
        ).order_by('-data')

        if cotacoes_existentes.count() >= dias:
            serializer = self.get_serializer(cotacoes_existentes[:dias], many=True)
            return Response(serializer.data)

        # Se n houver dados suficientes no banco busca na API externa
        cotacoes = []
        data_atual = datetime.now()
        coletados = 0

        while coletados < dias:
            if data_atual.weekday() < 5:  # Dia util (0-4 = segunda a sexta)
                data_formatada = data_atual.strftime("%Y-%m-%d")
                
                # Verifica se ja existe no banco
                cotacao_existente = Cotacao.objects.filter(
                    moeda=moeda,
                    data=data_atual.date()
                ).first()

                if cotacao_existente:
                    cotacoes.append(cotacao_existente)
                    coletados += 1
                else:
                    try:
                        response = requests.get(
                            f"https://api.vatcomply.com/rates?date={data_formatada}&base=USD",
                            timeout=5
                        )
                        response.raise_for_status()
                        
                        data = response.json()
                        taxa = data["rates"].get(moeda)
                        
                        if taxa:
                            cotacao = Cotacao.objects.create(
                                moeda=moeda,
                                data=data_atual.date(),
                                valor=taxa
                            )
                            cotacoes.append(cotacao)
                            coletados += 1
                            
                    except requests.exceptions.RequestException as e:
                        logger.error(f"Erro ao buscar cotação: {str(e)}")
                    except KeyError as e:
                        logger.error(f"Erro ao processar resposta da API: {str(e)}")

            data_atual -= timedelta(days=1)

        serializer = self.get_serializer(cotacoes, many=True)
        return Response(serializer.data)