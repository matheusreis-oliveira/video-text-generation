import cv2
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import pandas as pd
import subprocess
import requests
import time  # Para medir o tempo de execução

def load_quotes_from_csv(file_path):
    print("Carregando citações do arquivo CSV...")
    start_time = time.time()
    df = pd.read_csv(file_path, encoding='ISO-8859-1')
    quotes = [f"{row['frase']} - {row['autor']}" for _, row in df.iterrows()]
    print(f"Citações carregadas com sucesso em {time.time() - start_time:.2f} segundos.")
    return quotes

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    line = ""
    
    for word in words:
        test_line = f"{line}{word} "
        bbox = font.getbbox(test_line)
        if bbox[2] <= max_width:
            line = test_line
        else:
            lines.append(line.strip())
            line = f"{word} "
    
    if line:
        lines.append(line.strip())
    
    return lines

def add_text_to_frame(frame, text, author, font_path, img_size, transparency=0.5):
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert("RGBA")
    txt_layer = Image.new("RGBA", img_pil.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_layer)

    max_width = img_size[0] - 40
    max_height = img_size[1] - 40
    
    font_size = int(img_size[1] * 0.03)  # Diminuído para 0.03
    font = ImageFont.truetype(font_path, font_size)
    author_font_size = int(font_size * 0.8)
    author_font = ImageFont.truetype(font_path, author_font_size)
    
    lines = wrap_text(text, font, max_width)
    author_text = " - " + author
    
    total_text_height = sum(draw.textbbox((0, 0), line, font=font)[3] for line in lines)
    author_height = draw.textbbox((0, 0), author_text, font=author_font)[3]
    total_height = total_text_height + len(lines) * 4 + author_height + 20  # Ajusta espaçamento

    y = (img_size[1] - total_height - 20) // 2

    for line in lines:
        text_width, text_height = draw.textbbox((0, 0), line, font=font)[2:4]
        x = (img_size[0] - text_width) // 2
        draw.text((x, y), line, font=font, fill=(255, 255, 255, int(255 * transparency)))
        y += text_height + 4  # Ajusta espaçamento

    author_width, author_height = draw.textbbox((0, 0), author_text, font=author_font)[2:4]
    y += 10  # Ajusta o espaçamento entre o texto e o autor
    x = (img_size[0] - author_width) // 2
    draw.text((x, y), author_text, font=author_font, fill=(255, 255, 255, int(255 * transparency)))

    combined = Image.alpha_composite(img_pil, txt_layer)
    return cv2.cvtColor(np.array(combined.convert("RGB")), cv2.COLOR_RGB2BGR)

def add_text_to_video(input_video_path, output_video_path, quote, ffmpeg_path, font_path):
    print(f"Processando vídeo: {input_video_path}")
    start_time = time.time()
    text, author = quote.rsplit(' - ', 1)
    
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Erro ao abrir o vídeo: {input_video_path}")
        return
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    try:
        font = ImageFont.truetype(font_path, int(height * 0.03))
    except IOError:
        print(f"Erro ao carregar a fonte '{font_path}'. Usando Arial como fallback.")
        font = ImageFont.truetype("arial.ttf", int(height * 0.03))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = add_text_to_frame(frame, text, author, font_path, (width, height))
        out.write(frame)
        frame_count += 1

        if frame_count % 50 == 0:
            print(f"Processado {frame_count} frames...")

    cap.release()
    out.release()

    temp_video_path = output_video_path.replace('.mp4', '_temp.mp4')
    os.rename(output_video_path, temp_video_path)
    subprocess.run([ffmpeg_path, '-i', temp_video_path, '-i', input_video_path, '-c', 'copy', '-map', '0:v:0', '-map', '1:a:0', output_video_path])
    os.remove(temp_video_path)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Vídeo processado com sucesso: {output_video_path} em {elapsed_time:.2f} segundos")
    return elapsed_time

def get_unique_output_path(output_path):
    base, ext = os.path.splitext(output_path)
    counter = 1
    new_output_path = output_path
    while os.path.exists(new_output_path):
        new_output_path = f"{base}_{counter}{ext}"
        counter += 1
    return new_output_path

def download_font(url, save_path):
    print(f"Baixando a fonte de {url}...")
    start_time = time.time()
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"Fonte baixada e salva em {save_path} em {time.time() - start_time:.2f} segundos")

def create_example_files(base_dir):
    input_dir = os.path.join(base_dir, "video-input")
    output_dir = os.path.join(base_dir, "video-output")
    quotes_file = os.path.join(base_dir, "quotes.csv")
    font_path = os.path.join(base_dir, "DejaVuSans-Bold.ttf")
    font_url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans-Bold.ttf"

    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(quotes_file):
        with open(quotes_file, "w", encoding='ISO-8859-1') as f:
            f.write("frase,autor\n")
            f.write("A persistência é o caminho do êxito.,Charles Chaplin\n")
            f.write("O único lugar onde o sucesso vem antes do trabalho é no dicionário.,Albert Einstein\n")

    if len(os.listdir(input_dir)) == 0:
        create_example_video(os.path.join(input_dir, "example.mp4"))

    if not os.path.exists(font_path):
        try:
            download_font(font_url, font_path)
        except Exception as e:
            print(f"Erro ao baixar a fonte: {e}")
            font_path = "arial.ttf"

    return input_dir, output_dir, quotes_file, font_path

def create_example_video(path):
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))
    frame = np.zeros((height, width, 3), np.uint8)
    cv2.putText(frame, "Exemplo", (50, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    for _ in range(fps * 5):  # 5 segundos de vídeo
        out.write(frame)
    out.release()

base_dir = os.path.dirname(os.path.abspath(__file__))

input_directory, output_directory, csv_file_path, font_path = create_example_files(base_dir)

quotes = load_quotes_from_csv(csv_file_path)

ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"

total_start_time = time.time()
total_elapsed_time = 0

for filename in os.listdir(input_directory):
    if filename.endswith(".mp4"):
        input_video_path = os.path.join(input_directory, filename)
        for j, quote in enumerate(quotes):
            output_video_path = os.path.join(output_directory, f"output_{os.path.splitext(filename)[0]}_{j+1}.mp4")
            output_video_path = get_unique_output_path(output_video_path)
            elapsed_time = add_text_to_video(input_video_path, output_video_path, quote, ffmpeg_path, font_path)
            total_elapsed_time += elapsed_time

total_end_time = time.time()
total_time = total_end_time - total_start_time
print(f"\nTodos os vídeos foram processados com sucesso!")
print(f"Tempo total de processamento: {total_time:.2f} segundos")
