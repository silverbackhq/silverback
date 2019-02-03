require(['jscookie', 'toastr', 'pace', 'vue', 'axios']);

$.jMaskGlobals.watchDataMask = true;

var silverback_app = silverback_app || {};


/**
 * App Install
 */
silverback_app.install_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_install',
        data() {
            return {
                isInProgress: false,
            }
        },
        methods: {
            installAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * App Notifications
 */
silverback_app.notifications = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_notifications',
        data() {
            return {
                notification_status: 'read',
                notifications: []
            }
        },
        mounted() {
            this.fetch();
            setInterval(() => {
                this.fetch()
            }, 3000)
        },
        methods: {
            fetch() {
                axios.get(app_globals.notifications_endpoint)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.notifications = response.data.payload.notifications;
                            this.notification_status = response.data.payload.status;
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
            },
            mouseOver(id, delivered) {
                if (delivered == false) {
                    const params = new URLSearchParams();
                    params.append('notification_id', id);
                    axios({
                        method: 'post',
                        url: app_globals.notifications_endpoint,
                        data: params
                    });
                }
            }
        }
    });

}


/**
 * Manage Settings
 */
silverback_app.manage_settings_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#manage_settings',
        data() {
            return {
                isInProgress: false,
            }
        },
        methods: {
            updateSettingsAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                        this.isInProgress = false;
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * App Login
 */
silverback_app.login_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_login',
        data() {
            return {
                isInProgress: false,
            }
        },
        methods: {
            loginAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * App Register
 */
silverback_app.register_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_register',
        data() {
            return {
                isInProgress: false,
            }
        },
        methods: {
            registerAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * App Forgot Password
 */
silverback_app.forgot_password_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_forgot_password',
        data() {
            return {
                isInProgress: false,
            }
        },
        methods: {
            forgotPasswordAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * App Reset Password
 */
silverback_app.reset_password_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_reset_password',
        data() {
            return {
                isInProgress: false,
            }
        },
        methods: {
            resetPasswordAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * App Profile
 */
silverback_app.profile_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#app_profile',
        data() {
            return {
                isUpdatePasswordInProgress: false,
                isUpdateProfileInProgress: false,
                isUpdateAccessTokenInProgress: false,
                isUpdateRefreshTokenInProgress: false
            }
        },
        methods: {
            updatePassword(event) {
                event.preventDefault();
                this.isUpdatePasswordInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.reload();
                            }, _form.attr('data-reload-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isUpdatePasswordInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isUpdatePasswordInProgress = false;
                    });
                });
            },
            updateProfile(event) {
                event.preventDefault();
                this.isUpdateProfileInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.reload();
                            }, _form.attr('data-reload-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isUpdateProfileInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isUpdateProfileInProgress = false;
                    });
                });
            },

            updateAccessToken(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                this.isUpdateAccessTokenInProgress = true;

                var _self = $(event.target);

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _self.attr('data-url'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken'),
                            "action": "_update_access_token",
                            "token": $('input[name="access_token"]').val()
                        }
                    }).done((response) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            $('input[name="access_token"]').val(response.payload.token);
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                        this.isUpdateAccessTokenInProgress = false;
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isUpdateAccessTokenInProgress = false;
                    });
                });
            },
            updateRefreshToken(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                this.isUpdateRefreshTokenInProgress = true;

                var _self = $(event.target);

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _self.attr('data-url'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken'),
                            "action": "_update_refresh_token",
                            "token": $('input[name="refresh_token"]').val()
                        }
                    }).done((response) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            $('input[name="refresh_token"]').val(response.payload.token);
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                        this.isUpdateRefreshTokenInProgress = false;
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isUpdateRefreshTokenInProgress = false;
                    });
                });
            },

        }
    });
}


/**
 * User Add
 */
silverback_app.add_user_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#user_add_app',
        data() {
            return {
                isInProgress: false,
                disableInvitation: false
            }
        },
        methods: {
            addUserAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * User Edit
 */
silverback_app.edit_user_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#user_edit_app',
        data() {
            return {
                isInProgress: false,
                updatePassword: false
            }
        },
        methods: {
            editUserAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * App User List
 */
silverback_app.user_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#user_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#user_list').attr('data-fetch-users') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.users);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadUsersAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            },
            deleteUserAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Component Group Add
 */
silverback_app.add_component_group_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#component_group_add_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            addGroupAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * Component Group Edit
 */
silverback_app.edit_component_group_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#component_group_edit_app',
        data() {
            return {
                isInProgress: false,
                updatePassword: false
            }
        },
        methods: {
            editGroupAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * Component Group List
 */
silverback_app.component_group_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#component_group_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#component_group_list').attr('data-fetch-component_groups') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.groups);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadGroupsAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            },
            deleteGroupAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Component Add
 */
silverback_app.add_component_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#component_add_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            addComponentAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * Component Edit
 */
silverback_app.edit_component_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#component_edit_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            editComponentAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}

/**
 * Component List
 */
silverback_app.component_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#component_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#component_list').attr('data-fetch-components') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.components);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadComponentsAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            },
            deleteComponentAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Incident Add
 */
silverback_app.add_incident_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#incident_add_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            addIncidentAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * Incident Edit
 */
silverback_app.edit_incident_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#incident_edit_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            editIncidentAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}

/**
 * Incident List
 */
silverback_app.incident_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#incident_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#incident_list').attr('data-fetch-incidents') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.incidents);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadIncidentsAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            },
            deleteIncidentAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Update Add
 */
silverback_app.add_update_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#update_add_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            addUpdateAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * Update Edit
 */
silverback_app.edit_update_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#update_edit_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            editUpdateAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}

/**
 * Update List
 */
silverback_app.update_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#update_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#update_list').attr('data-fetch-updates') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.updates);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadUpdatesAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            },
            deleteUpdateAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Metric Add
 */
silverback_app.add_metric_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#metric_add_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            addMetricAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * Metric Edit
 */
silverback_app.edit_metric_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#metric_edit_app',
        data() {
            return {
                isInProgress: false
            }
        },
        methods: {
            editMetricAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}

/**
 * Metric List
 */
silverback_app.metric_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#metric_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#metric_list').attr('data-fetch-metrics') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.metrics);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadMetricsAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            },
            deleteMetricAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Subscriber Add
 */
silverback_app.add_subscriber_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#subscriber_add_app',
        data() {
            return {
                isInProgress: false,
                subscriptionType: ""
            }
        },
        methods: {
            addSubscriberAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}


/**
 * Subscriber Edit
 */
silverback_app.edit_subscriber_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#subscriber_edit_app',
        data() {
            return {
                isInProgress: false,
                subscriptionType: $('select[name="type"]').val()
            }
        },
        methods: {
            editSubscriberAction(event) {
                event.preventDefault();
                this.isInProgress = true;

                var _self = $(event.target);
                var _form = _self.closest("form");

                var inputs = {};
                _form.serializeArray().map((item, index) => {
                    inputs[item.name] = item.value;
                });

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _form.attr('action'),
                        data: inputs
                    }).done((response, textStatus, jqXHR) => {
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.href = _form.attr('data-redirect-url');
                            }, _form.attr('data-redirect-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                            this.isInProgress = false;
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        toastr.clear();
                        toastr.error(error);
                        this.isInProgress = false;
                    });
                });
            }
        }
    });
}

/**
 * Subscriber List
 */
silverback_app.subscriber_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#subscriber_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#subscriber_list').attr('data-fetch-subscribers') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.subscribers);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadSubscribersAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            },
            deleteSubscriberAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Activity List
 */
silverback_app.activity_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#activity_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#activity_list').attr('data-fetch-activities') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.activities);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadActivitiesAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            }
        }
    });

}


/**
 * Incident Update View
 */
silverback_app.incident_update_view_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#incident_update_view',
        data() {
            return {

            }
        },
        methods: {
            addAffectedComponentAction(event){
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                if(_self.prop("tagName") == "I"){
                    _self = _self.closest("a");
                }

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _self.attr('data-url'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken'),
                            "component_id": _self.closest("tr").find('[name="component"]').val(),
                            "type":  _self.closest("tr").find('[name="type"]').val()
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.reload();
                            }, _self.attr('data-reload-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            },
            deliverNotificationsAction(event){
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                if(_self.prop("tagName") == "I"){
                    _self = _self.closest("a");
                }

                _self.attr('disabled', 'disabled');

                Pace.track(() => {
                    $.ajax({
                        method: "POST",
                        url: _self.attr('data-url'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            setTimeout(() => {
                                location.reload();
                            }, _self.attr('data-reload-after'));
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            },
            deleteAffectedComponentAction(event) {
                event.preventDefault();

                if (!confirm(_i18n.confirm_msg)) {
                    return false;
                }

                var _self = $(event.target);

                if(_self.prop("tagName") == "I"){
                    _self = _self.closest("a");
                }

                _self.attr('disabled', 'disabled');
                Pace.track(() => {
                    $.ajax({
                        method: "DELETE",
                        url: _self.attr('data-url') + "?csrfmiddlewaretoken=" + Cookies.get('csrftoken'),
                        data: {
                            "csrfmiddlewaretoken": Cookies.get('csrftoken')
                        }
                    }).done((response) => {
                        _self.removeAttr("disabled");
                        if (response.status == "success") {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.success(messageObj.message);
                                break;
                            }
                            _self.closest("tr").remove();
                        } else {
                            for (var messageObj of response.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    }).fail((jqXHR, textStatus, error) => {
                        _self.removeAttr("disabled");
                        toastr.clear();
                        toastr.error(error);
                    });
                });
            }
        }
    });

}


/**
 * Notification List
 */
silverback_app.notification_list_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#notification_list',
        data() {
            return {
                items: [],
                isDimmerActive: true,
                isLoadingActive: false,
                isLoadingDimmed: false,
                errored: false,
                i18n: _list_view_i18n,
                limit: 20,
                offset: 0
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {
                axios.get($('#notification_list').attr('data-fetch-notifications') + "?limit=" + this.limit + "&offset=" + this.offset)
                    .then(response => {
                        if (response.data.status == "success") {
                            this.items = this.items.concat(response.data.payload.notifications);
                            this.offset += this.limit
                            count = response.data.payload.metadata.count
                            if (count > this.offset){
                                this.isLoadingActive = true
                                this.isLoadingDimmed = false
                            }else{
                                this.isLoadingActive = false
                                this.isLoadingDimmed = false
                            }
                        } else {
                            for (var messageObj of response.data.messages) {
                                toastr.clear();
                                toastr.error(messageObj.message);
                                break;
                            }
                        }
                    })
                    .catch(error => {
                        toastr.clear();
                        toastr.error(error);
                    })
                    .finally(() => this.isDimmerActive = false)
            },
            loadNotificationsAction(event) {
                event.preventDefault();
                this.isLoadingDimmed = true
                this.fetch();
            }
        }
    });

}


/**
 * Dashboard
 */
silverback_app.dashboard_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

    return new Vue({
        delimiters: ['${', '}'],
        el: '#dashboard',
        data() {
            return {
                count: {
                    incidents: 2
                },
                color: "red"
            }
        },
        mounted() {
            this.fetch();
        },

        methods: {
            fetch() {

            }
        }
    });

}


$(document).ready(() => {

    $(document).ajaxStart(() => {
        require(['pace'], (Pace) => {
            Pace.restart();
        });
    });

    require(['vue', 'axios', 'jscookie', 'jquery', 'pace', 'toastr'], (Vue, axios, Cookies, $, Pace, toastr) => {
        axios.defaults.headers.common = {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': Cookies.get('csrftoken')
        };

        $.ajaxSetup({
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken')
            }
        });

        if (document.getElementById("app_notifications")) {
            silverback_app.notifications(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("manage_settings")) {
            silverback_app.manage_settings_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_login")) {
            silverback_app.login_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_register")) {
            silverback_app.register_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_forgot_password")) {
            silverback_app.forgot_password_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_reset_password")) {
            silverback_app.reset_password_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_install")) {
            silverback_app.install_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_profile")) {
            silverback_app.profile_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("user_add_app")) {
            silverback_app.add_user_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("user_edit_app")) {
            silverback_app.edit_user_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("user_list")) {
            silverback_app.user_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("component_group_add_app")) {
            silverback_app.add_component_group_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("component_group_edit_app")) {
            silverback_app.edit_component_group_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("component_group_list")) {
            silverback_app.component_group_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("component_add_app")) {
            silverback_app.add_component_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("component_edit_app")) {
            silverback_app.edit_component_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("component_list")) {
            silverback_app.component_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("incident_add_app")) {
            silverback_app.add_incident_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("incident_edit_app")) {
            silverback_app.edit_incident_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("incident_list")) {
            silverback_app.incident_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("update_add_app")) {
            silverback_app.add_update_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("update_edit_app")) {
            silverback_app.edit_update_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("update_list")) {
            silverback_app.update_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("metric_add_app")) {
            silverback_app.add_metric_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("metric_edit_app")) {
            silverback_app.edit_metric_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("metric_list")) {
            silverback_app.metric_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("subscriber_add_app")) {
            silverback_app.add_subscriber_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("subscriber_edit_app")) {
            silverback_app.edit_subscriber_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("subscriber_list")) {
            silverback_app.subscriber_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("activity_list")) {
            silverback_app.activity_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("incident_update_view")) {
            silverback_app.incident_update_view_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("notification_list")) {
            silverback_app.notification_list_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("dashboard")) {
            silverback_app.dashboard_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
    });

});


/**
 *
 */
let hexToRgba = function(hex, opacity) {
    let result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    let rgb = result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
    return 'rgba(' + rgb.r + ', ' + rgb.g + ', ' + rgb.b + ', ' + opacity + ')';
};

$(document).ready(function() {

    /** Constant div card */
    const DIV_CARD = 'div.card';

    /** Initialize tooltips */
    $('[data-toggle="tooltip"]').tooltip();

    /** Initialize popovers */
    $('[data-toggle="popover"]').popover({
        html: true
    });

    /** Function for remove card */
    $('[data-toggle="card-remove"]').on('click', function(e) {
        let $card = $(this).closest(DIV_CARD);
        $card.remove();
        e.preventDefault();
        return false;
    });

    /** Function for collapse card */
    $('[data-toggle="card-collapse"]').on('click', function(e) {
        let $card = $(this).closest(DIV_CARD);
        $card.toggleClass('card-collapsed');
        e.preventDefault();
        return false;
    });

    /** Function for fullscreen card */
    $('[data-toggle="card-fullscreen"]').on('click', function(e) {
        let $card = $(this).closest(DIV_CARD);
        $card.toggleClass('card-fullscreen').removeClass('card-collapsed');
        e.preventDefault();
        return false;
    });

    /**  */
    if ($('[data-sparkline]').length) {
        let generateSparkline = function($elem, data, params) {
            $elem.sparkline(data, {
                type: $elem.attr('data-sparkline-type'),
                height: '100%',
                barColor: params.color,
                lineColor: params.color,
                fillColor: 'transparent',
                spotColor: params.color,
                spotRadius: 0,
                lineWidth: 2,
                highlightColor: hexToRgba(params.color, .6),
                highlightLineColor: '#666',
                defaultPixelsPerValue: 5
            });
        }
        require(['sparkline'], function() {
            $('[data-sparkline]').each(function() {
                let $chart = $(this);
                generateSparkline($chart, JSON.parse($chart.attr('data-sparkline')), {
                    color: $chart.attr('data-sparkline-color')
                });
            });
        });
    }

    /**  */
    if ($('.chart-circle').length) {
        require(['circle-progress'], function() {
            $('.chart-circle').each(function() {
                let $this = $(this);

                $this.circleProgress({
                    fill: {
                        color: tabler.colors[$this.attr('data-color')] || tabler.colors.blue
                    },
                    size: $this.height(),
                    startAngle: -Math.PI / 4 * 2,
                    emptyFill: '#F4F4F4',
                    lineCap: 'round'
                });
            });
        });
    }
});