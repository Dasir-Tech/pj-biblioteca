from .models import Editor

def disattiva_editor(id):
    editor = Editor.objects.get(id=id)
    editor.attivo = False
    editor.save()

# Create your views here.
