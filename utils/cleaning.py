import pandas as pd
from pathlib import Path
import csv
from io import StringIO

def fix_unclosed_quotes(line: str) -> str:
    """
    Corrige aspas não fechadas em uma linha
    """
    # Contar aspas na linha
    quote_count = line.count('"')
    
    # Se o número de aspas é ímpar, significa que há uma aspa não fechada
    if quote_count % 2 == 1:
        # Adicionar uma aspa no final da linha (antes da quebra de linha)
        line = line.rstrip() + '"'
    
    return line

def fix_data_structure(file_path: Path) -> Path:
    """
    Corrige problemas de estrutura no arquivo CSV:
    1. Aspas não fechadas
    2. Remove "Extremamente Negativo" da posição incorreta e adiciona ,, no lugar
    """
    # Ler o arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    print("📋 Cabeçalho original:")
    header = content.split('\n')[0]
    print(header)
    print(f"Colunas esperadas: {len(header.split(','))}")

    # Correções simples e eficazes:
    # 1. Corrigir aspas não fechadas
    # 2. Substituir "Extremamente Negativo" por vírgula vazia (,)
    lines = content.split('\n')
    corrected_lines = []
    changes_made = 0

    for i, line in enumerate(lines):
        if i == 0:  # Header
            corrected_lines.append(line)
            continue
        
        if line.strip():  # Ignorar linhas vazias
            # Corrigir aspas não fechadas
            corrected_line = fix_unclosed_quotes(line)
            
            # "Extremamente Negativo" por vírgula
            if 'Extremamente Negativo' in corrected_line:
                corrected_line = corrected_line.replace('Extremamente Negativo', ',')
                changes_made += 1
            
            corrected_lines.append(corrected_line)
        else:
            corrected_lines.append(line)

    print(f"\n✅ Linhas corrigidas: {changes_made}")

    # Salvar arquivo corrigido
    save_path = file_path.parent / "02_churn_fixed.csv"
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(corrected_lines))
    
    return save_path