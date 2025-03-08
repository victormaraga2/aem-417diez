FROM odoo:17.0

# Instalar el paquete lxml con soporte para html_clean
#RUN pip install lxml_html_clean

# Eliminar dependencias conflictivas del sistema
#RUN apt-get remove -y python3-lxml && apt-get update

# Instalar la versión correcta de lxml
RUN pip install --force-reinstall --upgrade lxml[html_clean]==4.9.3

#RUN apt-get update && apt-get install -y python3.10 python3.10-distutils
#RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
#RUN pip3 install lxml[html_clean]
