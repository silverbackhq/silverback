"""
    Routes For Silverback
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.urls import include, path

# Local Library
from app.controllers.web.status_page import StatusPageIndex as StatusPageIndexView
from app.controllers.web.status_page import StatusPageHistory as StatusPageHistoryView
from app.controllers.web.status_page import StatusPageSingle as StatusPageSingleView
from app.controllers.web.install import Install as InstallView
from app.controllers.web.not_found import handler404 as handler404_view
from app.controllers.web.error import handler500 as handler500_view
from app.controllers.web.login import Login as LoginView
from app.controllers.web.register import Register as RegisterView
from app.controllers.web.forgot_password import ForgotPassword as ForgotPasswordView
from app.controllers.web.reset_password import ResetPassword as ResetPasswordView
from app.controllers.web.statistics import Statistics as StatisticsView
from app.controllers.web.history import AtomHistory as AtomHistoryView
from app.controllers.web.history import RssHistory as RssHistoryView
from app.controllers.web.health_check import HealthCheck as HealthCheckView
from app.controllers.web.admin.logout import Logout as LogoutView
from app.controllers.web.admin.dashboard import Dashboard as DashboardView
from app.controllers.web.admin.profile import Profile as ProfileView
from app.controllers.web.admin.settings import Settings as SettingsView
from app.controllers.web.admin.builder import Builder as BuilderView
from app.controllers.web.admin.activity import Activity as ActivityView
from app.controllers.web.admin.notification import Notification as NotificationView
from app.controllers.web.admin.user import UserList as UserListWeb
from app.controllers.web.admin.user import UserEdit as UserEditWeb
from app.controllers.web.admin.user import UserAdd as UserAddWeb
from app.controllers.web.admin.component import ComponentList as ComponentListView
from app.controllers.web.admin.component import ComponentAdd as ComponentAddView
from app.controllers.web.admin.component import ComponentEdit as ComponentEditView
from app.controllers.web.admin.component_group import ComponentGroupList as ComponentGroupListView
from app.controllers.web.admin.component_group import ComponentGroupAdd as ComponentGroupAddView
from app.controllers.web.admin.component_group import ComponentGroupEdit as ComponentGroupEditView
from app.controllers.web.admin.incident import IncidentList as IncidentListView
from app.controllers.web.admin.incident import IncidentAdd as IncidentAddView
from app.controllers.web.admin.incident import IncidentEdit as IncidentEditView
from app.controllers.web.admin.incident import IncidentView as IncidentViewView
from app.controllers.web.admin.incident_update import IncidentUpdateAdd as IncidentUpdateAddView
from app.controllers.web.admin.incident_update import IncidentUpdateEdit as IncidentUpdateEditView
from app.controllers.web.admin.incident_update import IncidentUpdateView as IncidentUpdateViewView
from app.controllers.web.admin.metric import MetricList as MetricListView
from app.controllers.web.admin.metric import MetricAdd as MetricAddView
from app.controllers.web.admin.metric import MetricEdit as MetricEditView
from app.controllers.web.admin.subscriber import SubscriberList as SubscriberListView
from app.controllers.web.admin.subscriber import SubscriberAdd as SubscriberAddView
from app.controllers.web.admin.subscriber import SubscriberEdit as SubscriberEditView
from app.controllers.api.private.v1.install import Install as InstallV1EndpointPrivate
from app.controllers.api.private.v1.status import StatusSubscribe as StatusSubscribeV1EndpointPrivate
from app.controllers.api.private.v1.login import Login as LoginV1EndpointPrivate
from app.controllers.api.private.v1.register import Register as RegisterV1EndpointPrivate
from app.controllers.api.private.v1.forgot_password import ForgotPassword as ForgotPasswordV1EndpointPrivate
from app.controllers.api.private.v1.reset_password import ResetPassword as ResetPasswordV1EndpointPrivate
from app.controllers.api.private.v1.admin.settings import Settings as SettingsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.profile import Profile as ProfileAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.notifications import Notifications as NotificationsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.notifications import LatestNotifications as LatestNotificationsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.user import User as UserAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.user import Users as UsersAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.component_group import ComponentGroup as ComponentGroupAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.component_group import ComponentGroups as ComponentGroupsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.component import Component as ComponentAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.component import Components as ComponentsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.incident import Incident as IncidentAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.incident import Incidents as IncidentsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.incident_update import IncidentUpdate as IncidentUpdateAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.incident_update import IncidentUpdates as IncidentUpdatesAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.incident_update import IncidentUpdatesNotify as IncidentUpdatesNotifyAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.incident_update import IncidentUpdatesComponents as IncidentUpdatesComponentsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.incident_update import IncidentUpdatesComponent as IncidentUpdatesComponentAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.metric import Metric as MetricAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.metric import Metrics as MetricsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.metric import NewRelicApps as NewRelicAppsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.subscriber import Subscriber as SubscriberAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.subscriber import Subscribers as SubscribersAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.activity import Activities as ActivitiesAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.builder import BuilderSettings as BuilderSettingsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.builder import BuilderComponents as BuilderComponentsAdminV1EndpointPrivate
from app.controllers.api.private.v1.admin.builder import BuilderSystemMetrics as BuilderSystemMetricsAdminV1EndpointPrivate


urlpatterns = [
    # Public Views
    path('', StatusPageIndexView.as_view(), name='app.web.status_page_index'),
    path('history/<int:period>', StatusPageHistoryView.as_view(), name='app.web.status_page_history'),
    path('incidents/<uri>', StatusPageSingleView.as_view(), name='app.web.status_page_single'),
    path('install', InstallView.as_view(), name='app.web.install'),
    path('login', LoginView.as_view(), name='app.web.login'),
    path('register/<token>', RegisterView.as_view(), name='app.web.register'),
    path('forgot-password', ForgotPasswordView.as_view(), name='app.web.forgot_password'),
    path('reset-password/<token>', ResetPasswordView.as_view(), name='app.web.reset_password'),
    path('statistics/<type>', StatisticsView.as_view(), name='app.web.statistics'),
    path('history.atom', AtomHistoryView.as_view(), name='app.web.history_atom'),
    path('history.rss', RssHistoryView.as_view(), name='app.web.history_rss'),
    path('_healthcheck', HealthCheckView.as_view(), name='app.web.health_check'),

    # Authenticated Users Views
    path('admin/', include([

        path('logout', LogoutView.as_view(), name='app.web.admin.logout'),
        path('dashboard', DashboardView.as_view(), name='app.web.admin.dashboard'),
        path('profile', ProfileView.as_view(), name='app.web.admin.profile'),
        path('activity', ActivityView.as_view(), name='app.web.admin.activity.list'),
        path('notifications', NotificationView.as_view(), name='app.web.admin.notification.list'),
        path('settings', SettingsView.as_view(), name='app.web.admin.settings'),
        path('builder', BuilderView.as_view(), name='app.web.admin.builder'),
        path('users', UserListWeb.as_view(), name='app.web.admin.user.list'),
        path('users/add', UserAddWeb.as_view(), name='app.web.admin.user.add'),
        path('users/edit/<int:user_id>', UserEditWeb.as_view(), name='app.web.admin.user.edit'),

        path('components', ComponentListView.as_view(), name='app.web.admin.component.list'),
        path('components/add', ComponentAddView.as_view(), name='app.web.admin.component.add'),
        path('components/edit/<int:component_id>', ComponentEditView.as_view(), name='app.web.admin.component.edit'),

        path('component-groups', ComponentGroupListView.as_view(), name='app.web.admin.component_group.list'),
        path('component-groups/add', ComponentGroupAddView.as_view(), name='app.web.admin.component_group.add'),
        path('component-groups/edit/<int:group_id>', ComponentGroupEditView.as_view(), name='app.web.admin.component_group.edit'),

        path('incidents', IncidentListView.as_view(), name='app.web.admin.incident.list'),
        path('incidents/add', IncidentAddView.as_view(), name='app.web.admin.incident.add'),
        path('incidents/edit/<int:incident_id>', IncidentEditView.as_view(), name='app.web.admin.incident.edit'),
        path('incidents/view/<int:incident_id>', IncidentViewView.as_view(), name='app.web.admin.incident.view'),

        path('incidents/view/<int:incident_id>/updates/add', IncidentUpdateAddView.as_view(), name='app.web.admin.incident_update.add'),
        path('incidents/view/<int:incident_id>/updates/edit/<int:update_id>', IncidentUpdateEditView.as_view(), name='app.web.admin.incident_update.edit'),
        path('incidents/view/<int:incident_id>/updates/view/<int:update_id>', IncidentUpdateViewView.as_view(), name='app.web.admin.incident_update.view'),

        path('metrics', MetricListView.as_view(), name='app.web.admin.metric.list'),
        path('metrics/add', MetricAddView.as_view(), name='app.web.admin.metric.add'),
        path('metrics/edit/<int:metric_id>', MetricEditView.as_view(), name='app.web.admin.metric.edit'),

        path('subscribers', SubscriberListView.as_view(), name='app.web.admin.subscriber.list'),
        path('subscribers/add', SubscriberAddView.as_view(), name='app.web.admin.subscriber.add'),
        path('subscribers/edit/<int:subscriber_id>', SubscriberEditView.as_view(), name='app.web.admin.subscriber.edit'),

    ])),

    # Private API V1 Endpoints
    path('api/private/v1/', include([

        path('status_subscribe', StatusSubscribeV1EndpointPrivate.as_view(), name='app.api.private.v1.status_subscribe.endpoint'),
        path('install', InstallV1EndpointPrivate.as_view(), name='app.api.private.v1.install.endpoint'),
        path('login', LoginV1EndpointPrivate.as_view(), name='app.api.private.v1.login.endpoint'),
        path('register', RegisterV1EndpointPrivate.as_view(), name='app.api.private.v1.register.endpoint'),
        path('forgot-password', ForgotPasswordV1EndpointPrivate.as_view(), name='app.api.private.v1.forgot_password.endpoint'),
        path('reset-password', ResetPasswordV1EndpointPrivate.as_view(), name='app.api.private.v1.reset_password.endpoint'),

        path('admin/', include([
            path(
                'settings',
                SettingsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.settings.endpoint'
            ),
            path(
                'profile',
                ProfileAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.profile.endpoint'
            ),
            path(
                'notification',
                NotificationsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.notifications.endpoint'
            ),
            path(
                'latest_notifications',
                LatestNotificationsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.latest_notifications.endpoint'
            ),
            path(
                'user',
                UsersAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.users.endpoint'
            ),
            path(
                'user/<int:user_id>',
                UserAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.user.endpoint'
            ),
            path(
                'component-group',
                ComponentGroupsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.component_groups.endpoint'
            ),
            path(
                'component-group/<int:group_id>',
                ComponentGroupAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.component_group.endpoint'
            ),
            path(
                'component',
                ComponentsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.components.endpoint'
            ),
            path(
                'component/<int:component_id>',
                ComponentAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.component.endpoint'
            ),
            path(
                'incident',
                IncidentsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.incidents.endpoint'
            ),
            path(
                'incident/<int:incident_id>',
                IncidentAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.incident.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>',
                IncidentUpdatesAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.incident_updates.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>',
                IncidentUpdateAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.incident_update.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>/notify',
                IncidentUpdatesNotifyAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.incident_update.notify.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>/components',
                IncidentUpdatesComponentsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.incident_update.components.endpoint'
            ),
            path(
                'incident-update/<int:incident_id>/<int:update_id>/component/<int:item_id>',
                IncidentUpdatesComponentAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.incident_update.component.endpoint'
            ),
            path(
                'metric',
                MetricsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.metrics.endpoint'
            ),
            path(
                'metric/<int:metric_id>',
                MetricAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.metric.endpoint'
            ),
            path(
                'subscriber',
                SubscribersAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.subscribers.endpoint'
            ),
            path(
                'subscriber/<int:subscriber_id>',
                SubscriberAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.subscriber.endpoint'
            ),
            path(
                'activity',
                ActivitiesAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.activities.endpoint'
            ),
            path(
                'action/metric/new-relic-apps',
                NewRelicAppsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.metric.action.new_relic_apps.endpoint'
            ),
            path(
                'builder/settings',
                BuilderSettingsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.builder.settings.endpoint'
            ),
            path(
                'builder/component',
                BuilderComponentsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.builder.components.endpoint'
            ),
            path(
                'builder/component/<component_id>',
                BuilderComponentsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.builder.component.endpoint'
            ),
            path(
                'builder/metric',
                BuilderSystemMetricsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.builder.metrics.endpoint'
            ),
            path(
                'builder/metric/<metric_id>',
                BuilderSystemMetricsAdminV1EndpointPrivate.as_view(),
                name='app.api.private.v1.admin.builder.metric.endpoint'
            ),
        ]))

    ])),

    # Public API V1 Endpoints
    path('api/public/v1/', include([

    ]))
]

handler404 = handler404_view
handler500 = handler500_view
