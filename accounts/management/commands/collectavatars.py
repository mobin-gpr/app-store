import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from accounts.models import AvatarImagesModel


class Command(BaseCommand):
    help = "Collects avatar images from the static directory and adds them to the AvatarImagesModel."

    def handle(self, *args, **kwargs):
        # Get the path to the avatars directory
        avatars_path = os.path.join(settings.BASE_DIR, "static", "avatars")

        if not os.path.exists(avatars_path):
            self.stdout.write(
                self.style.ERROR(f"The directory {avatars_path} does not exist.")
            )
            return

        # Iterate through all files in the avatars directory
        added_images = []
        for filename in os.listdir(avatars_path):
            file_path = os.path.join(avatars_path, filename)
            if os.path.isfile(file_path):
                # Add new image to the model
                with open(file_path, "rb") as f:
                    image_file = File(f, name=filename)
                    AvatarImagesModel.objects.create(image=image_file)
                    added_images.append(filename)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully added image "{filename}".')
                )

        if not added_images:
            self.stdout.write(self.style.WARNING("No new images were added."))
        else:
            self.stdout.write(
                self.style.SUCCESS(f"Added {len(added_images)} new images.")
            )
