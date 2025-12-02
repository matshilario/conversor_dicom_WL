#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de conversão TIFF para DICOM usando pylinac
Baseado na documentação oficial do pylinac
"""

from pylinac import image
import os


def converter_tiff_para_dicom_exemplo():
    """
    Exemplo básico de conversão TIFF para DICOM
    """
    print("="*80)
    print("EXEMPLO: Conversão TIFF para DICOM com pylinac")
    print("="*80)

    # Exemplo 1: Imagem de Gantry 0°
    print("\nExemplo 1: Convertendo imagem com Gantry 0°")
    print("-" * 80)

    # Verificar se arquivo existe (substitua pelo seu arquivo)
    arquivo_tiff = "minha_imagem.tiff"  # SUBSTITUA PELO SEU ARQUIVO

    if not os.path.exists(arquivo_tiff):
        print(f"⚠ Arquivo '{arquivo_tiff}' não encontrado.")
        print("Substitua 'minha_imagem.tiff' pelo caminho do seu arquivo TIFF")
        return

    # Converter TIFF para DICOM
    new_dicom = image.tiff_to_dicom(
        arquivo_tiff,
        sid=1000,      # Source-to-Image Distance = 1000 mm
        gantry=0,      # Gantry em 0 graus
        coll=0,        # Collimator em 0 graus
        couch=0,       # Couch em 0 graus
        dpi=400        # 400 DPI de resolução
    )

    # Salvar arquivo DICOM
    arquivo_saida = "gantry_0.dcm"
    new_dicom.save(arquivo_saida)
    print(f"✓ Arquivo convertido e salvo em: {arquivo_saida}")

    # Verificar tags DICOM criadas
    print("\nTags DICOM criadas:")
    print(f"  Gantry Angle: {new_dicom.metadata.GantryAngle}")
    print(f"  Modality: {new_dicom.metadata.Modality}")
    print(f"  Rows x Columns: {new_dicom.metadata.Rows} x {new_dicom.metadata.Columns}")


def exemplo_winston_lutz_completo():
    """
    Exemplo: Converter 4 imagens para análise Winston-Lutz
    """
    print("\n\n" + "="*80)
    print("EXEMPLO: Preparar conjunto completo para Winston-Lutz")
    print("="*80)

    # Configurações para 4 ângulos de gantry
    configuracoes = [
        {"arquivo": "wl_g0.tiff", "gantry": 0, "saida": "g0.dcm"},
        {"arquivo": "wl_g90.tiff", "gantry": 90, "saida": "g90.dcm"},
        {"arquivo": "wl_g180.tiff", "gantry": 180, "saida": "g180.dcm"},
        {"arquivo": "wl_g270.tiff", "gantry": 270, "saida": "g270.dcm"},
    ]

    # Parâmetros comuns
    sid = 1000  # mm
    coll = 0    # graus
    couch = 0   # graus
    dpi = 400   # DPI

    print("\nConvertendo imagens...")
    for config in configuracoes:
        arquivo_entrada = config["arquivo"]
        arquivo_saida = config["saida"]
        gantry = config["gantry"]

        if not os.path.exists(arquivo_entrada):
            print(f"⚠ {arquivo_entrada} não encontrado - pulando...")
            continue

        # Converter
        new_dicom = image.tiff_to_dicom(
            arquivo_entrada,
            sid=sid,
            gantry=gantry,
            coll=coll,
            couch=couch,
            dpi=dpi
        )

        # Salvar
        new_dicom.save(arquivo_saida)
        print(f"✓ {arquivo_entrada} → {arquivo_saida} (Gantry {gantry}°)")

    print("\nConversão concluída!")
    print("\nAgora você pode analisar com pylinac:")
    print("  from pylinac import WinstonLutz")
    print("  wl = WinstonLutz('.')")
    print("  wl.analyze()")
    print("  wl.plot_summary()")


def exemplo_personalizado():
    """
    Exemplo com parâmetros personalizados
    """
    print("\n\n" + "="*80)
    print("EXEMPLO: Conversão com parâmetros personalizados")
    print("="*80)

    # Parâmetros personalizados
    arquivo_entrada = "meu_teste.tiff"
    arquivo_saida = "teste_convertido.dcm"

    if not os.path.exists(arquivo_entrada):
        print(f"⚠ Arquivo '{arquivo_entrada}' não encontrado")
        print("\nMODELO DE CÓDIGO:")
        print("-" * 80)
        print("""
from pylinac import image

# Configurar parâmetros
sid = 1500        # SID customizado (1500 mm)
gantry = 45       # Gantry em 45 graus
coll = 15         # Collimator em 15 graus
couch = 30        # Couch em 30 graus
dpi = 600         # Alta resolução (600 DPI)

# Converter
dicom = image.tiff_to_dicom(
    "arquivo.tiff",
    sid=sid,
    gantry=gantry,
    coll=coll,
    couch=couch,
    dpi=dpi
)

# Salvar
dicom.save("saida.dcm")
print("✓ Conversão concluída!")
        """)
        return

    # Converter com parâmetros personalizados
    new_dicom = image.tiff_to_dicom(
        arquivo_entrada,
        sid=1500,      # SID diferente
        gantry=45,     # Ângulo customizado
        coll=15,       # Collimator rotacionado
        couch=30,      # Couch rotacionado
        dpi=600        # Alta resolução
    )

    new_dicom.save(arquivo_saida)
    print(f"✓ Arquivo convertido com parâmetros personalizados: {arquivo_saida}")


if __name__ == "__main__":
    # Verificar se pylinac está instalado
    try:
        import pylinac
        print("✓ pylinac está instalado")
        print(f"  Versão: {pylinac.__version__}\n")
    except ImportError:
        print("✗ pylinac NÃO está instalado!")
        print("\nPara instalar:")
        print("  pip install pylinac")
        print("\nou")
        print("  .venv\\Scripts\\pip.exe install pylinac")
        exit(1)

    # Executar exemplos
    print("\nEscolha um exemplo para executar:\n")
    print("1. Exemplo básico (converter 1 arquivo)")
    print("2. Exemplo Winston-Lutz completo (4 ângulos)")
    print("3. Exemplo com parâmetros personalizados")
    print("4. Sair\n")

    escolha = input("Digite o número da opção: ")

    if escolha == "1":
        converter_tiff_para_dicom_exemplo()
    elif escolha == "2":
        exemplo_winston_lutz_completo()
    elif escolha == "3":
        exemplo_personalizado()
    else:
        print("Saindo...")
