"""Main Flask application module."""

from flask import Flask
from crew_automation_for_shopify_e_commerce_integration.controllers.sales_controller import app as sales_app
from crew_automation_for_shopify_e_commerce_integration.controllers.temu_controller import app as temu_app
from crew_automation_for_shopify_e_commerce_integration.controllers.marketplace_controller import app as marketplace_app

app = Flask(__name__)
app.register_blueprint(sales_app, url_prefix='/')
app.register_blueprint(temu_app, url_prefix='/temu')
app.register_blueprint(marketplace_app, url_prefix='/marketplace')

if __name__ == '__main__':
    app.run(debug=True)