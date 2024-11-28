# Usa una imagen base de Python
FROM python:3.12-slim

# Instalar dependencias necesarias para tkinter y X11
RUN apt-get update && apt-get install -y \
    libtk8.6 \
    tk \
    libx11-dev \
    libxft-dev \
    libxext-dev \
    locales \
    && apt-get clean

# Configurar los locales
RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

# Configurar variables de entorno para los locales
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo requirements.txt
COPY requirements.txt /app/

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el proyecto al contenedor
COPY . /app/

# Comando por defecto para ejecutar el script
CMD ["python", "src/main_gui.py"]
