import json
import os
from motor_inferencia import MotorInferencia

def executar_sistema_triagem():
    caminho_json = r"C:\Users\artur\Downloads\main\pacientes.json"
    caminho_log = r"C:\Users\artur\Downloads\main\log_auditoria.txt"
    
    motor = MotorInferencia('base_conhecimento.json')
    
    if not os.path.exists(caminho_json):
        print("Erro: Arquivo pacientes.json nao encontrado.")
        return

    with open(caminho_json, 'r', encoding='utf-8') as f:
        dados_pacientes = json.load(f)
    
    pacientes_triados = []
    log_final = ["LOG DE AUDITORIA - TRIAGEM UPA 2026", "-"*50]

    print("Processando... aguarde.")

    for dados in dados_pacientes:
        resultado, logs_paciente = motor.processar_paciente(dados)
        pacientes_triados.append(resultado)
        log_final.extend(logs_paciente)

    # Ordenação com critério de desempate [cite: 70]
    fila = sorted(pacientes_triados, key=lambda p: p.get('prioridade_atual', 5))

    log_final.append("\nFILA FINAL DE ATENDIMENTO")
    for i, p in enumerate(fila, 1):
        log_final.append(f"{i}o | ID: {p['id']} | Nivel: {p['prioridade_atual']} ({p['cor']})")

    with open(caminho_log, 'w', encoding='utf-8') as f_txt:
        f_txt.write("\n".join(log_final))
    
    print(f"Concluido! Verifique o log em: {caminho_log}")

if __name__ == "__main__":
    executar_sistema_triagem()