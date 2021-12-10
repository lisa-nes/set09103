"""DATABASE"""
from flask import Flask, g, render_template, url_for, request, redirect
import sqlite3
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER']="static/img"



db_location = 'var/recipes2.db'


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


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404_page.html')

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
        recipetype = request.form['type']


        recipeImage=request.files['imageRecipe']

        if recipeImage.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], recipeImage.filename)
            recipeImage.save(filepath)

        #with open(imageRecipe, 'rb') as file:
         #   blobData = file.read()
        
        # recipeId = db.cursor().execute ('SELECT last_insert_rowid()')
        if category1 == "on":
            sweet = 1
        else:
            sweet = 0

        if category2 == "on":
            savoury = 1
        else:
            savoury = 0

        if category3 == "on":
            vegetarian = 1
        else: 
            vegetarian = 0

        if category4 == "on":
            vegan = 1
        else:
            vegan = 0

        if category5 == "on":
            glutenfree = 1
        else:
            glutenfree = 0

        db = get_db()
        cursor = db.cursor()

        cursor.execute('INSERT INTO recipe (title, description, ingredients, instructions, image, sweet, savoury, vegetarian, vegan, glutenfree, recipetype) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (titleRecipe, description, ingredients, instructions, recipeImage.filename, sweet, savoury, vegetarian, vegan, glutenfree, recipetype))
        db.commit()

        recipeId = cursor.lastrowid


        cursor.execute('SELECT title from recipe WHERE recipeId=?', (recipeId,))

        # db.close()
        return redirect(url_for('showRecipe', recipeCategory='cooking', recipeId=recipeId, recipeName=titleRecipe))        

    return render_template('add_recipe2.html')

@app.route('/recipe/new/baking',  methods=('GET', 'POST'))
def addRecipe3():

    if request.method == 'POST':
        titleRecipe = request.form['titleRecipe']
       # imageRecipe = request.form['imageRecipe']
        category1 = request.form.get('category1')
        category2 = request.form.get('category2')
        category5 = request.form.get('category5')

        description = request.form['description']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']
        recipetype = request.form['type']

        recipeImage=request.files['imageRecipe']

        if recipeImage.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], recipeImage.filename)
            recipeImage.save(filepath)

        #with open(imageRecipe, 'rb') as file:
         #   blobData = file.read()

        # recipeId = db.cursor().execute ('SELECT last_insert_rowid()')
        if category1 == "on":
            sweet = 1
        else:
            sweet = 0

        if category2 == "on":
            savoury = 1
        else:
            savoury = 0

        if category5 == "on":
            glutenfree = 1
        else:
            glutenfree = 0

        db = get_db()
        cursor = db.cursor()

        cursor.execute('INSERT INTO recipe (title, description, ingredients, instructions, image, sweet, savoury, glutenfree, recipetype) VALUES (?,?,?,?,?,?,?,?,?)', (titleRecipe, description, ingredients, instructions, recipeImage.filename, sweet, savoury, glutenfree, recipetype))
        db.commit()

        recipeId = cursor.lastrowid

        # db.close()
        return redirect(url_for('showRecipe', recipeCategory='baking', recipeId=recipeId, recipeName=titleRecipe))

    return render_template('add_recipe3.html')


@app.route('/recipes/cooking')
def showCookingRecipes():

    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
   # sql = 'SELECT * FROM recipe WHERE recipeId=?'
   # recipe = cursor.execute(sql, [recipeId]).fetchall()

    recipetype = 'cooking'

    recipes = cursor.execute('SELECT * FROM recipe WHERE recipetype=?', (recipetype,)).fetchall()

    # Query for inner join (recipe and diet)
   # join = cursor.execute('SELECT rd.recipeId, d.dietId FROM recipeDiet rd INNER JOIN diet d on d.dietId = rd.dietId').fetchall()

    return render_template('overview_cooking.html', recipes=recipes) #join=join


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

    db = get_db()
    db.row_factory = sqlite3.Row

    cursor = db.cursor()
   # sql = 'SELECT * FROM recipe WHERE recipeId=?'
   # recipe = cursor.execute(sql, [recipeId]).fetchall()

    recipetype = 'baking'

    recipes = cursor.execute('SELECT * FROM recipe WHERE recipetype=?', (recipetype,)).fetchall()


    # Query for inner join (recipe and diet)
   # join = cursor.execute('SELECT rd.recipeId, d.dietId FROM recipeDiet rd INNER JOIN diet d on d.dietId = rd.dietId').fetchall()

    return render_template('overview_baking.html', recipes=recipes)

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

    wantToTry = request.args.get('wantToTry', '')

    if wantToTry == '':
        db = get_db()
        db.row_factory = sqlite3.Row
        cursor = db.cursor()
   # sql = 'SELECT * FROM recipe WHERE recipeId=?'
   # recipe = cursor.execute(sql, [recipeId]).fetchall()
        recipe = cursor.execute('SELECT * FROM recipe WHERE recipeId=?', (recipeId,)).fetchone()
        wanttotry = cursor.execute('SELECT wantToTry FROM recipe WHERE recipeId=?', (recipeId,)).fetchone()

    else:
        db = get_db()
        db.row_factory = sqlite3.Row
        cursor = db.cursor()

        if wantToTry == "true":
            cursor.execute('UPDATE recipe SET wantToTry=1 WHERE recipeId=?', (recipeId,))

        if wantToTry == "false":
            cursor.execute('UPDATE recipe SET wantToTry=0 WHERE recipeId=?', (recipeId,))
        return redirect(url_for('showRecipe', recipeCategory=recipeCategory, recipeId=recipeId, recipeName=recipeName))

   # if request.method == 'POST':
    #    name = request.form['username']
     #   comment = request.form['commenttext']

       # "conn = get_db_connection()" 
       # cursor.execute('INSERT INTO recipeComment (comment,name,recipeId) VALUES (?,?,?)',(comment, name, recipeId)) 
       # db.commit()

   # comments = cursor.execute('SELECT * FROM recipeComment WHERE recipeId=?', (recipeId,)).fetchall()

        
    return render_template('comments.html', wanttotry=wanttotry, recipe=recipe, recipeCategory=recipeCategory, recipeId=recipeId, recipeName=recipeName) #comments=comments


@app.route('/have-tried')
def haveTried():
    return render_template('wtt_recipe_box.html')


@app.route('/want-to-try')
def wantToTry():
    return render_template('wtt_recipe_box.html')








if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


