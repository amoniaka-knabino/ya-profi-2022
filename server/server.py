from flask import jsonify, Flask, request
from db_module import (
    add_promo_to_db,
    get_promos_dict_list,
    get_promo_by_id,
    edit_promo,
    delete_promo,
    add_participant,
    delete_participant,
    add_prize,
    delete_prize,
    session_factory,
    can_ruffle,
    ruffle
)

app = Flask(__name__)


@app.route('/promo', methods=["GET", "POST"])
def promo():
    if request.method == "POST":
        session = session_factory()
        name = request.json.get('name')
        description = request.json.get('description')
        promo_id = add_promo_to_db(session, name, description)
        return jsonify(promo_id), 200
    if request.method == "GET":
        session = session_factory()
        promos = get_promos_dict_list(session)
        return jsonify(promos), 200

@app.route('/promo/<id>', methods=["GET", "PUT", "DELETE"])
def promo_by_id(id):
    assert id == request.view_args['id']
    session = session_factory()
    if request.method == "GET":
        promo = get_promo_by_id(session, id)
        return jsonify(promo), 200
    if request.method == "PUT":
        name = request.json.get('name')
        description = request.json.get('description')
        if not name:
            return "error", 400
        edit_promo(session, id, name, description)
        return "ok"
    if request.method == "DELETE":
        delete_promo(session, id)
        return "ok", 200

@app.route('/promo/<id>/participant', methods=["POST"])
def promo_by_id_participant(id):
    assert id == request.view_args['id']
    session = session_factory()
    name = request.json.get('name')
    if not name:
        return "error", 400
    p_id = add_participant(session, id, name)
    return jsonify(p_id), 200


@app.route('/promo/<promo_id>/participant/<part_id>', methods=["DELETE"])
def delete_participant_from_promo(promo_id, part_id):
    assert promo_id == request.view_args['promo_id']
    assert part_id == request.view_args['part_id']
    session = session_factory()
    delete_participant(session, part_id)
    return "ok", 200

@app.route('/promo/<id>/prize', methods=["POST"])
def promo_by_id_prize(id):
    assert id == request.view_args['id']
    session = session_factory()
    desc = request.json.get('description')
    if not desc:
        return "error", 400
    p_id = add_prize(session, id, desc)
    return jsonify(p_id), 200


@app.route('/promo/<promo_id>/participant/<prize_id>', methods=["DELETE"])
def delete_prize_from_promo(promo_id, prize_id):
    assert promo_id == request.view_args['promo_id']
    assert prize_id == request.view_args['prize_id']
    session = session_factory()
    delete_prize(session, prize_id)
    return "ok", 200


@app.route('/promo/<id>/ruffle', methods=["POST"])
def do_ruffle(id):
    assert id == request.view_args['id']
    session = session_factory()
    if not can_ruffle(session, id):
        return "conflict", 409
    return jsonify(ruffle(session, id)), 200


if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0')
