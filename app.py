import streamlit as st
from docx import Document
from docx.shared import Pt
import PyPDF2
import io

def crear_escrito(datos, texto_condena):
    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Arial'
    style.font.size = Pt(12)

    p = doc.add_paragraph()
    p.add_run("SUMILLA: SOLICITA DECLARACIÓN DE EXTINCIÓN DE RESPONSABILIDAD PENAL.\n").bold = True
    p.add_run(f"RIT: {datos['rit']}\n")
    p.add_run(f"RUC: {datos['ruc']}\n")
    p.add_run(f"TRIBUNAL: {datos['juzgado']}\n")

    doc.add_paragraph("\nEN LO PRINCIPAL: SOLICITA DECLARACIÓN DE EXTINCIÓN; OTROSÍ: ACOMPAÑA DOCUMENTO.")
    
    p_juez = doc.add_paragraph()
    p_juez.add_run(f"\nS.J.L. DE GARANTÍA DE {datos['juzgado'].upper()}").bold = True

    cuerpo = doc.add_paragraph()
    cuerpo.add_run(f"\n{datos['nombre_defensor']}, abogado de la Defensoría Penal Pública, en representación del adolescente {datos['nombre_adolescente']}, en la causa RIT {datos['rit']}, a SS. con respeto digo:\n")
    
    cuerpo.add_run("\nQue, por este acto y de acuerdo a lo previsto en la Ley 20.084, vengo en solicitar se declare la extinción de la responsabilidad penal de mi representado en la presente causa. Esto, fundado en que el adolescente ha sido condenado por un tribunal de adultos a una pena privativa de libertad, lo cual hace incompatible la ejecución de la sanción en el sistema de responsabilidad penal adolescente, conforme a los principios de coherencia del sistema punitivo y las normas de extinción del Código Penal.\n")

    doc.add_paragraph("\nFUNDAMENTOS DE LA CONDENA DE ADULTO ADJUNTA:").bold = True
    doc.add_paragraph(texto_condena)
    
    p_final = doc.add_paragraph()
    p_final.add_run("\nPOR TANTO, de acuerdo a lo dispuesto en la Ley 20.084 y las normas generales sobre extinción de responsabilidad penal:\n")
    p_final.add_run("SOLICITO A SS. tener por solicitada la extinción, declarar la misma y ordenar el archivo de los antecedentes.").bold = True

    target = io.BytesIO()
    doc.save(target)
    target.seek(0)
    return target

st.set_page_config(page_title="Generador de Escritos RPA", layout="centered")
st.title("⚖️ Generador de Escritos de Extinción")

with st.form("formulario_defensoria"):
    col1, col2 = st.columns(2)
    with col1:
        nombre_defensor = st.text_input("Nombre del Defensor")
        nombre_adolescente = st.text_input("Nombre del Adolescente")
        juzgado = st.text_input("Juzgado de Ejecución")
    with col2:
        ruc = st.text_input("RUC")
        rit = st.text_input("RIT")
        condenado_en = st.text_input("Tribunal de Condena Adulto")

    pdf_file = st.file_uploader("Subir PDF de Condena Adulto", type="pdf")
    boton_generar = st.form_submit_button("Generar Escrito Word")

if boton_generar:
    if not pdf_file or not nombre_defensor:
        st.error("Debe completar los campos y subir el PDF.")
    else:
        try:
            reader = PyPDF2.PdfReader(pdf_file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text() + "\n"

            datos_causa = {
                "nombre_defensor": nombre_defensor,
                "nombre_adolescente": nombre_adolescente,
                "juzgado": juzgado,
                "ruc": ruc,
                "rit": rit,
                "condenado_en": condenado_en
            }

            archivo_resultado = crear_escrito(datos_causa, texto_completo)
            
            st.success("✅ Escrito generado.")
            st.download_button(
                label="📥 Descargar Escrito Word",
                data=archivo_resultado,
                file_name=f"Escrito_Extincion_{nombre_adolescente}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        except Exception as e:
            st.error(f"Error: {e}")
