#!/bin/env python
# ncoding: utf-8

# ./xmind_markdown_converter/xmind_md.py '/d/Docs/Particular/My Maps/MP XMind/MP.xmind' '/d/Docs/Particular/My Maps/MD/MP.md'

import os
import sys
import re
# import base64
import regex
import xmind
from xmind.core.workbook import WorkbookDocument, SheetElement
from xmind.core.mixin import WorkbookMixinElement
from xmind.core.topic import TopicElement
from xmind.core.title import TitleElement
from xmind.core.relationship import RelationshipElement, RelationshipsElement
from xmind.core.markerref import MarkerRefElement, MarkerRefsElement

from pathlib import Path

regex_lf_spc = re.compile('((?:\r?\n)+)')
regex_ext = re.compile('\.xmind$')
regex_file = re.compile('^file:')
regex_escape = re.compile('([\[\]\*\|])')
regex_url = re.compile('(https?://\S*)')
markdown_content: list[str] = []


def extract_topics_to_markdown(xmind_file_path: str, output_file_path: str = None):
    """
    Extrai todos os tópicos, links e imagens de um arquivo XMind e converte para Markdown.

    Args:
        xmind_file_path (str): Caminho para o arquivo XMind
        output_file_path (str, optional): Caminho para o arquivo de saída. Se None, usa o nome do arquivo XMind
    """
    global markdown_content
    markdown_content = []

    # Carrega o arquivo XMind
    try:
        workbook: WorkbookDocument = xmind.load(xmind_file_path)
    except Exception as e:
        print(f"Erro ao carregar o arquivo XMind: {e}")
        return

    # Define o arquivo de saída
    if output_file_path is None:
        base_name = Path(xmind_file_path).stem
        output_file_path = f"{base_name}.md"

    markdown_content.append(f"# {md_escape(Path(xmind_file_path).stem)}\n")

    # Processa todas as folhas do workbook
    for sheet_index, sheet in enumerate(workbook.getSheets()):
        sheet_title = md_escape(sheet.getTitle()) or f"Folha {sheet_index + 1}"
        markdown_content.append(f"## {sheet_title}\n")

        # Processa o tópico raiz
        root_topic: TopicElement = sheet.getRootTopic()
        if root_topic:
            process_topic(root_topic)

    # Escreve o arquivo Markdown
    try:
        with open(output_file_path, 'w', encoding='utf-8') as f:
            content = '\n'.join(markdown_content)
            # content = regex_lf_spc.sub('\n', content)
            f.write(content.strip() + '\n')
        print(f"Arquivo Markdown criado com sucesso: {output_file_path}")
    except Exception as e:
        print(f"Erro ao escrever o arquivo: {e}")

    # Processa imagens anexadas
    # extract_images_from_workbook(workbook)


def md_escape(content):
    content=regex_url.sub('<\\1>',content)
    return regex_escape.sub('\\\\\\1',content)


def process_topic(topic: TopicElement, level: int = 0):
    """
    Processa um tópico e seus subtópicos recursivamente.

    Args:
        topic: Objeto tópico do XMind
        markdown_content (list): Lista para armazenar o conteúdo Markdown
        level (int): Nível de hierarquia (para os headers do Markdown)
    """
    global markdown_content

    # Cria o header do Markdown baseado no nível
    spaces = ' ' * (level*2) if level else ''
    spaces2 = spaces+'  '
    header_prefix = spaces + '-'  # Máximo 6 níveis no Markdown

    # Obtém o título do tópico
    title: str = topic.getTitle() or "Sem título"
    title = regex_lf_spc.sub('', title).strip()

    # Verifica se há link (hyperlink)
    hyperlink: str = topic.getHyperlink()
    if hyperlink:
        if not title:
            title = 'link'
        hyperlink = str(regex_ext.sub('.md', hyperlink))
        hyperlink = str(regex_file.sub('', hyperlink))
        markdown_content.append(
            f"{header_prefix} [{md_escape(title)}]({hyperlink})  ")
    elif title:
        markdown_content.append(f"{header_prefix} {md_escape(title)}  ")

    # Processa notas do tópico
    notes = topic.getNotes()
    if notes:
        notes = str(regex_lf_spc.sub('\\1'+spaces2, notes.strip()))
        markdown_content.append(f"{spaces2}**Notas:** {md_escape(notes)}\n")

    # Processa labels/tags
    labels = topic.getLabels()
    if labels:
        labels_text = ", ".join([f"`{label.strip()}`" for label in labels])
        markdown_content.append(
            f"{spaces2}**Tags:** {md_escape(labels_text)}  ")

    # Processa marcadores/markers
    markers: list[MarkerRefElement | str] = topic.getMarkers()
    if markers:
        marker_list = []
        for marker in markers:
            marker_id = marker.getMarkerId() if hasattr(
                marker, 'getMarkerId') else str(marker)
            if marker_id:
                marker_list.append(str(marker_id).strip())
        if marker_list:
            markdown_content.append(
                f"{spaces2}**Marcadores:** {md_escape(', '.join(marker_list))}  ")

    # xxxx = topic.getComments()
    # xxxx = topic.getAttribute()
    # Processa subtópicos recursivamente
    subtopics = topic.getSubTopics()
    if subtopics:
        for subtopic in subtopics:
            process_topic(subtopic, level + 1)

    # Adiciona uma linha em branco após cada tópico principal
    # if level <= 3:
    #     markdown_content.append("")


def extract_images_from_workbook(workbook: WorkbookDocument, output_dir="."):
    """
    Extrai todas as imagens do workbook XMind.

    Args:
        workbook: Objeto workbook do XMind
        output_dir (str): Diretório onde salvar as imagens

    Returns:
        dict: Dicionário mapeando IDs de imagem para caminhos de arquivo
    """

    image_map = {}

    try:
        # Acessa o arquivo ZIP interno do XMind
        if hasattr(workbook, '_workbook_path'):
            import zipfile
            with zipfile.ZipFile(workbook._workbook_path, 'r') as zip_file:
                # Lista todos os arquivos no ZIP
                for file_info in zip_file.filelist:
                    # Procura por arquivos de imagem
                    if file_info.filename.startswith('attachments/') and any(
                        file_info.filename.lower().endswith(ext)
                        for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg']
                    ):
                        # Extrai a imagem
                        image_data = zip_file.read(file_info.filename)

                        # Cria o nome do arquivo de saída
                        image_filename = os.path.basename(file_info.filename)
                        output_path = os.path.join(output_dir, image_filename)

                        # Salva a imagem
                        with open(output_path, 'wb') as img_file:
                            img_file.write(image_data)

                        # Mapeia o ID da imagem para o caminho
                        image_id = file_info.filename
                        image_map[image_id] = image_filename
                        print(f"Imagem extraída: {image_filename}")

    except Exception as e:
        print(f"Erro ao extrair imagens: {e}")

    return image_map


def batch_convert_xmind_files(directory_path: str, output_directory: str = None):
    """
    Converte todos os arquivos XMind de um diretório para Markdown.

    Args:
        directory_path (str): Caminho do diretório com arquivos XMind
        output_directory (str, optional): Diretório de saída. Se None, usa o mesmo diretório
    """

    directory = Path(directory_path)
    if not directory.exists():
        print(f"Diretório não encontrado: {directory_path}")
        return

    output_dir = Path(output_directory) if output_directory else directory
    output_dir.mkdir(exist_ok=True)

    xmind_files = list(directory.glob("*.xmind"))

    if not xmind_files:
        print("Nenhum arquivo XMind encontrado no diretório.")
        return

    print(f"Encontrados {len(xmind_files)} arquivos XMind")

    for xmind_file in xmind_files:
        print(f"Processando: {xmind_file.name}")
        output_file = output_dir / f"{xmind_file.stem}.md"
        extract_topics_to_markdown(str(xmind_file), str(output_file))


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo 1: Converter um arquivo específico
    # extract_topics_to_markdown("meu_mapa_mental.xmind", "saida.md")

    # Exemplo 2: Converter todos os arquivos XMind de um diretório
    # batch_convert_xmind_files("./mapas_mentais", "./markdown_output")
    if not sys.argv[1]:
        print(f'{sys.argv[0]} <from> [to]')
        quit()
    if not os.path.isfile(sys.argv[1]):
        print('From is not file')
        quit()
    xmind_file = sys.argv[1]
    output_file = sys.argv.__getitem__(2)
    extract_topics_to_markdown(xmind_file, output_file)
