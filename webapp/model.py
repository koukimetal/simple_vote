from mongoengine import *

connect('simple_vote', host='db')


class Item(Document):
    name = StringField()
    point = IntField()


class Vote(Document):
    name = StringField()
    items = ListField(ReferenceField(Item))