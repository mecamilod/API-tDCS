#titulo: gerar_cabeca_10_20.py
import numpy as np

# =============================================
# PARÂMETROS EDITÁVEIS (em centímetros)
circunferencia_cm = 56.0
nasion_inion_cm = 36.0
tragus_tragus_cm = 34.0
# =============================================

# Derivar dimensões aproximadas da cabeça
raio_aprox = circunferencia_cm / (2 * np.pi)  # ~8.9 cm para 56 cm
comprimento_aprox = nasion_inion_cm * 0.95     # pequena correção
largura_aprox = tragus_tragus_cm * 0.95

# Vértices da malha simplificada (elipsoide)
theta = np.linspace(0, np.pi, 12)           # 12 fatias verticais
phi = np.linspace(0, 2*np.pi, 20)           # 20 colunas
vertices = []
for t in theta:
    for p in phi:
        x = largura_aprox/2 * np.sin(t) * np.cos(p)
        y = comprimento_aprox/2 * np.sin(t) * np.sin(p) + comprimento_aprox/2 * 0.2  # desloca para ficar acima do pescoço
        z = raio_aprox * np.cos(t)
        vertices.append((x, y, z))

# Pescoço (cilindro simples)
pesc_y_start = -comprimento_aprox/2 * 0.3
pesc_y_end = -comprimento_aprox/2 * 0.8
pesc_raio = raio_aprox * 0.6
for y in np.linspace(pesc_y_start, pesc_y_end, 4):
    for p in phi:
        x = pesc_raio * np.cos(p)
        z = pesc_raio * np.sin(p)
        vertices.append((x, y, z))

# Marcadores dos pontos 10/20 (nome, x, y, z) - em cm
# Posições aproximadas sobre a superfície calculada a partir das medidas
pontos = {
    "Nasion":       (0, comprimento_aprox/2, 0),  # frontal superior
    "Inion":        (0, -comprimento_aprox/2, 0),
    "FPz":          (0, comprimento_aprox/2 * 0.7, raio_aprox * 0.95),
    "Tragus_D":     (largura_aprox/2, 0, 0),
    "Tragus_E":     (-largura_aprox/2, 0, 0),
    "Fz":           (0, comprimento_aprox/2 * 0.3, raio_aprox * 0.8),
    "Cz":           (0, 0, raio_aprox),
    "Pz":           (0, -comprimento_aprox/2 * 0.3, raio_aprox * 0.8),
    "Oz":           (0, -comprimento_aprox/2 * 0.7, raio_aprox * 0.6),
    "F3":           (largura_aprox/4, comprimento_aprox/2 * 0.3, raio_aprox * 0.7),
    "F4":           (-largura_aprox/4, comprimento_aprox/2 * 0.3, raio_aprox * 0.7),
    "F7":           (largura_aprox/2 * 0.85, comprimento_aprox/2 * 0.7, raio_aprox * 0.35),
    "F8":           (-largura_aprox/2 * 0.85, comprimento_aprox/2 * 0.7, raio_aprox * 0.35),
    "C3":           (largura_aprox/4, 0, raio_aprox * 0.85),
    "C4":           (-largura_aprox/4, 0, raio_aprox * 0.85),
    "T3/T7":        (largura_aprox/2, comprimento_aprox/2 * 0.15, 0),
    "T4/T8":        (-largura_aprox/2, comprimento_aprox/2 * 0.15, 0),
    "P3":           (largura_aprox/4, -comprimento_aprox/2 * 0.3, raio_aprox * 0.65),
    "P4":           (-largura_aprox/4, -comprimento_aprox/2 * 0.3, raio_aprox * 0.65),
    "T5/P7":        (largura_aprox/2 * 0.85, -comprimento_aprox/2 * 0.7, raio_aprox * 0.2),
    "T6/P8":        (-largura_aprox/2 * 0.85, -comprimento_aprox/2 * 0.7, raio_aprox * 0.2),
    "O1":           (largura_aprox/4, -comprimento_aprox/2 * 0.7, raio_aprox * 0.5),
    "O2":           (-largura_aprox/4, -comprimento_aprox/2 * 0.7, raio_aprox * 0.5),
    "F5":           (largura_aprox/2 * 0.65, comprimento_aprox/2 * 0.3, raio_aprox * 0.5),
    "CP5":          (largura_aprox/2 * 0.65, -comprimento_aprox/2 * 0.1, raio_aprox * 0.5),
}

# Escrever arquivo OBJ
with open("cabeca_10_20.obj", "w") as f:
    f.write("# Cabeca editavel em centimetros\n")
    f.write(f"# Circunferencia: {circunferencia_cm} cm\n")
    f.write(f"# Nasion-Inion: {nasion_inion_cm} cm\n")
    f.write(f"# Tragus-Tragus: {tragus_tragus_cm} cm\n\n")
    
    for i, (x, y, z) in enumerate(vertices, 1):
        f.write(f"v {x:.4f} {y:.4f} {z:.4f}\n")
    
    f.write("\n# Marcadores 10/20 como grupos\n")
    for nome, (x, y, z) in pontos.items():
        f.write(f"v {x:.4f} {y:.4f} {z:.4f} #{nome}\n")
    
    # Gerar faces (triângulos da malha principal)
    f.write("\n# Faces (malha)\n")
    n_theta = 12
    n_phi = 20
    for i in range(n_theta - 1):
        for j in range(n_phi - 1):
            a = i * n_phi + j + 1
            b = a + 1
            c = (i + 1) * n_phi + j + 1
            d = c + 1
            f.write(f"f {a} {c} {b}\n")
            f.write(f"f {b} {c} {d}\n")

print("Arquivo 'cabeca_10_20.obj' gerado com sucesso!")
