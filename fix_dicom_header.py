#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corretor de header DICOM - Adiciona File Meta Information Header correto
"""

import pydicom
from pydicom.dataset import FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
import os
import sys

# Configurar codificação UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

def fix_dicom_file(input_path, output_path):
    """
    Lê arquivo DICOM (com ou sem header) e salva com header completo
    """
    print(f"\nProcessando: {os.path.basename(input_path)}")

    # Ler arquivo (com force=True se necessário)
    try:
        ds = pydicom.dcmread(input_path)
        print("  ✓ Arquivo lido normalmente")
    except:
        ds = pydicom.dcmread(input_path, force=True)
        print("  ✓ Arquivo lido com force=True")

    # Criar ou corrigir File Meta Information Header
    if not hasattr(ds, 'file_meta') or not ds.file_meta:
        print("  ⚠ Arquivo não tem file_meta, criando...")
        ds.file_meta = FileMetaDataset()

    # Garantir que tem Transfer Syntax UID
    if not hasattr(ds.file_meta, 'TransferSyntaxUID') or not ds.file_meta.TransferSyntaxUID:
        # Usar Explicit VR Little Endian (padrão DICOM)
        ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
        print(f"  + Adicionado Transfer Syntax UID: {ExplicitVRLittleEndian}")

    # Garantir que tem Media Storage SOP Class UID
    if not hasattr(ds.file_meta, 'MediaStorageSOPClassUID'):
        if hasattr(ds, 'SOPClassUID'):
            ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
            print(f"  + Adicionado Media Storage SOP Class UID")

    # Garantir que tem Media Storage SOP Instance UID
    if not hasattr(ds.file_meta, 'MediaStorageSOPInstanceUID'):
        if hasattr(ds, 'SOPInstanceUID'):
            ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
            print(f"  + Adicionado Media Storage SOP Instance UID")

    # Garantir que tem Implementation Class UID
    if not hasattr(ds.file_meta, 'ImplementationClassUID'):
        ds.file_meta.ImplementationClassUID = generate_uid()
        print(f"  + Adicionado Implementation Class UID")

    # Garantir que tem Implementation Version Name
    if not hasattr(ds.file_meta, 'ImplementationVersionName'):
        ds.file_meta.ImplementationVersionName = "PYDICOM_" + pydicom.__version__
        print(f"  + Adicionado Implementation Version Name")

    # Salvar com header completo
    ds.save_as(output_path, write_like_original=False)
    print(f"  ✓ Arquivo salvo com header completo em: {os.path.basename(output_path)}")

    # Verificar se o arquivo salvo pode ser lido normalmente
    try:
        test_ds = pydicom.dcmread(output_path)
        print("  ✓ Verificação: Arquivo pode ser lido normalmente (sem force=True)!")
        return True
    except Exception as e:
        print(f"  ✗ Verificação falhou: {str(e)}")
        return False


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("="*80)
    print("CORRETOR DE HEADER DICOM")
    print("="*80)

    # Corrigir o arquivo convertido
    input_file = os.path.join(current_dir, "DCM4_Processed.img")
    output_file = os.path.join(current_dir, "WL_fixed.dcm")

    if os.path.exists(input_file):
        success = fix_dicom_file(input_file, output_file)

        if success:
            print("\n" + "="*80)
            print("✓ SUCESSO! Arquivo DICOM corrigido e pronto para uso com pylinac")
            print("="*80)
        else:
            print("\n" + "="*80)
            print("✗ AVISO: Arquivo salvo mas pode ter problemas")
            print("="*80)
    else:
        print(f"\n✗ Arquivo não encontrado: {input_file}")
