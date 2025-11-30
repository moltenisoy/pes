import tkinter as tk
from tkinter import ttk, filedialog
import struct

PES6_PARAMS = {
    'Sistema': {
        'system_gamespeed': {'offset': 0x11A784, 'type': 'float', 'default': 1.0, 'label': 'Velocidad del Juego'},
        'system_ml_start_year': {'offset': 0x11A78B, 'type': 'uint16', 'default': 2006, 'label': 'Año Inicio Liga Master'},
        'system_option_file_path': {'offset': 0x10F8E8, 'type': 'string:11', 'default': 'save\\folder1', 'label': 'Ruta Option File'},
    },
    'Física del Balón': {
        'physics_ball_weight': {'offset': 0x98E4E8, 'type': 'float', 'default': 3.5, 'label': 'Peso del Balón'},
        'physics_ball_friction': {'offset': 0x98E4EC, 'type': 'float', 'default': 0.05, 'label': 'Fricción del Balón'},
        'ball_ground_friction': {'offset': 0x00A85520, 'type': 'float', 'default': 0.985, 'label': 'Fricción en Suelo'},
        'ball_air_resistance': {'offset': 0x00A85524, 'type': 'float', 'default': 0.996, 'label': 'Resistencia del Aire'},
        'ball_restitution': {'offset': 0x00A85528, 'type': 'float', 'default': 0.75, 'label': 'Rebote del Balón'},
        'ball_shot_power': {'offset': 0x00A85530, 'type': 'float', 'default': 1.12, 'label': 'Potencia de Tiro'},
        'ball_spin_decay': {'offset': 0x00A85534, 'type': 'float', 'default': 0.05, 'label': 'Decaimiento del Efecto'},
        'ball_weight_factor': {'offset': 0x00A85538, 'type': 'float', 'default': 1.5, 'label': 'Factor de Masa'},
        'gravity_constant': {'offset': 0x68C4F0, 'type': 'float', 'default': -9.84, 'label': 'Gravedad'},
        'ground_friction_alt': {'offset': 0x68C4F4, 'type': 'float', 'default': 0.1, 'label': 'Fricción Suelo Alt'},
        'air_resistance_alt': {'offset': 0x68C4F8, 'type': 'float', 'default': 0.01, 'label': 'Resistencia Aire Alt'},
        'bounce_retention': {'offset': 0x68C4FC, 'type': 'float', 'default': 0.7, 'label': 'Retención Rebote'},
        'player_proximity': {'offset': 0x68C500, 'type': 'float', 'default': 0.2, 'label': 'Proximidad Jugador'},
        'spin_decay_rate': {'offset': 0x68C504, 'type': 'float', 'default': 0.95, 'label': 'Tasa Decaimiento Spin'},
    },
    'Jugadores': {
        'player_inertia': {'offset': 0x98E4F0, 'type': 'float', 'default': 0.1, 'label': 'Inercia del Jugador'},
        'player_shot_accuracy': {'offset': 0x98E4F4, 'type': 'float', 'default': 1.0, 'label': 'Precisión de Disparo'},
        'player_acceleration': {'offset': 0x00A9B1C0, 'type': 'float', 'default': 1.08, 'label': 'Aceleración'},
        'player_max_speed': {'offset': 0x00A9B1C4, 'type': 'float', 'default': 0.97, 'label': 'Velocidad Máxima'},
        'player_deceleration': {'offset': 0x00A9B1C8, 'type': 'float', 'default': 0.92, 'label': 'Deceleración'},
        'dribble_speed_limit': {'offset': 0x00A9B1CC, 'type': 'float', 'default': 0.85, 'label': 'Velocidad Dribbling'},
        'player_turning_rate': {'offset': 0x00A9B1D0, 'type': 'float', 'default': 1.2, 'label': 'Tasa de Giro'},
    },
    'Inteligencia Artificial': {
        'ai_goalkeeper_agility': {'offset': 0x98E500, 'type': 'float', 'default': 1.0, 'label': 'Agilidad Portero'},
        'ai_referee_strictness': {'offset': 0x98E510, 'type': 'float', 'default': 1.0, 'label': 'Severidad Árbitro'},
        'ai_pass_assist': {'offset': 0x98E518, 'type': 'float', 'default': 0.8, 'label': 'Asistencia Pases'},
        'ai_ml_strategy': {'offset': 0x790A3C, 'type': 'uint32', 'default': 67372036, 'label': 'Estrategia LM'},
        'ai_foul_tolerance': {'offset': 0x009F4E10, 'type': 'uint32', 'default': 50, 'label': 'Tolerancia Faltas'},
        'ai_gk_reaction': {'offset': 0x009F4E14, 'type': 'float', 'default': 1.0, 'label': 'Reacción Portero'},
        'ai_pass_error': {'offset': 0x009F4E18, 'type': 'float', 'default': 0.7, 'label': 'Error Pases IA'},
        'ai_defensive_line': {'offset': 0x009F4E1C, 'type': 'float', 'default': 25.0, 'label': 'Línea Defensiva'},
        'ai_stamina_drain': {'offset': 0x009F4E20, 'type': 'uint32', 'default': 80, 'label': 'Gasto Resistencia'},
    },
    'Cámara': {
        'camera_wide_zoom': {'offset': 0x5A4B2C, 'type': 'float', 'default': 1.0, 'label': 'Zoom Cámara'},
        'camera_wide_angle': {'offset': 0x5A4B30, 'type': 'float', 'default': 0.0, 'label': 'Ángulo Cámara'},
        'camera_wide_height': {'offset': 0x5A4B38, 'type': 'float', 'default': 1.0, 'label': 'Altura Cámara'},
    },
}

class PES6Patcher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PES6 Patcher")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.exe_path = None
        self.entries = {}
        self.setup_ui()
        
    def setup_ui(self):
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)
        ttk.Button(top_frame, text="Cargar PES6.exe", command=self.load_exe).pack(side=tk.LEFT, padx=5)
        self.path_label = ttk.Label(top_frame, text="No se ha cargado ningún archivo")
        self.path_label.pack(side=tk.LEFT, padx=10)
        ttk.Button(top_frame, text="Parchear", command=self.patch_exe).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="Restaurar Defaults", command=self.restore_defaults).pack(side=tk.RIGHT, padx=5)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for category, params in PES6_PARAMS.items():
            frame = ttk.Frame(notebook, padding=10)
            notebook.add(frame, text=category)
            canvas = tk.Canvas(frame)
            scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            scrollable_frame.bind("<Configure>", lambda e, c=canvas: c.configure(scrollregion=c.bbox("all")))
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            for i, (key, data) in enumerate(params.items()):
                row_frame = ttk.Frame(scrollable_frame)
                row_frame.pack(fill=tk.X, pady=5)
                ttk.Label(row_frame, text=data['label'], width=25, anchor='w').pack(side=tk.LEFT, padx=5)
                ttk.Label(row_frame, text=f"[0x{data['offset']:X}]", width=12, anchor='w').pack(side=tk.LEFT, padx=5)
                entry = ttk.Entry(row_frame, width=20)
                entry.insert(0, str(data['default']))
                entry.pack(side=tk.LEFT, padx=5)
                self.entries[key] = entry
                ttk.Label(row_frame, text=data['type'], width=10, anchor='w').pack(side=tk.LEFT, padx=5)
                
    def load_exe(self):
        path = filedialog.askopenfilename(filetypes=[("Ejecutable", "*.exe"), ("Todos", "*.*")])
        if path:
            self.exe_path = path
            self.path_label.config(text=path)
            self.read_current_values()
            
    def read_current_values(self):
        if not self.exe_path:
            return
        try:
            with open(self.exe_path, 'rb') as f:
                for category, params in PES6_PARAMS.items():
                    for key, data in params.items():
                        try:
                            f.seek(data['offset'])
                            if data['type'] == 'float':
                                value = struct.unpack('<f', f.read(4))[0]
                                self.entries[key].delete(0, tk.END)
                                self.entries[key].insert(0, f"{value:.6f}")
                            elif data['type'] == 'uint16':
                                value = struct.unpack('<H', f.read(2))[0]
                                self.entries[key].delete(0, tk.END)
                                self.entries[key].insert(0, str(value))
                            elif data['type'] == 'uint32':
                                value = struct.unpack('<I', f.read(4))[0]
                                self.entries[key].delete(0, tk.END)
                                self.entries[key].insert(0, str(value))
                            elif data['type'].startswith('string:'):
                                length = int(data['type'].split(':')[1])
                                value = f.read(length).decode('latin-1').rstrip('\x00')
                                self.entries[key].delete(0, tk.END)
                                self.entries[key].insert(0, value)
                        except:
                            pass
        except:
            pass
            
    def patch_exe(self):
        if not self.exe_path:
            return
        try:
            with open(self.exe_path, 'r+b') as f:
                for category, params in PES6_PARAMS.items():
                    for key, data in params.items():
                        try:
                            value_str = self.entries[key].get()
                            f.seek(data['offset'])
                            if data['type'] == 'float':
                                value = float(value_str)
                                f.write(struct.pack('<f', value))
                            elif data['type'] == 'uint16':
                                value = int(value_str)
                                f.write(struct.pack('<H', value))
                            elif data['type'] == 'uint32':
                                value = int(value_str)
                                f.write(struct.pack('<I', value))
                            elif data['type'].startswith('string:'):
                                length = int(data['type'].split(':')[1])
                                encoded = value_str.encode('latin-1')
                                padded = encoded[:length].ljust(length, b'\x00')
                                f.write(padded)
                        except:
                            pass
        except:
            pass
            
    def restore_defaults(self):
        for category, params in PES6_PARAMS.items():
            for key, data in params.items():
                self.entries[key].delete(0, tk.END)
                self.entries[key].insert(0, str(data['default']))
                
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = PES6Patcher()
    app.run()
