from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_products_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.CharField(
                blank=True,
                help_text='Path relative to static/, for example category/example.jpg.',
                max_length=255,
                null=True,
                verbose_name='Static image path',
            ),
        ),
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.CharField(
                blank=True,
                help_text='Path relative to static/, for example products/example.jpg.',
                max_length=255,
                verbose_name='Static image path',
            ),
        ),
    ]