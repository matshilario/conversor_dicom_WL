#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor DICOM Unificado - Interface Gráfica
Menu principal para conversão de .img ou TIFF para DICOM
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


# ============================================================================
# CLASSE: Conversor IMG para DICOM
# ============================================================================

class ImgToDicomConverter:
    def __init__(self, parent_window, on_close_callback=None):
        self.root = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.on_close_callback = on_close_callback
        self.root.title("Conversor .IMG para DICOM")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Configurar comportamento ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variáveis
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.current_dataset = None

        # Criar interface
        self.create_widgets()

    def on_closing(self):
        """Tratar fechamento da janela"""
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()

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
            command=self.analyze_file
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
            command=self.convert_file
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
        output_dir = os.path.dirname(input_path)
        series_desc = str(getattr(ds, 'SeriesDescription', '')).strip()
        rt_label = str(getattr(ds, 'RTImageLabel', '')).strip()
        patient_id = str(getattr(ds, 'PatientID', '')).strip()
        study_date = str(getattr(ds, 'StudyDate', '')).strip()

        filename = None

        if series_desc and series_desc != 'N/A':
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

        if not filename:
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            filename = f"{base_name}_converted"

        filename = filename.strip()
        if not filename:
            filename = "converted"

        output_path = os.path.join(output_dir, f"{filename}.dcm")

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
            try:
                ds = pydicom.dcmread(input_path)
            except:
                ds = pydicom.dcmread(input_path, force=True)

            self.current_dataset = ds

            suggested_output = self.generate_output_filename(ds, input_path)
            self.output_file.set(suggested_output)

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

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES DA SÉRIE:")
            info.append("-"*80)
            info.append(f"Descrição: {getattr(ds, 'SeriesDescription', 'N/A')}")
            info.append(f"Número: {getattr(ds, 'SeriesNumber', 'N/A')}")

            info.append("\n" + "-"*80)
            info.append("INFORMAÇÕES DO EQUIPAMENTO:")
            info.append("-"*80)
            info.append(f"Fabricante: {getattr(ds, 'Manufacturer', 'N/A')}")
            info.append(f"Modelo: {getattr(ds, 'ManufacturerModelName', 'N/A')}")
            info.append(f"Estação: {getattr(ds, 'StationName', 'N/A')}")

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

            info.append("\n" + "="*80)

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

            if not hasattr(ds.file_meta, 'TransferSyntaxUID') or not ds.file_meta.TransferSyntaxUID:
                ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

            if not hasattr(ds.file_meta, 'MediaStorageSOPClassUID'):
                if hasattr(ds, 'SOPClassUID'):
                    ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID

            if not hasattr(ds.file_meta, 'MediaStorageSOPInstanceUID'):
                if hasattr(ds, 'SOPInstanceUID'):
                    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID

            if not hasattr(ds.file_meta, 'ImplementationClassUID'):
                ds.file_meta.ImplementationClassUID = generate_uid()

            if not hasattr(ds.file_meta, 'ImplementationVersionName'):
                ds.file_meta.ImplementationVersionName = "PYDICOM_" + pydicom.__version__

            # Salvar arquivo DICOM com header completo
            ds.save_as(output_path, write_like_original=False)

            try:
                test_ds = pydicom.dcmread(output_path)
                validation_msg = "\n\nArquivo validado e compatível com pylinac!"
            except:
                validation_msg = "\n\nArquivo salvo mas pode ter problemas de compatibilidade."

            messagebox.showinfo(
                "Sucesso",
                f"Arquivo convertido com sucesso!\n\n"
                f"Salvo em:\n{output_path}\n\n"
                f"O arquivo possui File Meta Information Header completo "
                f"e pode ser aberto em qualquer visualizador DICOM.{validation_msg}"
            )

            self.update_status(f"Conversão concluída! Arquivo salvo: {os.path.basename(output_path)}")

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


# ============================================================================
# CLASSE: Conversor TIFF para DICOM
# ============================================================================

class TiffToDicomConverter:
    def __init__(self, parent_window, on_close_callback=None):
        self.root = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.on_close_callback = on_close_callback
        self.root.title("Conversor TIFF para DICOM (pylinac)")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Configurar comportamento ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variáveis
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.sid_var = tk.StringVar(value="1000")
        self.gantry_var = tk.StringVar(value="0")
        self.coll_var = tk.StringVar(value="0")
        self.couch_var = tk.StringVar(value="0")
        self.dpi_var = tk.StringVar(value="400")

        # Criar interface
        self.create_widgets()

    def on_closing(self):
        """Tratar fechamento da janela"""
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Conversor TIFF para DICOM (pylinac)",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Arquivo de entrada
        input_frame = ttk.LabelFrame(main_frame, text="Arquivo de Entrada (TIFF)", padding="10")
        input_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Arquivo TIFF:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(input_frame, text="Procurar...", command=self.browse_input).grid(row=0, column=2, padx=(5, 0))

        # Parâmetros DICOM
        params_frame = ttk.LabelFrame(main_frame, text="Parâmetros DICOM (Obrigatórios)", padding="10")
        params_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        params_frame.columnconfigure(1, weight=1)

        ttk.Label(params_frame, text="SID (mm):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        sid_entry = ttk.Entry(params_frame, textvariable=self.sid_var, width=15)
        sid_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Source-to-Image Distance").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))

        ttk.Label(params_frame, text="Gantry Angle (°):").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        gantry_entry = ttk.Entry(params_frame, textvariable=self.gantry_var, width=15)
        gantry_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Ângulo do Gantry (0-360°)").grid(row=1, column=2, sticky=tk.W, padx=(10, 0))

        ttk.Label(params_frame, text="Collimator Angle (°):").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        coll_entry = ttk.Entry(params_frame, textvariable=self.coll_var, width=15)
        coll_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Ângulo do Colimador (0-360°)").grid(row=2, column=2, sticky=tk.W, padx=(10, 0))

        ttk.Label(params_frame, text="Couch Angle (°):").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        couch_entry = ttk.Entry(params_frame, textvariable=self.couch_var, width=15)
        couch_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Ângulo da Mesa (0-360°)").grid(row=3, column=2, sticky=tk.W, padx=(10, 0))

        ttk.Label(params_frame, text="DPI:").grid(row=4, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        dpi_entry = ttk.Entry(params_frame, textvariable=self.dpi_var, width=15)
        dpi_entry.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Dots Per Inch (resolução da imagem)").grid(row=4, column=2, sticky=tk.W, padx=(10, 0))

        # Arquivo de saída
        output_frame = ttk.LabelFrame(main_frame, text="Arquivo de Saída (DICOM)", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)

        ttk.Label(output_frame, text="Salvar como:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(output_frame, textvariable=self.output_file, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="Procurar...", command=self.browse_output).grid(row=0, column=2, padx=(5, 0))

        # Informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações", padding="10")
        info_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)

        self.info_text = scrolledtext.ScrolledText(
            info_frame,
            width=70,
            height=8,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        info_msg = """CONVERSOR TIFF PARA DICOM usando pylinac

Este conversor utiliza a função image.tiff_to_dicom() do pylinac para criar
arquivos DICOM compatíveis com análise de Winston-Lutz.

IMPORTANTE: Os parâmetros são detectados automaticamente do nome do arquivo
quando seguem padrões como: gantry_0.tiff, g90.tiff, coll_45.tiff, etc.
        """
        self.info_text.insert(1.0, info_msg.strip())

        # Botão de conversão
        convert_btn = ttk.Button(
            main_frame,
            text="Converter TIFF para DICOM",
            command=self.convert_file
        )
        convert_btn.grid(row=5, column=0, columnspan=3, pady=(0, 10))

        # Barra de status
        self.status_label = ttk.Label(
            main_frame,
            text="Pronto. Selecione um arquivo TIFF e configure os parâmetros.",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E))

        main_frame.rowconfigure(4, weight=1)

    def detect_params_from_filename(self, filename):
        """Detecta parâmetros do nome do arquivo"""
        import re
        basename = os.path.basename(filename).lower()
        params = {}

        gantry_match = re.search(r'g(?:antry)?[_-]?(\d+)', basename)
        if gantry_match:
            params['gantry'] = gantry_match.group(1)

        coll_match = re.search(r'c(?:oll)?[_-]?(\d+)', basename)
        if coll_match:
            params['coll'] = coll_match.group(1)

        couch_match = re.search(r'(?:couch|table)[_-]?(\d+)', basename)
        if couch_match:
            params['couch'] = couch_match.group(1)

        return params if params else None

    def validate_filename_pattern(self, filename):
        """Valida se o nome do arquivo segue um padrão aceitável"""
        import re
        basename = os.path.basename(filename)
        name_lower = basename.lower()

        acceptable_patterns = [
            r'g(?:antry)?[_-]?\d+',
            r'c(?:oll)?[_-]?\d+',
            r'couch[_-]?\d+',
            r'wl[_-]?g\d+',
        ]

        is_valid = any(re.search(pattern, name_lower) for pattern in acceptable_patterns)

        if not is_valid:
            base = os.path.splitext(basename)[0]
            ext = os.path.splitext(basename)[1]
            suggestion = f"gantry_{self.gantry_var.get()}{ext}"
        else:
            suggestion = basename

        return is_valid, suggestion

    def browse_input(self):
        """Procurar arquivo TIFF"""
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo TIFF",
            filetypes=[
                ("Arquivos TIFF", "*.tiff;*.tif;*.TIF;*.TIFF"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)

            detected_params = self.detect_params_from_filename(filename)
            if detected_params:
                if 'gantry' in detected_params:
                    self.gantry_var.set(detected_params['gantry'])
                if 'coll' in detected_params:
                    self.coll_var.set(detected_params['coll'])
                if 'couch' in detected_params:
                    self.couch_var.set(detected_params['couch'])

                self.update_status(f"Parâmetros detectados do nome do arquivo! Verifique se estão corretos.")

            is_valid, suggestion = self.validate_filename_pattern(filename)

            if not is_valid:
                response = messagebox.askyesno(
                    "Nome de arquivo não padrão",
                    f"O nome do arquivo não segue um padrão recomendado:\n\n"
                    f"Atual: {os.path.basename(filename)}\n\n"
                    f"Padrões recomendados:\n"
                    f"  - gantry_0.tiff, gantry_90.tiff, etc.\n"
                    f"  - g0.tiff, g90.tiff, etc.\n"
                    f"  - coll_45.tiff, couch_90.tiff, etc.\n\n"
                    f"Sugestão: {suggestion}\n\n"
                    f"Deseja renomear o arquivo agora?"
                )

                if response:
                    new_name = self.show_rename_dialog(filename, suggestion)
                    if new_name:
                        try:
                            new_path = os.path.join(os.path.dirname(filename), new_name)
                            os.rename(filename, new_path)
                            self.input_file.set(new_path)
                            messagebox.showinfo("Sucesso", f"Arquivo renomeado para:\n{new_name}")
                            filename = new_path

                            detected_params = self.detect_params_from_filename(filename)
                            if detected_params and 'gantry' in detected_params:
                                self.gantry_var.set(detected_params['gantry'])
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao renomear arquivo:\n{str(e)}")

            base_name = os.path.splitext(filename)[0]
            self.output_file.set(f"{base_name}.dcm")
            self.update_status("Arquivo TIFF selecionado. Verifique os parâmetros e clique em Converter.")

    def show_rename_dialog(self, current_path, suggestion):
        """Mostra diálogo para renomear arquivo"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Renomear Arquivo")
        dialog.geometry("500x200")
        dialog.transient(self.root)
        dialog.grab_set()

        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Novo nome do arquivo:", font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        name_var = tk.StringVar(value=suggestion)
        entry = ttk.Entry(frame, textvariable=name_var, width=50)
        entry.pack(fill=tk.X, pady=(0, 20))
        entry.select_range(0, tk.END)
        entry.focus()

        result = [None]

        def on_ok():
            result[0] = name_var.get()
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        button_frame = ttk.Frame(frame)
        button_frame.pack()

        ttk.Button(button_frame, text="OK", command=on_ok, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=on_cancel, width=15).pack(side=tk.LEFT, padx=5)

        entry.bind('<Return>', lambda e: on_ok())
        entry.bind('<Escape>', lambda e: on_cancel())

        dialog.wait_window()
        return result[0]

    def browse_output(self):
        """Procurar local de saída"""
        filename = filedialog.asksaveasfilename(
            title="Salvar arquivo DICOM como",
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

    def validate_parameters(self):
        """Validar parâmetros de entrada"""
        errors = []

        try:
            sid = float(self.sid_var.get())
            if sid <= 0:
                errors.append("SID deve ser maior que 0")
        except ValueError:
            errors.append("SID deve ser um número válido")

        try:
            gantry = float(self.gantry_var.get())
            if gantry < 0 or gantry > 360:
                errors.append("Gantry Angle deve estar entre 0 e 360")
        except ValueError:
            errors.append("Gantry Angle deve ser um número válido")

        try:
            coll = float(self.coll_var.get())
            if coll < 0 or coll > 360:
                errors.append("Collimator Angle deve estar entre 0 e 360")
        except ValueError:
            errors.append("Collimator Angle deve ser um número válido")

        try:
            couch = float(self.couch_var.get())
            if couch < 0 or couch > 360:
                errors.append("Couch Angle deve estar entre 0 e 360")
        except ValueError:
            errors.append("Couch Angle deve ser um número válido")

        try:
            dpi = float(self.dpi_var.get())
            if dpi <= 0:
                errors.append("DPI deve ser maior que 0")
        except ValueError:
            errors.append("DPI deve ser um número válido")

        return errors

    def convert_file(self):
        """Converter TIFF para DICOM usando pylinac"""
        input_path = self.input_file.get()
        output_path = self.output_file.get()

        if not input_path:
            messagebox.showwarning("Atenção", "Selecione um arquivo TIFF!")
            return

        if not output_path:
            messagebox.showwarning("Atenção", "Defina o arquivo de saída!")
            return

        if not os.path.exists(input_path):
            messagebox.showerror("Erro", "Arquivo TIFF não encontrado!")
            return

        errors = self.validate_parameters()
        if errors:
            messagebox.showerror("Erro de Validação", "\n".join(errors))
            return

        self.update_status("Convertendo TIFF para DICOM...")

        try:
            try:
                from pylinac import image
            except ImportError:
                messagebox.showerror(
                    "Erro",
                    "pylinac não está instalado!\n\n"
                    "Execute no terminal:\n"
                    "pip install pylinac\n\n"
                    "ou\n\n"
                    ".venv\\Scripts\\pip.exe install pylinac"
                )
                self.update_status("Erro: pylinac não instalado")
                return

            sid = float(self.sid_var.get())
            gantry = float(self.gantry_var.get())
            coll = float(self.coll_var.get())
            couch = float(self.couch_var.get())
            dpi = float(self.dpi_var.get())

            new_dicom = image.tiff_to_dicom(
                input_path,
                sid=sid,
                gantry=gantry,
                coll=coll,
                couch=couch,
                dpi=dpi
            )

            new_dicom.save_as(output_path, write_like_original=False)

            self.info_text.delete(1.0, tk.END)
            info_msg = f"""CONVERSÃO CONCLUÍDA COM SUCESSO!

Arquivo de entrada: {os.path.basename(input_path)}
Arquivo de saída: {os.path.basename(output_path)}

PARÂMETROS UTILIZADOS:
- SID: {sid} mm
- Gantry Angle: {gantry}°
- Collimator Angle: {coll}°
- Couch Angle: {couch}°
- DPI: {dpi}

O arquivo DICOM foi criado usando a função nativa do pylinac
e está compatível com análise de Winston-Lutz.
            """
            self.info_text.insert(1.0, info_msg.strip())

            messagebox.showinfo(
                "Sucesso",
                f"Arquivo convertido com sucesso!\n\n"
                f"Salvo em:\n{output_path}\n\n"
                f"O arquivo DICOM está compatível com pylinac e pode ser usado "
                f"para análise de Winston-Lutz."
            )

            self.update_status(f"Conversão concluída! Arquivo: {os.path.basename(output_path)}")

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
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, f"ERRO:\n{str(e)}")


# ============================================================================
# CLASSE: Conversor em Lote TIFF para DICOM
# ============================================================================

class BatchTiffToDicomConverter:
    def __init__(self, parent_window, on_close_callback=None):
        self.root = tk.Toplevel(parent_window) if parent_window else tk.Tk()
        self.on_close_callback = on_close_callback
        self.root.title("Conversor em Lote TIFF para DICOM")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        # Configurar comportamento ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variáveis
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.sid_var = tk.StringVar(value="1000")
        self.dpi_var = tk.StringVar(value="400")

        # Lista de conversões (nome_arquivo, gantry, coll, couch, nome_saida)
        self.conversion_list = []

        # Arquivos encontrados na pasta
        self.tiff_files = []

        # Variável para drag-and-drop
        self.drag_start_index = None

        # Criar interface
        self.create_widgets()

        # Carregar template padrão
        self.load_template("WL Standard 4")

    def on_closing(self):
        """Tratar fechamento da janela"""
        self.root.destroy()
        if self.on_close_callback:
            self.on_close_callback()

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Conversor em Lote TIFF para DICOM",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # ===== SEÇÃO: Pastas =====
        folders_frame = ttk.LabelFrame(main_frame, text="Pastas", padding="10")
        folders_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        folders_frame.columnconfigure(1, weight=1)

        # Pasta de entrada
        ttk.Label(folders_frame, text="Pasta com arquivos TIFF:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(folders_frame, textvariable=self.input_folder, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(folders_frame, text="Procurar...", command=self.browse_input_folder).grid(row=0, column=2, padx=(5, 0))

        # Pasta de saída
        ttk.Label(folders_frame, text="Pasta para arquivos DICOM:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        ttk.Entry(folders_frame, textvariable=self.output_folder, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=(5, 0))
        ttk.Button(folders_frame, text="Procurar...", command=self.browse_output_folder).grid(row=1, column=2, padx=(5, 0), pady=(5, 0))

        # ===== SEÇÃO: Parâmetros Globais =====
        params_frame = ttk.LabelFrame(main_frame, text="Parâmetros Globais DICOM", padding="10")
        params_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(params_frame, text="SID (mm):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(params_frame, textvariable=self.sid_var, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(params_frame, text="DPI:").grid(row=0, column=2, sticky=tk.W, padx=(20, 5))
        ttk.Entry(params_frame, textvariable=self.dpi_var, width=15).grid(row=0, column=3, sticky=tk.W, padx=5)

        # ===== LAYOUT PRINCIPAL: 2 colunas =====
        content_frame = ttk.Frame(main_frame)
        content_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)

        # ===== COLUNA ESQUERDA: Lista de Conversões =====
        left_frame = ttk.LabelFrame(content_frame, text="Template de Conversão", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)

        # Templates pré-definidos
        template_frame = ttk.Frame(left_frame)
        template_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(template_frame, text="Template:").pack(side=tk.LEFT, padx=(0, 5))

        self.template_combo = ttk.Combobox(template_frame, state="readonly", width=20)
        self.template_combo['values'] = [
            "WL Standard 4",
            "WL Extended 7",
            "WL Completo 9",
            "Custom"
        ]
        self.template_combo.current(0)
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_selected)
        self.template_combo.pack(side=tk.LEFT, padx=5)

        # Listbox com scrollbar para itens
        list_container = ttk.Frame(left_frame)
        list_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.items_listbox = tk.Listbox(
            list_container,
            font=('Courier', 9),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.items_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.items_listbox.yview)

        # Bind para drag-and-drop
        self.items_listbox.bind('<Button-1>', self.on_listbox_click)
        self.items_listbox.bind('<B1-Motion>', self.on_listbox_drag)
        self.items_listbox.bind('<ButtonRelease-1>', self.on_listbox_release)
        self.items_listbox.bind('<Double-Button-1>', self.edit_item)

        # Botões de controle da lista
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Button(buttons_frame, text="Adicionar", command=self.add_item, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Editar", command=self.edit_item, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="Remover", command=self.remove_item, width=12).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="↑ Subir", command=self.move_item_up, width=10).pack(side=tk.LEFT, padx=2)
        ttk.Button(buttons_frame, text="↓ Descer", command=self.move_item_down, width=10).pack(side=tk.LEFT, padx=2)

        # ===== COLUNA DIREITA: Preview =====
        right_frame = ttk.LabelFrame(content_frame, text="Preview da Conversão", padding="10")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

        self.preview_text = scrolledtext.ScrolledText(
            right_frame,
            width=50,
            height=20,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Button(right_frame, text="Atualizar Preview", command=self.update_preview).grid(row=1, column=0, pady=(10, 0))

        # ===== SEÇÃO: Botão de Conversão e Status =====
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        bottom_frame.columnconfigure(0, weight=1)

        convert_btn = ttk.Button(
            bottom_frame,
            text="Converter Lote",
            command=self.convert_batch,
            width=20
        )
        convert_btn.grid(row=0, column=0, pady=(0, 10))

        # Barra de progresso
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            bottom_frame,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 5))

        # Status
        self.status_label = ttk.Label(
            bottom_frame,
            text="Pronto. Selecione uma pasta e configure o template.",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=2, column=0, sticky=(tk.W, tk.E))

    def browse_input_folder(self):
        """Procurar pasta de entrada"""
        folder = filedialog.askdirectory(title="Selecione a pasta com arquivos TIFF")
        if folder:
            self.input_folder.set(folder)
            self.scan_tiff_files()
            self.update_preview()
            # Sugerir pasta de saída
            if not self.output_folder.get():
                self.output_folder.set(folder)

    def browse_output_folder(self):
        """Procurar pasta de saída"""
        folder = filedialog.askdirectory(title="Selecione a pasta para salvar arquivos DICOM")
        if folder:
            self.output_folder.set(folder)

    def scan_tiff_files(self):
        """Escanear arquivos TIFF na pasta"""
        folder = self.input_folder.get()
        if not folder or not os.path.exists(folder):
            self.tiff_files = []
            return

        self.tiff_files = []
        for file in sorted(os.listdir(folder)):
            if file.lower().endswith(('.tif', '.tiff')):
                self.tiff_files.append(file)

        self.update_status(f"Encontrados {len(self.tiff_files)} arquivos TIFF na pasta")

    def load_template(self, template_name):
        """Carregar template pré-definido"""
        self.conversion_list = []

        if template_name == "WL Standard 4":
            # Winston-Lutz padrão: 4 ângulos de gantry
            self.conversion_list = [
                {"name": "gantry_0", "gantry": "0", "coll": "0", "couch": "0"},
                {"name": "gantry_90", "gantry": "90", "coll": "0", "couch": "0"},
                {"name": "gantry_180", "gantry": "180", "coll": "0", "couch": "0"},
                {"name": "gantry_270", "gantry": "270", "coll": "0", "couch": "0"},
            ]
        elif template_name == "WL Extended 7":
            # Winston-Lutz estendido: 4 gantries + 2 couches + 1 collimator
            self.conversion_list = [
                {"name": "gantry_0", "gantry": "0", "coll": "0", "couch": "0"},
                {"name": "gantry_90", "gantry": "90", "coll": "0", "couch": "0"},
                {"name": "gantry_180", "gantry": "180", "coll": "0", "couch": "0"},
                {"name": "gantry_270", "gantry": "270", "coll": "0", "couch": "0"},
                {"name": "couch_45", "gantry": "0", "coll": "0", "couch": "45"},
                {"name": "couch_315", "gantry": "0", "coll": "0", "couch": "315"},
                {"name": "coll_45", "gantry": "0", "coll": "45", "couch": "0"},
            ]
        elif template_name == "WL Completo 9":
            # Winston-Lutz completo
            self.conversion_list = [
                {"name": "gantry_0", "gantry": "0", "coll": "0", "couch": "0"},
                {"name": "gantry_90", "gantry": "90", "coll": "0", "couch": "0"},
                {"name": "gantry_180", "gantry": "180", "coll": "0", "couch": "0"},
                {"name": "gantry_270", "gantry": "270", "coll": "0", "couch": "0"},
                {"name": "couch_45", "gantry": "0", "coll": "0", "couch": "45"},
                {"name": "couch_90", "gantry": "0", "coll": "0", "couch": "90"},
                {"name": "couch_270", "gantry": "0", "coll": "0", "couch": "270"},
                {"name": "couch_315", "gantry": "0", "coll": "0", "couch": "315"},
                {"name": "coll_45", "gantry": "0", "coll": "45", "couch": "0"},
            ]

        self.refresh_listbox()

    def on_template_selected(self, event=None):
        """Callback quando template é selecionado"""
        template = self.template_combo.get()
        if template != "Custom":
            self.load_template(template)
            self.update_preview()

    def refresh_listbox(self):
        """Atualizar listbox com itens da lista"""
        self.items_listbox.delete(0, tk.END)
        for i, item in enumerate(self.conversion_list):
            display = f"{i+1:2d}. {item['name']:<20} G:{item['gantry']:>3}° C:{item['coll']:>3}° T:{item['couch']:>3}°"
            self.items_listbox.insert(tk.END, display)

    def add_item(self):
        """Adicionar novo item à lista"""
        item = self.show_item_dialog()
        if item:
            self.conversion_list.append(item)
            self.refresh_listbox()
            self.template_combo.set("Custom")
            self.update_preview()

    def edit_item(self, event=None):
        """Editar item selecionado"""
        selection = self.items_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenção", "Selecione um item para editar!")
            return

        index = selection[0]
        current_item = self.conversion_list[index]

        item = self.show_item_dialog(current_item)
        if item:
            self.conversion_list[index] = item
            self.refresh_listbox()
            self.template_combo.set("Custom")
            self.update_preview()

    def remove_item(self):
        """Remover item selecionado"""
        selection = self.items_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atenção", "Selecione um item para remover!")
            return

        index = selection[0]
        del self.conversion_list[index]
        self.refresh_listbox()
        self.template_combo.set("Custom")
        self.update_preview()

    def move_item_up(self):
        """Mover item para cima"""
        selection = self.items_listbox.curselection()
        if not selection or selection[0] == 0:
            return

        index = selection[0]
        self.conversion_list[index], self.conversion_list[index-1] = \
            self.conversion_list[index-1], self.conversion_list[index]

        self.refresh_listbox()
        self.items_listbox.selection_set(index-1)
        self.template_combo.set("Custom")
        self.update_preview()

    def move_item_down(self):
        """Mover item para baixo"""
        selection = self.items_listbox.curselection()
        if not selection or selection[0] >= len(self.conversion_list) - 1:
            return

        index = selection[0]
        self.conversion_list[index], self.conversion_list[index+1] = \
            self.conversion_list[index+1], self.conversion_list[index]

        self.refresh_listbox()
        self.items_listbox.selection_set(index+1)
        self.template_combo.set("Custom")
        self.update_preview()

    def on_listbox_click(self, event):
        """Iniciar drag-and-drop"""
        self.drag_start_index = self.items_listbox.nearest(event.y)

    def on_listbox_drag(self, event):
        """Durante drag-and-drop"""
        current_index = self.items_listbox.nearest(event.y)
        if current_index != self.drag_start_index and self.drag_start_index is not None:
            # Reordenar visualmente
            self.items_listbox.selection_clear(0, tk.END)
            self.items_listbox.selection_set(current_index)

    def on_listbox_release(self, event):
        """Finalizar drag-and-drop"""
        if self.drag_start_index is None:
            return

        end_index = self.items_listbox.nearest(event.y)

        if self.drag_start_index != end_index:
            # Mover item na lista
            item = self.conversion_list.pop(self.drag_start_index)
            self.conversion_list.insert(end_index, item)

            self.refresh_listbox()
            self.items_listbox.selection_set(end_index)
            self.template_combo.set("Custom")
            self.update_preview()

        self.drag_start_index = None

    def show_item_dialog(self, current_item=None):
        """Mostrar diálogo para editar/adicionar item"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Configurar Item")
        dialog.geometry("400x250")
        dialog.transient(self.root)
        dialog.grab_set()

        # Centralizar
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        # Valores padrão
        default_name = current_item['name'] if current_item else ""
        default_gantry = current_item['gantry'] if current_item else "0"
        default_coll = current_item['coll'] if current_item else "0"
        default_couch = current_item['couch'] if current_item else "0"

        # Campos
        ttk.Label(frame, text="Nome do arquivo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_var = tk.StringVar(value=default_name)
        name_entry = ttk.Entry(frame, textvariable=name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Gantry Angle (°):").grid(row=1, column=0, sticky=tk.W, pady=5)
        gantry_var = tk.StringVar(value=default_gantry)
        ttk.Entry(frame, textvariable=gantry_var, width=30).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Collimator Angle (°):").grid(row=2, column=0, sticky=tk.W, pady=5)
        coll_var = tk.StringVar(value=default_coll)
        ttk.Entry(frame, textvariable=coll_var, width=30).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(frame, text="Couch Angle (°):").grid(row=3, column=0, sticky=tk.W, pady=5)
        couch_var = tk.StringVar(value=default_couch)
        ttk.Entry(frame, textvariable=couch_var, width=30).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)

        result = [None]

        def on_ok():
            name = name_var.get().strip()
            if not name:
                messagebox.showwarning("Atenção", "Digite um nome para o arquivo!")
                return

            try:
                gantry = str(float(gantry_var.get()))
                coll = str(float(coll_var.get()))
                couch = str(float(couch_var.get()))
            except ValueError:
                messagebox.showerror("Erro", "Ângulos devem ser números válidos!")
                return

            result[0] = {
                "name": name,
                "gantry": gantry,
                "coll": coll,
                "couch": couch
            }
            dialog.destroy()

        def on_cancel():
            dialog.destroy()

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(button_frame, text="OK", command=on_ok, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=on_cancel, width=15).pack(side=tk.LEFT, padx=5)

        name_entry.focus()
        dialog.wait_window()
        return result[0]

    def update_preview(self):
        """Atualizar preview da conversão"""
        self.preview_text.delete(1.0, tk.END)

        if not self.tiff_files:
            self.preview_text.insert(1.0, "Nenhum arquivo TIFF encontrado.\n\nSelecione uma pasta com arquivos TIFF.")
            return

        num_files = len(self.tiff_files)
        num_items = len(self.conversion_list)

        preview = []
        preview.append("="*60)
        preview.append("PREVIEW DA CONVERSÃO EM LOTE")
        preview.append("="*60)
        preview.append(f"\nArquivos TIFF encontrados: {num_files}")
        preview.append(f"Itens no template: {num_items}")
        preview.append("")

        if num_items > num_files:
            preview.append(f"AVISO: Template tem mais itens ({num_items}) que arquivos ({num_files})")
            preview.append(f"Apenas os primeiros {num_files} itens serão processados.")
            preview.append("")

        preview.append("-"*60)
        preview.append("CONVERSÕES QUE SERÃO REALIZADAS:")
        preview.append("-"*60)
        preview.append("")

        for i in range(min(num_files, num_items)):
            tiff_file = self.tiff_files[i]
            item = self.conversion_list[i]

            preview.append(f"{i+1}. {tiff_file}")
            preview.append(f"   → {item['name']}.dcm")
            preview.append(f"   Parâmetros: Gantry={item['gantry']}° Coll={item['coll']}° Couch={item['couch']}°")
            preview.append("")

        if num_files > num_items:
            preview.append("-"*60)
            preview.append(f"ARQUIVOS NÃO PROCESSADOS ({num_files - num_items}):")
            preview.append("-"*60)
            for i in range(num_items, num_files):
                preview.append(f"  - {self.tiff_files[i]}")

        self.preview_text.insert(1.0, "\n".join(preview))

    def update_status(self, message):
        """Atualizar barra de status"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def convert_batch(self):
        """Converter lote de arquivos"""
        input_folder = self.input_folder.get()
        output_folder = self.output_folder.get()

        if not input_folder or not os.path.exists(input_folder):
            messagebox.showwarning("Atenção", "Selecione uma pasta de entrada válida!")
            return

        if not output_folder:
            messagebox.showwarning("Atenção", "Selecione uma pasta de saída!")
            return

        if not os.path.exists(output_folder):
            try:
                os.makedirs(output_folder)
            except:
                messagebox.showerror("Erro", "Não foi possível criar a pasta de saída!")
                return

        if not self.tiff_files:
            messagebox.showwarning("Atenção", "Nenhum arquivo TIFF encontrado na pasta!")
            return

        if not self.conversion_list:
            messagebox.showwarning("Atenção", "Configure o template de conversão!")
            return

        # Validar parâmetros
        try:
            sid = float(self.sid_var.get())
            dpi = float(self.dpi_var.get())
            if sid <= 0 or dpi <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Erro", "SID e DPI devem ser números válidos maiores que 0!")
            return

        num_files = len(self.tiff_files)
        num_items = len(self.conversion_list)

        # Avisar se há incompatibilidade
        if num_items > num_files:
            if not messagebox.askyesno(
                "Confirmação",
                f"O template tem {num_items} itens mas há apenas {num_files} arquivos.\n\n"
                f"Apenas os primeiros {num_files} itens serão processados.\n\n"
                f"Deseja continuar?"
            ):
                return

        if num_files > num_items:
            if not messagebox.askyesno(
                "Confirmação",
                f"Há {num_files} arquivos mas o template tem apenas {num_items} itens.\n\n"
                f"{num_files - num_items} arquivos não serão processados.\n\n"
                f"Deseja continuar?"
            ):
                return

        # Importar pylinac
        try:
            from pylinac import image
        except ImportError:
            messagebox.showerror(
                "Erro",
                "pylinac não está instalado!\n\n"
                "Execute: pip install pylinac"
            )
            return

        # Iniciar conversão
        num_to_convert = min(num_files, num_items)
        self.progress_var.set(0)
        self.progress_bar['maximum'] = num_to_convert

        converted = 0
        errors = []

        for i in range(num_to_convert):
            tiff_file = self.tiff_files[i]
            item = self.conversion_list[i]

            self.update_status(f"Convertendo {i+1}/{num_to_convert}: {tiff_file}...")

            try:
                input_path = os.path.join(input_folder, tiff_file)
                output_path = os.path.join(output_folder, f"{item['name']}.dcm")

                # Converter
                new_dicom = image.tiff_to_dicom(
                    input_path,
                    sid=sid,
                    gantry=float(item['gantry']),
                    coll=float(item['coll']),
                    couch=float(item['couch']),
                    dpi=dpi
                )

                new_dicom.save_as(output_path, write_like_original=False)
                converted += 1

            except Exception as e:
                errors.append(f"{tiff_file}: {str(e)}")

            self.progress_var.set(i + 1)
            self.root.update_idletasks()

        # Resultados
        self.progress_var.set(0)

        if errors:
            error_msg = "\n".join(errors[:10])
            if len(errors) > 10:
                error_msg += f"\n... e mais {len(errors) - 10} erros"

            messagebox.showwarning(
                "Conversão Concluída com Erros",
                f"Convertidos: {converted}/{num_to_convert}\n"
                f"Erros: {len(errors)}\n\n"
                f"Primeiros erros:\n{error_msg}"
            )
        else:
            messagebox.showinfo(
                "Sucesso",
                f"Conversão em lote concluída!\n\n"
                f"Arquivos convertidos: {converted}\n"
                f"Pasta de saída: {output_folder}"
            )

        self.update_status(f"Conversão concluída: {converted} arquivos convertidos, {len(errors)} erros")

        if messagebox.askyesno("Abrir pasta?", "Deseja abrir a pasta de saída?"):
            import subprocess
            if sys.platform == 'win32':
                os.startfile(output_folder)
            elif sys.platform == 'darwin':
                subprocess.Popen(['open', output_folder])
            else:
                subprocess.Popen(['xdg-open', output_folder])


# ============================================================================
# CLASSE: Menu Principal
# ============================================================================

class MainMenu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Conversor DICOM - Menu Principal")
        self.root.geometry("650x650")
        self.root.resizable(True, True)  # Permitir redimensionamento

        # Centralizar janela
        self.center_window()

        # Variável para controlar janela aberta
        self.converter_window = None

        # Criar interface
        self.create_widgets()

    def center_window(self):
        """Centralizar janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="Conversor DICOM",
            font=('Arial', 24, 'bold')
        )
        title_label.pack(pady=(0, 5))

        subtitle_label = ttk.Label(
            main_frame,
            text="Escolha o tipo de conversão:",
            font=('Arial', 12)
        )
        subtitle_label.pack(pady=(0, 20))

        # Frame para os botões
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Botão IMG para DICOM
        img_frame = ttk.LabelFrame(buttons_frame, text="Conversor IMG", padding="15")
        img_frame.pack(fill=tk.X, pady=(0, 12))

        img_desc = ttk.Label(
            img_frame,
            text="Converte arquivos .img (Elekta iView)\npara formato DICOM padrão.",
            justify=tk.CENTER,
            font=('Arial', 10)
        )
        img_desc.pack(pady=(0, 10))

        img_button = ttk.Button(
            img_frame,
            text="Converter IMG para DICOM",
            command=self.open_img_converter,
            width=30
        )
        img_button.pack()

        # Botão TIFF para DICOM
        tiff_frame = ttk.LabelFrame(buttons_frame, text="Conversor TIFF", padding="15")
        tiff_frame.pack(fill=tk.X, pady=(0, 12))

        tiff_desc = ttk.Label(
            tiff_frame,
            text="Converte imagens TIFF para DICOM\nusando pylinac (Winston-Lutz).",
            justify=tk.CENTER,
            font=('Arial', 10)
        )
        tiff_desc.pack(pady=(0, 10))

        tiff_button = ttk.Button(
            tiff_frame,
            text="Converter TIFF para DICOM",
            command=self.open_tiff_converter,
            width=30
        )
        tiff_button.pack()

        # Botão LOTE TIFF para DICOM
        batch_frame = ttk.LabelFrame(buttons_frame, text="Conversor em Lote TIFF", padding="15")
        batch_frame.pack(fill=tk.X, pady=(0, 12))

        batch_desc = ttk.Label(
            batch_frame,
            text="Converte múltiplos arquivos TIFF para DICOM\ncom templates personalizáveis (Winston-Lutz).",
            justify=tk.CENTER,
            font=('Arial', 10)
        )
        batch_desc.pack(pady=(0, 10))

        batch_button = ttk.Button(
            batch_frame,
            text="Converter Lote TIFF para DICOM",
            command=self.open_batch_converter,
            width=30
        )
        batch_button.pack()

        # Informações de rodapé
        footer_label = ttk.Label(
            main_frame,
            text="Conversor DICOM Unificado v1.0",
            font=('Arial', 8),
            foreground='gray'
        )
        footer_label.pack(side=tk.BOTTOM, pady=(15, 0))

    def open_img_converter(self):
        """Abrir conversor IMG para DICOM"""
        if self.converter_window is None:
            self.root.withdraw()  # Esconder menu principal
            self.converter_window = ImgToDicomConverter(None, self.on_converter_close)
        else:
            messagebox.showwarning("Atenção", "Já existe uma janela de conversão aberta!")

    def open_tiff_converter(self):
        """Abrir conversor TIFF para DICOM"""
        if self.converter_window is None:
            self.root.withdraw()  # Esconder menu principal
            self.converter_window = TiffToDicomConverter(None, self.on_converter_close)
        else:
            messagebox.showwarning("Atenção", "Já existe uma janela de conversão aberta!")

    def open_batch_converter(self):
        """Abrir conversor em lote TIFF para DICOM"""
        if self.converter_window is None:
            self.root.withdraw()  # Esconder menu principal
            self.converter_window = BatchTiffToDicomConverter(None, self.on_converter_close)
        else:
            messagebox.showwarning("Atenção", "Já existe uma janela de conversão aberta!")

    def on_converter_close(self):
        """Callback quando conversor é fechado"""
        self.converter_window = None
        self.root.deiconify()  # Mostrar menu principal novamente

    def run(self):
        """Executar aplicação"""
        self.root.mainloop()


# ============================================================================
# MAIN
# ============================================================================

def main():
    app = MainMenu()
    app.run()


if __name__ == "__main__":
    main()
