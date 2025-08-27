from flask import Flask, render_template, request, session, redirect, url_for, flash
from circuito import Serie, Paralelo  # importa suas classes

app = Flask(__name__)
app.secret_key = "123"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            V = float(request.form["V"])  # pega a tensão
            qtd = int(request.form["qtd"])  # quantidade de resistores
            resistores = []

            for i in range(qtd):
                valor = request.form.get(f"R{i+1}")
                if valor:
                    resistores.append(float(valor))

            tipo = request.form["tipo"]

            if tipo == "serie":
                circuito = Serie(resistores, V)
            elif tipo == "paralelo":
                circuito = Paralelo(resistores, V)
            else:
                flash("Tipo de circuito inválido")
                return redirect(url_for("index"))

            Req, resultados = circuito.calcular()
            
            # Armazena os dados na sessão
            session["Req"] = Req
            session["resultados"] = resultados
            session["V"] = V
            session["tipo"] = tipo
            
            return redirect(url_for("resultado"))
            
        except Exception as e:
            flash(f"Erro ao processar os dados: {str(e)}")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/resultado")
def resultado():
    Req = session.get("Req")
    resultados = session.get("resultados")
    V = session.get("V")
    tipo = session.get("tipo")
    
    # Verifica se os dados existem na sessão
    if Req is None or resultados is None:
        flash("Nenhum resultado encontrado. Por favor, calcule primeiro.")
        return redirect(url_for("index"))
    
    print("DEBUG Req:", Req)
    print("DEBUG resultados:", resultados)
    
    return render_template("resultado.html", 
                         Req=Req, 
                         resultados=resultados, 
                         V=V, 
                         tipo=tipo)

if __name__ == "__main__":
    app.run(debug=True)