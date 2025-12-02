# Conversor DICOM Unificado

Suite completa de conversores DICOM para radioterapia, com foco em análise de Winston-Lutz e QA de aceleradores lineares.

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

## 📋 Visão Geral

Este projeto oferece três conversores DICOM integrados em uma única interface gráfica:

1. **Conversor IMG para DICOM** - Converte arquivos .img do Elekta iView para DICOM padrão
2. **Conversor TIFF para DICOM** - Converte imagens TIFF individuais para DICOM
3. **Conversor em Lote TIFF para DICOM** - Converte múltiplos arquivos TIFF usando templates personalizáveis

Todos os arquivos DICOM gerados são **100% compatíveis com pylinac** para análise de Winston-Lutz e outros testes de QA.

## ✨ Características Principais

### Conversor IMG
- ✅ Converte arquivos Elekta iView (.img) para DICOM padrão
- ✅ Preserva todos os metadados originais do equipamento
- ✅ Geração automática de nome baseado em tags DICOM
- ✅ File Meta Information Header completo
- ✅ Validação automática pós-conversão

### Conversor TIFF Individual
- ✅ Usa função nativa do pylinac (`image.tiff_to_dicom()`)
- ✅ Detecção automática de parâmetros do nome do arquivo
- ✅ Validação e sugestão de renomeação
- ✅ Configuração de SID, ângulos (gantry, coll, couch) e DPI

### Conversor em Lote TIFF ⭐
- ✅ **Templates JSON editáveis** para Winston-Lutz (4, 7 ou 9 ângulos)
- ✅ **Salvar/carregar templates personalizados** (botões 💾 e 🗑)
- ✅ **Drag-and-drop** para reordenar conversões
- ✅ **Preview interativo** da conversão
- ✅ **Edição completa** de parâmetros por item
- ✅ **Barra de progresso** em tempo real
- ✅ **Validação inteligente** de incompatibilidades
- ✅ **Relatório detalhado** de erros

**⚠️ IMPORTANTE:** No conversor em lote, os ângulos (gantry, colimador, mesa) são definidos pelo **template**, não pelo nome do arquivo TIFF! Os arquivos TIFF são processados em ordem alfabética e cada um recebe os ângulos do item correspondente no template.

## 🚀 Instalação

### Pré-requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/conversor-dicom-unificado.git
cd conversor-dicom-unificado
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:
   - **Windows:**
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux/macOS:**
     ```bash
     source .venv/bin/activate
     ```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Uso

### Iniciar a Interface

Execute o conversor unificado:

```bash
python conversor_dicom_unificado.py
```

### Menu Principal

A interface apresenta três opções:

1. **Converter IMG para DICOM**
   - Selecione arquivo .img
   - Analise metadados
   - Converta para DICOM padrão

2. **Converter TIFF para DICOM**
   - Selecione arquivo TIFF
   - Configure parâmetros (SID, gantry, coll, couch, DPI)
   - Converta

3. **Converter Lote TIFF para DICOM**
   - Selecione pasta com arquivos TIFF
   - Escolha template ou personalize
   - Visualize preview
   - Converta em lote

### Exemplo: Winston-Lutz com 7 Imagens - Conversor em Lote

**Passo a Passo Detalhado:**

```bash
# 1. Organize arquivos TIFF em uma pasta (nome não importa!)
#    Exemplo: foto1.tiff, foto2.tiff, ..., foto7.tiff
#    ou: 1.tiff, 2.tiff, ..., 7.tiff
#    Os arquivos serão processados em ORDEM ALFABÉTICA

# 2. Abra "Converter Lote TIFF para DICOM"

# 3. Selecione a pasta com os arquivos

# 4. Escolha template "WL Extended 7"
#    O template define os ângulos para cada arquivo:
#    1º arquivo → gantry_0    (G:0°   C:0°  T:0°)
#    2º arquivo → gantry_90   (G:90°  C:0°  T:0°)
#    3º arquivo → gantry_180  (G:180° C:0°  T:0°)
#    4º arquivo → gantry_270  (G:270° C:0°  T:0°)
#    5º arquivo → couch_45    (G:0°   C:0°  T:45°)
#    6º arquivo → couch_315   (G:0°   C:0°  T:315°)
#    7º arquivo → coll_45     (G:0°   C:45° T:0°)

# 5. Configure SID (ex: 1600 mm) e DPI (ex: 400)

# 6. Verifique o Preview (mostra qual TIFF → qual ângulo)

# 7. Clique "Converter Lote"

# 8. Resultado: 7 arquivos DICOM com tags corretas!
#    gantry_0.dcm, gantry_90.dcm, gantry_180.dcm, gantry_270.dcm
#    couch_45.dcm, couch_315.dcm, coll_45.dcm
```

**🎯 O que determina os ângulos no DICOM:**
- ✅ **Template** define Gantry, Collimator e Couch angles
- ✅ **Ordem alfabética** dos arquivos TIFF determina qual item do template usar
- ✅ **Nome do arquivo TIFF não importa** (pode ser qualquer nome)
- ✅ **Tags DICOM** (300A,011E, 300A,0120, 300A,0122) são escritas automaticamente

**💡 Dica:** Use o botão 💾 para salvar seu próprio template personalizado!

### Análise com Pylinac

Após a conversão, use os arquivos DICOM com pylinac:

```python
from pylinac import WinstonLutz

# Carregar imagens convertidas
wl = WinstonLutz('pasta_com_dicoms/')

# Analisar
wl.analyze()

# Visualizar resultados
wl.plot_summary()

# Salvar relatório
wl.save_summary('relatorio_wl.pdf')
```

## 📁 Estrutura do Projeto

```
dicom_mosaiq/
├── conversor_dicom_unificado.py    # Interface principal (3 conversores)
├── templates_wl.json               # Templates Winston-Lutz editáveis
├── dicom_converter_gui.py          # Conversor IMG (standalone)
├── tiff_to_dicom_gui.py           # Conversor TIFF (standalone)
├── fix_dicom_header.py            # Utilitário para corrigir headers
├── comparar_img_vs_tiff.py        # Análise comparativa
├── read_dicom.py                  # Leitor de tags DICOM
├── requirements.txt               # Dependências
├── README.md                      # Este arquivo
├── CONVERSOR_EM_LOTE_GUIA.txt    # Guia completo do conversor em lote
├── COMPARACAO_IMG_TIFF_RESUMO.txt # Comparação técnica IMG vs TIFF
└── TESTE_REALIZADO.txt           # Documentação de testes
```

## 📝 Templates Winston-Lutz (templates_wl.json)

Os templates são armazenados em formato JSON editável. Você pode:

### Usar Templates Pré-definidos:
- **WL Standard 4** - 4 ângulos de gantry (0°, 90°, 180°, 270°)
- **WL Extended 7** - 4 gantries + 2 couches + 1 collimator
- **WL Completo 9** - 9 posições completas

### Criar Templates Personalizados:
1. Configure sua lista de conversões no conversor
2. Clique no botão 💾 (salvar)
3. Digite um nome e descrição
4. O template fica salvo permanentemente!

### Editar Manualmente o JSON:
```json
{
  "templates": {
    "Meu Template Custom": {
      "description": "Template personalizado para meu acelerador",
      "items": [
        {"name": "gantry_0", "gantry": "0", "coll": "0", "couch": "0"},
        {"name": "gantry_45", "gantry": "45", "coll": "0", "couch": "0"}
      ]
    }
  }
}
```

### Deletar Templates:
- Selecione o template no dropdown
- Clique no botão 🗑 (deletar)
- Confirme a exclusão

## 🔧 Dependências

- **pydicom** (>=2.3.0) - Manipulação de arquivos DICOM
- **pylinac** (>=3.0.0) - Conversão TIFF e análise QA
- **tkinter** - Interface gráfica (incluído no Python)

## 📊 Comparação: IMG vs TIFF

| Aspecto | Arquivos .IMG | Arquivos TIFF |
|---------|---------------|---------------|
| **Origem** | Elekta iView (real) | Qualquer fonte |
| **Metadados** | Preserva originais | Sintéticos configuráveis |
| **SID** | 1600mm (real) | Configurável |
| **Pixel Spacing** | 0.402mm (real) | Calculado de DPI |
| **Uso recomendado** | Produção/clínica | Testes/simulações |
| **Compatibilidade** | ✅ 100% pylinac | ✅ 100% pylinac |

Veja [COMPARACAO_IMG_TIFF_RESUMO.txt](COMPARACAO_IMG_TIFF_RESUMO.txt) para análise detalhada.

## 📚 Documentação Adicional

- **[CONVERSOR_EM_LOTE_GUIA.txt](CONVERSOR_EM_LOTE_GUIA.txt)** - Guia completo do conversor em lote
  - Passo a passo detalhado
  - Templates pré-definidos
  - Solução de problemas
  - Boas práticas

- **[TESTE_REALIZADO.txt](TESTE_REALIZADO.txt)** - Documentação de testes realizados

## 🛠️ Scripts Utilitários

### fix_dicom_header.py
Corrige headers DICOM ausentes ou incompletos:

```bash
python fix_dicom_header.py arquivo_entrada.dcm arquivo_saida.dcm
```

### comparar_img_vs_tiff.py
Compara tags DICOM de arquivos gerados por diferentes métodos:

```bash
python comparar_img_vs_tiff.py
```

### read_dicom.py
Lê e exibe tags DICOM de arquivos ou pastas:

```bash
python read_dicom.py
```

## ⚠️ Considerações Importantes

### Calibração
- **Use arquivos .img** quando disponíveis (dados reais do equipamento)
- **TIFF convertidos** devem ter SID e DPI corretos configurados
- Valores incorretos afetam cálculos de distância física

### Validação
- Todos os conversores geram **File Meta Information Header completo**
- Arquivos podem ser lidos **sem `force=True`**
- Transfer Syntax: **Explicit VR Little Endian**
- SOP Class: **RT Image Storage** (1.2.840.10008.5.1.4.1.1.481.1)

### Compatibilidade
- ✅ Compatível com pylinac
- ✅ Compatível com visualizadores DICOM padrão
- ✅ Compatível com sistemas PACS
- ✅ Segue especificação DICOM 3.0

## 🐛 Solução de Problemas

### "pylinac não está instalado"
```bash
pip install pylinac
```

### "Arquivo DICOM inválido" no pylinac
- Verifique se File Meta Information Header está presente
- Use `fix_dicom_header.py` para corrigir
- Confirme Transfer Syntax UID

### Erro ao converter TIFF
- Verifique formato do arquivo (deve ser .tif ou .tiff)
- Confirme que DPI é válido (> 0)
- Teste arquivo individualmente antes de lote

### Arquivos não aparecem no conversor em lote
- Extensão deve ser .tif ou .tiff (case-insensitive)
- Pasta deve ter permissão de leitura
- Clique em "Atualizar Preview"

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Changelog

### v1.1.0 (2025-12-02)
- 🐛 **FIX:** Corrigido bug no diálogo "Adicionar Item" - StringVar não sincronizava com Entry
- ✨ **NEW:** Sistema de templates JSON editável (templates_wl.json)
- ✨ **NEW:** Botões para salvar 💾 e deletar 🗑 templates personalizados
- ✨ **NEW:** Templates carregados dinamicamente do JSON
- 📚 **DOCS:** Explicação detalhada sobre como o conversor em lote determina ângulos
- 📚 **DOCS:** Seção sobre templates Winston-Lutz no README
- 🔧 **TECH:** Removido código hardcoded de templates, agora usa JSON
- 🔧 **TECH:** Entry widgets usam .get() direto em vez de StringVar

### v1.0.0 (2025-12-02)
- ✨ Lançamento inicial
- ✅ Conversor IMG para DICOM
- ✅ Conversor TIFF individual
- ✅ Conversor em lote TIFF
- ✅ Templates Winston-Lutz (4, 7, 9 ângulos)
- ✅ Drag-and-drop para reordenar
- ✅ Preview interativo
- ✅ Validação completa
- ✅ Documentação extensiva

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

- Desenvolvido para uso em radioterapia
- Baseado em pylinac e pydicom

## 🙏 Agradecimentos

- **[pylinac](https://github.com/jrkerns/pylinac)** - Framework de análise QA
- **[pydicom](https://github.com/pydicom/pydicom)** - Biblioteca DICOM para Python
- Comunidade de física médica e radioterapia

## 📞 Suporte

Para problemas ou dúvidas:
1. Consulte a documentação nos arquivos .txt
2. Verifique [Issues](https://github.com/seu-usuario/conversor-dicom-unificado/issues)
3. Abra uma nova issue se necessário

## 🔮 Roadmap

Futuras melhorias planejadas:
- [ ] Suporte a mais formatos de imagem (PNG, JPG)
- [ ] Templates salvos/carregados de arquivo
- [ ] Integração com análise pylinac direta na interface
- [ ] Suporte a conversão reversa (DICOM → TIFF)
- [ ] Batch processing via linha de comando
- [ ] Exportação de relatórios em PDF

---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

## 📸 Screenshots

### Menu Principal
Interface principal com 3 opções de conversão.

### Conversor em Lote
- Seleção de templates
- Preview interativo
- Drag-and-drop
- Barra de progresso

---

**Desenvolvido para física médica e radioterapia** | **Compatível com TG-142** | **100% Python**
