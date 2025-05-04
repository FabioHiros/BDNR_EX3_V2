from dbConnection import RedisConnection, connect_db
from redisRepository.redisRepo import RedisRepository
from bson import ObjectId
import json

class Synchronize():
    def __init__(self):
        self.__redis_db = RedisRepository(RedisConnection().connect())
        self.__mongo_db = connect_db()

    def sync(self):
   
        productKeys = self.__redis_db.getKeys('product:*')
        print(productKeys)
        for key in productKeys:
            product = json.loads(self.__redis_db.getOne(key))
            # print(product)
            
            self.__mongo_db.produtos.update_one(
                {"_id": ObjectId(key.replace('product:',''))}, 
                {"$set": product}
            )
            
            self.__mongo_db.usuarios.update_one(
                {"_id": ObjectId(product.get("idVendedor")), "products.id": key.replace('product:','')},
                {
                    "$set": {
                        "products.$.nome": product.get("nome"),
                        "products.$.valor": product.get("valor"),
                        "products.$.estoque": product.get("estoque")
                    }
                }
            )

            self.__mongo_db.usuarios.update_many(
                {"favorites.id": key.replace('product:','')},
                {
                    "$set": {
                        "favorites.$.nome": product.get("nome"),
                        "favorites.$.valor": product.get("valor"),
                        "favorites.$.estoque": product.get("estoque")
                    }
                }
            )
            self.__redis_db.deleteOne([key])
        

        favoriteKeys = self.__redis_db.getKeys('user:*:favorites')
        for key in favoriteKeys:
         
            user_id = key.decode('utf-8').split(':')[1] if isinstance(key, bytes) else key.split(':')[1]
            
            
            favorites_json = self.__redis_db.getOne(key)
            if not favorites_json:
                continue
                
          
            new_favorites = json.loads(favorites_json)
            
           
            user = self.__mongo_db.usuarios.find_one({"_id": ObjectId(user_id)})
            if not user:
                continue
                
           
            existing_favorites = user.get("favorites", [])
            
       
            existing_product_ids = {fav.get("id") for fav in existing_favorites}
            
           
            for new_fav in new_favorites:
                if new_fav.get("id") not in existing_product_ids:
                    existing_favorites.append(new_fav)
                    existing_product_ids.add(new_fav.get("id"))
            
           
            self.__mongo_db.usuarios.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"favorites": existing_favorites}}
            )
         
            self.__redis_db.deleteOne([key])
            
        print("Sincronização concluída com sucesso!")
        return True