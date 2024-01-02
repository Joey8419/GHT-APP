from flask import Blueprint, render_template
from flask.cli import with_appcontext
from .model import db, Outbreaks, datetime
import pandas as pd
from sqlalchemy import desc, not_

load_data = Blueprint('load_data', __name__)


@load_data.cli.command('init-db')
@with_appcontext
def init_db():
    db.create_all()


@load_data.cli.command('import-data')
@with_appcontext
def import_data():
    df = pd.read_csv('website/Outbreaks.csv')

    for index, row in df.iterrows():
        outbreak = Outbreaks(
            Country=row['Country'],
            iso2=row['iso2'],
            iso3=row['iso3'],
            Year=row['Year'],
            icd10n=row['icd10n'],
            icd103n=row['icd103n'],
            icd104n=row['icd104n'],
            icd10c=row['icd10c'],
            icd103c=row['icd103c'],
            icd104c=row['icd104c'],
            icd11c1=row['icd11c1'],
            icd11c2=row['icd11c2'],
            icd11c3=row['icd11c3'],
            icd11l1=row['icd11l1'],
            icd11l2=row['icd11l2'],
            icd11l3=row['icd11l3'],
            Disease=row['Disease'],
            DONs=row['DONs'],
            Definition=row['Definition'],
            search_timestamp=datetime.utcnow()
        )
        db.session.add(outbreak)

        # Commit the changes to the database
    db.session.commit()


@load_data.route('/data')
def data():
    outbreak = Outbreaks.query.all()
    return render_template('load_data.html', outbreak=outbreak)

