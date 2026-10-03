# VBC Player - Automação de Rádio

Aplicativo desktop em Python e PySide6, baseado no [frame VBC Player - Automacao de Radio](https://www.figma.com/design/vhHrQAYN6pifJngkRd2aUY/VBC-PLAYER?node-id=16-157). A tela principal reproduz o layout de 1440 × 900, com decks, playlist, explorador, relógio, modos e controles de reprodução.

## Executar

Requer Python 3.10+ e um sistema compatível com PySide6 6.11.2.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
```

No Windows, ative o ambiente com `.venv\Scripts\activate`. Neste workspace o ambiente `.venv` já está instalado: execute `.venv/bin/python main.py`.

## Uso

- A lista inicial é uma referência visual do Figma; não inclui as músicas. Clique em **Adicionar** ou use **Ctrl+O** para importar áudio. A primeira importação substitui a referência pelos arquivos reais.
- Clique duas vezes numa faixa para reproduzi-la. **Play**, **Stop**, **Pausa**, **Próximo**, volume e posição do áudio estão conectados ao Qt Multimedia.
- **Espaço** alterna reprodução/pausa; **Ctrl+→** avança; **Ctrl+S** salva a lista; **Esc** retorna ao player.
- **Automático** avança ao fim do áudio; **Manual** espera o operador. **Loop** repete a lista; **Aleatório** escolhe a próxima faixa.
- O explorador mantém o desenho do Figma, mas a árvore contém somente dados reais do computador. **Músicas**, **Pasta pessoal**, **Downloads**, **Documentos**, **Área de trabalho** e os volumes disponíveis no macOS ou Windows aparecem diretamente como raízes da árvore. Serviços ausentes, como OneDrive, não são exibidos.
- Clique numa pasta para expandir seus filhos dentro da mesma árvore. A seta permite recolhê-la. O nome da pasta no caminho abre o seletor nativo. **Backspace** seleciona a pasta superior e **F5** atualiza o conteúdo.
- A busca filtra nomes de áudio na pasta exibida e nas subpastas expandidas; as pastas continuam visíveis para navegação. Clique duas vezes num áudio para adicioná-lo, ou selecione vários e pressione **Enter**. O menu do botão direito também oferece **Adicionar selecionados**, navegação e atualização. **Ctrl+F** foca a busca.
- **Nova lista**, **Abrir** e **Salvar** trabalham com playlists JSON. Arquivos de áudio não são copiados para o projeto.
- **Agendador** executa eventos únicos com arquivos locais. Eventos existem somente durante a sessão e exigem o aplicativo aberto.
- **Eventos** exibe ações e erros da sessão; **Relatórios** exporta as reproduções iniciadas em CSV.
- Arraste o cabeçalho para mover a janela. Os botões de minimizar, maximizar/restaurar e fechar funcionam; o canto inferior direito permite redimensionar.

## Organização

```text
main.py
vbc_player/
  app.py                       # Inicialização, fonte e tema
  main_window.py               # Composição e navegação
  theme.py                     # Paths e estilo das páginas auxiliares
  models.py                    # Modelo de faixa e dados de demonstração
  pages/
    player/
      page.py
      widgets/                 # Widgets específicos do player
        deck.py
        clock.py
        modes.py
        playlist.py
        explorer.py
        transport.py
    schedule/
      page.py
    events/
      page.py
    reports/
      page.py
  common/
    widgets/                   # Componentes compartilhados
      design_panel.py          # Base para vetores, textos e controles Qt
      header.py
      toolbar.py
  services/
    playback.py                # Reprodução e fila compartilhadas
    playlist_storage.py        # Leitura e gravação de listas
    filesystem_locations.py    # Pastas do usuário e volumes do sistema
assets/
  figma/                       # 72 SVGs originais, usados localmente
  fonts/                       # Inter e licença OFL
design/
  geometry-*.json               # Geometria, tipografia e cores dos componentes
  assets.json                   # Mapeamento entre camadas e SVGs
  figma-reference.tsx            # Referência exportada; não é código do aplicativo
tests/
  test_app.py
```

Cada página possui seu próprio pacote em `pages/<nome>/`, com a composição em `page.py` e seus widgets específicos em `widgets/`. Apenas componentes compartilhados ficam em `common/widgets/`. As páginas de agendamento, eventos e relatórios usam controles Qt diretamente e ainda não precisam de widgets próprios. Para novas páginas, siga essa estrutura e registre a classe no mapa da janela.

Cada painel possui sua própria classe. As medidas do Figma são locais ao painel e escalam com ele; os layouts Qt compõem as linhas e mantêm os espaçamentos. Os SVGs permanecem intactos, sem dependência de URLs temporárias. Para mudanças visuais, ajuste o componente correspondente e seus dados em `design/`.

## Validação

```sh
QT_QPA_PLATFORM=offscreen .venv/bin/python -m unittest discover -s tests -v
```

Os testes verificam navegação e geometria, integridade dos assets, reprodução de WAV, volume, remoção, avanço automático, agendamento e validação de playlists. O explorador é testado com pastas temporárias, nomes Unicode, extensões em maiúsculas, busca, seleção múltipla, subpastas e atualização de arquivos. Geram capturas da interface em `design/implementation-*.png`.

O workflow `.github/workflows/tests.yml` executa essa suíte em macOS e Windows no GitHub Actions após um push ou pull request. A validação local foi feita no macOS; a execução nativa no Windows depende desse workflow ou de uma máquina Windows.

O explorador usa [QStandardPaths](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QStandardPaths.html), [QStorageInfo](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QStorageInfo.html) e os modelos de item do Qt. Ele respeita as permissões de leitura do sistema e mostra apenas pastas e os formatos de áudio aceitos pela interface.

## Limites atuais

AGC e medidores estéreo mantêm as leituras demonstrativas do design; não processam nem medem o áudio. Crossfade é uma referência visual e não mistura faixas. Satélite não está conectado. O relógio e o nome da saída usam os valores reais do computador. Não há streaming, gravação, persistência dos eventos ou recuperação de sessão nesta versão. A disponibilidade de formatos depende dos codecs do Qt e do sistema.

Reprodução usa [QMediaPlayer](https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QMediaPlayer.html) e [QAudioOutput](https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QAudioOutput.html), conforme a documentação oficial do Qt.
