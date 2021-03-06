"""
API Version 1
=============

LetLive Api using `Django REST framework`_.

.. _Django REST framework: https://www.django-rest-framework.org/

It has the following endpoints:
::

  {
    "articles": "http://domain/api_v1/articles/",
    "topics": "http://domain/api_v1/topics/",
    "admins": "http://domain/api_v1/admins/",
    "authors": "http://domain/api_v1/authors/",
    "subscribers": "http://domain/api_v1/subscribers/",
    "users": "http:://domain/api_v1/users/",
    "groups": "http://domain/api_v1/groups/",
    "profile": "http://domain/api_v1/profile/",
  }
  
Has Authentication using Django authentication

* BasicAuthentication.
* TokenAuthentication.
* SessionAuthentication.

Token Authentication
--------------------

Uses the default Django Rest authentication routes 
and a route for getting the user token:
::

  {
    "login": "http:://domain/api_v1/auth/login",
    "logout": "http:://domain/api_v1/auth/logout",
    "user": "http:://domain/api_v1/auth/user",
    "rest_password_change": "http:://domain/api_v1/auth/password/change",
    "rest_password_reset": "http:://domain/api_v1/auth/password/reset/confirm",
    "api-token": "http:://domain/api_v1/auth/api-token-auth/",
  }
"""
