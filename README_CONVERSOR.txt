================================================================================
CONVERSOR DE ARQUIVOS DICOM .img - GUIA DE USO
================================================================================

DESCRICAO:
----------
Este programa converte arquivos .img (formato DICOM sem header padrao) para
o formato DICOM padrao (.dcm) que pode ser aberto em qualquer visualizador
DICOM.

Ideal para converter imagens portal de aceleradores lineares (RTIMAGE) que
sao exportadas em formato .img.


COMO USAR:
----------

METODO 1 - Interface Grafica (Recomendado):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Dê um duplo clique no arquivo: executar_conversor.bat

2. A interface gráfica será aberta

3. Clique em "Procurar..." para selecionar o arquivo .img

4. Clique em "Analisar Arquivo" para ver as informações

5. Verifique se o caminho de saída está correto

6. Clique em "Converter para DICOM Padrão"

7. Pronto! O arquivo .dcm foi criado


METODO 2 - Linha de Comando:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
1. Abra o PowerShell nesta pasta

2. Ative o ambiente virtual:
   .\.venv\Scripts\Activate.ps1

3. Execute:
   python dicom_converter_gui.py


RECURSOS DA INTERFACE:
----------------------
- Seleção fácil de arquivos com botão "Procurar"
- Visualização completa das informações DICOM
- NOMEAÇÃO AUTOMÁTICA INTELIGENTE do arquivo de saída
- Mensagens de sucesso/erro claras
- Opção de abrir a pasta após conversão

NOMEAÇÃO AUTOMÁTICA:
--------------------
O nome do arquivo de saída é gerado automaticamente baseado nos campos DICOM,
seguindo esta ordem de prioridade:

1. Series Description (ex: "WL:" vira "WL.dcm")
2. RT Image Label (ex: "iViewIMRTSegment" vira "iViewIMRTSegment.dcm")
3. Patient ID + Study Date (ex: "WL2025_20251201.dcm")
4. Nome do arquivo original + "_converted"

Caracteres inválidos são removidos automaticamente.
Se o arquivo já existe, adiciona um contador (ex: "WL_1.dcm", "WL_2.dcm")


INFORMACOES EXIBIDAS:
---------------------
- Nome e ID do paciente
- Data e hora do estudo
- Modalidade (RTIMAGE, RTDOSE, etc)
- Informações do equipamento
- Dimensões da imagem
- UIDs técnicos


FORMATOS SUPORTADOS:
--------------------
Entrada:  .img (DICOM sem header)
Saída:    .dcm (DICOM padrão)


REQUISITOS:
-----------
- Python 3.x
- pydicom (já instalado no ambiente virtual)
- tkinter (incluído no Python padrão)


SOLUCAO DE PROBLEMAS:
---------------------

Problema: "File is missing DICOM File Meta Information header"
Solução: O programa usa force=True automaticamente para ler esses arquivos

Problema: "Erro ao converter arquivo"
Solução: Verifique se você tem permissão de escrita na pasta de destino

Problema: A interface não abre
Solução: Execute pelo PowerShell com: python dicom_converter_gui.py


ARQUIVOS DO PROJETO:
--------------------
dicom_converter_gui.py     - Código principal da interface
executar_conversor.bat     - Atalho para executar (Windows)
README_CONVERSOR.txt       - Este arquivo


AUTOR:
------
Criado com Claude Code em 01/12/2025
Para conversão de imagens DICOM de aceleradores lineares


SUPORTE:
--------
Para problemas ou dúvidas, consulte a documentação do pydicom:
https://pydicom.github.io/


================================================================================
