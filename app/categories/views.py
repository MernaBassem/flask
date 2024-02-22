from flask import render_template, redirect, url_for, flash
from .forms import CategoryForm
from models import Category, db
from . import category_blueprint
@category_blueprint.route('/home', methods=['GET'], endpoint='home')
def category_home():
    return "<h1>Welcome to categorys Home</h1>"


@category_blueprint.route('/', methods=['GET'], endpoint='index')
def category_index():
    categories = Category.get_all_categories()
    return render_template("categories/index.html", categories=categories)



 # Import th e CategoryForm

@category_blueprint.route('/createCategory', methods=['GET', 'POST'], endpoint='createCategory')
def create_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category_data = {
            'name': form.name.data,
            'description': form.description.data
        }
        Category.save_category(category_data)
        flash('Category created successfully', 'success')
        return redirect(url_for('category.index'))
    return render_template('categories/createCategory.html', form=form)


@category_blueprint.route('/updateCategory/<int:category_id>', methods=['GET', 'POST'], endpoint='updateCategory')
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        form.populate_obj(category)
        category.save()  # Save the category object
        flash('Category updated successfully', 'success')
        return redirect(url_for('category.index'))
    return render_template('categories/updateCategory.html', form=form, category=category)



@category_blueprint.route('/deleteCategory/<int:category_id>', methods=['POST'], endpoint='deleteCategory')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('category.index'))
