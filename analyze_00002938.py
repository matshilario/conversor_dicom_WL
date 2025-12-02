#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar arquivos DICOM da pasta 00002938
"""

import pydicom
import os
import sys
from pathlib import Path
from datetime import datetime

# Configurar codificação UTF-8 para o console Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


def format_date(date_str):
    """Formata data DICOM (YYYYMMDD) para formato legível"""
    if date_str and len(date_str) == 8:
        try:
            return datetime.strptime(date_str, "%Y%m%d").strftime("%d/%m/%Y")
        except:
            return date_str
    return date_str or 'N/A'


def find_dicom_files(directory):
    """Encontra todos os arquivos DICOM em um diretório"""
    dicom_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.dcm') or file.endswith('.DCM'):
                dicom_files.append(os.path.join(root, file))
    return dicom_files


def analyze_folder(folder_path):
    """Analisa pasta específica para verificar se há apenas um paciente"""

    print("="*80)
    print(f"ANALISE DA PASTA: {folder_path}")
    print("="*80)

    dicom_files = find_dicom_files(folder_path)

    if not dicom_files:
        print("\nNenhum arquivo DICOM encontrado nesta pasta!")
        return None

    print(f"\nTotal de arquivos DICOM encontrados: {len(dicom_files)}")

    # Coletar informações de todos os arquivos
    pacientes = {}
    modalidades = set()
    estudos = set()
    series = set()

    for filepath in dicom_files:
        try:
            ds = pydicom.dcmread(filepath)

            # Informações do paciente
            patient_name = str(getattr(ds, 'PatientName', 'N/A'))
            patient_id = str(getattr(ds, 'PatientID', 'N/A'))
            patient_birth = format_date(getattr(ds, 'PatientBirthDate', ''))
            patient_sex = getattr(ds, 'PatientSex', 'N/A') or 'N/A'

            # Informações do estudo
            modality = getattr(ds, 'Modality', 'N/A') or 'N/A'
            study_desc = getattr(ds, 'StudyDescription', 'N/A') or 'N/A'
            study_uid = getattr(ds, 'StudyInstanceUID', 'N/A') or 'N/A'
            series_desc = getattr(ds, 'SeriesDescription', 'N/A') or 'N/A'
            series_uid = getattr(ds, 'SeriesInstanceUID', 'N/A') or 'N/A'

            # Agrupar por paciente
            if patient_id not in pacientes:
                pacientes[patient_id] = {
                    'nome': patient_name,
                    'nascimento': patient_birth,
                    'sexo': patient_sex,
                    'arquivos': 0,
                    'modalidades': set(),
                    'estudos': set(),
                    'series': set(),
                    'study_uids': set(),
                    'series_uids': set()
                }

            pacientes[patient_id]['arquivos'] += 1
            pacientes[patient_id]['modalidades'].add(modality)
            pacientes[patient_id]['estudos'].add(study_desc)
            pacientes[patient_id]['series'].add(series_desc)
            pacientes[patient_id]['study_uids'].add(study_uid)
            pacientes[patient_id]['series_uids'].add(series_uid)

            modalidades.add(modality)
            estudos.add(study_desc)
            series.add(series_desc)

        except Exception as e:
            print(f"Erro ao ler arquivo {os.path.basename(filepath)}: {str(e)}")

    # Análise dos resultados
    print("\n" + "="*80)
    print("RESULTADO DA ANALISE")
    print("="*80)

    num_pacientes = len(pacientes)

    if num_pacientes == 0:
        print("\nNENHUM PACIENTE IDENTIFICADO (todos os arquivos falharam)")
        return None

    elif num_pacientes == 1:
        print("\n✓ SIM - Todos os arquivos se referem a UMA UNICA PACIENTE")
        print("\nDetalhes da paciente:")

        for patient_id, data in pacientes.items():
            print(f"\n  Nome: {data['nome']}")
            print(f"  ID: {patient_id}")
            print(f"  Data de Nascimento: {data['nascimento']}")
            print(f"  Sexo: {data['sexo']}")
            print(f"\n  Total de arquivos: {data['arquivos']}")
            print(f"  Modalidades: {', '.join(sorted(data['modalidades']))}")
            print(f"  Numero de estudos: {len(data['study_uids'])}")
            print(f"  Numero de series: {len(data['series_uids'])}")

            print(f"\n  Descricoes dos estudos:")
            for estudo in sorted(data['estudos']):
                print(f"    - {estudo}")

            print(f"\n  Descricoes das series:")
            for serie in sorted(data['series']):
                print(f"    - {serie}")

        return True

    else:
        print(f"\n✗ NAO - Encontrados {num_pacientes} PACIENTES DIFERENTES nesta pasta:")

        for patient_id, data in pacientes.items():
            print(f"\n  Paciente: {data['nome']}")
            print(f"  ID: {patient_id}")
            print(f"  Arquivos: {data['arquivos']}")

        return False


def save_to_file(folder_path, output_file):
    """Salva análise em arquivo de texto"""

    # Redirecionar saída para arquivo
    original_stdout = sys.stdout

    with open(output_file, 'w', encoding='utf-8') as f:
        sys.stdout = f
        analyze_folder(folder_path)

    sys.stdout = original_stdout

    print(f"\nRelatorio salvo em: {output_file}")


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_00002938 = os.path.join(current_dir, "00002938")
    output_file = os.path.join(current_dir, "analise_paciente_00002938.txt")

    # Mostrar na tela
    result = analyze_folder(folder_00002938)

    # Salvar em arquivo
    print("\n" + "="*80)
    print("Salvando relatorio em arquivo...")
    save_to_file(folder_00002938, output_file)

    print("\nConcluido!")
