#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para encontrar arquivos RTPLAN na pasta 00002938
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
folder_00002938 = os.path.join(current_dir, "00002938")

print("Procurando arquivos RTPLAN na pasta 00002938...")
print("="*80)

rtplan_files = []
rtdose_files = []
rtstruct_files = []
ct_files = []

for root, dirs, files in os.walk(folder_00002938):
    for file in files:
        if file.endswith('.dcm') or file.endswith('.DCM'):
            filepath = os.path.join(root, file)
            try:
                ds = pydicom.dcmread(filepath)
                modality = getattr(ds, 'Modality', 'N/A')

                if modality == 'RTPLAN':
                    rtplan_files.append({
                        'path': filepath,
                        'file': file,
                        'label': getattr(ds, 'RTPlanLabel', 'N/A'),
                        'name': getattr(ds, 'RTPlanName', 'N/A'),
                        'date': getattr(ds, 'RTPlanDate', 'N/A'),
                        'time': getattr(ds, 'RTPlanTime', 'N/A')
                    })
                elif modality == 'RTDOSE':
                    rtdose_files.append(file)
                elif modality == 'RTSTRUCT':
                    rtstruct_files.append(file)
                elif modality == 'CT':
                    ct_files.append(file)

            except Exception as e:
                pass

print(f"\nRESULTADO:")
print(f"  Arquivos RTPLAN: {len(rtplan_files)}")
print(f"  Arquivos RTDOSE: {len(rtdose_files)}")
print(f"  Arquivos RTSTRUCT: {len(rtstruct_files)}")
print(f"  Arquivos CT: {len(ct_files)}")

if rtplan_files:
    print("\n" + "="*80)
    print("DETALHES DOS ARQUIVOS RTPLAN ENCONTRADOS:")
    print("="*80)

    for idx, rtplan in enumerate(rtplan_files, 1):
        print(f"\nArquivo RTPLAN #{idx}:")
        print(f"  Nome do arquivo: {rtplan['file']}")
        print(f"  Caminho completo: {rtplan['path']}")
        print(f"  RT Plan Label: {rtplan['label']}")
        print(f"  RT Plan Name: {rtplan['name']}")
        print(f"  Data: {rtplan['date']}")
        print(f"  Hora: {rtplan['time']}")
else:
    print("\nNENHUM arquivo RTPLAN encontrado!")

# Salvar em arquivo
output_file = os.path.join(current_dir, "rtplan_info.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("ARQUIVOS RTPLAN NA PASTA 00002938\n")
    f.write("="*80 + "\n\n")
    f.write(f"Total de arquivos RTPLAN: {len(rtplan_files)}\n")
    f.write(f"Total de arquivos RTDOSE: {len(rtdose_files)}\n")
    f.write(f"Total de arquivos RTSTRUCT: {len(rtstruct_files)}\n")
    f.write(f"Total de arquivos CT: {len(ct_files)}\n\n")

    if rtplan_files:
        for idx, rtplan in enumerate(rtplan_files, 1):
            f.write("="*80 + "\n")
            f.write(f"ARQUIVO RTPLAN #{idx}\n")
            f.write("="*80 + "\n")
            f.write(f"Nome do arquivo: {rtplan['file']}\n")
            f.write(f"Caminho: {rtplan['path']}\n")
            f.write(f"RT Plan Label: {rtplan['label']}\n")
            f.write(f"RT Plan Name: {rtplan['name']}\n")
            f.write(f"Data: {rtplan['date']}\n")
            f.write(f"Hora: {rtplan['time']}\n\n")

print(f"\n\nInformacoes salvas em: {output_file}")
