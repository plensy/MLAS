from mongoengine import Document, EmbeddedDocument, fields

# Create your models here

#datasource


class FileSource(EmbeddedDocument):
    libelle = fields.StringField(null=True, blank=True)
    lien = fields.StringField(null=True, blank=True)


class ModelGenerated(EmbeddedDocument):
    api = fields.StringField()
    precision = fields.FloatField()


class DataSource(Document):
    problematique = fields.StringField(required=False)
    DataOut = fields.StringField(null=True, blank=True)
    DataInt = fields.ListField(fields.StringField(null=True, blank=True))
    sourcesLink = fields.EmbeddedDocumentField(FileSource)
    ModelGenerated = fields.EmbeddedDocumentListField(ModelGenerated)

