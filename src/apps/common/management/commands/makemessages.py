from django.core.management.commands import makemessages


class Command(makemessages.Command):
    # Prevent generating fuzzy messages
    msgmerge_options = makemessages.Command.msgmerge_options + ["--no-fuzzy-matching"]
