# Generated by Django 3.2.4 on 2022-05-22 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='default_html',
            field=models.TextField(default='\n<style>\n    /*\n        Main Frukost user profile Stylesheet\n        (c) 2020-2021 Samkelo Rocks (Pty) Ltd\n    */\n\n    :root {\n        font-size: .8em;\n    }\n\n    *,\n    *::before,\n    *::after {\n        box-sizing: border-box;\n    }\n\n    body {\n        font-family: "Open Sans", Arial, sans-serif;\n        min-height: 100vh;\n        background-color: #fafafa;\n        color: #000;\n        padding-bottom: 3rem;\n    }\n\n    img {\n        display: block;\n    }\n\n    .container {\n        max-width: 93.5rem;\n        margin: 0 auto;\n        padding: 0 2rem;\n    }\n    \n    /* Profile Section */\n    .profile {\n        padding: 5rem 0;\n    }\n\n    .profile::after {\n        content: "";\n        display: block;\n        clear: both;\n    }\n\n    .profile-image {\n        float: left;\n        width: calc(33.333% - 1rem);\n        display: flex;\n        justify-content: center;\n        align-items: center;\n        margin-right: 3rem;\n    }\n\n    .profile-image img {\n        border-radius: 50%;\n        height: 200px;\n        width: 200px;\n    }\n\n    .profile-user-settings {\n        margin-top: 1.1rem;\n    }\n\n    .profile-user-name {\n        display: inline-block;\n        font-size: 2rem;\n        font-weight: 300;\n    }\n    \n    .profile-settings-btn {\n        font-size: 2rem;\n        margin-left: 1rem;\n    }\n\n    .profile-stats {\n        margin-top: 2.3rem;\n    }\n\n    .profile-stats li {\n        display: inline-block;\n        font-size: 1.6rem;\n        line-height: 1.5;\n        margin-right: 4rem;\n        cursor: pointer;\n    }\n\n    .profile-stats li:last-of-type {\n        margin-right: 0;\n    }\n\n    .profile-bio {\n        font-size: 1.6rem;\n        font-weight: 400;\n        line-height: 1.5;\n        margin-top: 2.3rem;\n    }\n\n    .profile-real-name,\n    .profile-stat-count,\n    .profile-btn {\n        font-weight: 600;\n    }\n\n    /* Gallery Section */\n\n    .gallery {\n        display: flex;\n        flex-wrap: wrap;\n        margin: -1rem -1rem;\n        padding-bottom: 3rem;\n    }\n\n    .gallery-item {\n        position: relative;\n        flex: 1 0 22rem;\n        margin: 1rem;\n        color: #fff;\n        cursor: pointer;\n    }\n    .gallery-item-link {\n        color: #fff;\n        text-decoration: none;\n    }\n\n    .gallery-item-info {\n        display: none;\n    }\n\n    .gallery-item-info li {\n        display: inline-block;\n        font-size: 1.7rem;\n        font-weight: 600;\n    }\n\n    .gallery-item-type {\n        position: absolute;\n        top: 1rem;\n        right: 1rem;\n        font-size: 2.5rem;\n        text-shadow: 0.2rem 0.2rem 0.2rem rgba(0, 0, 0, 0.1);\n    }\n    \n    .gallery-image {\n        width: 100%;\n        height: 30rem;\n        object-fit: cover;\n    }\n\n    @supports (display: grid) {\n        .profile {\n            display: grid;\n            grid-template-columns: 1fr 2fr;\n            grid-template-rows: repeat(3, auto);\n            grid-column-gap: 3rem;\n            align-items: center;\n        }\n\n        .profile-image {\n            grid-row: 1 / -1;\n        }\n\n        .gallery {\n            display: grid;\n            grid-template-columns: repeat(auto-fit, minmax(22rem, 1fr));\n            grid-gap: 2rem;\n        }\n\n        .profile-image,\n        .profile-user-settings,\n        .profile-stats,\n        .profile-bio,\n        .gallery-item,\n        .gallery {\n            width: auto;\n            margin: 0;\n        }\n    }\n</style>\n    '),
        ),
    ]
