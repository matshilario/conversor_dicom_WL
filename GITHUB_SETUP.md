# Como Publicar no GitHub

## ✅ Status Atual

- [x] Repositório Git inicializado
- [x] Branch main criada
- [x] Arquivos adicionados ao staging
- [ ] Configurar identidade Git
- [ ] Fazer commit inicial
- [ ] Criar repositório no GitHub
- [ ] Conectar repositório local ao GitHub
- [ ] Push do código

## 📋 Passo a Passo Completo

### 1. Configure sua identidade no Git (se ainda não fez)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@example.com"
```

**Verificar configuração:**
```bash
git config --global user.name
git config --global user.email
```

### 2. Fazer o commit inicial

```bash
git commit -m "Initial commit: Conversor DICOM Unificado v1.0

Suite completa de conversores DICOM para radioterapia com três interfaces:
- Conversor IMG para DICOM (Elekta iView)
- Conversor TIFF individual para DICOM
- Conversor em lote TIFF para DICOM com templates Winston-Lutz

Funcionalidades principais:
- Templates pré-definidos (WL Standard 4, Extended 7, Completo 9)
- Drag-and-drop para reordenar conversões
- Preview interativo da conversão em lote
- Validação completa de parâmetros
- File Meta Information Header completo
- 100% compatível com pylinac"
```

### 3. Criar repositório no GitHub

**Opção A: Pela interface web (mais fácil)**

1. Acesse: https://github.com/new
2. Nome do repositório: `conversor-dicom-unificado`
3. Descrição: `Suite de conversores DICOM para radioterapia - Winston-Lutz e QA`
4. Escolha: **Public** ou **Private**
5. **NÃO** marque:
   - ❌ Add a README file
   - ❌ Add .gitignore
   - ❌ Choose a license

   (já temos esses arquivos localmente)

6. Clique em **"Create repository"**

**Opção B: Via GitHub CLI (se instalado)**

```bash
gh repo create conversor-dicom-unificado --public --source=. --remote=origin --push
```

### 4. Conectar repositório local ao GitHub

Após criar o repositório no GitHub, você verá instruções. Use:

```bash
git remote add origin https://github.com/SEU-USUARIO/conversor-dicom-unificado.git
```

**Ou se usar SSH:**
```bash
git remote add origin git@github.com:SEU-USUARIO/conversor-dicom-unificado.git
```

**Verificar:**
```bash
git remote -v
```

### 5. Push do código para o GitHub

```bash
git push -u origin main
```

Se pedir autenticação:
- **Username:** seu usuário do GitHub
- **Password:** use um **Personal Access Token** (não a senha da conta)

#### Como criar Personal Access Token:

1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. "Generate new token" → "Generate new token (classic)"
3. Nome: `Conversor DICOM`
4. Scopes necessários:
   - ✅ `repo` (todos)
5. "Generate token"
6. **COPIE O TOKEN** (não será mostrado novamente!)
7. Use o token como senha no `git push`

### 6. Verificar no GitHub

Acesse: `https://github.com/SEU-USUARIO/conversor-dicom-unificado`

Você deve ver:
- ✅ Código-fonte
- ✅ README.md formatado
- ✅ 14 arquivos
- ✅ Licença MIT

## 🔄 Comandos Úteis Após Configurar

### Fazer alterações futuras:

```bash
# Ver status
git status

# Adicionar arquivos modificados
git add arquivo.py

# Ou adicionar todos
git add .

# Commit
git commit -m "Descrição da mudança"

# Push para GitHub
git push
```

### Ver histórico:

```bash
git log --oneline
```

### Ver diferenças:

```bash
git diff
```

### Criar nova branch:

```bash
git checkout -b feature/nova-funcionalidade
```

## 📦 Arquivos no Repositório

Arquivos incluídos no commit:
- ✅ `conversor_dicom_unificado.py` - Interface principal
- ✅ `dicom_converter_gui.py` - Conversor IMG
- ✅ `tiff_to_dicom_gui.py` - Conversor TIFF individual
- ✅ `fix_dicom_header.py` - Correção de headers
- ✅ `comparar_img_vs_tiff.py` - Comparação
- ✅ `read_dicom.py` - Leitor DICOM
- ✅ `analyze_00002938.py` - Análise de pasta
- ✅ `README.md` - Documentação principal
- ✅ `LICENSE` - Licença MIT
- ✅ `.gitignore` - Arquivos ignorados
- ✅ `requirements.txt` - Dependências
- ✅ `CONVERSOR_EM_LOTE_GUIA.txt` - Guia detalhado
- ✅ `COMPARACAO_IMG_TIFF_RESUMO.txt` - Comparação técnica
- ✅ `TESTE_REALIZADO.txt` - Documentação de testes

Arquivos **excluídos** (.gitignore):
- ❌ Arquivos .dcm, .img, .tiff (dados de pacientes)
- ❌ Pasta `00002938/` (dados de pacientes)
- ❌ Pasta `imagens TIFF/` (dados de teste)
- ❌ `.venv/` (ambiente virtual)
- ❌ `__pycache__/` (cache Python)

## 🛡️ Segurança

**IMPORTANTE:** O `.gitignore` está configurado para **NÃO** incluir:
- Dados de pacientes (arquivos DICOM, IMG, TIFF)
- Pastas com dados sensíveis
- Credenciais
- Arquivos de configuração local

**Sempre verifique** antes de fazer push:
```bash
git status
```

Se aparecer algum arquivo sensível, adicione ao `.gitignore`:
```bash
echo "nome_do_arquivo.dcm" >> .gitignore
git add .gitignore
git commit -m "Update .gitignore"
```

## 📝 Modelo de Commit Messages

Formato recomendado:

```
Tipo: Descrição curta (50 caracteres)

Descrição detalhada (opcional)
- Lista de mudanças
- O que foi alterado
- Por que foi alterado

Closes #issue-number (se aplicável)
```

**Tipos:**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

**Exemplos:**
```bash
git commit -m "feat: Adicionar template WL Completo 13"
git commit -m "fix: Corrigir validação de ângulos negativos"
git commit -m "docs: Atualizar guia do conversor em lote"
```

## 🔧 Solução de Problemas

### "Permission denied (publickey)"
Use HTTPS em vez de SSH:
```bash
git remote set-url origin https://github.com/SEU-USUARIO/conversor-dicom-unificado.git
```

### "Authentication failed"
1. Use Personal Access Token, não senha
2. Ou configure SSH keys

### "Updates were rejected"
Faça pull primeiro:
```bash
git pull origin main --rebase
git push
```

### Ver configuração atual:
```bash
git config --list
```

## 📊 Badges para o README

Após publicar, você pode adicionar badges ao README.md:

```markdown
![GitHub stars](https://img.shields.io/github/stars/SEU-USUARIO/conversor-dicom-unificado)
![GitHub forks](https://img.shields.io/github/forks/SEU-USUARIO/conversor-dicom-unificado)
![GitHub issues](https://img.shields.io/github/issues/SEU-USUARIO/conversor-dicom-unificado)
![Last commit](https://img.shields.io/github/last-commit/SEU-USUARIO/conversor-dicom-unificado)
```

## 🌐 URL do Repositório

Após criar, seu repositório estará em:
```
https://github.com/SEU-USUARIO/conversor-dicom-unificado
```

Clone URL (para outros usuários):
```bash
git clone https://github.com/SEU-USUARIO/conversor-dicom-unificado.git
```

## ✅ Checklist Final

Antes de publicar, confirme:
- [ ] Git configurado (nome e email)
- [ ] Commit feito com mensagem descritiva
- [ ] Repositório criado no GitHub
- [ ] Remote origin configurado
- [ ] Push realizado com sucesso
- [ ] README aparece formatado no GitHub
- [ ] Nenhum dado de paciente foi incluído
- [ ] .gitignore funcionando corretamente

## 🎉 Pronto!

Seu projeto está agora no GitHub e pronto para:
- Compartilhar com colegas
- Receber contribuições
- Versionar alterações
- Fazer backup na nuvem

---

**Dúvidas?** Consulte a documentação do Git: https://git-scm.com/doc
