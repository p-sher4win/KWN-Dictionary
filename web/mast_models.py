from . import db

# WORDNET MASTER DATABASE MODELS
# MASTER CATEGORY MODEL
class MasterCategory(db.Model):
    __tablename__ = 'wn_master_category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_pid = db.Column(db.Integer, db.ForeignKey('wn_master_category.category_id'), default=0)
    category_value = db.Column(db.String(255))
    parent = db.relationship('MasterCategory',
                             remote_side=[category_id],
                             backref='subcategory')


# MASTER LANGUAGE MODEL
class MasterLanguage(db.Model):
    __tablename__ = 'wn_master_language'
    language_id = db.Column(db.Integer, primary_key=True)
    language_name = db.Column(db.String(255))
    language_desc = db.Column(db.Text)
    language_script = db.Column(db.String(255))
    language_direction = db.Column(db.String(3), nullable=False, default='LTR')
    iso_code_char2 = db.Column(db.String(2))
    iso_code_char3 = db.Column(db.String(3))
    keyboard_xml_filename = db.Column(db.String(255), nullable=False)
    database_name = db.Column(db.String(255))
    language = db.relationship('MasterLanguageLSSRange', backref='lss_ranges')


# MASTER LANGUAGE LSS RANGE MODEL
class MasterLanguageLSSRange(db.Model):
    __tablename__ = 'wn_master_language_lss_range'
    language_id = db.Column(db.Integer, db.ForeignKey('wn_master_language.language_id'), primary_key=True)
    start_range_id = db.Column(db.BigInteger, primary_key=True, default=0)
    end_range_id = db.Column(db.BigInteger, primary_key=True, default=0)


# MASTER DOMAIN MODEL
class MasterDomain(db.Model):
    __tablename__ = 'wn_master_domain'
    domain_id = db.Column(db.Integer, primary_key=True)
    domain_value = db.Column(db.String(255), index=True)
    

# MASTER PROPERTY ANTONYMY GRADATION MODEL
class MasterPropertyAntonymyGradation(db.Model):
    __tablename__ = 'wn_master_property_antonymy_gradation'
    anto_grad_property_id = db.Column(db.Integer, primary_key=True)
    anto_grad_property_value = db.Column(db.String(255))


# MASTER PROPERTY MERONYMY HOLONYMY MODEL
class MasterPropertyMeronymyHolonymy(db.Model):
    __tablename__ = 'wn_master_property_meronymy_holonymy'
    mero_holo_property_id = db.Column(db.Integer, primary_key=True)
    mero_holo_property_value = db.Column(db.String(255))
    mero_holo_rel = db.relationship('MasterRelMeronymyHolonymy', backref='mero_holo_rel') 


# MASTER PROPERTY LINK TYPE MODEL
class MasterPropertyLinkType(db.Model):
    __tablename__ = 'wn_master_property_link_type'
    link_id = db.Column(db.Integer, primary_key=True)
    link_type = db.Column(db.String(255))
    noun_verb_link = db.relationship('MasterRelNounVerbLink', backref='noun_verb_link')


# MASTER RELATION TYPES MODEL
class MasterRelationTypes(db.Model):
    __tablename__ = 'wn_master_relation_types'
    relation_id = db.Column(db.Integer, primary_key=True)
    rel_description = db.Column(db.String(255))
    table_name = db.Column(db.String(255))
    table_from_column = db.Column(db.String(255))
    relation = db.relationship('MasterSemanticRelations', backref='relation')


# MASTER MEMBERSHIP MODEL
class MasterMembership(db.Model):
    __tablename__ = 'wn_master_membership'
    member_id = db.Column(db.Integer, primary_key=True)
    member_type = db.Column(db.Text, nullable=False)
    memberhip = db.relationship('MasterSynsetMembership', backref='memberhip')


# MASTER SYNSET MEMBERSHIP MODEL
class MasterSynsetMembership(db.Model):
    __tablename__ = 'wn_master_synset_membership'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey('wn_master_membership.member_id'), primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER SEMANTIC RELATIONS MODEL
class MasterSemanticRelations(db.Model):
    __tablename__ = 'wn_master_semantic_relations'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    relation_id = db.Column(db.Integer, db.ForeignKey('wn_master_relation_types.relation_id'), primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL HYPERNYMY HYPONYMY MODEL
class MasterRelHypernymyHyponymy(db.Model):
    __tablename__ = 'wn_master_rel_hypernymy_hyponymy'
    parent_synset_id = db.Column(db.BigInteger, primary_key=True)
    child_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_parent_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.parent_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_child_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.child_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL MERONYMY HOLONYMY MODEL
class MasterRelMeronymyHolonymy(db.Model):
    __tablename__ = 'wn_master_rel_meronymy_holonymy'
    whole_synset_id = db.Column(db.BigInteger, primary_key=True)
    part_synset_id = db.Column(db.BigInteger, primary_key=True)
    mero_holo_property_id = db.Column(db.Integer, db.ForeignKey('wn_master_property_meronymy_holonymy.mero_holo_property_id'), nullable=False)

    def get_whole_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.whole_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_part_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.part_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL TROPONYMY MODEL
class MasterRelTroponymy(db.Model):
    __tablename__ = 'wn_master_rel_troponymy'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    troponym_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_troponymy_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.troponym_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL ENTAILMENT MODEL
class MasterRelEntailment(db.Model):
    __tablename__ = 'wn_master_rel_entailment'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    entailed_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_entailed_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.entailed_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL SIMILAR MODEL
class MasterRelSimilar(db.Model):
    __tablename__ = 'wn_master_rel_similar'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    similar_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_similar_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.similar_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL ALSO SEE MODEL
class MasterRelAlsoSee(db.Model):
    __tablename__ = 'wn_master_rel_also_see'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    also_see_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_also_see_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.also_see_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL NOUN VERB LINK MODEL
class MasterRelNounVerbLink(db.Model):
    __tablename__ = 'wn_master_rel_noun_verb_link'
    noun_synset_id = db.Column(db.BigInteger, primary_key=True)
    verb_synset_id = db.Column(db.BigInteger, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('wn_master_property_link_type.link_id'), nullable=False)

    def get_noun_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.noun_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_verb_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.verb_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL NOUN ADJECTIVE ATTRIBUTE LINK MODEL
class MasterRelNounAdjectiveAttributeLink(db.Model):
    __tablename__ = 'wn_master_rel_noun_adjective_attribute_link'
    noun_synset_id = db.Column(db.BigInteger, primary_key=True)
    adjective_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_noun_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.noun_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_adjective_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.adjective_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL ADJECTIVE MODIFIES NOUN MODEL
class MasterRelAdjectiveModifiesNoun(db.Model):
    __tablename__ = 'wn_master_rel_adjective_modifies_noun'
    adjective_synset_id = db.Column(db.BigInteger, primary_key=True)
    noun_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_adjective_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.adjective_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_noun_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.noun_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL ADVERB MODIFIES VERB MODEL
class MasterRelAdverbModifiesVerb(db.Model):
    __tablename__ = 'wn_master_rel_adverb_modifies_verb'
    adverb_synset_id = db.Column(db.BigInteger, primary_key=True)
    verb_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_adverb_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.adverb_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_verb_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.verb_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL CAUSATIVE MODEL
class MasterRelCausative(db.Model):
    __tablename__ = 'wn_master_rel_causative'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    causes_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_causes_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.causes_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER REL NEAR SYNSETS MODEL
class MasterRelNearSynsets(db.Model):
    __tablename__ = 'wn_master_rel_near_synsets'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    near_synset_id = db.Column(db.BigInteger, primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }
    
    def get_near_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.near_synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }


# MASTER ONTOLOGY NODES MODEL
class MasterOntologyNodes(db.Model):
    __tablename__ = 'wn_master_ontology_nodes'
    onto_id = db.Column(db.Integer, primary_key=True)
    onto_data = db.Column(db.String(255))
    onto_desc = db.Column(db.Text)
    tree_parent = db.relationship('MasterOntologyTree', foreign_keys='MasterOntologyTree.parent_id', backref='tree_parent')
    tree_child = db.relationship('MasterOntologyTree', foreign_keys='MasterOntologyTree.child_id', backref='tree_child')
    synset_map = db.relationship('MasterOntologySynsetMap', backref='synset_map')


# MASTER ONTOLOGY TREE MODEL
class MasterOntologyTree(db.Model):
    __tablename__ = 'wn_master_ontology_tree'
    parent_id = db.Column(db.Integer, db.ForeignKey('wn_master_ontology_nodes.onto_id'), primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('wn_master_ontology_nodes.onto_id'), primary_key=True)
    

# MASTER ONTOLOGY SYNSET MAP MODEL
class MasterOntologySynsetMap(db.Model):
    __tablename__ = 'wn_master_ontology_synset_map'
    synset_id = db.Column(db.BigInteger, primary_key=True)
    onto_nodes_id = db.Column(db.Integer, db.ForeignKey('wn_master_ontology_nodes.onto_id'), primary_key=True)

    def get_synset(self):
        from .konk_models import KonkaniSynset
        synset = KonkaniSynset.query.get(self.synset_id)
        return {
            "synset_id": synset.synset_id if synset else None,
            "concept_definition": synset.concept_definition if synset else None,
            "category_id": synset.category_id if synset else None,
            "source_id": synset.source_id if synset else None,
            "domain_id": synset.domain_id if synset else None,
        }