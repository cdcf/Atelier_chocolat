from app import create_app, db
from app.models import User, Production, Currency, Product, ProductFamily, Supplier, ProductionItem

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Production': Production, 'Currency': Currency, 'Product': Product,
            'ProductFamily': ProductFamily, 'Supplier': Supplier, 'ProductionItem': ProductionItem}
