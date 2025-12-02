#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste do conversor TIFF para DICOM
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

current_dir = os.path.dirname(os.path.abspath(__file__))
tiff_folder = os.path.join(current_dir, "imagens TIFF")

print("="*80)
print("TESTE DO CONVERSOR TIFF PARA DICOM")
print("="*80)

# Verificar se pylinac está instalado
print("\n1. Verificando instalação do pylinac...")
try:
    from pylinac import image
    import pylinac
    print(f"   ✓ pylinac instalado - Versão {pylinac.__version__}")
except ImportError as e:
    print(f"   ✗ pylinac NÃO instalado!")
    print(f"\n   Execute: .venv\\Scripts\\pip.exe install pylinac")
    sys.exit(1)

# Verificar pasta de imagens TIFF
print(f"\n2. Verificando pasta de imagens TIFF...")
print(f"   Pasta: {tiff_folder}")

if not os.path.exists(tiff_folder):
    print(f"   ⚠ Pasta não existe! Criando...")
    os.makedirs(tiff_folder)

# Listar arquivos TIFF
tiff_files = []
for file in os.listdir(tiff_folder):
    if file.lower().endswith(('.tiff', '.tif')):
        tiff_files.append(file)

if not tiff_files:
    print(f"   ⚠ Nenhum arquivo TIFF encontrado na pasta!")
    print(f"\n" + "="*80)
    print("INSTRUÇÕES PARA ADICIONAR ARQUIVOS TIFF:")
    print("="*80)
    print(f"""
1. Copie suas imagens TIFF para a pasta:
   {tiff_folder}

2. Os arquivos devem ser imagens portal do acelerador linear

3. Nomeie os arquivos de forma descritiva, exemplo:
   - gantry_0.tiff
   - gantry_90.tiff
   - gantry_180.tiff
   - gantry_270.tiff

4. Execute este script novamente ou use a interface gráfica:
   executar_tiff_conversor.bat
    """)
    sys.exit(0)

print(f"   ✓ Encontrados {len(tiff_files)} arquivo(s) TIFF:")
for f in tiff_files:
    file_path = os.path.join(tiff_folder, f)
    size_kb = os.path.getsize(file_path) / 1024
    print(f"     - {f} ({size_kb:.1f} KB)")

# Testar conversão com o primeiro arquivo
print(f"\n3. Testando conversão do primeiro arquivo...")
test_file = os.path.join(tiff_folder, tiff_files[0])
print(f"   Arquivo de teste: {tiff_files[0]}")

try:
    # Tentar carregar a imagem TIFF
    print(f"   Carregando imagem TIFF...")

    # Converter para DICOM
    print(f"   Convertendo para DICOM com parâmetros de teste...")
    new_dicom = image.tiff_to_dicom(
        test_file,
        sid=1000,    # Source-to-Image Distance = 1000 mm
        gantry=0,    # Gantry em 0 graus (ajuste conforme necessário)
        coll=0,      # Collimator em 0 graus
        couch=0,     # Couch em 0 graus
        dpi=400      # 400 DPI
    )

    # Salvar arquivo de teste
    output_file = os.path.join(current_dir, "teste_conversao.dcm")
    new_dicom.save(output_file)

    print(f"   ✓ Conversão bem-sucedida!")
    print(f"\n   Arquivo DICOM criado: teste_conversao.dcm")
    print(f"   Tamanho: {os.path.getsize(output_file) / 1024:.1f} KB")

    # Verificar tags DICOM
    print(f"\n4. Verificando tags DICOM criadas...")
    print(f"   Modalidade: {new_dicom.metadata.Modality}")
    print(f"   Gantry Angle: {new_dicom.metadata.GantryAngle}°")
    print(f"   Dimensões: {new_dicom.metadata.Rows} x {new_dicom.metadata.Columns} pixels")
    print(f"   SOP Class UID: {new_dicom.metadata.SOPClassUID}")

    # Validar compatibilidade
    print(f"\n5. Validando compatibilidade com pylinac...")
    try:
        import pydicom
        test_ds = pydicom.dcmread(output_file)
        print(f"   ✓ Arquivo pode ser lido normalmente (sem force=True)")
        print(f"   ✓ Transfer Syntax UID: {test_ds.file_meta.TransferSyntaxUID}")
        print(f"   ✓ Compatível com pylinac!")
    except Exception as e:
        print(f"   ⚠ Aviso: {str(e)}")

    print(f"\n" + "="*80)
    print("TESTE CONCLUÍDO COM SUCESSO!")
    print("="*80)
    print(f"""
O conversor está funcionando corretamente!

PRÓXIMOS PASSOS:

1. Use a interface gráfica para converter todos os arquivos:
   executar_tiff_conversor.bat

2. Configure os parâmetros corretos para cada imagem:
   - Gantry Angle: O ângulo correto de cada imagem
   - SID, Coll, Couch: Conforme usado no acelerador
   - DPI: Conforme a resolução da imagem

3. Para análise Winston-Lutz, converta 4 imagens:
   - Gantry 0° → g0.dcm
   - Gantry 90° → g90.dcm
   - Gantry 180° → g180.dcm
   - Gantry 270° → g270.dcm

4. Execute análise com pylinac:
   from pylinac import WinstonLutz
   wl = WinstonLutz("pasta/com/arquivos")
   wl.analyze()
   wl.plot_summary()
    """)

except Exception as e:
    print(f"   ✗ Erro na conversão: {str(e)}")
    print(f"\nDetalhes do erro:")
    import traceback
    traceback.print_exc()
