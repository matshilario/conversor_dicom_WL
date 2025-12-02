#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ler arquivos DICOM e extrair informações relevantes dos pacientes
Versão automática sem interação do usuário
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
    return 'N/A'


def get_dicom_info(filepath):
    """Extrai informações relevantes de um arquivo DICOM"""
    try:
        ds = pydicom.dcmread(filepath)

        info = {
            'arquivo': os.path.basename(filepath),
            'caminho': filepath
        }

        # Informações do Paciente
        info['nome_paciente'] = str(getattr(ds, 'PatientName', 'N/A'))
        info['id_paciente'] = str(getattr(ds, 'PatientID', 'N/A'))
        info['data_nascimento'] = format_date(getattr(ds, 'PatientBirthDate', ''))
        info['sexo'] = getattr(ds, 'PatientSex', 'N/A') or 'N/A'
        info['idade'] = getattr(ds, 'PatientAge', 'N/A') or 'N/A'

        # Informações do Estudo
        info['modalidade'] = getattr(ds, 'Modality', 'N/A') or 'N/A'
        info['descricao_estudo'] = getattr(ds, 'StudyDescription', 'N/A') or 'N/A'
        info['data_estudo'] = format_date(getattr(ds, 'StudyDate', ''))
        info['hora_estudo'] = format_time(getattr(ds, 'StudyTime', ''))
        info['study_instance_uid'] = getattr(ds, 'StudyInstanceUID', 'N/A') or 'N/A'

        # Informações da Série
        info['descricao_serie'] = getattr(ds, 'SeriesDescription', 'N/A') or 'N/A'
        info['numero_serie'] = getattr(ds, 'SeriesNumber', 'N/A') or 'N/A'
        info['data_serie'] = format_date(getattr(ds, 'SeriesDate', ''))

        # Informações do Equipamento
        info['fabricante'] = getattr(ds, 'Manufacturer', 'N/A') or 'N/A'
        info['modelo'] = getattr(ds, 'ManufacturerModelName', 'N/A') or 'N/A'
        info['instituicao'] = getattr(ds, 'InstitutionName', 'N/A') or 'N/A'

        # Informações Técnicas
        info['sop_class_uid'] = getattr(ds, 'SOPClassUID', 'N/A') or 'N/A'
        info['instance_number'] = getattr(ds, 'InstanceNumber', 'N/A') or 'N/A'

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
    print(f"  Descricao: {info['descricao_estudo']}")
    print(f"  Data: {info['data_estudo']}")
    print(f"  Hora: {info['hora_estudo']}")

    print("\nINFORMACOES DA SERIE:")
    print(f"  Descricao: {info['descricao_serie']}")
    print(f"  Numero: {info['numero_serie']}")
    print(f"  Data: {info['data_serie']}")

    print("\nINFORMACOES DO EQUIPAMENTO:")
    print(f"  Fabricante: {info['fabricante']}")
    print(f"  Modelo: {info['modelo']}")
    print(f"  Instituicao: {info['instituicao']}")


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

    print("="*80)
    print("LEITOR DE ARQUIVOS DICOM - Relatorio Completo")
    print("="*80)

    print("\nProcurando arquivos DICOM...")
    dicom_files = find_dicom_files(current_dir)

    if not dicom_files:
        print("Nenhum arquivo DICOM encontrado!")
        return

    print(f"Encontrados {len(dicom_files)} arquivos DICOM\n")

    # Processar todos os arquivos e agrupar por paciente
    pacientes = {}
    erros = []

    print("Processando arquivos...")
    for idx, filepath in enumerate(dicom_files, 1):
        if idx % 50 == 0:
            print(f"  Processados {idx}/{len(dicom_files)} arquivos...")

        info, ds = get_dicom_info(filepath)

        if 'erro' in info:
            erros.append(info)
        else:
            patient_id = info['id_paciente']
            if patient_id not in pacientes:
                pacientes[patient_id] = {
                    'nome': info['nome_paciente'],
                    'data_nascimento': info['data_nascimento'],
                    'sexo': info['sexo'],
                    'arquivos': [],
                    'modalidades': set(),
                    'estudos': set(),
                    'series': set(),
                    'instituicoes': set(),
                    'exemplo_info': info  # Guardar um exemplo para detalhes
                }
            pacientes[patient_id]['arquivos'].append(info['arquivo'])
            pacientes[patient_id]['modalidades'].add(info['modalidade'])
            pacientes[patient_id]['estudos'].add(info['descricao_estudo'])
            pacientes[patient_id]['series'].add(str(info['descricao_serie']))
            pacientes[patient_id]['instituicoes'].add(info['instituicao'])

    print(f"\nProcessamento concluido!\n")

    # Exibir resumo
    print("="*80)
    print("RESUMO GERAL - PACIENTES ENCONTRADOS")
    print("="*80)

    for idx, (patient_id, data) in enumerate(pacientes.items(), 1):
        print(f"\n{'='*80}")
        print(f"PACIENTE #{idx}")
        print(f"{'='*80}")
        print(f"Nome: {data['nome']}")
        print(f"ID: {patient_id}")
        print(f"Data de Nascimento: {data['data_nascimento']}")
        print(f"Sexo: {data['sexo']}")
        print(f"\nESTATISTICAS:")
        print(f"  Total de arquivos: {len(data['arquivos'])}")
        print(f"  Modalidades: {', '.join(sorted(data['modalidades']))}")
        print(f"  Numero de estudos diferentes: {len(data['estudos'])}")
        print(f"  Numero de series diferentes: {len(data['series'])}")
        print(f"  Instituicoes: {', '.join(sorted([i for i in data['instituicoes'] if i != 'N/A']))}")

        # Mostrar detalhes de um arquivo exemplo
        print(f"\nDETALHES DE UM ARQUIVO EXEMPLO:")
        exemplo = data['exemplo_info']
        print(f"  Arquivo: {exemplo['arquivo']}")
        print(f"  Modalidade: {exemplo['modalidade']}")
        print(f"  Data do estudo: {exemplo['data_estudo']}")
        print(f"  Hora do estudo: {exemplo['hora_estudo']}")
        print(f"  Descricao do estudo: {exemplo['descricao_estudo']}")
        print(f"  Fabricante: {exemplo['fabricante']}")
        print(f"  Modelo: {exemplo['modelo']}")

    # Exibir erros se houver
    if erros:
        print(f"\n{'='*80}")
        print(f"ERROS ENCONTRADOS ({len(erros)} arquivos)")
        print(f"{'='*80}")
        for erro in erros[:5]:  # Mostrar apenas os primeiros 5 erros
            print(f"  Arquivo: {erro['arquivo']}")
            print(f"  Erro: {erro['erro']}\n")
        if len(erros) > 5:
            print(f"  ... e mais {len(erros) - 5} erros")

    print(f"\n{'='*80}")
    print("FIM DO RELATORIO")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
