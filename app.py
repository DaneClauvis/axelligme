from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'axelligme-secret-key'

# Liste des phrases et réponses correctes
lettre_codee = [
    ("Ma chère Axelle,", [""]),
    ("Depuis que tu es entrée dans ma vie, tu es mon ____ contre toutes les douleurs de l'âme.", ["Antidote"]),
    ("Ton amour agit comme un ____ qui calme mes inquiétudes et m'apporte une sérénité infinie.", ["Sédatif"]),
    ("Te souviens tu des premières fois où on restait tard au téléphone ! Où je veillais pendant tes  ____ à l'hôpital !", ["Gardes"]),
    ("A ce moment là, je ne t'avais pas encore rencontré ! Je n'aurai jamais imaginé que tu deviendrais l' ____ que je respire quotidiennement!", ["Oxygène"]),
    ("Tu as su me captiver jour après jour par tes histoires aussi fascinantes les unes que les autres à tel point qu'elles devenaient les ____ qui m'apportaient l'énergie nécessaire.", ["Vitamines"]),
    ("Puis nous traçions nos premiers projets. Ceux de nous voir en Janvier 2024 et finir avec les restaurants de Ouagadougou😂.", [""]),
    ("C'était sans savoir à ce moment là que manger rendait ton ventre 'lourd' et que la nourriture était comme un ____ pour toi.", ["Somnifère"]),
    ("Je dois t'avouer que je n'étais pas si impatient de te rencontrer. Mais j'aimais bien ce que tu dégageais.", [""]),
    ("Mais par-dessus tout, j'aimais l'idée de pouvoir échanger avec toi, comme une décharge de ____ qui nourrit mon plaisir et ma motivation à te parler.💖🧠 ", ["dopamine"]),
    ("Contrairement aux médecins ici, toi tu m'écoutais quand je me sentais mal et t'efforçais de me prodiguer de bons ____ .", ["Médicaments"]),
    ("Quand je suis rentré ! Ahhh Quand je suis rentré ! Janvier 2024, je te dis ! Incroyablissement incroyable !", [""]),
    ("Je venais de périodes difficiles comme tu le sais. Tu as su trouver la ____ pour me faire tout oublier et repartir de 0.", ["Formule"]),
    ("Me mettre en ta présence pour la première fois était une véritable injection d’____, un instant de bien-être et de bonheur pur.💖💉", ["Endorphine"]),
    ("Sois honnête ; ce premier soir, tu as diffusé des ____ envoûtantes, rendant toute résistance à ton charme impossible. N'est ce pas ?😏🔥", ["Phéromones"]),
    ("Puis, comprendre l'effet que tu avais sur moi était devenu plus qu'une ____.", ["Obsession"]),
    ("À chaque rencontre, l’____ montait, me rendant impatient de me retrouver dans ta sphère.💖", ["Adrénaline"]),
    ("Je me demande toujours pourquoi tu fuyais mon regard au second RDV. Comme si on t'avait annoncer qu'on allait devoir te faire des ____ de cortisone.💉😆", ["Piqûres"]),
    ("Je redevenais un enfant de 2 ans qu'on confiait à un ____ à notre troisième RDV, à l'hôpital, la nuit.", ["Pédiatre"]),
    ("Le mélange de sentiments qui m'animait m'échappait encore, comme un effet ____ imprévu.", ["Secondaire"]),
    ("Le danger ! ⚠️ Tu me snobais quelques fois. Encore de quoi me rendre fou telle une ____.", ["Drogue"]),
    ("Puis vint ce quatrième et dernier RDV. Févier 2024. Celui qui allait me captiver irrémédiablement, comme une ____ à l'effet irréversible.", ["Substance"]),
    ("Celui où tu me portais une attention particulière et sans détail en reste. Celui où j'ai compris pourquoi tu faisais la ____ comme filière.", ["Filière"]),
    ("L'oreille que tu étais pour moi en ce jour m'a guéris de toutes les ____ internes.", ["Blessures"]),
    ("J'ai été particulièrement touché par le temps que tu m'as consacré, ma ____.", ["Pharmacienne"]),
    ("Quand tu posais ce ____ à mon poignet, tu sais ce que je voyais ?", ["Bracelet"]),
    ("Je vais te le dire.", [""]),
    ("Je voyais la reine qu’il me fallait, celle qui m’aidait à conquérir mon royaume et qui, comme un précieux , scellait ma victoire en posant cette couronne sur ma tête. 👑💖💊", ["Remède"]),
    ("Je voyais celle, la reine, qui me disait : 'Mon roi, dors tranquille, ta reine est là.' Comme un ____ apaisant, elle prenait les choses en main, dissipant mes tourments.", ["Sédatif"]),
    ("J'aimais chaque sourire, chaque mot de flirt, chaque caresse, j'aimais ressentir les batements de ton ____.", ["Coeur"]),
    ("Ton baiser ! Tel un ____ aux vertus enivrantes, il apaisa mon âme, éveilla mes sens et scella en moi l’empreinte d’un doux envoûtement.", ["Baume"]),
    ("Je n'avais plus qu'une seule mission.", [""]),
    ("Celle de te marquer de mon empreinte. Celle graver ma signature en toi, tel un artisan signant son ____.", ["Oeuvre"]),
    ("Car oui, tu es cette oeuvre qu'on ne pourrait même pas vendre aux enchères. Cette oeuvre que tout le monde veut s'arracher. Cette oeuvre qui élève l'artiste.", [""]),
    ("Quel ne fut mon désaroi de te savoir sur le départ, de 'Me' savoir sur le départ pour la France.", [""]),
    ("Ecoute ces mots : ", [""]),
    ("Chaque message de toi agit comme une ____ qui réchauffe mon cœur et me donne de la force.", ["Injection"]),
    ("Ton absence est un ____ dont je ressens les effets, mais ton amour est le meilleur traitement.", ["Manque"]),
    ("Comme une ____ bien dosée, notre relation repose sur un équilibre parfait entre amour et compréhension.", ["Formule"]),
    ("Tu es la ____ qui stabilise mes émotions et m’apporte un bien-être constant.", ["Molécule"]),
    ("Cette molécule, cette molécule, cette molécule : elle est celle de l'____ que je te voue.", ["Amour"]),
    ("Quand je suis avec toi, chaque battement de mon cœur est un ____ harmonieux avec la mélodie de notre amour.", ["Rythme"]),
    ("Comme un ____ essentiel, notre amour est vital pour mon équilibre et mon bonheur.", ["Supplément"]),
    ("Même si nous sommes loin, mon coeur reste scellé au tien par une ____ indestructible, plus forte que la distance :", ["Substance"]),
    ("Le temps que nous passons loin l’un de l’autre est une simple ____ avant une nouvelle dose de bonheur ensemble.", ["Pause"]),
    ("Peu importe la distance, ce lien est encapsulé dans une ____ qui nous protège de tout obstacle.", ["Gélule"]),
    ("Je prie que nos retrouvailles soient comme une ____ d’amour, un moment de pure joie et de bonheur renouvelé.", ["Régénération"]),
    ("Je t'aime, princesse", [""]),
    ("Ton bien-aimé, ____ ❤️", ["A.C"])
]

@app.route("/", methods=["GET", "POST"])
def index():
    if 'index' not in session:
        session['index'] = 0
        session['score'] = 0
        session['attempts'] = 0
        session['answers'] = []

    idx = session['index']

    if request.method == "POST":
        user_input = request.form.get("reponse", "").strip().lower()
        correct_answer = lettre_codee[idx][1].lower()

        if user_input == correct_answer:
            session['score'] += 1
            session['answers'].append(correct_answer)
            session['index'] += 1
            session['attempts'] = 0
            message = "✅ Bravo mon amour, tu avances un peu plus vers mon cœur !"
        else:
            session['attempts'] += 1
            if session['attempts'] >= 3:
                session['answers'].append(correct_answer)
                session['index'] += 1
                session['attempts'] = 0
                message = f"📢 La bonne réponse était : {correct_answer}"
            else:
                message = f"❌ Encore un effort ma princesse ! ({session['attempts']}/3)"

        return redirect(url_for('index'))

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

    question = lettre_codee[idx][0]
    return render_template("index.html", question=question, index=idx + 1, total=len(lettre_codee))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
