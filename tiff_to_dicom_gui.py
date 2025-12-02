#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor TIFF para DICOM - Interface Gráfica
Usa a função nativa do pylinac para conversão compatível com Winston-Lutz
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys

# Configurar codificação UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass


class TiffToDicomConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor TIFF para DICOM (pylinac)")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Variáveis
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.sid_var = tk.StringVar(value="1000")  # Source-to-Image Distance (mm)
        self.gantry_var = tk.StringVar(value="0")
        self.coll_var = tk.StringVar(value="0")
        self.couch_var = tk.StringVar(value="0")
        self.dpi_var = tk.StringVar(value="400")

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

        # SID
        ttk.Label(params_frame, text="SID (mm):").grid(row=0, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        sid_entry = ttk.Entry(params_frame, textvariable=self.sid_var, width=15)
        sid_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Source-to-Image Distance").grid(row=0, column=2, sticky=tk.W, padx=(10, 0))

        # Gantry Angle
        ttk.Label(params_frame, text="Gantry Angle (°):").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        gantry_entry = ttk.Entry(params_frame, textvariable=self.gantry_var, width=15)
        gantry_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Ângulo do Gantry (0-360°)").grid(row=1, column=2, sticky=tk.W, padx=(10, 0))

        # Collimator Angle
        ttk.Label(params_frame, text="Collimator Angle (°):").grid(row=2, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        coll_entry = ttk.Entry(params_frame, textvariable=self.coll_var, width=15)
        coll_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Ângulo do Colimador (0-360°)").grid(row=2, column=2, sticky=tk.W, padx=(10, 0))

        # Couch Angle
        ttk.Label(params_frame, text="Couch Angle (°):").grid(row=3, column=0, sticky=tk.W, padx=(0, 5), pady=5)
        couch_entry = ttk.Entry(params_frame, textvariable=self.couch_var, width=15)
        couch_entry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Label(params_frame, text="Ângulo da Mesa (0-360°)").grid(row=3, column=2, sticky=tk.W, padx=(10, 0))

        # DPI
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
            height=10,
            wrap=tk.WORD,
            font=('Courier', 9)
        )
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Texto informativo inicial
        info_msg = """
CONVERSOR TIFF PARA DICOM usando pylinac

Este conversor utiliza a função image.tiff_to_dicom() do pylinac para criar
arquivos DICOM compatíveis com análise de Winston-Lutz.

PARÂMETROS OBRIGATÓRIOS:
- SID: Source-to-Image Distance (distância da fonte ao detector) em mm
  Exemplo: 1000 mm para aceleradores lineares padrão

- Gantry Angle: Ângulo do gantry em graus (0-360°)
  Exemplo: 0, 90, 180, 270 para Winston-Lutz

- Collimator Angle: Ângulo do colimador em graus (0-360°)
  Geralmente 0 para Winston-Lutz padrão

- Couch Angle: Ângulo da mesa em graus (0-360°)
  Geralmente 0 para Winston-Lutz padrão

- DPI: Resolução da imagem em Dots Per Inch
  Exemplo: 400 DPI para imagens portal padrão

IMPORTANTE: Certifique-se de que o pylinac está instalado:
pip install pylinac
        """
        self.info_text.insert(1.0, info_msg.strip())

        # Botão de conversão
        convert_btn = ttk.Button(
            main_frame,
            text="Converter TIFF para DICOM",
            command=self.convert_file,
            style='Accent.TButton'
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

        # Configurar peso das linhas
        main_frame.rowconfigure(4, weight=1)

    def detect_params_from_filename(self, filename):
        """
        Detecta parâmetros do nome do arquivo
        Retorna dict com parâmetros detectados ou None
        """
        import re
        basename = os.path.basename(filename).lower()

        params = {}

        # Detectar Gantry Angle
        gantry_match = re.search(r'g(?:antry)?[_-]?(\d+)', basename)
        if gantry_match:
            params['gantry'] = gantry_match.group(1)

        # Detectar Collimator Angle
        coll_match = re.search(r'c(?:oll)?[_-]?(\d+)', basename)
        if coll_match:
            params['coll'] = coll_match.group(1)

        # Detectar Couch Angle
        couch_match = re.search(r'(?:couch|table)[_-]?(\d+)', basename)
        if couch_match:
            params['couch'] = couch_match.group(1)

        return params if params else None

    def validate_filename_pattern(self, filename):
        """
        Valida se o nome do arquivo segue um padrão aceitável
        Retorna (is_valid, suggestion)
        """
        import re
        basename = os.path.basename(filename)
        name_lower = basename.lower()

        # Padrões aceitáveis
        acceptable_patterns = [
            r'g(?:antry)?[_-]?\d+',  # gantry_0, g0, gantry0
            r'c(?:oll)?[_-]?\d+',     # coll_45, c45
            r'couch[_-]?\d+',         # couch_90
            r'wl[_-]?g\d+',           # wl_g0, wlg90
        ]

        is_valid = any(re.search(pattern, name_lower) for pattern in acceptable_patterns)

        if not is_valid:
            # Sugerir renomeação baseada no ângulo de gantry que será usado
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

            # Tentar detectar parâmetros do nome do arquivo
            detected_params = self.detect_params_from_filename(filename)
            if detected_params:
                if 'gantry' in detected_params:
                    self.gantry_var.set(detected_params['gantry'])
                if 'coll' in detected_params:
                    self.coll_var.set(detected_params['coll'])
                if 'couch' in detected_params:
                    self.couch_var.set(detected_params['couch'])

                self.update_status(f"Parâmetros detectados do nome do arquivo! Verifique se estão corretos.")

            # Validar padrão do nome do arquivo
            is_valid, suggestion = self.validate_filename_pattern(filename)

            if not is_valid:
                # Perguntar se deseja renomear
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
                    # Mostrar diálogo de renomeação
                    new_name = self.show_rename_dialog(filename, suggestion)
                    if new_name:
                        try:
                            new_path = os.path.join(os.path.dirname(filename), new_name)
                            os.rename(filename, new_path)
                            self.input_file.set(new_path)
                            messagebox.showinfo("Sucesso", f"Arquivo renomeado para:\n{new_name}")
                            filename = new_path

                            # Redetectar parâmetros
                            detected_params = self.detect_params_from_filename(filename)
                            if detected_params and 'gantry' in detected_params:
                                self.gantry_var.set(detected_params['gantry'])
                        except Exception as e:
                            messagebox.showerror("Erro", f"Erro ao renomear arquivo:\n{str(e)}")

            # Sugerir nome de saída
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

        # Centralizar janela
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

        # Validar SID
        try:
            sid = float(self.sid_var.get())
            if sid <= 0:
                errors.append("SID deve ser maior que 0")
        except ValueError:
            errors.append("SID deve ser um número válido")

        # Validar Gantry
        try:
            gantry = float(self.gantry_var.get())
            if gantry < 0 or gantry > 360:
                errors.append("Gantry Angle deve estar entre 0 e 360")
        except ValueError:
            errors.append("Gantry Angle deve ser um número válido")

        # Validar Collimator
        try:
            coll = float(self.coll_var.get())
            if coll < 0 or coll > 360:
                errors.append("Collimator Angle deve estar entre 0 e 360")
        except ValueError:
            errors.append("Collimator Angle deve ser um número válido")

        # Validar Couch
        try:
            couch = float(self.couch_var.get())
            if couch < 0 or couch > 360:
                errors.append("Couch Angle deve estar entre 0 e 360")
        except ValueError:
            errors.append("Couch Angle deve ser um número válido")

        # Validar DPI
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

        # Validar parâmetros
        errors = self.validate_parameters()
        if errors:
            messagebox.showerror("Erro de Validação", "\n".join(errors))
            return

        self.update_status("Convertendo TIFF para DICOM...")

        try:
            # Importar pylinac
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

            # Obter parâmetros
            sid = float(self.sid_var.get())
            gantry = float(self.gantry_var.get())
            coll = float(self.coll_var.get())
            couch = float(self.couch_var.get())
            dpi = float(self.dpi_var.get())

            # Converter usando pylinac
            new_dicom = image.tiff_to_dicom(
                input_path,
                sid=sid,
                gantry=gantry,
                coll=coll,
                couch=couch,
                dpi=dpi
            )

            # Salvar arquivo DICOM (Dataset usa save_as, não save)
            new_dicom.save_as(output_path, write_like_original=False)

            # Atualizar informações
            self.info_text.delete(1.0, tk.END)
            info_msg = f"""
CONVERSÃO CONCLUÍDA COM SUCESSO!

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

Você pode agora usar este arquivo com:
- pylinac.WinstonLutz()
- Outros softwares de análise DICOM
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
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(1.0, f"ERRO:\n{str(e)}")


def main():
    root = tk.Tk()
    app = TiffToDicomConverter(root)
    root.mainloop()


if __name__ == "__main__":
    main()
