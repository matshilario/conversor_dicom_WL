#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ler arquivos DICOM e extrair informações relevantes dos pacientes
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
    return date_str


def format_time(time_str):
    """Formata hora DICOM (HHMMSS.ffffff) para formato legível"""
    if time_str:
        try:
            # Remove microsegundos se existirem
            time_str = str(time_str).split('.')[0]
            if len(time_str) >= 6:
                return f"{time_str[0:2]}:{time_str[2:4]}:{time_str[4:6]}"
            elif len(time_str) >= 4:
                return f"{time_str[0:2]}:{time_str[2:4]}"
        except:
            return time_str
    return time_str


def get_dicom_info(filepath):
    """Extrai informações relevantes de um arquivo DICOM"""
    try:
        ds = pydicom.dcmread(filepath)

        info = {
            'arquivo': os.path.basename(filepath),
            'caminho': filepath
        }

        # Informações do Paciente
        info['nome_paciente'] = getattr(ds, 'PatientName', 'N/A')
        info['id_paciente'] = getattr(ds, 'PatientID', 'N/A')
        info['data_nascimento'] = format_date(getattr(ds, 'PatientBirthDate', ''))
        info['sexo'] = getattr(ds, 'PatientSex', 'N/A')
        info['idade'] = getattr(ds, 'PatientAge', 'N/A')

        # Informações do Estudo
        info['modalidade'] = getattr(ds, 'Modality', 'N/A')
        info['descricao_estudo'] = getattr(ds, 'StudyDescription', 'N/A')
        info['data_estudo'] = format_date(getattr(ds, 'StudyDate', ''))
        info['hora_estudo'] = format_time(getattr(ds, 'StudyTime', ''))
        info['study_instance_uid'] = getattr(ds, 'StudyInstanceUID', 'N/A')

        # Informações da Série
        info['descricao_serie'] = getattr(ds, 'SeriesDescription', 'N/A')
        info['numero_serie'] = getattr(ds, 'SeriesNumber', 'N/A')
        info['data_serie'] = format_date(getattr(ds, 'SeriesDate', ''))

        # Informações do Equipamento
        info['fabricante'] = getattr(ds, 'Manufacturer', 'N/A')
        info['modelo'] = getattr(ds, 'ManufacturerModelName', 'N/A')
        info['instituicao'] = getattr(ds, 'InstitutionName', 'N/A')

        # Informações Técnicas
        info['sop_class_uid'] = getattr(ds, 'SOPClassUID', 'N/A')
        info['instance_number'] = getattr(ds, 'InstanceNumber', 'N/A')

        return info, ds

    except Exception as e:
        return {'erro': str(e), 'arquivo': filepath}, None


def print_dicom_info(info):
    """Imprime informações DICOM de forma formatada"""
    print("\n" + "="*80)
    print(f"ARQUIVO: {info.get('arquivo', 'N/A')}")
    print("="*80)

    if 'erro' in info:
        print(f"ERRO ao ler arquivo: {info['erro']}")
        return

    print("\nINFORMACOES DO PACIENTE:")
    print(f"  Nome: {info['nome_paciente']}")
    print(f"  ID: {info['id_paciente']}")
    print(f"  Data de Nascimento: {info['data_nascimento']}")
    print(f"  Sexo: {info['sexo']}")
    print(f"  Idade: {info['idade']}")

    print("\nINFORMACOES DO ESTUDO:")
    print(f"  Modalidade: {info['modalidade']}")
    print(f"  Descrição: {info['descricao_estudo']}")
    print(f"  Data: {info['data_estudo']}")
    print(f"  Hora: {info['hora_estudo']}")
    print(f"  Study UID: {info['study_instance_uid']}")

    print("\nINFORMACOES DA SERIE:")
    print(f"  Descrição: {info['descricao_serie']}")
    print(f"  Número: {info['numero_serie']}")
    print(f"  Data: {info['data_serie']}")

    print("\nINFORMACOES DO EQUIPAMENTO:")
    print(f"  Fabricante: {info['fabricante']}")
    print(f"  Modelo: {info['modelo']}")
    print(f"  Instituição: {info['instituicao']}")

    print("\nINFORMACOES TECNICAS:")
    print(f"  SOP Class UID: {info['sop_class_uid']}")
    print(f"  Instance Number: {info['instance_number']}")


def find_dicom_files(directory):
    """Encontra todos os arquivos DICOM em um diretório"""
    dicom_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.dcm') or file.endswith('.DCM'):
                dicom_files.append(os.path.join(root, file))
    return dicom_files


def main():
    # Diretório atual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("Procurando arquivos DICOM...")
    dicom_files = find_dicom_files(current_dir)

    if not dicom_files:
        print("Nenhum arquivo DICOM encontrado!")
        return

    print(f"Encontrados {len(dicom_files)} arquivos DICOM\n")

    # Processar apenas o primeiro arquivo para resumo inicial
    print("Informacoes do primeiro arquivo DICOM:")
    info, ds = get_dicom_info(dicom_files[0])
    print_dicom_info(info)

    # Perguntar se deseja ver todos os arquivos
    if len(dicom_files) > 1:
        print("\n" + "="*80)
        resposta = input(f"\nDeseja visualizar todos os {len(dicom_files)} arquivos? (s/n): ")
        if resposta.lower() == 's':
            for filepath in dicom_files[1:]:
                info, ds = get_dicom_info(filepath)
                print_dicom_info(info)
        else:
            print("\nRESUMO DE TODOS OS ARQUIVOS:")
            print("="*80)
            # Agrupar por paciente
            pacientes = {}
            for filepath in dicom_files:
                info, ds = get_dicom_info(filepath)
                if 'erro' not in info:
                    patient_id = info['id_paciente']
                    if patient_id not in pacientes:
                        pacientes[patient_id] = {
                            'nome': info['nome_paciente'],
                            'arquivos': 0,
                            'modalidades': set(),
                            'estudos': set()
                        }
                    pacientes[patient_id]['arquivos'] += 1
                    pacientes[patient_id]['modalidades'].add(info['modalidade'])
                    pacientes[patient_id]['estudos'].add(info['descricao_estudo'])

            for patient_id, data in pacientes.items():
                print(f"\nPaciente: {data['nome']} (ID: {patient_id})")
                print(f"  Total de arquivos: {data['arquivos']}")
                print(f"  Modalidades: {', '.join(data['modalidades'])}")
                print(f"  Estudos: {', '.join(data['estudos'])}")


if __name__ == "__main__":
    main()
