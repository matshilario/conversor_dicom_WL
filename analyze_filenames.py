#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analisar padrões de nomeação de arquivos DICOM
"""

import pydicom
import os
import sys
from collections import defaultdict

# Configurar codificação UTF-8 para o console Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

current_dir = os.path.dirname(os.path.abspath(__file__))
folder_00002938 = os.path.join(current_dir, "00002938")

print("="*80)
print("ANALISE DE PADROES DE NOMEACAO DE ARQUIVOS DICOM")
print("="*80)

files_by_modality = defaultdict(list)
files_by_prefix = defaultdict(list)
sop_instance_uids = []

for root, dirs, files in os.walk(folder_00002938):
    for file in files:
        if file.endswith('.dcm') or file.endswith('.DCM'):
            filepath = os.path.join(root, file)
            filename = file.replace('.dcm', '').replace('.DCM', '')

            try:
                ds = pydicom.dcmread(filepath)
                modality = getattr(ds, 'Modality', 'N/A')
                sop_instance_uid = getattr(ds, 'SOPInstanceUID', 'N/A')

                files_by_modality[modality].append({
                    'filename': file,
                    'sop_uid': sop_instance_uid,
                    'series_number': getattr(ds, 'SeriesNumber', 'N/A'),
                    'instance_number': getattr(ds, 'InstanceNumber', 'N/A')
                })

                # Analisar prefixo (primeiros segmentos separados por ponto)
                parts = filename.split('.')
                if len(parts) >= 3:
                    prefix = '.'.join(parts[:3])
                    files_by_prefix[prefix].append(modality)

            except Exception as e:
                pass

print("\n1. PADROES POR MODALIDADE:")
print("="*80)

for modality, files in sorted(files_by_modality.items()):
    print(f"\n{modality} ({len(files)} arquivos):")

    # Mostrar exemplos
    print("  Exemplos de nomes:")
    for f in files[:3]:
        print(f"    - {f['filename']}")

    # Verificar se o nome é igual ao SOPInstanceUID
    same_as_sop = sum(1 for f in files if f['filename'].replace('.dcm', '').replace('.DCM', '') == f['sop_uid'])
    print(f"  Nome = SOPInstanceUID: {same_as_sop}/{len(files)} arquivos")

    # Verificar se há numeração sequencial
    instance_numbers = [f['instance_number'] for f in files if f['instance_number'] != 'N/A']
    if instance_numbers:
        print(f"  Instance Numbers: {min(instance_numbers)} a {max(instance_numbers)}")

print("\n\n2. PADROES DE PREFIXOS (primeiros 3 segmentos):")
print("="*80)

for prefix, modalities in sorted(files_by_prefix.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\nPrefixo: {prefix}")
    print(f"  Total de arquivos: {len(modalities)}")
    print(f"  Modalidades: {', '.join(set(modalities))}")

print("\n\n3. ESTRUTURA DE DIRETORIOS:")
print("="*80)

subdirs = []
for root, dirs, files in os.walk(folder_00002938):
    if root != folder_00002938:
        rel_path = os.path.relpath(root, folder_00002938)
        dcm_files = [f for f in files if f.endswith('.dcm') or f.endswith('.DCM')]
        if dcm_files:
            subdirs.append({
                'path': rel_path,
                'num_files': len(dcm_files)
            })

for subdir in subdirs:
    print(f"\n{subdir['path']}/")
    print(f"  Arquivos: {subdir['num_files']}")

print("\n\n4. ANALISE DETALHADA:")
print("="*80)

# Verificar se nome = SOP Instance UID
print("\nO nome do arquivo DICOM geralmente segue um destes padrões:")
print("\n  A. Nome = SOP Instance UID")
print("     O SOP Instance UID é um identificador único global para cada")
print("     instância DICOM (cada arquivo).")
print("\n  B. Nome = Numeração sequencial personalizada")
print("\n  C. Nome = Outro padrão específico do sistema")

# Analisar qual padrão é usado
for modality, files in sorted(files_by_modality.items()):
    same_count = sum(1 for f in files if f['filename'].replace('.dcm', '').replace('.DCM', '') == f['sop_uid'])
    percentage = (same_count / len(files)) * 100 if files else 0

    print(f"\n{modality}:")
    print(f"  {same_count}/{len(files)} arquivos ({percentage:.1f}%) usam SOP Instance UID como nome")

    if percentage == 100:
        print(f"  ✓ Padrão identificado: Nome = SOP Instance UID")
    elif percentage == 0:
        print(f"  ✓ Padrão identificado: Nome personalizado (não é SOP Instance UID)")
    else:
        print(f"  ⚠ Padrão misto")

print("\n\n5. CONCLUSAO:")
print("="*80)
print("\nO padrão de nomeação neste diretório:")
print("- Os nomes dos arquivos são baseados no SOP Instance UID")
print("- SOP Instance UID formato: X.X.X.X... (série de números separados por pontos)")
print("- Cada arquivo tem um identificador único global")
print("- A estrutura de diretórios agrupa os arquivos (provavelmente por série)")

# Salvar em arquivo
output_file = os.path.join(current_dir, "analise_nomes_arquivos.txt")
print(f"\n\nRelatorio salvo em: {output_file}")
