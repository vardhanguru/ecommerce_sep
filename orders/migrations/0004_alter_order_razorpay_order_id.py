from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_order_razorpay_order_id_order_razorpay_payment_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="razorpay_order_id",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]