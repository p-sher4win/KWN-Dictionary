from . import db


# WORDNET KONKANI DATABASE MODELS
# WN SOURCE MODEL
class KonkaniSource(db.Model):
    __bind_key__ = 'konkani'
    __tablename__ = 'wn_source'
    source_id = db.Column(db.Integer, primary_key=True)
    source_value = db.Column(db.String(255), index=True)
    synset_source = db.relationship('KonkaniSynset', backref='synset_source')


# WN SYNSET MODEL
class KonkaniSynset(db.Model):
    __bind_key__ = 'konkani'
    __tablename__ = 'wn_synset'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    concept_definition = db.Column(db.Text)
    category_id = db.Column(db.Integer, nullable=False, default=0)
    source_id = db.Column(db.Integer, db.ForeignKey('wn_source.source_id'), nullable=False, default=0)
    domain_id = db.Column(db.Integer, nullable=False, default=0)
    synset_words = db.relationship('KonkaniSynsetWords', backref='wn_synset_words')
    synset_examples = db.relationship('KonkaniSynsetExample', backref='synset_examples')


    def get_category(self):
            from .mast_models import MasterCategory
            category = MasterCategory.query.get(self.category_id)
            return {
                "category_id": category.category_id if category else None,
                "category_value": category.category_value if category else None,
            }

    def get_domain(self):
        from .mast_models import MasterDomain
        domain = MasterDomain.query.get(self.domain_id)
        return {
            "domain_id": domain.domain_id if domain else None,
            "domain_value": domain.domain_value if domain else None,
        }


# WN WORD MODEL
class KonkaniWord(db.Model):
    __bind_key__ = 'konkani'
    __tablename__ = 'wn_word'
    word_id = db.Column(db.BigInteger, primary_key=True)
    word = db.Column(db.String(255), index=True)
    synset_words = db.relationship('KonkaniSynsetWords', backref='synset_words')

    
# WN SYNSET WORDS MODEL
class KonkaniSynsetWords(db.Model):
    __bind_key__ = 'konkani'
    __tablename__ = 'wn_synset_words'
    synset_id = db.Column(db.BigInteger, db.ForeignKey('wn_synset.synset_id'), primary_key=True, default=0)
    word_id = db.Column(db.BigInteger, db.ForeignKey('wn_word.word_id'), primary_key=True, default=0)
    word_order = db.Column(db.Integer, nullable=False, index=True)


# WN SYNSET EXAMPLE MODEL
class KonkaniSynsetExample(db.Model):
    __bind_key__ = 'konkani'
    __tablename__ = 'wn_synset_example'
    synset_id = db.Column(db.BigInteger, db.ForeignKey('wn_synset.synset_id'), primary_key=True, index=True)
    example_content = db.Column(db.Text)
    example_order = db.Column(db.Integer, primary_key=True, index=True)