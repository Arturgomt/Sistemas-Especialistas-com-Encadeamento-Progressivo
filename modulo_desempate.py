class ModuloDesempate:
    @staticmethod
    def resolver(paciente_a, paciente_b):
        """
        Critério Próprio: Pontuação de Risco Agregado (PRA).
        Justificativa: Prioriza o risco objetivo de morte sobre o tempo de espera.
        """
        # Exemplo para o Cenário E2: Velocidade de piora [cite: 52]
        ponto_a = 0
        ponto_b = 0
        
        # Se houve piora clínica (Cenário E2/E3), soma pontos
        if ModuloDesempate.detectar_piora(paciente_b): ponto_b += 50
        
        # Se for vulnerável (Equidade), soma pontos
        if paciente_a['idade'] >= 60: ponto_a += 20
        
        return paciente_a if ponto_a >= ponto_b else paciente_b

    @staticmethod
    def detectar_piora(paciente):
        if len(paciente['leituras']) < 2: return False
        # Lógica para comparar as duas últimas leituras
        return paciente['leituras'][-1]['spo2'] < paciente['leituras'][-2]['spo2']