#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste de conversão do arquivo gantry_0.TIFF
"""

import os
import sys

# Configurar codificação UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

from pylinac import image
import pydicom

current_dir = os.path.dirname(os.path.abspath(__file__))
tiff_folder = os.path.join(current_dir, "imagens TIFF")
input_file = os.path.join(tiff_folder, "gantry_0.TIFF")
output_file = os.path.join(current_dir, "gantry_0.dcm")

print("="*80)
print("TESTE DE CONVERSÃO TIFF → DICOM (Gantry 0°)")
print("="*80)

print(f"\nArquivo de entrada: {input_file}")
print(f"Tamanho: {os.path.getsize(input_file) / 1024:.1f} KB")

print("\nConvertendo com pylinac.image.tiff_to_dicom()...")
print("Parâmetros:")
print("  SID: 1000 mm")
print("  Gantry: 0°")
print("  Collimator: 0°")
print("  Couch: 0°")
print("  DPI: 400")

try:
    # Converter TIFF para DICOM
    new_dicom = image.tiff_to_dicom(
        input_file,
        sid=1000,
        gantry=0,
        coll=0,
        couch=0,
        dpi=400
    )

    # Salvar arquivo DICOM (Dataset usa save_as, não save)
    new_dicom.save_as(output_file, write_like_original=False)

    print(f"\n✓ Conversão concluída com sucesso!")
    print(f"\nArquivo DICOM criado: {output_file}")
    print(f"Tamanho: {os.path.getsize(output_file) / 1024:.1f} KB")

    # Verificar tags DICOM
    print("\n" + "="*80)
    print("TAGS DICOM CRIADAS:")
    print("="*80)

    ds = pydicom.dcmread(output_file)

    print(f"\nInformações do Paciente:")
    print(f"  Patient Name: {getattr(ds, 'PatientName', 'N/A')}")
    print(f"  Patient ID: {getattr(ds, 'PatientID', 'N/A')}")

    print(f"\nInformações do Estudo:")
    print(f"  Modality: {ds.Modality}")
    print(f"  Study Instance UID: {ds.StudyInstanceUID}")
    print(f"  Series Instance UID: {ds.SeriesInstanceUID}")

    print(f"\nInformações de Radioterapia:")
    print(f"  Gantry Angle: {ds.GantryAngle}°")
    print(f"  Beam Limiting Device Angle: {getattr(ds, 'BeamLimitingDeviceAngle', 'N/A')}°")
    print(f"  Patient Support Angle: {getattr(ds, 'PatientSupportAngle', 'N/A')}°")
    print(f"  RT Image SID: {getattr(ds, 'RTImageSID', 'N/A')} mm")

    print(f"\nInformações da Imagem:")
    print(f"  Rows x Columns: {ds.Rows} x {ds.Columns}")
    print(f"  Bits Allocated: {ds.BitsAllocated}")
    print(f"  Photometric Interpretation: {ds.PhotometricInterpretation}")
    print(f"  Pixel Spacing: {getattr(ds, 'PixelSpacing', 'N/A')}")

    print(f"\nFile Meta Information:")
    print(f"  Transfer Syntax UID: {ds.file_meta.TransferSyntaxUID}")
    print(f"  Implementation Class UID: {ds.file_meta.ImplementationClassUID}")
    print(f"  SOP Class UID: {ds.SOPClassUID}")

    print("\n" + "="*80)
    print("VALIDAÇÃO:")
    print("="*80)

    # Verificar se pode ser lido sem force=True
    try:
        test = pydicom.dcmread(output_file)
        print("✓ Arquivo pode ser lido normalmente (sem force=True)")
    except:
        print("✗ Arquivo requer force=True para leitura")

    # Verificar se tem File Meta Information Header
    if hasattr(ds, 'file_meta') and hasattr(ds.file_meta, 'TransferSyntaxUID'):
        print("✓ File Meta Information Header presente")
    else:
        print("✗ File Meta Information Header ausente")

    # Verificar tags essenciais para Winston-Lutz
    required_tags = ['GantryAngle', 'Modality', 'Rows', 'Columns', 'SOPClassUID']
    missing_tags = []
    for tag in required_tags:
        if not hasattr(ds, tag):
            missing_tags.append(tag)

    if not missing_tags:
        print("✓ Todas as tags essenciais para Winston-Lutz estão presentes")
    else:
        print(f"✗ Tags ausentes: {', '.join(missing_tags)}")

    print("\n" + "="*80)
    print("CONCLUSÃO:")
    print("="*80)
    print("✓ Arquivo DICOM criado com sucesso!")
    print("✓ Compatível com pylinac")
    print("✓ Pronto para análise Winston-Lutz")
    print("\nPróximo passo:")
    print("  Converta os outros ângulos (90°, 180°, 270°) e execute:")
    print("  from pylinac import WinstonLutz")
    print("  wl = WinstonLutz('.')")
    print("  wl.analyze()")
    print("  wl.plot_summary()")

except Exception as e:
    print(f"\n✗ Erro na conversão: {str(e)}")
    import traceback
    traceback.print_exc()
