"""
Routes For Silverback
"""

# Django
from django.urls import include, path

# local Django
from app.controllers.web.home import Home as Home_View
from app.controllers.web.install import Install as Install_View
from app.controllers.web.not_found import handler404 as handler404_view
from app.controllers.web.error import handler500 as handler500_view
from app.controllers.web.login import Login as Login_View
from app.controllers.web.register import Register as Register_View
from app.controllers.web.forgot_password import Forgot_Password as Forgot_Password_View
from app.controllers.web.reset_password import Reset_Password as Reset_Password_View
from app.controllers.web.statistics import Statistics as Statistics_View
from app.controllers.web.incidents import Incidents as Incidents_View
from app.controllers.web.history import AtomHistory as AtomHistory_View
from app.controllers.web.history import RssHistory as RssHistory_View

from app.controllers.web.admin.logout import Logout as Logout_View
from app.controllers.web.admin.dashboard import Dashboard as Dashboard_View
from app.controllers.web.admin.profile import Profile as Profile_View
from app.controllers.web.admin.settings import Settings as Settings_View
from app.controllers.web.admin.builder import Builder as Builder_View
from app.controllers.web.admin.activity import Activity as Activity_View
from app.controllers.web.admin.notification import Notification as Notification_View
from app.controllers.web.admin.user import User_List as User_List_Web
from app.controllers.web.admin.user import User_Edit as User_Edit_Web
from app.controllers.web.admin.user import User_Add as User_Add_Web

from app.controllers.web.admin.component import Component_List as Component_List_View
from app.controllers.web.admin.component import Component_Add as Component_Add_View
from app.controllers.web.admin.component import Component_Edit as Component_Edit_View
from app.controllers.web.admin.component_group import Component_Group_List as Component_Group_List_View
from app.controllers.web.admin.component_group import Component_Group_Add as Component_Group_Add_View
from app.controllers.web.admin.component_group import Component_Group_Edit as Component_Group_Edit_View
from app.controllers.web.admin.incident import Incident_List as Incident_List_View
from app.controllers.web.admin.incident import Incident_Add as Incident_Add_View
from app.controllers.web.admin.incident import Incident_Edit as Incident_Edit_View
from app.controllers.web.admin.incident import Incident_View as Incident_View_View
from app.controllers.web.admin.incident_update import Incident_Update_Add as Incident_Update_Add_View
from app.controllers.web.admin.incident_update import Incident_Update_Edit as Incident_Update_Edit_View
from app.controllers.web.admin.incident_update import Incident_Update_View as Incident_Update_View_View
from app.controllers.web.admin.metric import Metric_List as Metric_List_View
from app.controllers.web.admin.metric import Metric_Add as Metric_Add_View
from app.controllers.web.admin.metric import Metric_Edit as Metric_Edit_View
from app.controllers.web.admin.subscriber import Subscriber_List as Subscriber_List_View
from app.controllers.web.admin.subscriber import Subscriber_Add as Subscriber_Add_View
from app.controllers.web.admin.subscriber import Subscriber_Edit as Subscriber_Edit_View

from app.controllers.api.private.v1.install import Install as Install_V1_Endpoint_Private
from app.controllers.api.private.v1.login import Login as Login_V1_Endpoint_Private
from app.controllers.api.private.v1.register import Register as Register_V1_Endpoint_Private
from app.controllers.api.private.v1.forgot_password import Forgot_Password as Forgot_Password_V1_Endpoint_Private
from app.controllers.api.private.v1.reset_password import Reset_Password as Reset_Password_V1_Endpoint_Private

from app.controllers.api.private.v1.admin.settings import Settings as Settings_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.profile import Profile as Profile_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.notifications import Notifications as Notifications_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.notifications import LatestNotifications as LatestNotifications_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.user import User as User_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.user import Users as Users_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.component_group import Component_Group as Component_Group_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.component_group import Component_Groups as Component_Groups_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.component import Component as Component_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.component import Components as Components_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.incident import Incident as Incident_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.incident import Incidents as Incidents_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.incident_update import Incident_Update as Incident_Update_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.incident_update import Incident_Updates as Incident_Updates_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.incident_update import Incident_Updates_Notify as Incident_Updates_Notify_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.incident_update import Incident_Updates_Components as Incident_Updates_Components_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.incident_update import Incident_Updates_Component as Incident_Updates_Component_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.metric import Metric as Metric_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.metric import Metrics as Metrics_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.metric import NewRelic_Apps as NewRelic_Apps_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.subscriber import Subscriber as Subscriber_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.subscriber import Subscribers as Subscribers_Admin_V1_Endpoint_Private
from app.controllers.api.private.v1.admin.activity import Activities as Activities_Admin_V1_Endpoint_Private


urlpatterns = [
    # Public Views
    path('', Home_View.as_view(), name='app.web.home'),
    path('incidents/<uri>', Incidents_View.as_view(), name='app.web.incidents'),
    path('install', Install_View.as_view(), name='app.web.install'),
    path('login', Login_View.as_view(), name='app.web.login'),
    path('register/<token>', Register_View.as_view(), name='app.web.register'),
    path('forgot-password', Forgot_Password_View.as_view(), name='app.web.forgot_password'),
    path('reset-password/<token>', Reset_Password_View.as_view(), name='app.web.reset_password'),
    path('statistics/<type>', Statistics_View.as_view(), name='app.web.statistics'),
    path('history.atom', AtomHistory_View.as_view(), name='app.web.history_atom'),
    path('history.rss', RssHistory_View.as_view(), name='app.web.history_rss'),

    # Authenticated Users Views
    path('admin/', include([

        path('logout', Logout_View.as_view(), name='app.web.admin.logout'),
        path('dashboard', Dashboard_View.as_view(), name='app.web.admin.dashboard'),
        path('profile', Profile_View.as_view(), name='app.web.admin.profile'),
        path('activity', Activity_View.as_view(), name='app.web.admin.activity.list'),
        path('notifications', Notification_View.as_view(), name='app.web.admin.notification.list'),
        path('settings', Settings_View.as_view(), name='app.web.admin.settings'),
        path('builder', Builder_View.as_view(), name='app.web.admin.builder'),
        path('users', User_List_Web.as_view(), name='app.web.admin.user.list'),
        path('users/add', User_Add_Web.as_view(), name='app.web.admin.user.add'),
        path('users/edit/<int:user_id>', User_Edit_Web.as_view(), name='app.web.admin.user.edit'),

        path('components', Component_List_View.as_view(), name='app.web.admin.component.list'),
        path('components/add', Component_Add_View.as_view(), name='app.web.admin.component.add'),
        path('components/edit/<int:component_id>', Component_Edit_View.as_view(), name='app.web.admin.component.edit'),

        path('component-groups', Component_Group_List_View.as_view(), name='app.web.admin.component_group.list'),
        path('component-groups/add', Component_Group_Add_View.as_view(), name='app.web.admin.component_group.add'),
        path('component-groups/edit/<int:group_id>', Component_Group_Edit_View.as_view(), name='app.web.admin.component_group.edit'),

        path('incidents', Incident_List_View.as_view(), name='app.web.admin.incident.list'),
        path('incidents/add', Incident_Add_View.as_view(), name='app.web.admin.incident.add'),
        path('incidents/edit/<int:incident_id>', Incident_Edit_View.as_view(), name='app.web.admin.incident.edit'),
        path('incidents/view/<int:incident_id>', Incident_View_View.as_view(), name='app.web.admin.incident.view'),

        path('incidents/view/<int:incident_id>/updates/add', Incident_Update_Add_View.as_view(), name='app.web.admin.incident_update.add'),
        path('incidents/view/<int:incident_id>/updates/edit/<int:update_id>', Incident_Update_Edit_View.as_view(), name='app.web.admin.incident_update.edit'),
        path('incidents/view/<int:incident_id>/updates/view/<int:update_id>', Incident_Update_View_View.as_view(), name='app.web.admin.incident_update.view'),

        path('metrics', Metric_List_View.as_view(), name='app.web.admin.metric.list'),
        path('metrics/add', Metric_Add_View.as_view(), name='app.web.admin.metric.add'),
        path('metrics/edit/<int:metric_id>', Metric_Edit_View.as_view(), name='app.web.admin.metric.edit'),

        path('subscribers', Subscriber_List_View.as_view(), name='app.web.admin.subscriber.list'),
        path('subscribers/add', Subscriber_Add_View.as_view(), name='app.web.admin.subscriber.add'),
        path('subscribers/edit/<int:subscriber_id>', Subscriber_Edit_View.as_view(), name='app.web.admin.subscriber.edit'),

    ])),

    # Private API V1 Endpoints
    path('api/private/v1/', include([

        path('install', Install_V1_Endpoint_Private.as_view(), name='app.api.private.v1.install.endpoint'),
        path('login', Login_V1_Endpoint_Private.as_view(), name='app.api.private.v1.login.endpoint'),
        path('register', Register_V1_Endpoint_Private.as_view(), name='app.api.private.v1.register.endpoint'),
        path('forgot-password', Forgot_Password_V1_Endpoint_Private.as_view(), name='app.api.private.v1.forgot_password.endpoint'),
        path('reset-password', Reset_Password_V1_Endpoint_Private.as_view(), name='app.api.private.v1.reset_password.endpoint'),

        path('admin/', include([
            path(
                'settings',
                Settings_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.settings.endpoint'
            ),
            path(
                'profile',
                Profile_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.profile.endpoint'
            ),
            path(
                'notification',
                Notifications_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.notifications.endpoint'
            ),
            path(
                'latest_notifications',
                LatestNotifications_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.latest_notifications.endpoint'
            ),
            path(
                'user',
                Users_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.users.endpoint'
            ),
            path(
                'user/<int:user_id>',
                User_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.user.endpoint'
            ),
            path(
                'component-group',
                Component_Groups_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.component_groups.endpoint'
            ),
            path(
                'component-group/<int:group_id>',
                Component_Group_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.component_group.endpoint'
            ),
            path(
                'component',
                Components_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.components.endpoint'
            ),
            path(
                'component/<int:component_id>',
                Component_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.component.endpoint'
            ),
            path(
                'incident',
                Incidents_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.incidents.endpoint'
            ),
            path(
                'incident/<int:incident_id>',
                Incident_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.incident.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>',
                Incident_Updates_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.incident_updates.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>',
                Incident_Update_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.incident_update.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>/notify',
                Incident_Updates_Notify_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.incident_update.notify.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>/components',
                Incident_Updates_Components_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.incident_update.components.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>/component/<int:item_id>',
                Incident_Updates_Component_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.incident_update.component.endpoint'
            ),
            path(
                'metric',
                Metrics_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.metrics.endpoint'
            ),
            path(
                'metric/<int:metric_id>',
                Metric_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.metric.endpoint'
            ),
            path(
                'subscriber',
                Subscribers_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.subscribers.endpoint'
            ),
            path(
                'subscriber/<int:subscriber_id>',
                Subscriber_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.subscriber.endpoint'
            ),
            path(
                'activity',
                Activities_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.activities.endpoint'
            ),
            path(
                'action/metric/new-relic-apps',
                NewRelic_Apps_Admin_V1_Endpoint_Private.as_view(),
                name='app.api.private.v1.admin.metric.action.new_relic_apps.endpoint'
            ),
        ]))

    ])),

    # Public API V1 Endpoints
    path('api/public/v1/', include([

    ]))
]

handler404 = handler404_view
handler500 = handler500_view
