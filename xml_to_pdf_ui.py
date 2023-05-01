import os
import glob
import pdfkit
from lxml import etree
import tkinter as tk
from tkinter import filedialog


def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    folder_path_label.config(text=folder_path)


def select_template():
    global template_path
    template_path = filedialog.askopenfilename(filetypes=[("XSLT Files", "*.xslt")])
    template_path_label.config(text=template_path)


def convert():
    # Path to wkhtmltopdf program
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

    # pdfkit configuration
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

    # Root directory
    root_dir = folder_path

    # Template file
    xslt_file = template_path

    # All XML files
    xml_files = glob.glob(root_dir + "/**/*.xml", recursive=True)

    # Process each XML file
    for xml_file in xml_files:
        # Open XML file
        tree = etree.parse(xml_file)

        # Load XSLT processor
        xslt = etree.parse(xslt_file)
        transform = etree.XSLT(xslt)

        # Perform XSLT transformation
        result = transform(tree)

        # Convert to PDF
        pdf_content = "<html><body>" + str(result) + "</body></html>"
        pdfkit.from_string(pdf_content, os.path.splitext(xml_file)[0] + ".pdf", configuration=config)


# Create a Tkinter interface
root = tk.Tk()
root.title("XML to PDF Converter")
root.geometry("400x200")

# Select folder button
select_folder_button = tk.Button(root, text="Select Folder", command=select_folder)
select_folder_button.pack(pady=10)

# Select template button
select_template_button = tk.Button(root, text="Select Template", command=select_template)
select_template_button.pack()

# Folder path label
folder_path_label = tk.Label(root, text="")
folder_path_label.pack()

# Template file label
template_path_label = tk.Label(root, text="")
template_path_label.pack()

# Convert button
convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.pack(pady=10)

root.mainloop()
