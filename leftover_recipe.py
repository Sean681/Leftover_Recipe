import pandas as pd
import pymysql
import pymongo


def leftoverRecipe(leftover):
    # SQL settings
    db_settings = {
        'host': 'IP',
        'port': "port",
        'user': 'YOUR_USERNAME',
        'password': 'YOUR_PASSWORD',
        'db': 'YOUR_DATABASE'
    }
    # 連接到 MySQL
    conn = pymysql.connect(**db_settings)
    # 讀取 view_recipe_energe
    get_energe = f"SELECT * FROM view_recipe_energe;"
    energe = pd.read_sql(get_energe, conn)
    # 從 view_recipe_energe 取出 recipe 的 id
    cache_id = energe.iloc[:, 0].to_list()
    # 讀取 recipe_to_sql
    get_recipe = f"SELECT * FROM recipe_to_sql;"
    recipes = pd.read_sql(get_recipe, conn)
    # 連接到 MongoDB
    mongo_info = "YOUR_CONNECTION_STRING"
    client = pymongo.MongoClient(mongo_info)
    # MongoDB database
    db = client.food
    # MongoDB collection
    monrecipe = db.recipe

    outputs = list()
    rec_outputs = list()
    for i in cache_id:
        recipe = recipes.loc[recipes["id"] == i]
        mates = recipe["material"].to_list()
        quants = recipe["quantity"].to_list()
        # 若包含該食譜所有食材
        if all(m in leftover[0] for m in mates):
            # materials of the recipe
            need = [_ for _ in leftover[0] if _ in mates]
            for ingred in need:
                q = float(leftover[1][leftover[0].index(ingred)].strip("g"))
                # if inputs has sufficient quantity of the material
                if q >= quants[mates.index(ingred)] and i not in rec_outputs:
                    rec_outputs.append(i)
                    # get recipe info from MongoDB
                    mongoData = monrecipe.find_one({'id': str(i)},
                                                   {'id': 0, '_id': 0, '料理時間': 0, '簡介': 0, '作者': 0})
                    output = [v for k, v in mongoData.items()]
                    # get recipe_energe info from view_recipe_energe
                    recipe_energe = energe.loc[energe["id"] == i].drop(["id"], axis=1).to_dict("records")[0]
                    output.append(recipe_energe)
                    outputs.append(output)
    return outputs

if __name__ == "__main__":
    leftover = [['toast', 'egg', 'cucumber', 'tomato sauce', 'sheep flank hot pot slices'],
                ['25g', '55g', '100g', '5g', '405g']]

    print(leftoverRecipe(leftover))