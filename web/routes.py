from flask import Blueprint, render_template, flash, redirect,url_for
from . import db
from .mast_models import *
from .webforms import SearchWordForm
from googletrans import Translator
import requests
from config import Config


# UNOFFICIAL GOOGLE TRANSLATE INSTANCE
translator = Translator()

# GOOGLE TRANSLATE FUNCTION (UNOFFICIAL)
def translate_text(text, target_lang):
    try:
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        print("Translation error:", e)
        return text

def translate_to_english(text):
    try:
        result = translator.translate(text, dest="en")
        return result.text
    except Exception as e:
        print("Translation error:", e)
        return text


# IMAGE GENERATION
PIXAZO_API_KEY = Config.PIXAZO_API_KEY

def generate_image_from_prompt(prompt, negative_prompt=None, width=1024, height=1024, num_steps=20, guidance_scale=5, seed=None):
    url = "https://gateway.pixazo.ai/getImage/v1/getSDXLImage"
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
        "Ocp-Apim-Subscription-Key": PIXAZO_API_KEY
    }
    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt or "",
        "width": width,
        "height": height,
        "num_steps": num_steps,
        "guidance_scale": guidance_scale
    }
    if seed is not None:
        payload["seed"] = seed

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("imageUrl")
    
    except Exception as e:
        print("Pixazo API error:", e)


# GET SYNONYMS OF A WORD
def get_synonyms(word_id):

    synonyms = []

    # GET ALL SYNSETS FOR THE WORD
    synsets = (
        KonkaniSynset.query.join(KonkaniSynsetWords, KonkaniSynset.synset_id == KonkaniSynsetWords.synset_id).filter(KonkaniSynsetWords.word_id == word_id).all()
        )
    
    for synset in synsets:
        # GET ALL WORDS IN THIS SYNSET
        words_in_synset = (
            KonkaniWord.query.join(KonkaniSynsetWords, KonkaniWord.word_id == KonkaniSynsetWords.word_id).filter(KonkaniSynsetWords.synset_id == synset.synset_id).order_by(KonkaniSynsetWords.word_order).all()
        )

        for w in words_in_synset:
            if w.word_id != word_id:
                synonyms.append({
                    "id": w.word_id,
                    "word": w.word.replace("_", " "),
                    "sid": synset.synset_id,
                    "concept": synset.concept_definition
                })

    return synonyms


# GET SEMANTIC RELATIONS FOR A WORD
def get_semantic_rel(synset_id):

    collection = []

    synset = KonkaniSynset.query.get_or_404(synset_id)

    def get_words_by_synset(synset_id):
        words = (
            KonkaniWord.query
            .join(KonkaniSynsetWords)
            .filter(KonkaniSynsetWords.synset_id == synset_id)
            .order_by(KonkaniSynsetWords.word_order)
            .all()
        )
        return [w.word.replace("_", " ") for w in words]

    if synset:
        semantic_synet =  MasterSemanticRelations.query.filter(MasterSemanticRelations.synset_id == synset_id).all()

        semantic_rel = (
            MasterSemanticRelations.query.join(MasterRelationTypes, MasterSemanticRelations.relation_id == MasterRelationTypes.relation_id).filter(MasterSemanticRelations.synset_id == synset.synset_id).all()
        )

        # GET HYPERNYMY DATA
        hyper = MasterRelHypernymyHyponymy.query.filter(MasterRelHypernymyHyponymy.parent_synset_id == synset_id).all()

        hyper_exm_ids = [hr.child_synset_id for hr in hyper]

        hyper_synonyms = []

        for hr in hyper:
            child_synset_id = hr.child_synset_id

            hyper_synonyms.append({
                "synset_id": child_synset_id,
                "words": get_words_by_synset(child_synset_id)
            })


        hyper_exm = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id.in_(hyper_exm_ids)).all()
        )

        # GET HYPONYMY DATA
        hypo = MasterRelHypernymyHyponymy.query.filter(MasterRelHypernymyHyponymy.child_synset_id == synset_id).all()

        hypo_exm_ids = [hy.parent_synset_id for hy in hypo]

        hypo_synonyms = []

        for hy in hypo:
            parent_synset_id = hy.parent_synset_id

            hypo_synonyms.append({
                "synset_id": parent_synset_id,
                "words": get_words_by_synset(parent_synset_id)
            })


        hypo_exm = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id.in_(hypo_exm_ids)).all()
        )

        # GET HOLONYMY DATA
        holo = MasterRelMeronymyHolonymy.query.filter(MasterRelMeronymyHolonymy.whole_synset_id == synset_id).all()

        holo_exm_ids = [hl.part_synset_id for hl in holo]

        holo_synonyms = []

        for hl in holo:
            part_synset_id = hl.part_synset_id

            holo_synonyms.append({
                "synset_id": part_synset_id,
                "words": get_words_by_synset(part_synset_id)
            })

        holo_exm = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id.in_(holo_exm_ids)).all()
        )

        # GET MERONYMY DATA
        mero = MasterRelMeronymyHolonymy.query.filter(MasterRelMeronymyHolonymy.part_synset_id == synset_id).all()

        mero_exm_ids = [mr.whole_synset_id for mr in mero]

        mero_synonyms = []

        for mr in mero:
            whole_synset_id = mr.whole_synset_id

            holo_synonyms.append({
                "synset_id": whole_synset_id,
                "words": get_words_by_synset(whole_synset_id)
            })

        mero_exm = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id.in_(mero_exm_ids)).all()
        )

    
    collection.append ({
        "synset_id": synset.synset_id,
        "relation": [sem.get_synset() for sem in semantic_synet],
        "semantic": [rel.relation for rel in semantic_rel],
        "hyper": [hr.get_child_synset() for hr in hyper],
        "hyper_exm": hyper_exm,
        "hypo_exm": hypo_exm,
        "holo_exm": holo_exm,
        "mero_exm": mero_exm,
        "hyper_syn": hyper_synonyms,
        "hypo_syn": hypo_synonyms,
        "holo_syn": holo_synonyms,
        "mero_syn": mero_synonyms,
        "hypo": [ho.get_parent_synset() for ho in hypo],
        "holo": [hl.get_part_synset() for hl in holo],
        "mero": [mr.get_whole_synset() for mr in mero]
    })

    return collection


# WEBSITE ROUTES
routes = Blueprint('routes', __name__)


# HOME PAGE ROUTE
@routes.route('/')
def home():
    form = SearchWordForm()

    konk_count = KonkaniWord.query.count()

    noun_count = KonkaniSynset.query.filter(KonkaniSynset.category_id == 1 ).count()
    verb_count = KonkaniSynset.query.filter(KonkaniSynset.category_id == 2 ).count()
    adjective_count = KonkaniSynset.query.filter(KonkaniSynset.category_id == 3 ).count()
    adverb_count = KonkaniSynset.query.filter(KonkaniSynset.category_id == 4 ).count()

    return render_template('view/home.html',
                           form=form,
                           konk_count=konk_count,
                           noun_count=noun_count,
                           verb_count=verb_count,
                           adjective_count=adjective_count,
                           adverb_count=adverb_count)


# SEARCH WORD ROUTE
@routes.route('/search_word', methods=['POST'])
def search():
    form = SearchWordForm()
    konkani = KonkaniWord.query

    if form.validate_on_submit():
        search = form.search_for.data

        word = konkani.filter(KonkaniWord.word == search)
        word = word.order_by(KonkaniWord.word).first()

        synsets = (
            KonkaniSynset.query.join(KonkaniSynsetWords, KonkaniSynset.synset_id == KonkaniSynsetWords.synset_id).filter(KonkaniSynsetWords.word_id == word.word_id).all()
        )

        s_count = len(synsets)

        return render_template('view/search_result.html',
                               form=form,
                               search=search,
                               word=word,
                               synsets=synsets,
                               count=s_count)
    
    else:
        flash("Search cannot be empty!", category='error')
        return redirect(url_for('routes.dictionary'))


# SEARCH PAGE ROUTE
@routes.route('/search')
def dictionary():
    form = SearchWordForm()
    # word_day = KonkaniWord.query.order_by(db.func.rand()).first()
    word_day = KonkaniWord.query.get_or_404(4826)

    word_info = None
    if word_day:
        synset = (
            KonkaniSynset.query.join(KonkaniSynsetWords, KonkaniSynset.synset_id == KonkaniSynsetWords.synset_id).filter(KonkaniSynsetWords.word_id == word_day.word_id).first()
        )

        this_synset_id = synset.synset_id

        example = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id == this_synset_id).order_by(KonkaniSynsetExample.example_order).first()
        )

        word = word_day.word.replace("_", " ")
        category = synset.category
        definiton = synset.concept_definition
        example_sent = example.example_content

        word_info = {
            "word_id": word_day.word_id,
            "synset_id": synset.synset_id,
            "eid": example.synset_id,

            "word": word,
            "category": category,
            "concept_definition": definiton,
            "example": example_sent
        }

    return render_template('view/search.html',
                           form=form,
                           word_info=word_info)


# GENERATE IMAGE ROUTE
@routes.route('/generate_img/<int:word_id>')
def generate_img(word_id):
    konk_word = KonkaniWord.query.get_or_404(word_id)
    word_konk = konk_word.word.replace("_", " ")
    word_eng = translate_to_english(word_konk)
    
    prompt = f"A high-resolution, realistic photograph of {word_eng} on a plain white background. The {word_eng} should be centered, clearly visible, in natural colors and proportions, well-lit, with sharp focus and no additional objects, text, or people in the image. The style should be photorealistic, studio lighting, no blur, no abstract or cartoonish elements."
    negative_prompt = "blurry, low-resolution, abstract, cartoonish, text, extra objects, people, animals, dark lighting, distorted proportions"
    
    image_url = generate_image_from_prompt(prompt, negative_prompt=negative_prompt)
    print("Image URL:", image_url)

    if image_url:
        return redirect(image_url)
    else:
        return "Pixazo API error", 500


# PARTICULAR WORD DATA PAGE ROUTE
@routes.route('/word/<int:word_id>/<int:synset_id>')
def get_word(word_id, synset_id):

    word = KonkaniWord.query.get_or_404(word_id)

    if word:
        synset = (
                KonkaniSynset.query.filter(KonkaniSynset.synset_id == synset_id).first()
            )
        
        example = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id == synset_id).order_by(KonkaniSynsetExample.example_order).first()
        )

    word_text = word.word.replace("_", " ")
    category = synset.category
    definiton = synset.concept_definition
    example_sent = example.example_content

    # GET WORD SYNONYMS
    synonyms = get_synonyms(word_id)

    # GET SEMANTIC RELATIONS
    relations = get_semantic_rel(synset_id)

    # TRANSLATE WORD DATA
    translated_eng_data = {
        "eng_word": translate_text(word_text, "en"),
        "gloss": translate_text(definiton, "en"),
        "usage": translate_text(example_sent, "en")
    }

    translated_hi_data = {
        "hindi_word": translate_text(word_text, "hi"),
        "gloss": translate_text(definiton, "hi"),
        "usage": translate_text(example_sent, "hi")
    }

    translated_mr_data = {
        "marathi_word": translate_text(word_text, "mr"),
        "gloss": translate_text(definiton, "mr"),
        "usage": translate_text(example_sent, "mr")
    }

    word_info = {
        "word": word_text,
        "category": category,
        "concept_definition": definiton,
        "example": example_sent
    }

    return render_template('view/word.html',
                           word=word.word_id,
                           synset=synset.synset_id,
                           example=example.synset_id,
                           word_data=word_info,
                           eng_data=translated_eng_data,
                           hindi_data=translated_hi_data,
                           marathi_data=translated_mr_data,
                           synonyms=synonyms,
                           relations=relations
                        )


# INTRODUCTION PAGE ROUTE
@routes.route('/introduction')
def introduction():

    return render_template('view/introduction.html')