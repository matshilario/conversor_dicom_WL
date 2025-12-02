#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar arquivo .img e extrair informações DICOM
"""

import pydicom
import os
import sys

# Configurar codificação UTF-8 para o console Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

current_dir = os.path.dirname(os.path.abspath(__file__))
img_file = os.path.join(current_dir, "DCM4_Processed.img")

print("="*80)
print("ANALISE DO ARQUIVO DCM4_Processed.img")
print("="*80)

print(f"\nArquivo: {img_file}")
print(f"Tamanho: {os.path.getsize(img_file) / 1024:.2f} KB")

# Tentar ler como DICOM sem header
print("\n" + "="*80)
print("Tentando ler como arquivo DICOM...")
print("="*80)

try:
    # Primeiro tentar sem force
    print("\nTentativa 1: Leitura normal...")
    ds = pydicom.dcmread(img_file)
    print("✓ Arquivo lido com sucesso!")
except Exception as e1:
    print(f"✗ Falhou: {str(e1)}")

    try:
        # Tentar com force=True (ignora falta de header DICM)
        print("\nTentativa 2: Leitura forçada (force=True)...")
        ds = pydicom.dcmread(img_file, force=True)
        print("✓ Arquivo lido com sucesso usando force=True!")
    except Exception as e2:
        print(f"✗ Falhou: {str(e2)}")
        ds = None

if ds:
    print("\n" + "="*80)
    print("INFORMACOES EXTRAIDAS DO ARQUIVO")
    print("="*80)

    # Informações do paciente
    print("\nINFORMACOES DO PACIENTE:")
    print(f"  Nome: {getattr(ds, 'PatientName', 'N/A')}")
    print(f"  ID: {getattr(ds, 'PatientID', 'N/A')}")
    print(f"  Data de Nascimento: {getattr(ds, 'PatientBirthDate', 'N/A')}")
    print(f"  Sexo: {getattr(ds, 'PatientSex', 'N/A')}")

    # Informações do estudo
    print("\nINFORMACOES DO ESTUDO:")
    print(f"  Modalidade: {getattr(ds, 'Modality', 'N/A')}")
    print(f"  Descricao do Estudo: {getattr(ds, 'StudyDescription', 'N/A')}")
    print(f"  Data do Estudo: {getattr(ds, 'StudyDate', 'N/A')}")
    print(f"  Hora do Estudo: {getattr(ds, 'StudyTime', 'N/A')}")
    print(f"  Study Instance UID: {getattr(ds, 'StudyInstanceUID', 'N/A')}")

    # Informações da série
    print("\nINFORMACOES DA SERIE:")
    print(f"  Descricao da Serie: {getattr(ds, 'SeriesDescription', 'N/A')}")
    print(f"  Numero da Serie: {getattr(ds, 'SeriesNumber', 'N/A')}")
    print(f"  Series Instance UID: {getattr(ds, 'SeriesInstanceUID', 'N/A')}")

    # Informações do equipamento
    print("\nINFORMACOES DO EQUIPAMENTO:")
    print(f"  Fabricante: {getattr(ds, 'Manufacturer', 'N/A')}")
    print(f"  Modelo: {getattr(ds, 'ManufacturerModelName', 'N/A')}")
    print(f"  Nome da Estacao: {getattr(ds, 'StationName', 'N/A')}")
    print(f"  Instituicao: {getattr(ds, 'InstitutionName', 'N/A')}")

    # Informações específicas de RT Image
    if hasattr(ds, 'RTImageLabel'):
        print("\nINFORMACOES DE RT IMAGE:")
        print(f"  RT Image Label: {getattr(ds, 'RTImageLabel', 'N/A')}")
        print(f"  RT Image Description: {getattr(ds, 'RTImageDescription', 'N/A')}")
        print(f"  RT Image Name: {getattr(ds, 'RTImageName', 'N/A')}")

    # Informações da imagem
    print("\nINFORMACOES DA IMAGEM:")
    print(f"  Linhas: {getattr(ds, 'Rows', 'N/A')}")
    print(f"  Colunas: {getattr(ds, 'Columns', 'N/A')}")
    print(f"  Bits Alocados: {getattr(ds, 'BitsAllocated', 'N/A')}")
    print(f"  Interpretacao Fotometrica: {getattr(ds, 'PhotometricInterpretation', 'N/A')}")

    # SOP Class
    print("\nINFORMACOES TECNICAS:")
    print(f"  SOP Class UID: {getattr(ds, 'SOPClassUID', 'N/A')}")
    print(f"  SOP Instance UID: {getattr(ds, 'SOPInstanceUID', 'N/A')}")

    # Identificar tipo de SOP Class
    sop_class = getattr(ds, 'SOPClassUID', '')
    if '481.1' in sop_class:
        print(f"  Tipo: RT Image Storage")
    elif '481.2' in sop_class:
        print(f"  Tipo: RT Dose Storage")
    elif '481.5' in sop_class:
        print(f"  Tipo: RT Plan Storage")

    # Salvar informações em arquivo de texto
    output_file = os.path.join(current_dir, "analise_img_dicom.txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("ANALISE DO ARQUIVO DCM4_Processed.img\n")
        f.write("="*80 + "\n\n")

        f.write("INFORMACOES DO PACIENTE:\n")
        f.write(f"  Nome: {getattr(ds, 'PatientName', 'N/A')}\n")
        f.write(f"  ID: {getattr(ds, 'PatientID', 'N/A')}\n")
        f.write(f"  Data de Nascimento: {getattr(ds, 'PatientBirthDate', 'N/A')}\n")
        f.write(f"  Sexo: {getattr(ds, 'PatientSex', 'N/A')}\n\n")

        f.write("INFORMACOES DO ESTUDO:\n")
        f.write(f"  Modalidade: {getattr(ds, 'Modality', 'N/A')}\n")
        f.write(f"  Data: {getattr(ds, 'StudyDate', 'N/A')}\n")
        f.write(f"  Hora: {getattr(ds, 'StudyTime', 'N/A')}\n")
        f.write(f"  Study UID: {getattr(ds, 'StudyInstanceUID', 'N/A')}\n\n")

        f.write("EQUIPAMENTO:\n")
        f.write(f"  Fabricante: {getattr(ds, 'Manufacturer', 'N/A')}\n")
        f.write(f"  Modelo: {getattr(ds, 'ManufacturerModelName', 'N/A')}\n\n")

        f.write("TIPO DE ARQUIVO:\n")
        f.write(f"  Este e um arquivo de imagem portal (RT Image)\n")
        f.write(f"  do sistema Elekta iView\n")

    print(f"\n\nRelatorio salvo em: {output_file}")

    # Tentar converter para DICOM padrão
    print("\n" + "="*80)
    print("CONVERTENDO PARA FORMATO DICOM PADRAO")
    print("="*80)

    output_dcm = os.path.join(current_dir, "DCM4_Processed_converted.dcm")
    try:
        ds.save_as(output_dcm)
        print(f"\n✓ Arquivo convertido salvo em: DCM4_Processed_converted.dcm")
        print(f"  Agora voce pode abrir este arquivo em qualquer visualizador DICOM")
    except Exception as e:
        print(f"\n✗ Erro ao salvar: {str(e)}")

else:
    print("\n✗ Nao foi possivel ler o arquivo como DICOM")
    print("\nO arquivo pode estar em um formato proprietario ou corrompido.")
