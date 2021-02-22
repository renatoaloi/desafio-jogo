from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_imob_report.sqlite3'
db = SQLAlchemy(app)


class Relatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vencedor = db.Column(db.Integer, nullable=False)
    rodadas = db.Column(db.Integer, nullable=False)

    def __init__(self, vencedor, rodadas):
        self.vencedor = vencedor
        self.rodadas = rodadas

    def __repr__(self):
        return '<Relatorio vencedor=%s rodadas=%s>' % (self.vencedor, self.rodadas)


db.create_all()


def return_handler(msg, obj):
    return jsonify({ 'msg': msg, 'object': obj })

@app.route('/jogo/resultado', methods=['POST'])
def criar_resultado():
    vencedor = request.json['vencedor_id'] or abort(400)
    rodadas = request.json['rodadas'] or abort(400)
    relatorio = Relatorio(vencedor, rodadas)
    db.session.add(relatorio)
    db.session.commit()
    return return_handler("Relatorio criado com sucesso!", {})

@app.route('/jogo/relatorio', methods=['GET'])
def relatorio_jogo():
    partidas = Relatorio.query.count()
    timeout = Relatorio.query.filter(Relatorio.rodadas > 1000).count()
    media_turnos = Relatorio.query.with_entities(func.avg(Relatorio.rodadas)).all()
    media_turnos = media_turnos[0][0]
    # comportamento
    perfis = [
        'impulsivo',
        'exigente',
        'cauteloso',
        'aleatório'
    ]
    vencedores = Relatorio.query.with_entities(Relatorio.vencedor, func.count(Relatorio.vencedor)).group_by(Relatorio.vencedor).all()
    comportamentos = [{ perfis[int(v[0])-1]: "{:.2f}".format(float(v[1]) / partidas * 100.0) } for v in vencedores]
    max_vencedor = max([( perfis[int(v[0])-1], int(v[1]) ) for v in vencedores], key=lambda x: x[1])
    return return_handler("Relatório de partidas", {
        'partidas_totais': partidas,
        'partidas_por_timeout': timeout,
        'media_turnos': media_turnos,
        'comportamentos': comportamentos,
        'comportamento_vencedor': max_vencedor[0]
    })