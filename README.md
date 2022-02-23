# Task 14 - Add a little nice look
> *Modify your project using frontend tools like a webpack and add CSS framework bootstrap 4*

### Objective

The main task is to create a web application like Instagram. 
The program must be based on Django, must have a web interface. The user can register on the site with e-mail. 
After basic registration, the user receives a confirmation to continue registration. 
This letter must have a unique link. By following the link, the user can add his full name, bio and avatar. 
You can then use DjangoGram. You can create posts with images, view posts by other users. 
You can also like posts, or follow other users. Unauthorized users are not allowed to create and view posts. 
At this stage of the project it is necessary to supplement the use of CSS and JS frameworks with the use of Webpack. 
The project should be deployed on Heroku. 

### Realization

The project consists of two relatively independent Django applications 
The registration system is based on the Django authentication system with extensive use of built-in models, views, 
templates.
`AbstractUser` was used to achieve the two-stage registration, which allows in the first stage to create an inactive 
user only with an e-mail address as a username. Therefore, the `Signup` and `Activate` classes also inherit the base 
`View` class.

At the same time, the rest of the classes are explored from the existed `DetailView`, `UpdateView`, and classes 
`LogoutView, LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView` are used without changes.

#### CSS framework

It was decided to use the CSS Bulma framework in the project. However, Django's built-in authentication templates 
use Widgets to build basic form elements. Widgets are easy to upgrade by matching them to custom templates. 

But the structure of the Django widgets did not match the structure of the Bulma classes. For example, 
the standard input widget contains only the `<input>` tag:

```html
<input type="{{ widget.type }}" name="{{ widget.name }}" value="{{ widget.value|stringformat:'s' }}">
```

Rendering of other related items relied on the `_html_output` function of the `BaseForm` class. 
In Bulma the layout of the desired field is significantly different: 

```html
<div class="field is-horizontal">
  <div class="field-label is-normal">
    <label class="label">From</label>
  </div>
  <div class="field-body">
    <div class="field">
      <p class="control">
        <input class="input is-static" type="email" value="me@example.com" readonly>
      </p>
    </div>
  </div>
</div>
```
In this regard, the project widely used custom template filters, which allowed making form templates quite 
concise:

```html
{% extends 'base.html' %}
{% block content %}
   {% load bulma_filters %}
   <div class="columns is-centered">
       <form class="box column is-half" method="POST" enctype="multipart/form-data">
           <h3 class="title">Activation form</h3>
           {% csrf_token %}
           {% form_bulma %}
           <div class="field">
               <p class="control">
                   {% button_bulma name='activate' %}
               </p>
           </div>
       </form>
   </div>
{% endblock %}
```

It should be noted that there is a `django-bulma` project, but it was not used due to the complexity of customization. 

#### Third-party service for storing images

The Cloudinary service is used to save images of avatars and posts. 

In addition to the standard settings, there is a distinction between the folders 
of avatars and posts, saving the original file names: 
`… folder='django_gramm/pasts_images',
use_filename=True)`

Also, configure to delete images after deleting the main object:

```python
def delete_media(self):
    cloudinary.api.delete_resources([self.image])
```

#### JS framework

JS used for

- preview downloadable images;
- likes (likes);
- tracking other users.

Used Vue 3 framework.

Likes and following work in such a way that pressing again turns on or off like or tracking, respectively. 
However, unlike likes, which can be applied to your own posts, the user can not follow himself.

The `ValidationError` exception rises in the save method of the `Following` model and then tracked 
in the `FollowingView` class. Django messages and related markup elements were not used. 
Instead, the tag on tracking oneself is reflected in the animation: ![forbidden follow](https://res.cloudinary.com/dgh6qdngr/image/upload/v1645389428/django_gramm/other/follow_forbidden.gif).
Acceptable action is animated differently: ![allow follow](https://res.cloudinary.com/dgh6qdngr/image/upload/v1645390101/django_gramm/other/follow_allow.gif).

#### Project development and deployment

Vue-CLI and webpack-bundle-tracker were used during the development. 
This allows you to start the Vue development server. Start the server from the `/frontend/` 
directory with the `npm run serve` command. 
Django used the `django-webpack-loader` and `django-cors-headers` packages.

##### Settings:

Vue-CLI is configured by creating `vue.config.json`. The main parameters are well described in the Vue-CLI documentation. 
The `configureWebpack` or `chainWebpack` object will be included in the final Webpack configuration.
Vue-CLI and django-webpack-loader initial settings are enough for development. During development, you need to run Django 
and webpack servers at the same time.


Before deploying to the server you need:
to compile JS files with the npm run build command. They will be placed in the directory specified in `vue.config.js` 
in the `outputDir` variable: `./dist/webpack_bundles/`,
transfer these files to the Django directory for statics with the `python manage.py collectstatic` 
command. The path to the folder from the previous item must be in the `STATICFILES_DIRS` list, for the `DEBUG = False` 
mode the `STATIC_ROOT` variable must be defined and it must not be included in `STATICFILES_DIRS`.


Connect compiled statics to Django templates. 
There are two options:
- remove all django-webpack-loader settings from the template and from the whole project and insert a direct link to the compiled JS file in the template; 
- leave django-webpack-loader, which can also handle static files. 
  > It should be kept in mind that this feature django-webpack-loader - it looks for static files starting 
  > from the folder webpack_bundles, although the settings do not specify. 
  > Therefore, outputDir must contain these folders, which will later go to static and django-webpack-loader 
  > will be able to enter its compiled JS.


After this stage, it is enough to start only the Django server.





# django_blog

![forbidden follow](https://res.cloudinary.com/dgh6qdngr/image/upload/v1645389428/django_gramm/other/follow_forbidden.gif)

![allow follow](https://res.cloudinary.com/dgh6qdngr/image/upload/v1645390101/django_gramm/other/follow_allow.gif)