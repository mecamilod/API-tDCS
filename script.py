from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="App tDCS 10/20")

class MedidasCranianas(BaseModel):
    nasion_inion: float
    tragus_tragus: float
    circunferencia: float

@app.post("/calcular_alvos")
def calcular_alvos(medidas: MedidasCranianas):
    ni = medidas.nasion_inion
    tt = medidas.tragus_tragus
    
    alvos = {
        "Fpz": {"x": 0.0, "y": ni * 0.40},
        "Fp1": {"x": -tt * 0.20, "y": ni * 0.40},
        "Fp2": {"x": tt * 0.20, "y": ni * 0.40},
        "F7": {"x": -tt * 0.40, "y": ni * 0.20},
        "F3": {"x": -tt * 0.20, "y": ni * 0.20},
        "Fz": {"x": 0.0, "y": ni * 0.20},
        "F4": {"x": tt * 0.20, "y": ni * 0.20},
        "F8": {"x": tt * 0.40, "y": ni * 0.20},
        "T3": {"x": -tt * 0.40, "y": 0.0},
        "C3": {"x": -tt * 0.20, "y": 0.0},
        "Cz": {"x": 0.0, "y": 0.0},
        "C4": {"x": tt * 0.20, "y": 0.0},
        "T4": {"x": tt * 0.40, "y": 0.0},
        "T5": {"x": -tt * 0.40, "y": -ni * 0.20},
        "P3": {"x": -tt * 0.20, "y": -ni * 0.20},
        "Pz": {"x": 0.0, "y": -ni * 0.20},
        "P4": {"x": tt * 0.20, "y": -ni * 0.20},
        "T6": {"x": tt * 0.40, "y": -ni * 0.20},
        "O1": {"x": -tt * 0.20, "y": -ni * 0.40},
        "Oz": {"x": 0.0, "y": -ni * 0.40},
        "O2": {"x": tt * 0.20, "y": -ni * 0.40},
        "F5_Broca": {"x": -tt * 0.30, "y": ni * 0.20},
        "CP5_Wernicke": {"x": -tt * 0.30, "y": -ni * 0.10}
    }
    return {"alvos_cm": alvos}

html_content = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mapeamento 3D - tDCS 10/20</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; color: #333; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 100%; max-width: 800px; margin-bottom: 20px; }
        .inputs { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }
        label { font-weight: bold; font-size: 14px; }
        input { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { background-color: #007bff; color: white; padding: 12px; border: none; border-radius: 4px; cursor: pointer; width: 100%; font-size: 16px; font-weight: bold; }
        button:hover { background-color: #0056b3; }
        #cerebro3d { width: 100%; height: 600px; background: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align: center; margin-top: 0;">Mapeamento Craniano tDCS</h2>
        <div class="inputs">
            <div>
                <label>Nasion-Inion (cm)</label>
                <input type="number" id="ni" value="36" step="0.1">
            </div>
            <div>
                <label>Tragos-Tragos (cm)</label>
                <input type="number" id="tt" value="36" step="0.1">
            </div>
            <div>
                <label>Circunferência (cm)</label>
                <input type="number" id="circ" value="56" step="0.1">
            </div>
        </div>
        <button onclick="gerarModelo()">Calcular e Gerar Modelo 3D</button>
    </div>
    
    <div id="cerebro3d"></div>

    <script>
        async function gerarModelo() {
            const ni = parseFloat(document.getElementById('ni').value);
            const tt = parseFloat(document.getElementById('tt').value);
            const circ = parseFloat(document.getElementById('circ').value);

            const resposta = await fetch('/calcular_alvos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nasion_inion: ni, tragos_tragus: tt, circunferencia: circ })
            });
            
            const dados = await resposta.json();
            const alvos = dados.alvos_cm;

            let x = [], y = [], z = [], labels = [], colors = [];
            const raio = Math.max(ni, tt) / 2;

            for (let [nome, coord] of Object.entries(alvos)) {
                labels.push(nome);
                x.push(coord.x);
                y.push(coord.y);
                
                let val_z = Math.sqrt(Math.max(0, raio*raio - coord.x*coord.x - coord.y*coord.y));
                z.push(val_z);

                colors.push((nome.includes('Broca') || nome.includes('Wernicke')) ? '#ff0000' : '#007bff');
            }

            const traco = [{
                x: x, y: y, z: z, text: labels,
                mode: 'markers+text', type: 'scatter3d',
                marker: { size: 6, color: colors },
                textposition: 'top center'
            }];

            const layout = {
                title: 'Alvos 10/20 em 3D',
                scene: {
                    xaxis: { title: 'Tragos-Tragos (X)' },
                    yaxis: { title: 'Nasion-Inion (Y)' },
                    zaxis: { title: 'Curvatura (Z)' }
                },
                margin: { l: 0, r: 0, b: 0, t: 40 }
            };

            Plotly.newPlot('cerebro3d', traco, layout);
        }
        
        window.onload = gerarModelo;
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def interface_web():
    return html_content