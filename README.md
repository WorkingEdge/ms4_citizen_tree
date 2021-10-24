# Citizen Tree <!-- omit in toc -->
Citizen Tree is an online space to foster networks of people interested in growing trees to help one another brings trees from seed through to woodland. 

<a href="https://ms4-citizen-tree.herokuapp.com/" target="_blank">View the live project here</a>

# Table of Contents <!-- omit in toc -->  
- [Scenario Outline / Strategy](#scenario-outline--strategy)
- [User Experience](#user-experience)
  - [User Stories by User Type](#user-stories-by-user-type)
      - [Non-Registered Visitor](#non-registered-visitor)
    - [Registered Non-Contributing User](#registered-non-contributing-user)
    - [Registered Contributing User](#registered-contributing-user)
    - [Admin/Site-Owner](#adminsite-owner)
- [Design - UI](#design---ui)
    - [Additional Design Notes](#additional-design-notes)
- [Design - Database](#design---database)
      - [Using the CustomUser Model](#using-the-customuser-model)
- [Features](#features)
  - [Admin perspective](#admin-perspective)
    - [Email Verification](#email-verification)
    - [User Image Upload](#user-image-upload)
    - [Donations with Stripe](#donations-with-stripe)
  - [Technical Info](#technical-info)
    - [Initial Setup based on Django for Professinoals by William S. Vincent](#initial-setup-based-on-django-for-professinoals-by-william-s-vincent)
  - [Set up static files](#set-up-static-files)
  - [Problem using docker-compose to install packages](#problem-using-docker-compose-to-install-packages)
  - [Class-based generic views](#class-based-generic-views)
  - [Calculator Page](#calculator-page)
  - [Stripe](#stripe)
  - [Git](#git)
  - [Deployment](#deployment)
    - [Notes on Development](#notes-on-development)
      - [Why not use Gitpod?](#why-not-use-gitpod)
      - [Resources on Docker, Docker Compose, and Pipenv](#resources-on-docker-docker-compose-and-pipenv)
      - [Installing Docker](#installing-docker)
      - [Setting up the Virtual Environment and Managing Dependencies](#setting-up-the-virtual-environment-and-managing-dependencies)
      - [Using Docker Compose](#using-docker-compose)



# Scenario Outline / Strategy
The intended user of Citizen Tree falls broadly into one of three posible categories:
1. User with time and interest in growing trees but no space/land to do so.
   An example of this might be a school. As part of their learning about climate change, biodiversity etc, kids are introduced to the value of trees. Perhaps they visit a local forest on occasion. The kids would be interested in contributing to a tree-growing project but the school has no land to facilitate that. However, they do have space for 2-3 raised beds in which the kids could grow seeds to the seedling or one-year-old stage.At that point they would need to partner with a landowner to get those trees planted into a space where they could grow to maturity.
   Other potential users in this category might be individuals with small (or large) gardens, community groups, allotment groups, retirement groups, mens sheds etc.
2. User with space/land to grow trees but in need of help and/or trees. 
   The other side of the coin is the person or institution who owns some land and would like to have it planted with trees and are interested in community engagement. Maybe they don't have enough land to justify a commercial approach or perhaps they are just not interested in becoming commercial forestry owners. Rather they would be happy for a group of interested people to come and plant the land with them, for free, and provide the trees for free. It might also suit a company who has a land bank and sees the opportunity for devloping a positive profile using the partnerships facilitated bythe site.
3. A user who is interested in the aims of theproject and wishes to support it by making a donation or purchasing trees for their own use.

The site aims to help foster connections between people in the first two categories so that land might get planted and long-standing relationships might develop to help manage the trees and enjoy the spaces they create.

It also has a donation page where supporters can support the project financially and a shop where users can buy a specific subset of trees grown at project sites.

# User Experience
Users envisaged for the site are as follows:
* An admin superuser who can see and edit all content on the site. When a new project joins, it must be set up in the Django Admin by an admin user.This person is also required to give authoring rights to the designated 'author' for a project. This user is essentially the site owner and in a real world scenario would work together with a board to decide how donations were spent, whether requesting projects would be invited to join etc.
* The admin user is also responsible for adding products tot he site shop absed on real-world info and for setting initial stock numbers and prices.
* A project coordinator/author who is responsible for maintaing the information for a project - whether the project details page or periodic updates for the project progress. The rights associated with this user are limited to authoring for a specified subset of projects and cannot be self-assigned.
* A general user with read-only access. Although this user may be registered with the site, and may be a member of a project that is affiliated with the site, they do not have authoring or upload rights. They can make donations, use the shop, and view all content.
* A non-registered visitor has limited access. In order to make a donation or check out from the shop, users are required to register. A non-registered visitor can use the calculator app without restriction.


## User Stories by User Type

#### Non-Registered Visitor
* As a first-time or non-registered vistor to the site, I have access to the content but I cannot make a donation.
However, as an enticement to register and to set up a degreee of trust in the site and establish the scientific basis for the site's aims:
* I can interact with the CO2 calculator and get a sense of my personal CO2 emission (currently from transport fuel only) and how this might be counter-balanced by trees.
* I can clearly get a sense of the sites aims.
* I can add items from the shop to my cart but cannot check out without registering.
  
### Registered Non-Contributing User
* I can access any content that is available to a non-registered user.
* In addition, I can use the shop and make donations.

### Registered Contributing User
* I have access to all content that a non-registered user has. 
* If my user has been designated the 'author' for one or more projects, I can update the information for a project and and can add or delete updates (no edit option for project updates).

### Admin/Site-Owner
The interaction of this user with the site assumes integration with offline processes. For example, potential projects need to be vetted in person. Assuming this is all in place, the main points in relation to site use are:
* I can add a project and assign an 'author' - the designated person for a project to edit the project details page and add project updates.
* I can access information about donations.
* I can add products to the shop and edit price and stock information.
* I can view order information and payment status with a view to order fulfillment.
* I can edit or delete any project or update content.

# Design - UI
Wireframes and initial mockups:

* [Desktop](docs/MS4_Desktop.pdf)
* [Mobile](docs/MS4_Mobile.pdf)
* [Initial Outline](docs/MS4Draft_InitialOutline.pdf)

### Additional Design Notes
The aim is to maintain an 'earthy' look and feel to the site. The same background image is used throughout and colours for bottons and the background for project inof etc pick up on the greens and browns that would be familiar from a forest or farm setting.
Further input on the look and feel would be on the list of to-dos for the first update.

# Design - Database

The models used on the different apps interact across the project as a whole. For ease of reading, I have separated out the most important models per app:

* [FAQ model in the calculator app, plus resource info on DRF and fetch](/docs/faq_models.md)
* [Shop-related models](/docs/shop_models.md)
* [Project-related models](/docs/projects_models.md)
* [Donations-related models](/docs/donations_models.md)


#### Using the CustomUser Model
The Django docs explicitly recommend using a custom user model: "If you’re starting a new project, it’s highly recommended to set up a custom user model, even if the default User model is sufficient for you."
This advice was echoed in Django for Beginners and Django for Professionals books and I went with it. In retrospect, for this project I think it was a bad idea and if I were to start over, I think I would use the default user model.
Main resources on setting up and using the custom user model:

* [Django for Professionals](https://djangoforprofessionals.com/) book by William S. Vincent
* [Django Docs](https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project)
* [Django Best Practices: Referencing the User Model](https://learndjango.com/tutorials/django-best-practices-referencing-user-model)

Using it did not really bring any benefit and there was a small extra overhead when trying to figure out how to access the user. Resources consulted at various points for this are commented in the code.


# Features
(For testing, go to [Testing](/docs/testing.md))

## Admin perspective
It is easy for users to register with the site using an email and password or some level of social authentication (currently GitHub only).
It is not possible for an email account to be associated with 2 users.
Donation functionality on the site is user-friendly and professional. In addition to the success page, users get an email when their donation has been processed, but not before.

### Email Verification
Based on the functionality provided by django-allauth and the direction in 'Django for Professionals'
all-auth email templates: https://github.com/pennersr/django-allauth/tree/master/allauth/templates/account/email
all-auth settings: https://django-allauth.readthedocs.io/en/latest/configuration.html

Password reset functionality based on django-allauth and uses the allauth templates only slightly modified:
https://github.com/pennersr/django-allauth/tree/master/allauth/templates/account
Additional resource: https://www.youtube.com/watch?v=d9aCpxQfnOg

### User Image Upload
Image upload is available for users who are designated as the 'author' for a project. The option is part of the form when editing the project details or adding a new update.
Images uploaded by users in this way are stored and served from an Amazon S3 bucket.
![S3 Image Storage](/docs/readme_images/s3_image_storage.png)

### Donations with Stripe
The app uses Stripe to take donations payments. Options are limited to 3 donation levels and a user must be logged in to access the donate page.
The payment process can be cancelled by a user in which case they are redirected to a cancel page. Otherwise, when they commit to the payment, they are redirected to a success page.
In addition to the success page that confirms the amount they have paid, the user is also sent an email from the app to confirm the payment.
This email only issues after the payment has been successful. This is implemented using a webhook:
```python
@csrf_exempt
def stripe_webhook(request):
  endpoint_secret = settings.STRIPE_WH_SECRET
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event - send confirmation email
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    customer_email = session["customer_details"]["email"]
    amount = session["amount_total"]
    display_amount = "{0:.2f}".format(amount / 100)

    print(session)
    send_mail('Your donation', f'Thank you for your donation of {display_amount} euros to Citizen Tree.', 'ms4.citizentree@gmail.com', [customer_email], fail_silently=False)

```
The email is sent using SendGrid.

## Technical Info
### Initial Setup based on Django for Professinoals by William S. Vincent
Create virtual environment using pipenv
Install Django (this project uses 3.2.6 - see pipfile.lock)
Install psycopg2 for using postgres in development
Start the Django project and run the server to check - ok

Stop the virtual env.

Set up the Dockerfile and docker-compose files

Change settings so that default db is postgres and not sqlite3.

Before running migrations, set up custom user model: https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

## Set up static files
Based on:
* Django for Professionals
* Django docs
* Boutique Ado

## Problem using docker-compose to install packages
For much of the basic setup of the project, I'm following Django for Professionals by William S. Vincent. To install packages, eg Crispy Forms, he recommends the following command in the terminal:
```sh
$ docker-compose exec web pipenv install <django-crispy-forms==1.9.2>
```
I found that this did not work. The problem seems to be known but I didn't find a perfect solution.
See:
https://stackoverflow.com/questions/53400385/django-docker-and-pipenv-error-adding-new-packages
https://stackoverflow.com/questions/60949436/django-docker-and-pipenv-error-adding-new-packages-not-transfering-from-con

The command that seems to work is to remove the docker-compose element and just install using pipenv. The package gets added to the pipfile and pipfile.lock:
```sh
pipenv install django-crispy-forms
```

## Class-based generic views
I'm using mostly class-based views in the project.
For the Projects app, info for this has come from:
* Django for professionals
* Very Academy - Learn Django Class-Based View series - https://www.youtube.com/watch?v=GxA2I-n8NR8

Other Resources included:
For some issues passing context data (breaking if no user is logged in):
https://stackoverflow.com/questions/54444196/get-context-data-breaking-breaking-django-listview
https://stackoverflow.com/questions/51632952/get-the-user-id-class-based-view
https://stackoverflow.com/questions/65685752/getting-django-db-models-query-utils-deferredattribute-object-at-0x7fca8f1d3d50

Also, class-based edit views.
Resources for DeleteView:
https://www.codingforentrepreneurs.com/projects/try-django/class-based-views-deleteview
https://www.geeksforgeeks.org/deleteview-class-based-views-django/
https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic-editing/#django.views.generic.edit.DeleteView

## Calculator Page
The purpose of the calculator page is to give some context to the figures and emphasise the purpose of the project and the scales involved.
How it works:
The user can enter a Euro amount that they spend on transportation fuel weekly. 
Using figures from the AA re fuel price, this is converted to a litre amount of either petrol or diesel, as selected.

Using this litre amount, the CO2 emission for that amount of fuel is calculated and returned as the weekly and annual (*52) CO2 emissions arising from transport fuel usage.
Note: A future iteration of the site would have a more complete CO2 calculator (eg, food, other transport, heating etc). For the first iteration, the CO2 arising from fuel usage is relatively straightforward to calculate and it is also straightforward to isolate so it was chosen as an indicative metric.

After calculating the emissions, the user is presented with information relating to the potential sequestration arising from a donation to Citizen Tree and this is presented as a % of the fuel emission calculated previously. For example 'A 50 euro donation would amount to x trees and represent an offset of about 2% of your transport emissions.
The purpose here is to reinforce the scales involved and to serve as a call to action for the user.

To give legitimacy to the calculations and to the project, a further section outlines some background and FAQs.

Note on tech setup:
The page updates dynamically and asynchronously as the user progresses through it. The HTML is updated according to the inputs and some hard-coded HTML (template literal) in the corresponding JS functions. 
For the FAQs, the page is updated (no reload) using fetch (similar to Ajax). The API endpoints from which fetch retrieves the data are set up using the Django Rest Framework (DRF).

Additional information on the assumptions used for the calculation and relevant resources are here.


## Stripe
Stripe integration is based on:
* Boutique Ado
* Stripe docs
* JustDjango tutorial: https://justdjango.com/blog/django-stripe-payments-tutorial and https://www.youtube.com/watch?v=722A27IoQnk
* testdriven.io tutorial: https://testdriven.io/blog/django-stripe-tutorial/
* re session object: https://stripe.com/docs/api/checkout/sessions/line_items
* https://bhoey.com/blog/stripe-checkout-with-django/

## Git
Branching and merging: https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging

## Deployment
The deployment steps below are the procedure followed for this app. It differs from the procedure used for Boutique Ado and the MS3 project in that the development and delpoyment process use Docker. 
Development also differed and was done using Docker Compose and VS Code locally, (as opposed to Gitpod).

### Notes on Development
#### Why not use Gitpod?
Gitpod had served well for the three milestone projects so far. I decided to switch to using VS Code locally in combination with Docker Compose for a couple of reasons:

* To expand my learning in relation to handling a development environment.
* Docker seemed like a useful technology/tool to become familiar with.
* When I started the MS4 project, I misjudged the time I had available.

All in all I think it was a good decision but it did add an additional load on the learning required to complete the project. 

#### Resources on Docker, Docker Compose, and Pipenv
For information on installing and using Docker and Docker Compose, I relied on these primary resources:

* [Django for Professionals](https://djangoforprofessionals.com/) book by William S. Vincent
* [Dive into Docker](https://nickjanetakis.com/courses/#dive-into-docker) online course by Nick Janetakis
* [Virtual Environment Setup](https://djangoforbeginners.com/initial-setup/) 
* [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/)

#### Installing Docker
To install Docker, I followed the steps outlined in the [Docker documentation](https://docs.docker.com/engine/install/ubuntu/).
To install Docker Compose, I followed the steps [here](https://docs.docker.com/compose/install/)
The versions used are: 
![Docker](/docs/readme_images/docker_verify_install.png)

#### Setting up the Virtual Environment and Managing Dependencies
Pipenv was used to install and manage dependencies (e.g. Django itself, crispy forms etc), using the following command:
```shell
pipenv install django
```
Because I used Pipenv, the ```requirements.txt``` file is replaced by ```Pipfile``` and ```Pipfile.lock```. Pipfile lists the dependencies and Pipfile.lock includes the versions used so that an exact repica of the development environment can be created. These files are updated automatically by Pipenv whenever a new package is installed.

Resources on using Pipenv included:
* [Django for Professionals](https://djangoforprofessionals.com/) book by William S. Vincent
* [pypi.org](https://pypi.org/project/pipenv/2021.5.29/)
* [Pipenv docs](https://pipenv.pypa.io/en/latest/)
* [Real Python](https://realpython.com/pipenv-guide/) 

#### Using Docker Compose
Once the project was set up, all manage.py commands were run via docker-compose, using the following pattern (using makemigrations for the projects app as example):
```sh
docker-compose exec web python manage.py makemigrations projects
``` 

Command to start the local server:
```sh
docker-compose up
```
OR
```sh
docker-compose up -d
```
The difference bewtween the two commands above being the terminal output was disabled with the ```-d``` flag.


