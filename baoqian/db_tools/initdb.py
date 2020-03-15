#!/usr/bin/env python

import os
import django


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "baoqian.settings")
    django.setup()

    from django.contrib.auth.models import User, Group, Permission

    if not User.objects.filter(username='admin'):
        user = User.objects.create_superuser(
            'admin', 'admin@test.com', '56e1E@ab1234')
        user.save()

    if not Group.objects.filter(name='Operator'):
        operatorGroup = Group.objects.create(name='Operator')
        operatorGroup.save()
        # operatorGroup.permissions.set([
        #     Permission.objects.get(name='Can view Index'),
        #     Permission.objects.get(name='Can view Detail'),
        # ])

    items = [
        ('chenyizhou', 'cyz@example.com', 'player'),
        ('baoqian', 'bq@example.com', '19920407'),
    ]
    for i in items:
        if not User.objects.filter(username=i[0]):
            user = User.objects.create_user(*i)
            user.is_staff = True
            user.is_superuser = False
            user.groups.add(operatorGroup)
            user.save()
