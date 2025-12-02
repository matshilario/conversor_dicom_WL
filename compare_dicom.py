#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para comparar estruturas de arquivos DICOM
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

current_dir = os.path.dirname(os.path.abspath(__file__))

# Arquivos a comparar
file_valid = os.path.join(current_dir, "gantry180.dcm")  # Arquivo válido
file_converted = os.path.join(current_dir, "DCM4_Processed_converted.dcm")  # Arquivo convertido

print("="*80)
print("COMPARAÇÃO DE ESTRUTURAS DICOM")
print("="*80)

print(f"\nArquivo VÁLIDO: {os.path.basename(file_valid)}")
print(f"Arquivo CONVERTIDO: {os.path.basename(file_converted)}")

# Ler arquivos
try:
    ds_valid = pydicom.dcmread(file_valid)
    print(f"\n✓ Arquivo válido lido com sucesso")
except Exception as e:
    print(f"\n✗ Erro ao ler arquivo válido: {str(e)}")
    ds_valid = None

try:
    ds_converted = pydicom.dcmread(file_converted)
    print(f"✓ Arquivo convertido lido com sucesso")
except Exception as e:
    print(f"⚠ Erro ao ler arquivo convertido: {str(e)}")
    print(f"  Tentando com force=True...")
    try:
        ds_converted = pydicom.dcmread(file_converted, force=True)
        print(f"✓ Arquivo convertido lido com force=True")
    except Exception as e2:
        print(f"✗ Falhou mesmo com force=True: {str(e2)}")
        ds_converted = None

if not ds_valid or not ds_converted:
    print("\nNão foi possível ler um ou ambos os arquivos!")
    sys.exit(1)

print("\n" + "="*80)
print("COMPARAÇÃO DE TAGS PRINCIPAIS")
print("="*80)

# Tags importantes para análise
important_tags = [
    'SOPClassUID',
    'SOPInstanceUID',
    'Modality',
    'Manufacturer',
    'ManufacturerModelName',
    'StationName',
    'StudyInstanceUID',
    'SeriesInstanceUID',
    'FrameOfReferenceUID',
    'PatientName',
    'PatientID',
    'StudyDate',
    'StudyTime',
    'SeriesDate',
    'SeriesTime',
    'AcquisitionDate',
    'AcquisitionTime',
    'ContentDate',
    'ContentTime',
    'Rows',
    'Columns',
    'BitsAllocated',
    'BitsStored',
    'HighBit',
    'PixelRepresentation',
    'PhotometricInterpretation',
    'SamplesPerPixel',
    'PixelSpacing',
    'ImageOrientationPatient',
    'ImagePositionPatient',
    'SliceThickness',
    'RTImageLabel',
    'RTImageName',
    'RTImageDescription',
    'RTImagePlane',
    'XRayImageReceptorTranslation',
    'XRayImageReceptorAngle',
    'RTImageOrientation',
    'ImagePlanePixelSpacing',
    'RTImagePosition',
    'RadiationMachineName',
    'RadiationMachineSAD',
    'RadiationMachineSSD',
    'RTImageSID',
    'PrimaryDosimeterUnit',
    'GantryAngle',
    'BeamLimitingDeviceAngle',
    'PatientSupportAngle',
    'TableTopVerticalPosition',
    'TableTopLongitudinalPosition',
    'TableTopLateralPosition',
    'IsocenterPosition',
]

print("\nTAG                                  VÁLIDO                    CONVERTIDO")
print("-" * 80)

differences = []

for tag_name in important_tags:
    val_valid = getattr(ds_valid, tag_name, None)
    val_converted = getattr(ds_converted, tag_name, None)

    # Converter para string para comparação
    str_valid = str(val_valid) if val_valid is not None else "N/A"
    str_converted = str(val_converted) if val_converted is not None else "N/A"

    # Truncar strings longas
    if len(str_valid) > 25:
        str_valid = str_valid[:22] + "..."
    if len(str_converted) > 25:
        str_converted = str_converted[:22] + "..."

    # Verificar se são diferentes
    if val_valid != val_converted:
        marker = " ← DIFERENTE"
        differences.append((tag_name, val_valid, val_converted))
    else:
        marker = ""

    print(f"{tag_name:35} {str_valid:25} {str_converted:25}{marker}")

# Resumo das diferenças
print("\n" + "="*80)
print("RESUMO DAS DIFERENÇAS ENCONTRADAS")
print("="*80)

if not differences:
    print("\n✓ Nenhuma diferença encontrada nas tags principais!")
else:
    print(f"\n✗ Encontradas {len(differences)} diferenças:\n")

    for tag_name, val_valid, val_converted in differences:
        print(f"\n{tag_name}:")
        print(f"  Válido:     {val_valid}")
        print(f"  Convertido: {val_converted}")

# Verificar File Meta Information Header
print("\n" + "="*80)
print("FILE META INFORMATION HEADER")
print("="*80)

print("\nArquivo VÁLIDO:")
if hasattr(ds_valid, 'file_meta'):
    print(f"  Transfer Syntax UID: {ds_valid.file_meta.TransferSyntaxUID}")
    print(f"  Implementation Class UID: {getattr(ds_valid.file_meta, 'ImplementationClassUID', 'N/A')}")
    print(f"  Implementation Version Name: {getattr(ds_valid.file_meta, 'ImplementationVersionName', 'N/A')}")
else:
    print("  ✗ Sem File Meta Information Header")

print("\nArquivo CONVERTIDO:")
if hasattr(ds_converted, 'file_meta'):
    print(f"  Transfer Syntax UID: {ds_converted.file_meta.TransferSyntaxUID}")
    print(f"  Implementation Class UID: {getattr(ds_converted.file_meta, 'ImplementationClassUID', 'N/A')}")
    print(f"  Implementation Version Name: {getattr(ds_converted.file_meta, 'ImplementationVersionName', 'N/A')}")
else:
    print("  ✗ Sem File Meta Information Header")

# Verificar tags presentes em cada arquivo
print("\n" + "="*80)
print("TAGS PRESENTES EM CADA ARQUIVO")
print("="*80)

tags_valid = set(ds_valid.dir())
tags_converted = set(ds_converted.dir())

only_in_valid = tags_valid - tags_converted
only_in_converted = tags_converted - tags_valid

if only_in_valid:
    print(f"\n✗ Tags presentes APENAS no arquivo VÁLIDO ({len(only_in_valid)}):")
    for tag in sorted(list(only_in_valid)[:20]):  # Mostrar apenas as primeiras 20
        print(f"  - {tag}: {getattr(ds_valid, tag, 'N/A')}")
    if len(only_in_valid) > 20:
        print(f"  ... e mais {len(only_in_valid) - 20} tags")

if only_in_converted:
    print(f"\n✗ Tags presentes APENAS no arquivo CONVERTIDO ({len(only_in_converted)}):")
    for tag in sorted(list(only_in_converted)[:20]):
        print(f"  - {tag}: {getattr(ds_converted, tag, 'N/A')}")
    if len(only_in_converted) > 20:
        print(f"  ... e mais {len(only_in_converted) - 20} tags")

# Salvar relatório
output_file = os.path.join(current_dir, "comparacao_dicom.txt")
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("RELATÓRIO DE COMPARAÇÃO DICOM\n")
    f.write("="*80 + "\n\n")

    f.write(f"Arquivo VÁLIDO: {os.path.basename(file_valid)}\n")
    f.write(f"Arquivo CONVERTIDO: {os.path.basename(file_converted)}\n\n")

    f.write("DIFERENÇAS ENCONTRADAS:\n")
    f.write("-"*80 + "\n\n")

    if differences:
        for tag_name, val_valid, val_converted in differences:
            f.write(f"{tag_name}:\n")
            f.write(f"  Válido:     {val_valid}\n")
            f.write(f"  Convertido: {val_converted}\n\n")
    else:
        f.write("Nenhuma diferença encontrada.\n\n")

    if only_in_valid:
        f.write(f"\nTags presentes APENAS no arquivo VÁLIDO:\n")
        for tag in sorted(only_in_valid):
            f.write(f"  - {tag}\n")

    if only_in_converted:
        f.write(f"\nTags presentes APENAS no arquivo CONVERTIDO:\n")
        for tag in sorted(only_in_converted):
            f.write(f"  - {tag}\n")

print(f"\n\nRelatório completo salvo em: {output_file}")
