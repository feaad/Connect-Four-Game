"""
File: signals.py
Project: Backend - Connect Four
File Created: Monday, 22nd July 2024 8:34:08 AM
Author: feaad
Email: fantwi02@student.bbk.ac.uk
Version: 1.0
Brief: The signals for the user app.
-----
Last Modified: Monday, 22nd July 2024 1:15:30 PM
Modified By: feaad
-----
Copyright ©2024 feaad
"""

from core.models import Algorithm, EloHistory, Guest, Player, User
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_or_convert_player_for_user(
    sender: User, instance: User, created: bool, **kwargs
) -> None:
    """
    Create a player object when a new user is created.

    Parameters
    ----------
    sender : User
        The user model.

    instance : User
        The user instance.

    created : bool
        A boolean value indicating whether the user was created.

    kwargs : dict
        Additional keyword arguments.

    """
    if created and not instance.is_staff:
        try:
            with transaction.atomic():
                if guest := Guest.objects.filter(
                    username=instance.username
                ).first():
                    player = Player.objects.get(guest=guest)
                    player.user = instance
                    player.save()
                else:
                    Player.objects.create(user=instance)
        except Exception as e:
            instance.delete()
            raise e


@receiver(post_save, sender=Guest)
def create_player_for_guest(
    sender: Guest, instance: Guest, created: bool, **kwargs
) -> None:
    """
    Create a player object when a new guest is created.

    Parameters
    ----------
    sender : Guest
        The guest model.

    instance : Guest
        The guest instance.

    created : bool
        A boolean value indicating whether the guest was created.

    kwargs : dict
        Additional keyword arguments.

    """
    if created:
        try:
            with transaction.atomic():
                Player.objects.create(guest=instance)
        except Exception as e:
            instance.delete()
            raise e


@receiver(post_save, sender=Algorithm)
def create_player_for_algorithm(
    sender: Algorithm, instance: Algorithm, created: bool, **kwargs
) -> None:
    """
    Create a player object when a new algorithm is created.

    Parameters
    ----------
    sender : Algorithm
        The algorithm model.

    instance : Algorithm
        The algorithm instance.

    created : bool
        A boolean value indicating whether the algorithm was created.

    kwargs : dict
        Additional keyword arguments.

    """
    if created:
        try:
            with transaction.atomic():
                Player.objects.create(algorithm=instance, is_human=False)
        except Exception as e:
            instance.delete()
            raise e


@receiver(pre_save, sender=Player)
def create_elo_history(sender: Player, instance: Player, **kwargs) -> None:
    if not instance.pk:
        return

    try:
        previous_instance = Player.objects.get(pk=instance.pk)
    except Player.DoesNotExist:
        return

    if previous_instance.elo != instance.elo:
        EloHistory.objects.create(
            player=instance,
            old_elo=previous_instance.elo,
            new_elo=instance.elo,
        )
