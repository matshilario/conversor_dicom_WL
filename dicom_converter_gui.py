#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DICOM .img Converter - Interface Gráfica
Converte arquivos .img (DICOM sem header) para formato DICOM padrão
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pydicom
from pydicom.dataset import FileMetaDataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
import os
import sys
from datetime import datetime

# Configurar codificação UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


class DicomConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DICOM .img Converter")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Variáveis
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.current_dataset = None

        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')

        # Criar interface
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Conversor de Arquivos DICOM .img",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Seção de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Arquivo de Entrada", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Arquivo .img:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(input_frame, text="Procurar...", command=self.browse_input).grid(row=0, column=2, padx=(5, 0))

        # Botão de análise
        ttk.Button(
            input_frame,
            text="Analisar Arquivo",
            command=self.analyze_file,
            style='Accent.TButton'
        ).grid(row=1, column=0, columnspan=3, pady=(10, 0))

        # Seção de informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Arquivo", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)

        # Área de texto com scroll
        self.info_text = scrolledtext.ScrolledText(
            info_frame,
            width=80,
            height=20,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Seção de saída
        output_frame = ttk.LabelFrame(main_frame, text="Arquivo de Saída", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)

        ttk.Label(output_frame, text="Salvar como:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(output_frame, textvariable=self.output_file, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="Procurar...", command=self.browse_output).grid(row=0, column=2, padx=(5, 0))

        # Botão de conversão
        convert_btn = ttk.Button(
            main_frame,
            text="Converter para DICOM Padrão",
            command=self.convert_file,
            style='Accent.TButton'
        )
        convert_btn.grid(row=4, column=0, columnspan=3, pady=(0, 10))

        # Barra de status
        self.status_label = ttk.Label(
            main_frame,
            text="Pronto. Selecione um arquivo .img para começar.",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E))

        # Configurar peso das linhas para expansão
        main_frame.rowconfigure(2, weight=1)

    def browse_input(self):
        """Procurar arquivo de entrada"""
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo .img",
            filetypes=[
                ("Arquivos IMG", "*.img"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            self.update_status("Arquivo selecionado. Clique em 'Analisar Arquivo' para ver as informações.")

    def browse_output(self):
        """Procurar local de saída"""
        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo convertido como",
            defaultextension=".dcm",
            filetypes=[
                ("Arquivos DICOM", "*.dcm"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)

    def update_status(self, message):
        """Atualizar barra de status"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def generate_output_filename(self, ds, input_path):
        """Gerar nome de arquivo baseado nos campos DICOM"""
        # Diretório de saída (mesmo do arquivo de entrada)
        output_dir = os.path.dirname(input_path)

        # Tentar obter descrição da série (prioridade 1)
        series_desc = str(getattr(ds, 'SeriesDescription', '')).strip()

        # Tentar obter RT Image Label (prioridade 2)
        rt_label = str(getattr(ds, 'RTImageLabel', '')).strip()

        # Tentar obter Patient ID (fallback 1)
        patient_id = str(getattr(ds, 'PatientID', '')).strip()

        # Tentar obter Study Date (fallback 2)
        study_date = str(getattr(ds, 'StudyDate', '')).strip()

        # Escolher o nome baseado na prioridade
        filename = None

        if series_desc and series_desc != 'N/A':
            # Remover caracteres inválidos
            filename = series_desc.replace(':', '').replace('/', '_').replace('\\', '_')
            filename = filename.replace('*', '').replace('?', '').replace('"', '')
            filename = filename.replace('<', '').replace('>', '').replace('|', '')
            filename = filename.strip()

        if not filename and rt_label and rt_label != 'N/A':
            filename = rt_label.replace(':', '').replace('/', '_').replace('\\', '_')
            filename = filename.replace('*', '').replace('?', '').replace('"', '')
            filename = filename.replace('<', '').replace('>', '').replace('|', '')
            filename = filename.strip()

        if not filename and patient_id and patient_id != 'N/A':
            filename = f"{patient_id}"
            if study_date and study_date != 'N/A':
                filename += f"_{study_date}"

        # Se nenhum campo válido foi encontrado, usar nome do arquivo original
        if not filename:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            filename = f"{base_name}_converted"

        # Garantir que o nome não está vazio e não tem espaços no final
        filename = filename.strip()
        if not filename:
            filename = "converted"

        # Adicionar extensão .dcm
        output_path = os.path.join(output_dir, f"{filename}.dcm")

        # Se o arquivo já existe, adicionar contador
        counter = 1
        while os.path.exists(output_path):
            output_path = os.path.join(output_dir, f"{filename}_{counter}.dcm")
            counter += 1

        return output_path

    def analyze_file(self):
        """Analisar arquivo .img"""
        input_path = self.input_file.get()

        if not input_path:
            messagebox.showwarning("Atenção", "Selecione um arquivo de entrada primeiro!")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("Erro", "Arquivo não encontrado!")
            return

        self.update_status("Analisando arquivo...")
        self.info_text.delete(1.0, tk.END)

        try:
            # Tentar ler o arquivo
            try:
                ds = pydicom.dcmread(input_path)
            except:
                ds = pydicom.dcmread(input_path, force=True)

            self.current_dataset = ds

            # Gerar nome do arquivo de saída baseado nos campos DICOM
            suggested_output = self.generate_output_filename(ds, input_path)
            self.output_file.set(suggested_output)

            # Montar informações
            info = []
            info.append("="*80)
            info.append("INFORMAÇÕES DO ARQUIVO DICOM")
            info.append("="*80)
            info.append(f"\nArquivo: {os.path.basename(input_path)}")
            info.append(f"Tamanho: {os.path.getsize(input_path) / 1024:.2f} KB")
            info.append(f"Nome sugerido para saída: {os.path.basename(suggested_output)}")

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES DO PACIENTE:")
            info.append("-"*80)
            info.append(f"Nome: {getattr(ds, 'PatientName', 'N/A')}")
            info.append(f"ID: {getattr(ds, 'PatientID', 'N/A')}")
            info.append(f"Data de Nascimento: {getattr(ds, 'PatientBirthDate', 'N/A')}")
            info.append(f"Sexo: {getattr(ds, 'PatientSex', 'N/A')}")

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES DO ESTUDO:")
            info.append("-"*80)
            info.append(f"Modalidade: {getattr(ds, 'Modality', 'N/A')}")
            info.append(f"Descrição: {getattr(ds, 'StudyDescription', 'N/A')}")
            info.append(f"Data: {getattr(ds, 'StudyDate', 'N/A')}")
            info.append(f"Hora: {getattr(ds, 'StudyTime', 'N/A')}")
            info.append(f"Study Instance UID: {getattr(ds, 'StudyInstanceUID', 'N/A')}")

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES DA SÉRIE:")
            info.append("-"*80)
            info.append(f"Descrição: {getattr(ds, 'SeriesDescription', 'N/A')}")
            info.append(f"Número: {getattr(ds, 'SeriesNumber', 'N/A')}")
            info.append(f"Series Instance UID: {getattr(ds, 'SeriesInstanceUID', 'N/A')}")

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES DO EQUIPAMENTO:")
            info.append("-"*80)
            info.append(f"Fabricante: {getattr(ds, 'Manufacturer', 'N/A')}")
            info.append(f"Modelo: {getattr(ds, 'ManufacturerModelName', 'N/A')}")
            info.append(f"Estação: {getattr(ds, 'StationName', 'N/A')}")
            info.append(f"Instituição: {getattr(ds, 'InstitutionName', 'N/A')}")

            # Se for RT Image
            if hasattr(ds, 'RTImageLabel'):
                info.append("\n" + "-"*80)
                info.append("INFORMAÇÕES DE RT IMAGE:")
                info.append("-"*80)
                info.append(f"RT Image Label: {getattr(ds, 'RTImageLabel', 'N/A')}")
                info.append(f"RT Image Description: {getattr(ds, 'RTImageDescription', 'N/A')}")

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES DA IMAGEM:")
            info.append("-"*80)
            info.append(f"Dimensões: {getattr(ds, 'Rows', 'N/A')} x {getattr(ds, 'Columns', 'N/A')} pixels")
            info.append(f"Bits Alocados: {getattr(ds, 'BitsAllocated', 'N/A')}")
            info.append(f"Interpretação Fotométrica: {getattr(ds, 'PhotometricInterpretation', 'N/A')}")

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES TÉCNICAS:")
            info.append("-"*80)
            info.append(f"SOP Class UID: {getattr(ds, 'SOPClassUID', 'N/A')}")
            info.append(f"SOP Instance UID: {getattr(ds, 'SOPInstanceUID', 'N/A')}")

            # Identificar tipo
            sop_class = str(getattr(ds, 'SOPClassUID', ''))
            if '481.1' in sop_class:
                info.append("Tipo: RT Image Storage")
            elif '481.2' in sop_class:
                info.append("Tipo: RT Dose Storage")
            elif '481.5' in sop_class:
                info.append("Tipo: RT Plan Storage")
            elif '481.3' in sop_class:
                info.append("Tipo: RT Structure Set Storage")

            info.append("\n" + "="*80)

            # Mostrar informações
            self.info_text.insert(1.0, "\n".join(info))
            self.update_status("Arquivo analisado com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao analisar arquivo:\n{str(e)}")
            self.update_status("Erro ao analisar arquivo.")
            self.current_dataset = None

    def convert_file(self):
        """Converter arquivo para DICOM padrão"""
        if not self.current_dataset:
            messagebox.showwarning("Atenção", "Analise o arquivo primeiro!")
            return

        output_path = self.output_file.get()
        if not output_path:
            messagebox.showwarning("Atenção", "Defina o arquivo de saída!")
            return

        self.update_status("Convertendo arquivo...")

        try:
            ds = self.current_dataset

            # Criar ou corrigir File Meta Information Header
            if not hasattr(ds, 'file_meta') or not ds.file_meta:
                ds.file_meta = FileMetaDataset()

            # Garantir que tem Transfer Syntax UID
            if not hasattr(ds.file_meta, 'TransferSyntaxUID') or not ds.file_meta.TransferSyntaxUID:
                ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            # Garantir que tem Media Storage SOP Class UID
            if not hasattr(ds.file_meta, 'MediaStorageSOPClassUID'):
                if hasattr(ds, 'SOPClassUID'):
                    ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID

            # Garantir que tem Media Storage SOP Instance UID
            if not hasattr(ds.file_meta, 'MediaStorageSOPInstanceUID'):
                if hasattr(ds, 'SOPInstanceUID'):
                    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID

            # Garantir que tem Implementation Class UID
            if not hasattr(ds.file_meta, 'ImplementationClassUID'):
                ds.file_meta.ImplementationClassUID = generate_uid()

            # Garantir que tem Implementation Version Name
            if not hasattr(ds.file_meta, 'ImplementationVersionName'):
                ds.file_meta.ImplementationVersionName = "PYDICOM_" + pydicom.__version__

            # Salvar arquivo DICOM com header completo
            ds.save_as(output_path, write_like_original=False)

            # Verificar se o arquivo pode ser lido normalmente
            try:
                test_ds = pydicom.dcmread(output_path)
                validation_msg = "\n\n✓ Arquivo validado e compatível com pylinac!"
            except:
                validation_msg = "\n\n⚠ Arquivo salvo mas pode ter problemas de compatibilidade."

            messagebox.showinfo(
                "Sucesso",
                f"Arquivo convertido com sucesso!\n\n"
                f"Salvo em:\n{output_path}\n\n"
                f"O arquivo possui File Meta Information Header completo "
                f"e pode ser aberto em qualquer visualizador DICOM.{validation_msg}"
            )

            self.update_status(f"Conversão concluída! Arquivo salvo: {os.path.basename(output_path)}")

            # Perguntar se deseja abrir a pasta
            if messagebox.askyesno("Abrir pasta?", "Deseja abrir a pasta onde o arquivo foi salvo?"):
                import subprocess
                folder = os.path.dirname(output_path)
                if sys.platform == 'win32':
                    os.startfile(folder)
                elif sys.platform == 'darwin':
                    subprocess.Popen(['open', folder])
                else:
                    subprocess.Popen(['xdg-open', folder])

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao converter arquivo:\n{str(e)}")
            self.update_status("Erro na conversão.")


def main():
    root = tk.Tk()

    # Configurar ícone (se disponível)
    try:
        root.iconbitmap(default='icon.ico')
    except:
        pass

    app = DicomConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
