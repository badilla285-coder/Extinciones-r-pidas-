import streamlit as st
from docx import Document
from docx.shared import Pt
import PyPDF2
import io

def crear_escrito(datos, texto_condena):
    doc = Document()
    
    # Configuración de estilo Arial 12 para que sea formal
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(12)

    # 1. ENCABEZADO (Sumilla)
    p = doc.add_paragraph()
    p.add_run("SUMILLA: SOLICITA DECLARACIÓN DE EXTINCIÓN DE RESPONSABILIDAD PENAL.\n").bold = True
    p.add_run(f"RIT: {datos['rit']}\n")
    p.add_run(f"RUC: {datos['ruc']}\n")
    p.add_run(f"TRIBUNAL: {datos['juzgado']}\n")

    # 2. CUERPO DEL ESCRITO
    doc.add_paragraph("\nEN LO PRINCIPAL: SOLICITA DECLARACIÓN DE EXTINCIÓN; OTROSÍ: ACOMPAÑA DOCUMENTO.")
    
    p_juez = doc.add_paragraph()
    p_juez.add_run(f"\nS.J.L. DE GARANTÍA DE {datos
