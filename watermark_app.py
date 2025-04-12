import tkinter as tk
from tkinter import filedialog, ttk, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")

        # Icona personalizzata
        try:
            icon = tk.PhotoImage(file="watermark.png")
            self.root.iconphoto(False, icon)
        except Exception as e:
            print("Icona non trovata o errore:", e)

        # Centro la finestra
        self.center_window(1000, 600)

        self.image_path = None
        self.modified_image = None
        self.text_color = (255, 255, 255, 80)  # Default: bianco semitrasparente

        # Cornice superiore con opzioni in una riga
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(top_frame, text="Testo:").grid(row=0, column=0, sticky='w')
        self.text_entry = tk.Entry(top_frame, width=20)
        self.text_entry.grid(row=0, column=1, padx=5)

        tk.Label(top_frame, text="Font:").grid(row=0, column=2, sticky='w')
        self.fonts = self.get_fonts()
        self.font_var = tk.StringVar(value=self.fonts[0])
        self.font_menu = ttk.Combobox(top_frame, textvariable=self.font_var, values=self.fonts, width=25)
        self.font_menu.grid(row=0, column=3, padx=5)

        tk.Label(top_frame, text="Dimensione:").grid(row=0, column=4, sticky='w')
        self.size_spin = tk.Spinbox(top_frame, from_=10, to=100, width=5)
        self.size_spin.grid(row=0, column=5, padx=5)

        self.color_btn = tk.Button(top_frame, text="Colore", command=self.choose_color)
        self.color_btn.grid(row=0, column=6, padx=5)

        self.choose_btn = tk.Button(top_frame, text="Scegli Immagine", command=self.choose_image)
        self.choose_btn.grid(row=0, column=7, padx=5)

        self.apply_btn = tk.Button(top_frame, text="Applica", command=self.apply_watermark)
        self.apply_btn.grid(row=0, column=8, padx=5)

        self.save_btn = tk.Button(top_frame, text="Salva", command=self.save_image)
        self.save_btn.grid(row=0, column=9, padx=5)

        # Area di anteprima
        self.preview_frame = tk.Frame(root, bg="gray")
        self.preview_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.preview_label = tk.Label(self.preview_frame, bg="black")
        self.preview_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Aggiungi l'evento di ridimensionamento della finestra
        self.root.bind("<Configure>", lambda e: self.show_image(self.modified_image) if self.modified_image else None)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def get_fonts(self):
        fonts_dir = "C:/Windows/Fonts" if os.name == 'nt' else "/usr/share/fonts"
        fonts = []
        for root, dirs, files in os.walk(fonts_dir):
            for file in files:
                if file.endswith(".ttf"):
                    fonts.append(os.path.join(root, file))
        return fonts[:20] if fonts else ["arial.ttf"]

    def choose_color(self):
        color = colorchooser.askcolor(title="Scegli colore del testo")
        if color[0]:
            r, g, b = map(int, color[0])
            self.text_color = (r, g, b, 80)

    def choose_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if path:
            self.image_path = path
            self.show_image(Image.open(path))

    def apply_watermark(self):
        if not self.image_path:
            return

        img = Image.open(self.image_path).convert("RGBA")
        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        text = self.text_entry.get()
        font_path = self.font_var.get()
        font_size = int(self.size_spin.get())

        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x_gap = text_width + 40
        y_gap = text_height + 40

        for y in range(0, img.height, y_gap):
            for x in range(0, img.width, x_gap):
                draw.text((x, y), text, font=font, fill=self.text_color)

        watermarked = Image.alpha_composite(img, txt_layer)
        self.modified_image = watermarked.convert("RGB")
        self.show_image(self.modified_image)

    def show_image(self, img):
        if not img:
            return
        
        # Ottieni le nuove dimensioni della finestra
        frame_width = self.preview_label.winfo_width()
        frame_height = self.preview_label.winfo_height()

        if frame_width > 0 and frame_height > 0:
            # Ridimensiona l'immagine per adattarsi alle nuove dimensioni della finestra
            preview = img.copy()

            # Mantieni il rapporto di aspetto dell'immagine
            preview.thumbnail((frame_width, frame_height))

            # Mostra l'immagine ridimensionata nell'anteprima
            self.tk_img = ImageTk.PhotoImage(preview)
            self.preview_label.config(image=self.tk_img)
            self.preview_label.image = self.tk_img

    def save_image(self):
        if self.modified_image:
            filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png")])
            if filepath:
                self.modified_image.save(filepath)
                print(f"Immagine salvata in: {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
