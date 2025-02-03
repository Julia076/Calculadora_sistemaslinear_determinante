from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)


def formatar_matriz(A):
    """Formata a matriz para exibição"""
    return "\n".join(["\t".join([f"{elem:.2f}" for elem in linha]) for linha in A])

def calculate_determinant(matrix):
    det = round(np.linalg.det(matrix), 2)  # Calcula o determinante e arredonda
    return det, f"Determinante calculado: {det}"
    
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

def solve_system(A, b):
    n = len(A)
    Ab = np.concatenate((A, b.reshape(n, 1)), axis=1)
    for i in range(n):
        pivot = Ab[i][i]
        if abs(pivot) < 1e-10:
            raise ValueError("O sistema não tem solução única (matriz singular).")
            
        for j in range(i + 1, n):
            factor = Ab[j][i] / pivot
            Ab[j] = Ab[j] - factor * Ab[i]
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = Ab[i][n]
        for j in range(i+1, n):
            x[i] -= Ab[i][j] * x[j]
        x[i] /= Ab[i][i]

    return x

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        matrix = np.array(data.get("matrix"), dtype=float)
        b = np.array(data.get("b"), dtype=float)
        
        # Calculate determinant
        det, steps = calculate_determinant(matrix)
        
        # Solve the system
        try:
            solution = solve_system(matrix, b)
            variable_names = ['x', 'y', 'z', 'w', 'v', 'u', 't', 's', 'r', 'q'][:len(solution)]
            formatted_solution = [f"{var} = {value:.4f}" for var, value in zip(variable_names, solution)]
            
            return jsonify({
                "determinant": det,
                "steps": steps,
                "solution": formatted_solution,
                "success": True
            })
            
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
            
    except Exception as error:
        return jsonify({"error": f"Calculation error: {str(error)}"}), 400

if __name__ == "__main__":
    app.run(debug=True)
