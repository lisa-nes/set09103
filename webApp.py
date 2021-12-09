"""DATABASE"""
from flask import Flask, g, render_template, url_for, request, redirect
import sqlite3
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER']="static/img"



db_location = 'var/sqlite.db'


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipe/new')
def addRecipe1():
    return render_template('add_recipe1.html')



@app.route('/recipe/new/cooking', methods=('GET', 'POST'))
def addRecipe2():
    if request.method == 'POST':
        titleRecipe = request.form['titleRecipe']
       # imageRecipe = request.form['imageRecipe']
        category1 = request.form.get('category1')
        category2 = request.form.get('category2')
        category3 = request.form.get('category3')
        category4 = request.form.get('category4')
        category5 = request.form.get('category5')
        description = request.form['description']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        recipeImage=request.files['imageRecipe']

        if recipeImage.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], recipeImage.filename)
            recipeImage.save(filepath)

        #with open(imageRecipe, 'rb') as file:
         #   blobData = file.read()
        
        db = get_db()
        cursor = db.cursor()

        cursor.execute('INSERT INTO recipe (title, description, ingredients, instructions, image) VALUES (?,?,?,?,?)', (titleRecipe, description, ingredients, instructions, recipeImage.filename,))
        db.commit()

        recipeId = cursor.lastrowid


      # recipeId = db.cursor().execute ('SELECT last_insert_rowid()')
        if category1 == "on": 
            cursor.execute('INSERT INTO recipeDiet (recipeId, dietId) VALUES (?,?)', (recipeId, '1'))
            db.commit()

        if category2 == "on":
            cursor.execute('INSERT INTO recipeDiet (recipeId, dietId) VALUES (?,?)', (recipeId, '2'))
            db.commit()


        if category3 == "on":
            cursor.execute('INSERT INTO recipeDiet (recipeId, dietId) VALUES (?,?)', (recipeId, '3'))
            db.commit()

        
        if category4 == "on":
            cursor.execute('INSERT INTO recipeDiet (recipeId, dietId) VALUES (?,?)', (recipeId, '4'))
            db.commit()


        if category5 == "on":
            cursor.execute('INSERT INTO recipeDiet (recipeId, dietId) VALUES (?,?)', (recipeId, '5'))
            db.commit()


        db.commit()
       # db.close()
        return redirect(url_for('showRecipe', recipeCategory='cooking', recipeId=recipeId, recipeName=titleRecipe))

        

    return render_template('add_recipe2.html')

@app.route('/recipe/new/baking')
def addRecipe3():
    return render_template('add_recipe3.html')


@app.route('/recipes/cooking')
def showCookingRecipes():
    return render_template('recipe_boxes_overview.html')

@app.route('/recipes/cooking/sweet')
def showCookingRecipesSweet():
    return render_template('recipe_boxes_overview.html')
@app.route('/recipes/cooking/savoury')
def showCookingRecipesSavoury():
    return render_template('recipe_boxes_overview.html')
@app.route('/recipes/cooking/gluten-free')
def showCookingRecipesGlutenfree():
    return render_template('recipe_boxes_overview.html')
@app.route('/recipes/cooking/vegan')
def showCookingRecipesVegan():
    return render_template('recipe_boxes_overview.html')
@app.route('/recipes/cooking/vegetarian')
def showCookingRecipesVegetarian():
    return render_template('recipe_boxes_overview.html')



@app.route('/recipes/baking')
def showBakingRecipes():
    return render_template('recipe_boxes_overview.html')

@app.route('/recipes/baking/savoury')
def showBakingRecipesSavoury():
    return render_template('recipe_boxes_overview.html')
@app.route('/recipes/baking/sweet')
def showBakingRecipesSweet():
    return render_template('recipe_boxes_overview.html')
@app.route('/recipes/baking/gluten-free')
def showBakingRecipesGlutenfree():
    return render_template('recipe_boxes_overview.html')



@app.route('/recipes/<recipeCategory>/<recipeId>/<recipeName>', methods=['POST','GET'])
def showRecipe(recipeCategory,recipeId,recipeName):

    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
   # sql = 'SELECT * FROM recipe WHERE recipeId=?'
   # recipe = cursor.execute(sql, [recipeId]).fetchall()
    
    recipe = cursor.execute('SELECT * FROM recipe WHERE recipeId=?', (recipeId,)).fetchone()

    if request.method == 'POST':
        name = request.form['username']
        comment = request.form['commenttext']

        "conn = get_db_connection()" 
        cursor.execute('INSERT INTO comment (comment,name) VALUES (?,?)',(comment, name)) 
        db.commit()
        db.close()
    return render_template('single_comment.html', recipe=recipe)


@app.route('/have-tried')
def haveTried():
    return render_template('wtt_recipe_box.html')


@app.route('/want-to-try')
def wantToTry():
    return render_template('wtt_recipe_box.html')








if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


