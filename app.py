from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'axelligme-secret-key'

# Liste des phrases et réponses correctes
lettre_codee = [
    ("Même si nous sommes loin, mon coeur reste scellé au tien par une ____ indestructible, plus forte que la distance :", "Substance"),
    ("Le temps que nous passons loin l’un de l’autre est une simple ____ avant une nouvelle dose de bonheur ensemble.", "Pause"),
    ("Peu importe la distance, ce lien est encapsulé dans une ____ qui nous protège de tout obstacle.", "Gélule"),
    ("Je prie que nos retrouvailles soient comme une ____ d’amour, un moment de pure joie et de bonheur renouvelé.", "Régénération"),
    ("Je t'____, princesse", "Aime"),
    ("Ton bien-aimé, ____ ❤️", "A.C")
]

@app.route("/", methods=["GET", "POST"])
def index():
    if 'index' not in session:
        session['index'] = 0
        session['score'] = 0
        session['attempts'] = 0
        session['answers'] = []
        session['last_message'] = ""

    idx = session['index']

    if idx >= len(lettre_codee):
        texte_final = []
        for i, (phrase, _) in enumerate(lettre_codee):
            rep = session['answers'][i] if i < len(session['answers']) else "____"
            texte_final.append(phrase.replace("____", rep))
        final_text = "<br><br>".join(texte_final)
        score = session['score']
        total = len(lettre_codee)
        session.clear()
        return render_template("result.html", score=score, total=total, texte=final_text)

    question, correct_answer = lettre_codee[idx]

    # Sauter les questions sans réponse attendue
    if isinstance(correct_answer, str) and correct_answer.strip() == "":
        session['answers'].append("")
        session['index'] += 1
        return redirect(url_for('index'))

    if request.method == "POST":
        user_input = request.form.get("reponse", "").strip().lower()
        expected_answer = correct_answer.lower() if isinstance(correct_answer, str) else str(correct_answer[0]).lower()

        if user_input == expected_answer:
            session['score'] += 1
            session['answers'].append(correct_answer)
            session['index'] += 1
            session['attempts'] = 0
            session['last_message'] = "✅ Bravo mon amour, tu avances un peu plus vers mon cœur !"
        else:
            session['attempts'] += 1
            if session['attempts'] >= 3:
                session['answers'].append(correct_answer)
                session['index'] += 1
                session['attempts'] = 0
                session['last_message'] = f"📢 La bonne réponse était : {correct_answer}"
            else:
                session['last_message'] = f"❌ Encore un effort ma princesse ! ({session['attempts']}/3)"
        return redirect(url_for('index'))

    return render_template("index.html", question=question, index=idx + 1, total=len(lettre_codee), message=session.get("last_message", ""))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)