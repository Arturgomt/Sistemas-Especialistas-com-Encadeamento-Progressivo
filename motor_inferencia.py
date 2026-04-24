import json
import operator

class MotorInferencia:
    def __init__(self, caminho_regras):
        try:
            with open(caminho_regras, 'r', encoding='utf-8') as f:
                self.base = json.load(f)
        except:
            self.base = {"niveis": []}
        
        # Mapeamento para processar regras como dados (sem if-else)
        self.operadores = {
            "==": operator.eq,
            "<": operator.lt,
            ">": operator.gt,
            ">=": operator.ge,
            "<=": operator.le
        }

    def avaliar_condicao(self, condicao, leitura):
        campo = condicao['campo']
        valor_paciente = leitura.get(campo)
        if valor_paciente is None: return False
        
        op_func = self.operadores.get(condicao['operador'])
        return op_func(valor_paciente, condicao['valor'])

    def processar_paciente(self, paciente):
        p_id = paciente.get('id', 'Desconhecido')
        logs = []
        
        # Inicialização da Memória de Trabalho [cite: 67]
        paciente['prioridade_atual'] = 5
        paciente['cor'] = "Azul"
        
        if not paciente.get('leituras'): return paciente, logs
        ultima_leitura = paciente['leituras'][-1]

        # Encadeamento Progressivo: busca nível baseado nos dados [cite: 19, 69]
        for nivel in self.base.get('niveis', []):
            # Se QUALQUER condição do nível for atingida (disparo de regra)
            if any(self.avaliar_condicao(c, ultima_leitura) for c in nivel.get('condicoes', [])):
                prio_nova = nivel['prioridade']
                if prio_nova < paciente['prioridade_atual']:
                    paciente['prioridade_atual'] = prio_nova
                    paciente['cor'] = nivel['cor']
                    logs.append(f"[{p_id}] Classificado como {nivel['nome']} ({nivel['cor']}).")
                break

        # Regra de Grupos Vulneráveis (Resolução SUS 2017) [cite: 31, 32]
        if (paciente.get('idade', 0) >= 60 or paciente.get('gestante') or paciente.get('deficiencia')):
            if paciente['prioridade_atual'] > 1:
                paciente['prioridade_atual'] -= 1
                logs.append(f"[{p_id}] Upgrade de prioridade: Paciente pertence a grupo vulneravel.")

        return paciente, logs