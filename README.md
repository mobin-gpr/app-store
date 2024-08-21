# App Store (rtl)
<img src="https://github.com/mobin-gpr/app-store/blob/main/screenshots/cover.png">

A complete project for downloading Android games and apps, which has been developed with significant effort. The project is very comprehensive and handles many issues. This script was not intended to be released as open source and was originally meant for commercial purposes. However, for various reasons, it has been made free and open source for the public, and I hope you benefit from it. Since the script was not meant to be public, there may be some shortcomings in the code comments and documentation, for which I apologize. Although I have tried to add necessary documentation and comments and apply required standards, if you find any unclear parts, please let me know and ask your questions. I recommend testing all parts of the site to ensure there are no bugs, as the project hasn't been updated for a while and something might have been overlooked. Also, if you have the time, you might consider improving parts of the code, such as the like and dislike system, which could be made more efficient with fewer queries. Currently, I'm not in a position to edit it, but I'll try to update it gradually.
Features

- Dark mode and light mode
- Dynamic and attractive design
- High speed
- Ability to add app information and screenshots by simply entering the Play Store ID
- Support for multiple versions of an app (e.g., mod, original, etc.)
- Ability to set colors for download links
- Advanced commenting system
- Ability to like and dislike comments
- Ability to reply to comments
- Visual distinction between admin comments and regular user comments
- Login with Gmail and GitHub
- Account activation with email confirmation
- Requesting apps by users
- And more...

## Developers

- [Mahyar Nasiri](https://github.com/Mhyar-nsi) (front-end dev)
- [Mobin Ghanbarpour](https://github.com/mobin-gpr/) (back-end dev)

## How to Run


#### Clone the project repository:

```bash
git clone https://github.com/mobin-gpr/app-store
```
#### Navigate to the project directory:

```bash
cd appstore
```
#### Install the required libraries:

```bash
pip install -r requirements.txt
```
#### Run the project:

```bash
python manage.py migrate
```
```bash
python manage.py runserver
```
#### Saving Avatars to the Database

```bash
python manage.py collectavatars
```
##### [FA README](https://github.com/mobin-gpr/app-store/blob/main/README-FA.md)

