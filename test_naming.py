#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste da função de nomeação automática
"""

import pydicom
import os
import sys

# Configurar codificação UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def generate_output_filename(ds, input_path):
    """Gerar nome de arquivo baseado nos campos DICOM"""
    output_dir = os.path.dirname(input_path)

    # Tentar obter descrição da série (prioridade 1)
    series_desc = str(getattr(ds, 'SeriesDescription', '')).strip()

    # Tentar obter RT Image Label (prioridade 2)
    rt_label = str(getattr(ds, 'RTImageLabel', '')).strip()

    # Tentar obter Patient ID (fallback 1)
    patient_id = str(getattr(ds, 'PatientID', '')).strip()

    # Tentar obter Study Date (fallback 2)
    study_date = str(getattr(ds, 'StudyDate', '')).strip()

    print(f"Series Description: '{series_desc}'")
    print(f"RT Image Label: '{rt_label}'")
    print(f"Patient ID: '{patient_id}'")
    print(f"Study Date: '{study_date}'")

    # Escolher o nome baseado na prioridade
    filename = None

    if series_desc and series_desc != 'N/A':
        # Remover caracteres inválidos
        filename = series_desc.replace(':', '').replace('/', '_').replace('\\', '_')
        filename = filename.replace('*', '').replace('?', '').replace('"', '')
        filename = filename.replace('<', '').replace('>', '').replace('|', '')
        filename = filename.strip()
        print(f"\nUsando Series Description: '{filename}'")

    if not filename and rt_label and rt_label != 'N/A':
        filename = rt_label.replace(':', '').replace('/', '_').replace('\\', '_')
        filename = filename.replace('*', '').replace('?', '').replace('"', '')
        filename = filename.replace('<', '').replace('>', '').replace('|', '')
        filename = filename.strip()
        print(f"\nUsando RT Image Label: '{filename}'")

    if not filename and patient_id and patient_id != 'N/A':
        filename = f"{patient_id}"
        if study_date and study_date != 'N/A':
            filename += f"_{study_date}"
        print(f"\nUsando Patient ID: '{filename}'")

    # Se nenhum campo válido foi encontrado, usar nome do arquivo original
    if not filename:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        filename = f"{base_name}_converted"
        print(f"\nUsando nome original: '{filename}'")

    # Garantir que o nome não está vazio
    filename = filename.strip()
    if not filename:
        filename = "converted"

    # Adicionar extensão .dcm
    output_path = os.path.join(output_dir, f"{filename}.dcm")

    return output_path


# Testar
current_dir = os.path.dirname(os.path.abspath(__file__))
img_file = os.path.join(current_dir, "DCM4_Processed.img")

print("="*80)
print("TESTE DE GERACAO DE NOME AUTOMATICO")
print("="*80)
print(f"\nArquivo de entrada: {img_file}\n")

try:
    ds = pydicom.dcmread(img_file, force=True)
    output_name = generate_output_filename(ds, img_file)

    print(f"\n{'='*80}")
    print(f"Nome do arquivo de saída: {os.path.basename(output_name)}")
    print(f"Caminho completo: {output_name}")
    print(f"{'='*80}")

except Exception as e:
    print(f"Erro: {str(e)}")
