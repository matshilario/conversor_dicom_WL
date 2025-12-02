#!/usr/bin/env python3
"""
Script simples para ler arquivos DICOM sem dependências externas
Nota: Para resultados mais completos, instale pydicom: pip install pydicom
"""

import struct
import os
from pathlib import Path


def read_dicom_tag(file_handle, group, element):
    """Procura e lê uma tag DICOM específica"""
    file_handle.seek(0)
    data = file_handle.read()

    # Procurar pela tag no formato (group, element)
    tag_bytes = struct.pack('<HH', group, element)

    idx = data.find(tag_bytes)
    if idx != -1:
        # Verificar se encontrou uma tag DICOM válida
        try:
            # Pular para depois da tag (4 bytes) e VR (2 bytes)
            start = idx + 4

            # Ler VR (Value Representation)
            vr = data[start:start+2].decode('ascii', errors='ignore')

            # Determinar onde está o comprimento
            if vr in ['OB', 'OW', 'OF', 'SQ', 'UN', 'UT']:
                # VR explícito com campo de comprimento de 4 bytes
                length = struct.unpack('<I', data[start+4:start+8])[0]
                value_start = start + 8
            else:
                # VR explícito com campo de comprimento de 2 bytes
                length = struct.unpack('<H', data[start+2:start+4])[0]
                value_start = start + 4

            if length > 0 and length < 1024:  # Limitar tamanho para segurança
                value = data[value_start:value_start+length]
                return value.decode('utf-8', errors='ignore').strip('\x00').strip()
        except:
            pass

    return None


def find_patient_name(data):
    """Procura o nome do paciente nos dados DICOM"""
    # Tag 0010,0010 = Patient's Name
    patterns = [
        b'\x10\x00\x10\x00',  # Little Endian
    ]

    for pattern in patterns:
        idx = data.find(pattern)
        if idx != -1:
            try:
                # Tentar extrair o valor
                start = idx + 4
                # Pular VR
                start += 2
                # Ler comprimento
                length = struct.unpack('<H', data[start:start+2])[0]
                if length > 0 and length < 200:
                    value_start = start + 2
                    name = data[value_start:value_start+length]
                    return name.decode('utf-8', errors='ignore').strip('\x00').strip()
            except:
                pass

    return "N/A"


def find_patient_id(data):
    """Procura o ID do paciente nos dados DICOM"""
    # Tag 0010,0020 = Patient ID
    pattern = b'\x10\x00\x20\x00'

    idx = data.find(pattern)
    if idx != -1:
        try:
            start = idx + 4
            start += 2  # Pular VR
            length = struct.unpack('<H', data[start:start+2])[0]
            if length > 0 and length < 100:
                value_start = start + 2
                patient_id = data[value_start:value_start+length]
                return patient_id.decode('utf-8', errors='ignore').strip('\x00').strip()
        except:
            pass

    return "N/A"


def extract_basic_info(filepath):
    """Extrai informações básicas de um arquivo DICOM"""
    try:
        with open(filepath, 'rb') as f:
            # Verificar se é um arquivo DICOM válido
            f.seek(128)  # Pular preâmbulo
            dicm = f.read(4)

            if dicm != b'DICM':
                return {'erro': 'Arquivo não possui assinatura DICOM válida'}

            # Voltar ao início para ler todo o conteúdo
            f.seek(0)
            data = f.read()

            info = {
                'arquivo': os.path.basename(filepath),
                'tamanho': f"{len(data) / 1024:.2f} KB"
            }

            # Extrair informações básicas
            info['nome_paciente'] = find_patient_name(data)
            info['id_paciente'] = find_patient_id(data)

            # Procurar outras informações comuns em formato de texto
            data_str = data.decode('latin-1', errors='ignore')

            # Tentar encontrar modalidade
            if 'CT' in data_str[:5000]:
                info['modalidade_provavel'] = 'CT'
            elif 'MR' in data_str[:5000]:
                info['modalidade_provavel'] = 'MR'
            elif 'RTPLAN' in data_str[:5000]:
                info['modalidade_provavel'] = 'RTPLAN (Plano de Radioterapia)'
            elif 'RTDOSE' in data_str[:5000]:
                info['modalidade_provavel'] = 'RTDOSE (Dose de Radioterapia)'
            elif 'RTSTRUCT' in data_str[:5000]:
                info['modalidade_provavel'] = 'RTSTRUCT (Estrutura de Radioterapia)'
            else:
                info['modalidade_provavel'] = 'Desconhecida'

            return info

    except Exception as e:
        return {'erro': str(e), 'arquivo': os.path.basename(filepath)}


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    print("="*80)
    print("LEITOR BÁSICO DE ARQUIVOS DICOM")
    print("="*80)
    print("\n⚠️  NOTA: Este é um leitor básico e limitado.")
    print("Para resultados completos, instale o pydicom:")
    print("   pip install pydicom")
    print("E execute: python read_dicom.py\n")
    print("="*80)

    # Encontrar arquivos DICOM
    dicom_files = []
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.dcm') or file.endswith('.DCM'):
                dicom_files.append(os.path.join(root, file))

    if not dicom_files:
        print("❌ Nenhum arquivo DICOM encontrado!")
        return

    print(f"\n✅ Encontrados {len(dicom_files)} arquivos DICOM\n")

    # Processar arquivos
    pacientes = {}

    for idx, filepath in enumerate(dicom_files, 1):
        info = extract_basic_info(filepath)

        if idx <= 3:  # Mostrar detalhes dos primeiros 3 arquivos
            print(f"\n{'='*80}")
            print(f"Arquivo {idx}: {info.get('arquivo', 'N/A')}")
            print(f"{'='*80}")

            if 'erro' in info:
                print(f"❌ ERRO: {info['erro']}")
            else:
                print(f"📄 Tamanho: {info.get('tamanho', 'N/A')}")
                print(f"👤 Nome do Paciente: {info.get('nome_paciente', 'N/A')}")
                print(f"🔢 ID do Paciente: {info.get('id_paciente', 'N/A')}")
                print(f"🏥 Modalidade (provável): {info.get('modalidade_provavel', 'N/A')}")

        # Agrupar por paciente
        if 'erro' not in info:
            patient_id = info.get('id_paciente', 'Desconhecido')
            if patient_id not in pacientes:
                pacientes[patient_id] = {
                    'nome': info.get('nome_paciente', 'N/A'),
                    'arquivos': []
                }
            pacientes[patient_id]['arquivos'].append(info['arquivo'])

    # Resumo
    print(f"\n\n{'='*80}")
    print("📊 RESUMO GERAL")
    print(f"{'='*80}\n")

    for patient_id, data in pacientes.items():
        print(f"👤 Paciente: {data['nome']}")
        print(f"   ID: {patient_id}")
        print(f"   Total de arquivos: {len(data['arquivos'])}")
        print()


if __name__ == "__main__":
    main()
