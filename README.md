# Django Skeleton

for Django 1.9

## Features
Adds the following on top of Django's startproject template

* A set of starter html templates using bootstrap and jquery.

  * `base.html` is a minimal bootstrap template. It also shows any pending Django
    messages from the messages framework, and shows the currently logged-in
    user, and a link to logout.
  * `login.html` has a minimal login form
  * `logout.html` has a logout message and a link to log in again
  * `password_change.html` has a minimal password change form
  * `password_change_done.html` has a success message and a link to the
    'home' view

* A settings file split into a `common_settings.py` and `settings.ex.py`.
* Settings configured for a top-level static files directory
* Settings configured for a top-level templates directory
* Settings configured with a good default logging configuration
* Settings configured to auto-generate a secret key on first invocation
* A starter `.gitignore`
* A starter `requirements.txt`
* Defined urls for django built-in authentication views (login,
  logout, and password change) and settings configured to use them
  (`LOGIN_URL`, `LOGOUT_URL`, and `LOGIN_REDIRECT_URL`).

## Getting Started
The bare minimum to get a working project is:

1. Create a virtualenv and install the requirements listed in `requirements.txt`
2. Change the project name in the following places:

   * The project directory name
   * `common_settings.py` ROOT_URLCONF
   * `common_settings.py` WSGI_APPLICATION
   * `wsgi.py` the default settings module path
   * `manage.py` the default settings module path

3. Change the app name in the following places:

   * The app directory name
   * `common_settings.py` INSTALLED_APPS
   * The import statement in the project-wide `urls.py`

3. Copy the `settings.ex.py` to `settings.py`. No changes are needed for
   development. It is recommended to not check this file in to version
   control. As per our convention, settings common to all deployments go in
   `common_settings.py` which is checked in to version control.
   Deployment-specific settings go in `settings.py` which is not checked in
   to version control, or is checked in only on a deployment-specific branch.

4. The app should run now. You probably want to do the following at some
   point, though:

   * Change the project title and navbar header in base.html

## About base.html

The base template is a simple bootstrap-based html template. It has 4 content
blocks to override in sub-templates:

* `header` is used to insert items into the header of the page, such as
  stylesheets.
* `content` is where all your content should go. It is placed inside a
  `<div>` with class `container`
* `scripts` is a block at the very end of the body, which can be used to
  insert javascript blocks.
* `title` overrides the document title.

## Notes

* A view named 'home' is referenced in the starter templates and in the
  `LOGIN_REDIRECT_URL` setting. If you change the home view to be named
  something else, make sure you update these references.
