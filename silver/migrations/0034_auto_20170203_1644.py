# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silver', '0033_auto_20170203_1540'),
    ]

    def ConditionalRunSQL(apps, schema_editor):
        if schema_editor.connection.vendor == 'postgres':
            return migrations.RunSQL("""
                    DROP VIEW IF EXISTS silver_document;
                    CREATE VIEW silver_document AS SELECT
                        'invoice' AS kind, id, series, number, issue_date, due_date,
                        paid_date, cancel_date, state, provider_id, customer_id,
                        proforma_id as related_document_id, archived_customer,
                        archived_provider, sales_tax_percent, sales_tax_name, currency, pdf,
                        transaction_currency
                        FROM silver_invoice
                    UNION
                    SELECT
                        'proforma' AS kind, id, series, number, issue_date, due_date,
                        paid_date, cancel_date, state, provider_id, customer_id,
                        NULL as related_document_id, archived_customer,
                        archived_provider, sales_tax_percent, sales_tax_name, currency, pdf,
                        transaction_currency
                        FROM silver_proforma WHERE invoice_id is NULL
            """)
        else:
            return migrations.RunSQL("""
                    DROP VIEW IF EXISTS silver_document;
                    CREATE VIEW silver_document AS SELECT
                        'invoice' AS `kind`, id, series, number, issue_date, due_date,
                        paid_date, cancel_date, state, provider_id, customer_id,
                        proforma_id as related_document_id, archived_customer,
                        archived_provider, sales_tax_percent, sales_tax_name, currency, pdf,
                        transaction_currency
                        FROM silver_invoice
                    UNION
                    SELECT
                        'proforma' AS `kind`, id, series, number, issue_date, due_date,
                        paid_date, cancel_date, state, provider_id, customer_id,
                        NULL as related_document_id, archived_customer,
                        archived_provider, sales_tax_percent, sales_tax_name, currency, pdf,
                        transaction_currency
                        FROM silver_proforma WHERE invoice_id is NULL
            """)



    operations = [
        migrations.AddField(
            model_name='Document',
            name='transaction_currency',
            field=models.CharField(max_length=4),
        ),
        migrations.RunPython(ConditionalRunSQL)
    ]
