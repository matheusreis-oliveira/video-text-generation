

# Tutorial para o Script de Edição de Vídeos

Este script processa vídeos adicionando citações em texto, utilizando fontes personalizadas e realizando a fusão com o áudio original do vídeo. A seguir, um guia completo para configurar e executar o script.

## Requisitos

Antes de começar, certifique-se de que você tem os seguintes requisitos instalados:

1.  **Python 3.x**: O script foi desenvolvido para Python 3.x. Você pode baixar o Python [aqui](https://www.python.org/downloads/).
    
2.  **Pacotes Python**: O script utiliza pacotes Python externos que precisam ser instalados. Você pode instalar todos os pacotes necessários usando o `pip`. Execute o seguinte comando no terminal ou prompt de comando:
`pip install opencv-python pillow numpy pandas requests` 
    
3.  **FFmpeg**: O FFmpeg é uma ferramenta de linha de comando para processar vídeo e áudio. Baixe e instale o FFmpeg [aqui](https://ffmpeg.org/download.html) e adicione o caminho do executável (`ffmpeg.exe`) ao seu PATH do sistema.
    
4.  **Fontes**: O script usa a fonte "DejaVuSans-Bold.ttf". Se você deseja usar outra fonte, certifique-se de atualizar o script conforme necessário.
    

## Preparação do Ambiente

### Estrutura de Diretórios

Certifique-se de que a estrutura de diretórios do projeto seja semelhante à seguinte:

    project-directory/
    │
    ├── video-input/
    │ └── example.mp4  # Vídeos a serem processados
    │
    ├── video-output/
    │ # Vídeos processados serão salvos aqui
    │
    ├── quotes.csv  # Arquivo CSV com citações
    │
    ├── DejaVuSans-Bold.ttf  # Fonte para uso no script
    │
    └── add_text_to_videos_opencv.py  # O script Python

 

### Arquivo CSV

Crie um arquivo chamado `quotes.csv` no diretório raiz do projeto com o seguinte formato:
frase,autor
"A persistência é o caminho do êxito.",Charles Chaplin
"O único lugar onde o sucesso vem antes do trabalho é no dicionário.",Albert Einstein

Adicione suas próprias citações conforme desejado.

### Fontes

Se a fonte "DejaVuSans-Bold.ttf" não estiver disponível, você pode baixá-la [aqui](https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans-Bold.ttf) e colocá-la no diretório raiz do projeto.

## Configuração do Script

### Localize o Caminho do FFmpeg

Atualize o caminho do FFmpeg no script. No script, `ffmpeg_path` está definido como:

`ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"` 

Certifique-se de que este caminho aponte para o executável `ffmpeg.exe` em seu sistema.

### Fonte

Se você deseja usar uma fonte diferente, atualize o caminho da fonte no script:

`font_path = os.path.join(base_dir, "DejaVuSans-Bold.ttf")` 

## Executando o Script

### Usando o Arquivo `.bat`

Para facilitar a execução do script, você pode usar o arquivo `run_script.bat`. Este arquivo configura o caminho do interpretador Python e o caminho para o script Python.

O conteúdo do `run_script.bat` é o seguinte:

    @echo off
    REM Define o caminho do interpretador Python
    set PYTHON_PATH=C:\Users\mathr\AppData\Local\Programs\Python\Python310\python.exe
    
    REM Caminho para o script Python
    set SCRIPT_PATH=%~dp0add_text_to_videos_opencv.py
    
    REM Executa o script Python
    %PYTHON_PATH% %SCRIPT_PATH%
    
    pause

Para usar o `run_script.bat`:

1.  **Navegue até o Diretório do Projeto**: Abra o terminal ou prompt de comando e navegue até o diretório onde o arquivo `run_script.bat` está localizado:

    `cd /caminho/para/o/diretório/do/projeto` 
    
2.  **Execute o Script**: Execute o arquivo `.bat`:

    `run_script.bat` 
    
O script processará todos os vídeos na pasta `video-input`, adicionará as citações e salvará os vídeos processados na pasta `video-output`.

## Personalização

Você pode personalizar o script conforme necessário:

-   **Tamanho da Fonte**: Modifique o valor `font_size` na função `add_text_to_frame` para ajustar o tamanho do texto.
-   **Transparência do Texto**: Ajuste o parâmetro `transparency` na função `add_text_to_frame` para alterar a transparência do texto sobre o vídeo.
-   **Espaçamento do Texto**: Modifique o espaçamento entre linhas e o espaçamento entre o texto e o autor ajustando os valores na função `add_text_to_frame`.

## Suporte

Se você encontrar problemas ou tiver dúvidas sobre o script, sinta-se à vontade para abrir