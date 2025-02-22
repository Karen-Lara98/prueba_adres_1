import pandas as pd
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def home(request):
    context = {}  # Inicializamos el contexto que se enviará al template
    
    # Verificamos que se haya enviado una petición POST con un archivo adjunto
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]

        # a. Validar que el archivo tenga extensión .txt
        if not uploaded_file.name.endswith(".txt"):
            context["result"] = "Error: Por favor sube un archivo txt válido."
            return render(request, "home.html", context)

        # Guardamos el archivo de forma temporal usando default_storage
        file_path = default_storage.save("temp/" + uploaded_file.name, ContentFile(uploaded_file.read()))

        try:
            # Leemos el archivo txt con pandas
            df = pd.read_csv(default_storage.path(file_path), delimiter=",", header=None)
        except Exception as e:
            context["result"] = f"Error al procesar el archivo: {str(e)}"
            return render(request, "home.html", context)

        # a. Validar que el archivo tenga exactamente 5 columnas
        if df.shape[1] != 5:
            context["result"] = "Error: El archivo debe tener exactamente 5 columnas."
            return render(request, "home.html", context)

        errores = []  # Lista para almacenar los errores encontrados

        # Recorremos cada fila del DataFrame para validar cada columna
        for index, row in df.iterrows():
            fila = index + 1  # Para que la numeración comience en 1

            # b. Columna 1: Solo números enteros de 3 a 10 caracteres
            col1 = str(row[0]).strip()
            print(row[0], type(row[0]), len(col1))
            if not len(col1) >= 3 and not len(col1) <= 10:
                errores.append(f"Fila {fila}, Columna 1: debe ser un número entero de 3 a 10 dígitos.")

            # c. Columna 2: Solo correos electrónicos válidos
            col2 = str(row[1]).strip()
            try:
                validate_email(col2)
            except ValidationError:
                errores.append(f"Fila {fila}, Columna 2: correo electrónico inválido.")

            # d. Columna 3: Solo se permiten los valores "CC" o "TI"
            col3 = str(row[2]).strip().upper()
            if col3 not in ["CC", "TI"]:
                errores.append(f"Fila {fila}, Columna 3: debe ser 'CC' o 'TI'.")

            # e. Columna 4: Solo valores numéricos entre 500000 y 1500000
            try:
                col4 = int(row[3])
                if not (500000 <= col4 <= 1500000):
                    errores.append(f"Fila {fila}, Columna 4: debe estar entre 500000 y 1500000.")
            except ValueError:
                errores.append(f"Fila {fila}, Columna 4: debe ser un número.")

            # f. Columna 5: No se requiere validación (se acepta cualquier valor)

        # Se envía al template el resultado de la validación
        if errores:
            # Si hay errores, los concatenamos en un solo mensaje
            context["result"] = "Se encontraron errores:\n" + "\n".join(errores)
        else:
            context["result"] = "Archivo validado correctamente."

    # Se renderiza el template 'home.html' enviando el contexto
    return render(request, "home.html", context)