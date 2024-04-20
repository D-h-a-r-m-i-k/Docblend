# pdf_converter/utils.py
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from img2pdf import convert
import shutil
from PyPDF2 import PdfReader,PdfWriter
from pathlib import Path
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

logger = logging.getLogger(__name__)

def convert_image_to_pdf(image_path, pdf_path):
    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Convert to RGB mode
            img.save(pdf_path, "PDF", resolution=100.0, save_all=True)
    except Exception as e:
        logger.error(f"Error converting image to PDF: {e}")

def convert_images_to_pdfs(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_output_folder = os.path.join(output_folder, "output_pdfs")
    if not os.path.exists(pdf_output_folder):
        os.makedirs(pdf_output_folder)

    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    def convert_image(image_file):
        image_path = os.path.join(input_folder, image_file)
        pdf_name = os.path.splitext(image_file)[0] + '.pdf'
        pdf_path = os.path.join(pdf_output_folder, pdf_name)
        try:
            convert_image_to_pdf(image_path, pdf_path)
        except Exception as e:
            logger.error(f"Error converting {image_path} to PDF: {e}")

    with ThreadPoolExecutor() as executor:
        executor.map(convert_image, image_files)

def collect_pdfs(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Walk through the input folder and its subfolders
    for foldername, _, filenames in os.walk(input_folder):
        for filename in filenames:
            # Check if the file is a PDF
            if filename.lower().endswith(".pdf"):
                # Construct the full path of the source PDF file
                source_path = os.path.join(foldername, filename)

                # Construct the full path of the destination PDF file
                destination_path = os.path.join(output_folder, filename)

                # Check if the destination file already exists
                counter = 1
                while os.path.exists(destination_path):
                    # If it does, append a number to the filename
                    new_filename = f"{os.path.splitext(filename)[0]}_{counter}.pdf"
                    destination_path = os.path.join(output_folder, new_filename)
                    counter += 1

                # Copy the PDF file to the destination folder
                shutil.copy2(source_path, destination_path)

    return "PDFs collected successfully!"

def count_images_in_folder(folder_path):
    total_images = 0
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.img', '.gif', '.bmp')):
                total_images += 1
    return total_images

def count_pdf_pages(folder_path):
    pdf_info = []
    sr = 1
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    pdf_reader = PdfReader(f)
                    pdf_pages = len(pdf_reader.pages)
                    pdf_info.append([sr, file_path, file, pdf_pages])
                    sr += 1
    return pdf_info

def rename_images(source_folder, destination_folder, image_name):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    image_files = sorted([f for f in os.listdir(source_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))], key=lambda x: int(''.join(filter(str.isdigit, x))))

    for index, image_file in enumerate(image_files, start=1):
        # Get the file extension
        _, extension = os.path.splitext(image_file)

        # Create a new filename with a sequential number and the original extension
        new_filename = f"{image_name}_{index}{extension}"

        # Construct the full paths for the source and destination files
        source_path = os.path.join(source_folder, image_file)
        destination_path = os.path.join(destination_folder, new_filename)

        # Copy and rename the file
        shutil.copy(source_path, destination_path)

def add_logo_to_pdf(pdf_file, output_pdf_path, logo):
    # Create a PDF canvas
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    #transparency=0.5
    # Draw the logo on the canvas
    logo_reader = ImageReader(logo)
    can.setFillColorRGB(1, 1, 1, 1)
    can.drawImage(logo_reader, 10, 10, width=570, height=150,mask="auto")

    # Close the canvas
    can.save()

    # Move the buffer position to the beginning
    packet.seek(0)
    
    # Create a new PDF with the logo
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(pdf_file)
    output = PdfWriter()

    # Add the logo to each page of the existing PDF
    for i in range(len(existing_pdf.pages)):
        page = existing_pdf.pages[i]
        page.merge_page(new_pdf.pages[0])
        output.add_page(page)

    # Write the result to the output PDF file
    with open(output_pdf_path, "wb") as outputStream:
        output.write(outputStream)