================================================================================
CONVERSOR TIFF PARA DICOM - PYLINAC - GUIA DE USO
================================================================================

DESCRICAO:
----------
Este programa converte arquivos TIFF (imagens de portal) para formato DICOM
compatível com análise de Winston-Lutz usando a função nativa do pylinac.

Baseado na documentação oficial do pylinac:
https://pylinac.readthedocs.io/en/latest/


COMO FUNCIONA:
--------------
O conversor utiliza a função image.tiff_to_dicom() do pylinac que:

1. Lê o arquivo TIFF
2. Cria tags DICOM apropriadas com os parâmetros fornecidos
3. Gera arquivo DICOM compatível com padrão de radioterapia
4. Compatível com análise Winston-Lutz do pylinac


COMO USAR:
----------

METODO 1 - Interface Grafica (Recomendado):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Dê um duplo clique no arquivo: executar_tiff_conversor.bat
   (O script instalará o pylinac automaticamente se necessário)

2. A interface gráfica será aberta

3. Clique em "Procurar..." para selecionar o arquivo TIFF

4. Configure os parâmetros obrigatórios:
   - SID: Source-to-Image Distance (ex: 1000 mm)
   - Gantry Angle: Ângulo do gantry (ex: 0, 90, 180, 270)
   - Collimator Angle: Ângulo do colimador (ex: 0)
   - Couch Angle: Ângulo da mesa (ex: 0)
   - DPI: Resolução da imagem (ex: 400)

5. Verifique o caminho de saída

6. Clique em "Converter TIFF para DICOM"

7. Pronto! O arquivo DICOM está pronto para uso com pylinac


METODO 2 - Linha de Comando Python:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from pylinac import image

# Converter TIFF para DICOM
new_dicom = image.tiff_to_dicom(
    "caminho/arquivo.tiff",
    sid=1000,      # Source-to-Image Distance em mm
    gantry=90,     # Ângulo do gantry
    coll=0,        # Ângulo do colimador
    couch=0,       # Ângulo da mesa
    dpi=400        # Resolução da imagem
)

# Salvar arquivo DICOM
new_dicom.save("caminho/saida.dcm")


PARAMETROS OBRIGATORIOS:
------------------------

SID (Source-to-Image Distance):
  - Distância da fonte ao detector em milímetros
  - Valor típico para aceleradores lineares: 1000 mm
  - Exemplo: 1000, 1500, 1600

Gantry Angle:
  - Ângulo do gantry em graus (0-360°)
  - Para Winston-Lutz, típicamente: 0, 90, 180, 270
  - Exemplo para gantry vertical: 0

Collimator Angle:
  - Ângulo do colimador em graus (0-360°)
  - Para Winston-Lutz padrão: 0
  - Exemplo: 0, 45, 90, 270

Couch Angle:
  - Ângulo da mesa em graus (0-360°)
  - Para Winston-Lutz padrão: 0
  - Exemplo: 0, 45, 90, 270

DPI (Dots Per Inch):
  - Resolução da imagem portal
  - Valor típico: 400 DPI
  - Afeta o PixelSpacing no DICOM
  - Exemplo: 300, 400, 600


EXEMPLO DE USO - WINSTON-LUTZ:
------------------------------

Para análise completa de Winston-Lutz, você precisa de 4 imagens:

1. Gantry 0°:
   - SID: 1000, Gantry: 0, Coll: 0, Couch: 0, DPI: 400
   - Arquivo: g0.dcm

2. Gantry 90°:
   - SID: 1000, Gantry: 90, Coll: 0, Couch: 0, DPI: 400
   - Arquivo: g90.dcm

3. Gantry 180°:
   - SID: 1000, Gantry: 180, Coll: 0, Couch: 0, DPI: 400
   - Arquivo: g180.dcm

4. Gantry 270°:
   - SID: 1000, Gantry: 270, Coll: 0, Couch: 0, DPI: 400
   - Arquivo: g270.dcm

Depois use com pylinac:
from pylinac import WinstonLutz
wl = WinstonLutz("pasta/com/arquivos")
wl.analyze()
wl.plot_summary()


INSTALACAO DO PYLINAC:
----------------------

Se o pylinac não estiver instalado, execute:

pip install pylinac

ou no ambiente virtual:

.venv\Scripts\pip.exe install pylinac


REQUISITOS:
-----------
- Python 3.x
- pylinac (será instalado automaticamente pelo .bat)
- pydicom (incluído como dependência do pylinac)
- numpy, scipy, pillow (incluídos como dependências)


TAGS DICOM CRIADAS:
-------------------

A função image.tiff_to_dicom() do pylinac cria automaticamente:
- SOP Class UID (RT Image Storage)
- SOP Instance UID
- Study Instance UID
- Series Instance UID
- Modality: RTIMAGE
- Rows, Columns (da imagem TIFF)
- Pixel Spacing (calculado do DPI)
- Bits Allocated, Bits Stored
- Photometric Interpretation
- Gantry Angle (valor fornecido)
- Beam Limiting Device Angle (collimator)
- Patient Support Angle (couch)
- RT Image SID (valor fornecido)
- File Meta Information Header completo


COMPATIBILIDADE:
----------------
✓ Compatível com pylinac.WinstonLutz()
✓ Compatível com visualizadores DICOM padrão
✓ Compatível com sistemas de planejamento de radioterapia
✓ Segue padrão DICOM RT Image Storage


SOLUCAO DE PROBLEMAS:
---------------------

Erro: "pylinac não está instalado"
Solução: Execute .venv\Scripts\pip.exe install pylinac

Erro: "No space left on device"
Solução: Libere espaço em disco e tente novamente

Erro: "Invalid DPI value"
Solução: Verifique se o DPI é um número positivo

Erro: "Angle out of range"
Solução: Todos os ângulos devem estar entre 0 e 360


ARQUIVOS DO PROJETO:
--------------------
tiff_to_dicom_gui.py           - Código principal da interface
executar_tiff_conversor.bat    - Atalho para executar (Windows)
README_TIFF_DICOM.txt          - Este arquivo


REFERENCIAS:
------------
Documentação oficial do pylinac:
https://pylinac.readthedocs.io/en/latest/

Função tiff_to_dicom():
https://pylinac.readthedocs.io/en/latest/image_analysis.html

Winston-Lutz Analysis:
https://pylinac.readthedocs.io/en/latest/winston_lutz.html


AUTOR:
------
Criado com Claude Code em 01/12/2025
Baseado na documentação oficial do pylinac


SUPORTE:
--------
Para dúvidas sobre pylinac, consulte:
https://github.com/jrkerns/pylinac


================================================================================
