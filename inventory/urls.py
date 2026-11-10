from django.urls import path

from . import api, views

urlpatterns = [
    path("", views.index),
    path("healthz", views.healthz),
    path("api/logo", views.logo),
    path("api/bootstrap", api.bootstrap),
    path("api/state", api.state),
    path("api/login", api.session_login),
    path("api/setup", api.setup),
    path("api/logout", api.session_logout),
    path("api/account/password", api.account_password),
    path("api/devices", api.device_create),
    path("api/devices/<int:pk>", api.device_update),
    path("api/devices/<int:pk>/assign", api.device_assign),
    path("api/devices/<int:pk>/return", api.device_return),
    path("api/devices/<int:pk>/incidents", api.device_incident),
    path("api/devices/<int:pk>/status", api.device_status),
    path("api/incidents/<int:pk>/resolve", api.incident_resolve),
    path("api/employees", api.employee_create),
    path("api/employees/<int:pk>", api.employee_update),
    path("api/employees/<int:pk>/status", api.employee_status),
    path("api/settings", api.settings_update),
    path("api/settings/password-policy", api.password_policy_update),
    path("api/settings/logo", api.logo_update),
    path("api/lists/<str:coll>", api.list_create),
    path("api/lists/<str:coll>/<int:pk>", api.list_item),
    path("api/users", api.user_create),
    path("api/users/<int:pk>", api.user_update),
    path("api/users/<int:pk>/toggle", api.user_toggle),
]
