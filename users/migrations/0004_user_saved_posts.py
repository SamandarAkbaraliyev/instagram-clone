# Generated by Django 4.2.7 on 2024-03-04 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0001_initial"),
        ("users", "0003_user_bio_user_blocked_accounts_user_close_friends_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="saved_posts",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="post.post"
            ),
        ),
    ]
