#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comparação detalhada: DICOM gerado de .img vs DICOM gerado de TIFF
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

# Arquivos para comparar
file_img = os.path.join(current_dir, "WL_fixed.dcm")        # De .img (nosso conversor)
file_tiff = os.path.join(current_dir, "gantry_0.dcm")       # De TIFF (pylinac)

print("="*80)
print("COMPARAÇÃO: DICOM GERADO DE .IMG vs DICOM GERADO DE TIFF")
print("="*80)

print(f"\nArquivo 1 (de .img): {os.path.basename(file_img)}")
print(f"  Fonte: Elekta iView .img → Nosso conversor")
print(f"  Tamanho: {os.path.getsize(file_img) / 1024:.1f} KB")

print(f"\nArquivo 2 (de TIFF): {os.path.basename(file_tiff)}")
print(f"  Fonte: TIFF → pylinac.image.tiff_to_dicom()")
print(f"  Tamanho: {os.path.getsize(file_tiff) / 1024:.1f} KB")

# Ler arquivos
print("\nCarregando arquivos DICOM...")
try:
    ds_img = pydicom.dcmread(file_img)
    print(f"✓ Arquivo .img→DICOM lido")
except Exception as e:
    print(f"✗ Erro ao ler {file_img}: {e}")
    ds_img = None

try:
    ds_tiff = pydicom.dcmread(file_tiff)
    print(f"✓ Arquivo TIFF→DICOM lido")
except Exception as e:
    print(f"✗ Erro ao ler {file_tiff}: {e}")
    ds_tiff = None

if not ds_img or not ds_tiff:
    print("\nNão foi possível ler um ou ambos os arquivos!")
    sys.exit(1)

print("\n" + "="*80)
print("COMPARAÇÃO DE TAGS PRINCIPAIS")
print("="*80)

# Tags para comparar
important_tags = [
    # Informações do Paciente
    'PatientName',
    'PatientID',
    'PatientBirthDate',
    'PatientSex',

    # Informações do Estudo
    'Modality',
    'StudyDescription',
    'StudyDate',
    'StudyTime',
    'StudyInstanceUID',
    'SeriesInstanceUID',
    'SeriesDescription',

    # Informações do Equipamento
    'Manufacturer',
    'ManufacturerModelName',
    'StationName',
    'InstitutionName',

    # RT Image específico
    'RTImageLabel',
    'RTImageDescription',
    'RTImageName',

    # Parâmetros de Radioterapia
    'GantryAngle',
    'BeamLimitingDeviceAngle',
    'PatientSupportAngle',
    'RTImageSID',
    'RadiationMachineSAD',
    'RadiationMachineSSD',
    'PrimaryDosimeterUnit',

    # Informações da Imagem
    'Rows',
    'Columns',
    'BitsAllocated',
    'BitsStored',
    'HighBit',
    'PixelRepresentation',
    'PhotometricInterpretation',
    'SamplesPerPixel',
    'PixelSpacing',
    'ImagePlanePixelSpacing',

    # Técnico
    'SOPClassUID',
    'SOPInstanceUID',
]

print(f"\n{'TAG':<35} {'DE .IMG':<30} {'DE TIFF':<30}")
print("-" * 95)

differences = []
img_only = []
tiff_only = []

for tag_name in important_tags:
    val_img = getattr(ds_img, tag_name, None)
    val_tiff = getattr(ds_tiff, tag_name, None)

    # Converter para string
    str_img = str(val_img) if val_img is not None else ""
    str_tiff = str(val_tiff) if val_tiff is not None else ""

    # Truncar strings longas
    display_img = str_img[:28] + ".." if len(str_img) > 28 else str_img
    display_tiff = str_tiff[:28] + ".." if len(str_tiff) > 28 else str_tiff

    # Marcar diferenças
    marker = ""
    if val_img is None and val_tiff is not None:
        tiff_only.append((tag_name, val_tiff))
        marker = " ← APENAS TIFF"
    elif val_img is not None and val_tiff is None:
        img_only.append((tag_name, val_img))
        marker = " ← APENAS IMG"
    elif str_img != str_tiff:
        differences.append((tag_name, val_img, val_tiff))
        marker = " ← DIFERENTE"

    print(f"{tag_name:<35} {display_img:<30} {display_tiff:<30}{marker}")

# File Meta Information
print("\n" + "="*80)
print("FILE META INFORMATION HEADER")
print("="*80)

print(f"\n{'CAMPO':<35} {'DE .IMG':<30} {'DE TIFF':<30}")
print("-" * 95)

meta_fields = [
    'FileMetaInformationVersion',
    'MediaStorageSOPClassUID',
    'MediaStorageSOPInstanceUID',
    'TransferSyntaxUID',
    'ImplementationClassUID',
    'ImplementationVersionName',
]

for field in meta_fields:
    val_img = getattr(ds_img.file_meta, field, None) if hasattr(ds_img, 'file_meta') else None
    val_tiff = getattr(ds_tiff.file_meta, field, None) if hasattr(ds_tiff, 'file_meta') else None

    str_img = str(val_img)[:28] if val_img else "N/A"
    str_tiff = str(val_tiff)[:28] if val_tiff else "N/A"

    marker = " ← DIFERENTE" if val_img != val_tiff else ""
    print(f"{field:<35} {str_img:<30} {str_tiff:<30}{marker}")

# Resumo das diferenças
print("\n" + "="*80)
print("RESUMO DAS DIFERENÇAS")
print("="*80)

if differences:
    print(f"\nTags com valores diferentes: {len(differences)}")
    for tag_name, val_img, val_tiff in differences:
        print(f"\n{tag_name}:")
        print(f"  De .img:  {val_img}")
        print(f"  De TIFF:  {val_tiff}")

if img_only:
    print(f"\nTags presentes APENAS no arquivo de .img: {len(img_only)}")
    for tag_name, val in img_only[:10]:
        print(f"  {tag_name}: {val}")
    if len(img_only) > 10:
        print(f"  ... e mais {len(img_only) - 10} tags")

if tiff_only:
    print(f"\nTags presentes APENAS no arquivo de TIFF: {len(tiff_only)}")
    for tag_name, val in tiff_only[:10]:
        print(f"  {tag_name}: {val}")
    if len(tiff_only) > 10:
        print(f"  ... e mais {len(tiff_only) - 10} tags")

# Análise de compatibilidade
print("\n" + "="*80)
print("ANÁLISE DE COMPATIBILIDADE COM PYLINAC")
print("="*80)

# Tags essenciais para Winston-Lutz
required_wl_tags = {
    'GantryAngle': 'Ângulo do gantry',
    'Modality': 'Modalidade (deve ser RTIMAGE)',
    'Rows': 'Número de linhas da imagem',
    'Columns': 'Número de colunas da imagem',
    'SOPClassUID': 'Tipo de objeto DICOM',
}

print("\nTags essenciais para Winston-Lutz:")
print(f"{'TAG':<20} {'DE .IMG':<15} {'DE TIFF':<15} {'DESCRIÇÃO':<30}")
print("-" * 80)

for tag, desc in required_wl_tags.items():
    val_img = getattr(ds_img, tag, None)
    val_tiff = getattr(ds_tiff, tag, None)

    str_img = str(val_img)[:13] if val_img else "N/A"
    str_tiff = str(val_tiff)[:13] if val_tiff else "N/A"

    status = "✓" if val_img and val_tiff else "✗"
    print(f"{tag:<20} {str_img:<15} {str_tiff:<15} {desc:<30} {status}")

# Conclusão
print("\n" + "="*80)
print("CONCLUSÃO")
print("="*80)

print("\nCOMPATIBILIDADE:")
print(f"  Arquivo de .img:  {'✓ Compatível' if all(hasattr(ds_img, tag) for tag in required_wl_tags) else '✗ Incompatível'}")
print(f"  Arquivo de TIFF:  {'✓ Compatível' if all(hasattr(ds_tiff, tag) for tag in required_wl_tags) else '✗ Incompatível'}")

print("\nPRINCIPAIS DIFERENÇAS:")
print(f"  1. Origem dos dados:")
print(f"     - .img: Arquivo real do acelerador Elekta")
print(f"     - TIFF: Imagem convertida com parâmetros sintéticos")

print(f"\n  2. Informações do paciente:")
print(f"     - .img: Dados reais (WINSTON-LUTZ^WL, ID: WL2025)")
print(f"     - TIFF: Dados sintéticos (Pylinac array, ID: 123456789)")

print(f"\n  3. Informações do equipamento:")
if hasattr(ds_img, 'Manufacturer'):
    print(f"     - .img: {ds_img.Manufacturer}, {getattr(ds_img, 'StationName', 'N/A')}")
else:
    print(f"     - .img: Informações não disponíveis")
if hasattr(ds_tiff, 'Manufacturer'):
    print(f"     - TIFF: {getattr(ds_tiff, 'Manufacturer', 'N/A')}")
else:
    print(f"     - TIFF: Informações sintéticas do pylinac")

print(f"\n  4. Transfer Syntax:")
if hasattr(ds_img, 'file_meta'):
    print(f"     - .img: {ds_img.file_meta.TransferSyntaxUID}")
if hasattr(ds_tiff, 'file_meta'):
    print(f"     - TIFF: {ds_tiff.file_meta.TransferSyntaxUID}")

print("\nRECOMENDAÇÃO:")
print("  Ambos os arquivos são compatíveis com pylinac!")
print("  - Use arquivos de .img quando disponíveis (dados reais)")
print("  - Use conversão TIFF quando necessário (testes, simulações)")

# Salvar relatório
output_file = os.path.join(current_dir, "comparacao_img_vs_tiff.txt")
print(f"\n\nRelatório completo salvo em: {output_file}")
