import sqlite3
from sqlite3.dbapi2 import Connection, Cursor
from flask_restful import Resource, reqparse
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


class Item(Resource):

    # @jwt_required()
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank!"
        
    )

    parser.add_argument('store_id',
        type = int,
        required = True,
        help = "Every item needs a store id."
        
    )

    def get(self, name):

        item = ItemModel.find_by_name(name)

        if item:

            return item.json()

        return {'message': 'Item not found'}, 404


    @classmethod

    def find_by_name(cls, name):

        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name = ?"

        result = cursor.execute(query, (name,))

        row = result.fetchone()

        connection.close()

        if row:

            return {'item': {'name': row[0], 'price':row[1]}}



    def post(self, name):

        if Item.find_by_name(name):

            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])  

        try:

            item.save_to_db()

        except:

            return {"message": "An error occurred in serting the item"}, 500  # Internal Server Error

        return item, 201


    @classmethod

    def insert(cls, item):

        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"

        cursor.execute(query, (item['name'], item['price']))

        connection.commit()

        connection.close()


    def delete(self, name):

        # item = Item.find_by_name(name)

        # if item:

        #     item.delete_from_db()

        # return {'message': 'Item deleted'}



        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name = ?"

        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}


    
    def put(self, name):

        # parser = reqparse.RequestParser()

        # parser.add_argument('price',
        #     type = float,
        #     required = True  ,
        #     help = "This field cannot be left blank!"
        
        # )

        data = Item.parser.parse_args()
        
        item = Item.find_by_name(name)

        # updated_item = {'name':name, 'price': data['price']}

        if not item:

            item = ItemModel(name, data['price'], data['store_id'])

        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()



            # try:
            #     Item.insert(updated_item)

            # except:
            #     return {"message": "An error occurred inserting the item."}, 500

        # else:

        #     try:
        #         Item.update(updated_item)

        #     except:
        #         return {"message": "An error occurred inserting the item."}, 500

        # return updated_item


    @classmethod
    def update(cls, item):

        connection = sqlite3.connect('data.db')

        cursor = connection.cursor()

        query = "UPDATE items SET price = ? WHERE name = ?"

        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()



    
class ItemList(Resource):

    def get(self):

        return {'items': [item.json() for item in ItemModel.query.all()]}   # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}

        # connection = sqlite3.connect('data.db')

        # cursor = connection.cursor()

        # query = "SELECT * FROM items"
        # result = cursor.execute(query)

        # items = []

        # for row in result:

        #     items.append({'name': row[0], 'price':row[1]})

        # connection.close()

        # return {'items': items}