from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)


def formatar_matriz(A):
    """Formata a matriz para exibição"""
    return "\n".join(["\t".join([f"{elem:.2f}" for elem in linha]) for linha in A])

def calcular_determinante_matriz(matriz):
    try:
        A = [linha.copy() for linha in matriz]  # Cópia da matriz original
        det = 1.0
        passos = []
        
        n = len(A)
        passos.append("Matriz inicial:\n" + formatar_matriz(A) + "\n")
        
        for i in range(n):
            if A[i][i] == 0:
                for j in range(i + 1, n):
                    if A[j][i] != 0:
                        A[i], A[j] = A[j], A[i]
                        det *= -1
                        passos.append(f"Troca de linhas {i+1} e {j+1}:\n" + formatar_matriz(A) + "\n")
                        break
            
            pivô = A[i][i]
            if pivô == 0:
                passos.append("Pivô zero encontrado. Determinante: 0\n")
                return 0, passos
            
            det *= pivô
            for j in range(i, n):
                A[i][j] /= pivô
            
            passos.append(f"Normalização da linha {i+1} pelo pivô {pivô:.2f}:\n" + formatar_matriz(A) + "\n")
            
            for k in range(i + 1, n):
                fator = A[k][i]
                for j in range(i, n):
                    A[k][j] -= fator * A[i][j]
                
                passos.append(f"Zerando elemento ({k+1}, {i+1}) com fator {fator:.2f}:\n" + formatar_matriz(A) + "\n")
        
        passos.append(f"Determinante final: {det:.2f}\n")
        return round(det, 2), passos
    
    except Exception as e:
        raise ValueError(f"Erro ao calcular determinante: {str(e)}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calcular", methods=["POST"])
def calcular_determinante():
    try:
        matriz = request.json.get("matrix")
        
        if not matriz:
            return jsonify({"error": "Matriz não fornecida"}), 400
        if len(matriz) > 10:
            return jsonify({"error": "Matriz não pode ser maior que 10x10"}), 400
        
        n = len(matriz)
        for linha in matriz:
            if len(linha) != n:
                return jsonify({"error": "Matriz precisa ser quadrada"}), 400
        
        det, passos = calcular_determinante_matriz(matriz)
        return jsonify({"determinante": det, "passos": passos})
    
    except Exception as erro:
        return jsonify({"error": f"Erro ao calcular: {str(erro)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
