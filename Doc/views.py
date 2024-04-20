from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from .utils import convert_images_to_pdfs,collect_pdfs,count_images_in_folder,count_pdf_pages,rename_images,add_logo_to_pdf
from django.http import JsonResponse
import os
from .forms import LogoForm,ContactForm
from .models import Task


def start(request):
    return render(request,'start.html')

def convert_images(request):
    if request.method == 'POST':
        input_folder = request.POST.get('input_folder')
        output_folder = request.POST.get('output_folder')

        input_exists = os.path.exists(input_folder)
        output_exists = os.path.exists(output_folder)

        # Check if input and output folders exist
        if not input_exists and not output_exists:
            messages.error(request, 'Both input and output folder paths do not exist.')
        elif not input_exists:
            messages.error(request, 'Input folder path does not exist.')
        elif not output_exists:
            messages.error(request, 'Output folder path does not exist.')
            
        if not input_exists or not output_exists:
            return render(request, 'convert_images.html')

        # Perform conversion
        convert_images_to_pdfs(input_folder, output_folder)

        messages.success(request, 'Conversion successful')
        return render(request, 'convert_images.html')

    return render(request, 'convert_images.html')


def pdf_collector_view(request):
    if request.method == 'POST':
        input_folder = request.POST.get('input_folder')
        output_folder = request.POST.get('output_folder')

        # Check if input and output folders are provided
        if input_folder and output_folder:
            input_exists = os.path.exists(input_folder)
            output_exists = os.path.exists(output_folder)

            # Check if both input and output folders exist
            if input_exists and output_exists:
                # Call collect_pdfs function
                collect_pdfs(input_folder, output_folder)
                messages.success(request, 'PDFs collected successfully!')
                return redirect('pdf_collector')
            elif not input_exists and not output_exists:
                messages.error(request, f"Both input folder '{input_folder}' and output folder '{output_folder}' paths do not exist.")
            elif not input_exists:
                messages.error(request, f"The specified input folder '{input_folder}' does not exist.")
            else:
                messages.error(request, f"The specified output folder '{output_folder}' does not exist.")
        else:
            messages.error(request, 'Please provide both input and output folder paths.')

    return render(request, 'pdf_collector.html')

def image_counter(request):
    folder_path = ''
    image_count = {}
    total_images = 0
    error_message = None

    if request.method == 'POST':
        folder_path = request.POST.get('folder_path', None)
        if folder_path:
            if os.path.exists(folder_path):
                for root, dirs, files in os.walk(folder_path):
                    if files:
                        folder_images = count_images_in_folder(root)
                        image_count[root] = folder_images
                total_images = count_images_in_folder(folder_path)
            else:
                error_message = f"The specified folder '{folder_path}' does not exist."

    return render(request, 'image_counter.html', {
        'folder_path': folder_path,
        'image_count': image_count,
        'total_images': total_images,
        'error_message': error_message
    })

def pdf_counter(request):
    folder_path = ''
    pdf_info = []
    error_message = None

    if request.method == 'POST':
        folder_path = request.POST.get('folder_path', None)
        if folder_path:
            if not os.path.exists(folder_path):
                error_message = "The specified folder path does not exist."
            else:
                pdf_info = count_pdf_pages(folder_path)

    return render(request, 'pdf_counter.html', {
        'folder_path': folder_path,
        'pdf_info': pdf_info,
        'error_message': error_message
    })



def rename_images_view(request):
    if request.method == 'POST':
        source_folder = request.POST.get('source_folder')
        destination_folder = request.POST.get('destination_folder')
        image_name = request.POST.get('image_name')

        # Check if source and destination folders exist
        if not os.path.exists(source_folder) or not os.path.exists(destination_folder):
            messages.error(request, "Source or destination folder does not exist.")
            return redirect('rename_images_view')

        # Call the function to rename images
        try:
            rename_images(source_folder, destination_folder, image_name)
            messages.success(request, "Images renamed successfully.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('rename_images_view')

    return render(request, 'rename_images.html')

def add_logo_view(request):
    if request.method == 'POST':
        form = LogoForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            logo = request.FILES['logo']
            output_pdf_path = f'media/pdfs/output_{pdf_file.name}'

            try:
                add_logo_to_pdf(pdf_file, output_pdf_path, logo)
                messages.success(request, 'PDF with the logo has been successfully generated.')
                return render(request, 'result.html', {'output_pdf_path': output_pdf_path,'pdf_file':pdf_file,'logo':logo})
            except Exception as e:
                error_message = f"Error: {e}"
                messages.error(request, error_message)
            
            return render(request, 'add_logo.html')
    else:
        form = LogoForm()
    
    return render(request, 'add_logo.html', {'form': form})

def download_pdf(request, path):
    # Extracting file name from path
    filename = path.split('/')[-1]
    # Constructing file path without the '/add_logo' prefix
    file_path = f'media/pdfs/{filename}'
    # Open the file in binary mode
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    
def Requerments(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('requerments')  # Redirect to a success page
        else:
            # If form is not valid, handle the errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = ContactForm()
    return render(request, 'requerments.html', {'form': form})

def index(request):
    tasks=Task.objects.all()
    if request.method == 'POST':
        to_do=request.POST.get('to_do')
        task=Task.objects.create(description=to_do)
        task.save()
        

    return render(request,'index.html',{'tasks':tasks})





def to_do_delete(request,to_do_id):
    task=Task.objects.get(id=to_do_id)
    task.delete()
    return redirect(index)

def mark_task_completed(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        try:
            task = Task.objects.get(id=task_id)
            task.completed = True
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)