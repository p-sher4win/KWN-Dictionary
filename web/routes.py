from flask import Blueprint, render_template, flash, redirect, request, send_file, url_for
import requests
from .webforms import SearchWordForm
from .konk_models import *
from .mast_models import *
from . import db
from config import Config

# IMAGE GENERATION IMPORTS ⬇️ 
import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, DiffusionPipeline
from io import BytesIO


# MICROSOFT TRANSLATOR API CREDENTIALS
MS_TRANSLATOR_KEY = Config.MS_TRANSLATOR_KEY
MS_TRANSLATOR_ENDPOINT = Config.MS_TRANSLATOR_ENDPOINT
MS_TRANSLATOR_REGION = Config.MS_TRANSLATOR_REGION




# FUNCTIONS
# MS TRANSLATE FUNCTION
def translate_text(text, source_lang, target_lang):
    headers = {
        'Ocp-Apim-Subscription-Key': MS_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': MS_TRANSLATOR_REGION,
        'Content-type': 'application/json'
    }

    params = {
        'api-version': '3.0',
        'from': source_lang,
        'to': target_lang
    }

    body = [{'text': text}]

    request = requests.post(MS_TRANSLATOR_ENDPOINT, params=params, headers=headers, json=body)

    try:
        response = request.json()
        return response[0]['translations'][0]['text'] if response else text
    except requests.exceptions.JSONDecodeError:
        return "Translation Error: Invalid response from API"


# MS TRANSLATE KONK TO ENG FUNCTION
def ms_translate_konk_eng(text):
    return translate_text(text, 'gom', 'en')

# MS TRANSLATE KONK TO HINDI FUNCTION
def ms_translate_konk_hindi(text):
    return translate_text(text, 'gom', 'hi')

# MS TRANSLATE KONK TO MARATHI FUNCTION
def ms_translate_konk_marathi(text):
    return translate_text(text, 'gom', 'mr')


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

    if synset:
        semantic_synet =  MasterSemanticRelations.query.filter(MasterSemanticRelations.synset_id == synset_id).all()

        semantic_rel = (
            MasterSemanticRelations.query.join(MasterRelationTypes, MasterSemanticRelations.relation_id == MasterRelationTypes.relation_id).filter(MasterSemanticRelations.synset_id == synset.synset_id).all()
        )


        hyper = MasterRelHypernymyHyponymy.query.filter(MasterRelHypernymyHyponymy.parent_synset_id == synset_id).all()

        hyper_exm_ids = [hr.child_synset_id for hr in hyper]

        print(f"IDs: {hyper_exm_ids}")

        hyper_synonyms_id = KonkaniSynsetWords.query.join(KonkaniSynset, KonkaniSynsetWords.synset_id == hyper_exm_ids).filter(KonkaniWord.word_id == KonkaniSynsetWords.word_id).all()

        hyper_synonyms = []
        for synset in hyper_synonyms_id:
            # GET ALL WORDS IN THIS SYNSET
            words_in_synset = (
                KonkaniWord.query.join(KonkaniSynsetWords, KonkaniWord.word_id == KonkaniSynsetWords.word_id).filter(KonkaniSynsetWords.synset_id == synset.synset_id).order_by(KonkaniSynsetWords.word_order).all()
            )

            for w in words_in_synset:
                if w.word_id != hyper_exm_ids:
                    hyper_synonyms.append({
                        "id": w.word_id,
                        "word": w.word.replace("_", " "),
                        "sid": synset.synset_id,
                    })

        hyper_exm = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id.in_(hyper_exm_ids)).all()
        )



        hypo = MasterRelHypernymyHyponymy.query.filter(MasterRelHypernymyHyponymy.child_synset_id == synset_id).all()

        hypo_exm_ids = [hy.parent_synset_id for hy in hypo]

        # hypo_synonyms_id = KonkaniSynsetWords.query.join(KonkaniSynset, KonkaniSynsetWords.synset_id == hypo_exm_ids).filter(KonkaniWord.word_id == KonkaniSynsetWords.word_id).all()

        # hypo_synonyms = []
        # for synset in hypo_synonyms_id:
        #     # GET ALL WORDS IN THIS SYNSET
        #     words_in_synset = (
        #         KonkaniWord.query.join(KonkaniSynsetWords, KonkaniWord.word_id == KonkaniSynsetWords.word_id).filter(KonkaniSynsetWords.synset_id == synset.synset_id).order_by(KonkaniSynsetWords.word_order).all()
        #     )

        #     for w in words_in_synset:
        #         if w.word_id != hyper_exm_ids:
        #             hypo_synonyms.append({
        #                 "id": w.word_id,
        #                 "word": w.word.replace("_", " "),
        #                 "sid": synset.synset_id,
        #             })

        # hypo_synonyms = get_synonyms(hypo_exm_ids)

        hypo_exm = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id.in_(hypo_exm_ids)).all()
        )



        holo = MasterRelMeronymyHolonymy.query.filter(MasterRelMeronymyHolonymy.whole_synset_id == synset_id).all()

        holo_exm_ids = [hl.part_synset_id for hl in holo]

        # holo_synonyms_id = KonkaniSynsetWords.query.join(KonkaniSynset, KonkaniSynsetWords.synset_id == holo_exm_ids).filter(KonkaniWord.word_id == KonkaniSynsetWords.word_id).all()

        # holo_synonyms = []
        # for synset in holo_synonyms_id:
        #     # GET ALL WORDS IN THIS SYNSET
        #     words_in_synset = (
        #         KonkaniWord.query.join(KonkaniSynsetWords, KonkaniWord.word_id == KonkaniSynsetWords.word_id).filter(KonkaniSynsetWords.synset_id == synset.synset_id).order_by(KonkaniSynsetWords.word_order).all()
        #     )

        #     for w in words_in_synset:
        #         if w.word_id != hyper_exm_ids:
        #             holo_synonyms.append({
        #                 "id": w.word_id,
        #                 "word": w.word.replace("_", " "),
        #                 "sid": synset.synset_id,
        #             })

        # holo_synonyms = get_synonyms(holo_exm_ids)

        holo_exm = (
            KonkaniSynsetExample.query.filter(KonkaniSynsetExample.synset_id.in_(holo_exm_ids)).all()
        )



        mero = MasterRelMeronymyHolonymy.query.filter(MasterRelMeronymyHolonymy.part_synset_id == synset_id).all()

        mero_exm_ids = [mr.whole_synset_id for mr in mero]

        # mero_synonyms_id = KonkaniSynsetWords.query.join(KonkaniSynset, KonkaniSynsetWords.synset_id == mero_exm_ids).filter(KonkaniWord.word_id == KonkaniSynsetWords.word_id).all()

        # mero_synonyms = []
        # for synset in mero_synonyms_id:
        #     # GET ALL WORDS IN THIS SYNSET
        #     words_in_synset = (
        #         KonkaniWord.query.join(KonkaniSynsetWords, KonkaniWord.word_id == KonkaniSynsetWords.word_id).filter(KonkaniSynsetWords.synset_id == synset.synset_id).order_by(KonkaniSynsetWords.word_order).all()
        #     )

        #     for w in words_in_synset:
        #         if w.word_id != hyper_exm_ids:
        #             mero_synonyms.append({
        #                 "id": w.word_id,
        #                 "word": w.word.replace("_", " "),
        #                 "sid": synset.synset_id,
        #             })

        # mero_synonyms = get_synonyms(mero_exm_ids)

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
        "hyper_syn": [h for h in hyper_synonyms],
        # "hypo_syn": [h for h in hyper_synonyms],
        # "holo_syn": [h for h in holo_synonyms],
        # "mero_syn": [m for m in mero_synonyms],
        "hypo": [ho.get_parent_synset() for ho in hypo],
        "holo": [hl.get_part_synset() for hl in holo],
        "mero": [mr.get_whole_synset() for mr in mero]
    })

    return collection


# IMAGE GENERATION PROCESS
# LOAD MODEL
model_id = "stabilityai/stable-diffusion-2-1-base"
scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

# model_id = "DeepFloyd/IF-I-XL-v1.0"
# def load_image_model():
#     pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
#     return pipe.to("cuda")




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
        category = synset.get_category()
        definiton = synset.concept_definition
        example_sent = example.example_content

        word_info = {
            "word_id": word_day.word_id,
            "synset_id": synset.synset_id,
            "eid": example.synset_id,

            "word": word,
            "category": category,
            "concept_definition": definiton,
            "example": example_sent,

            "img_url": url_for('routes.generate_img', word_id=word_day.word_id, synset_id=this_synset_id)
        }

    return render_template('view/search.html',
                           form=form,
                           word_info=word_info)



# GENERATE IMAGE ROUTE
@routes.route('/generate_img/<int:word_id>/<int:synset_id>')
def generate_img(word_id, synset_id):

    konk_word = KonkaniWord.query.filter(KonkaniWord.word_id == word_id).first()
    konk_synset = KonkaniSynset.query.filter(KonkaniSynset.synset_id == synset_id).first()
    get_word = konk_word.word.replace("_", " ")
    get_context = konk_synset.concept_definition

    word = ms_translate_konk_eng(get_word)
    context = ms_translate_konk_eng(get_context)

    prompt = f"A realistic image of {word}"

    print(f"\nImage Prompt = {prompt}\n")

    img = pipe(prompt, height=512, width=512).images[0]

    # pipe = load_image_model()

    # img = pipe(prompt, height=384, width=384, guidance_scale=7.0, num_inference_steps=20).images[0]

    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png", as_attachment=False)


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
    category = synset.get_category()
    definiton = synset.concept_definition
    example_sent = example.example_content

    # GET WORD SYNONYMS
    synonyms = get_synonyms(word_id)

    # GET SEMANTIC RELATIONS
    relations = get_semantic_rel(synset_id)


    # TRANSLATE WORD DATA
    translated_eng_data = {
        "eng_word": ms_translate_konk_eng(word_text),
        "gloss": ms_translate_konk_eng(definiton),
        "usage": ms_translate_konk_eng(example_sent)
    }

    translated_hi_data = {
        "hindi_word": ms_translate_konk_hindi(word_text),
        "gloss": ms_translate_konk_hindi(definiton),
        "usage": ms_translate_konk_hindi(example_sent)
    }

    translated_mr_data = {
        "marathi_word": ms_translate_konk_marathi(word_text),
        "gloss": ms_translate_konk_marathi(definiton),
        "usage": ms_translate_konk_marathi(example_sent)
    }

    word_info = {
        "word": word_text,
        "category": category,
        "concept_definition": definiton,
        "example": example_sent,
        "img_url": url_for('routes.generate_img', word_id=word_id, synset_id=synset_id)
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
                           relations=relations)


# INTRODUCTION PAGE ROUTE
@routes.route('/introduction')
def introduction():

    return render_template('view/introduction.html')