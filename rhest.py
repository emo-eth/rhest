from flask import Flask, jsonify, request, abort
from Phyme import Phyme
from PyRoget import PyRoget
app = Flask(__name__)

ph = Phyme()
ro = PyRoget()

RHYME_TYPE_MAP = {
    'additive': ph.get_additive_rhymes,
    'subtractive': ph.get_subtractive_rhymes,
    'substitution': ph.get_substitution_rhymes,
    'partner': ph.get_partner_rhymes,
    'family': ph.get_family_rhymes,
    'assonance': ph.get_assonance_rhymes,
    'consonant': ph.get_consonant_rhymes,
    'perfect': ph.get_perfect_rhymes
}


@app.route('/rhyme')
def rhyme():
    word = request.args.get('word')
    kind = request.args.get('kind')
    method = RHYME_TYPE_MAP.get(kind, ph.get_perfect_rhymes)
    try:
        return jsonify(method(word))
    except KeyError:
        if word:
            return abort(404)
    return abort(500)


@app.route('/categorize')
def categorize():
    word = request.args.get('word')
    try:
        return jsonify(ro.categorize_word(word))
    except KeyError:
        if word:
            return abort(404)
    return abort(500)


@app.route('/category/<category>')
def get_category_words(category):
    try:
        return jsonify(ro.get_words(category))
    except KeyError:
        if category:
            return abort(404)
    return abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2468)
