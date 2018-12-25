require(['jscookie', 'toastr', 'pace', 'vue', 'axios']);

var kraven_app = kraven_app || {};


/**
 * App Install
 */
kraven_app.install_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

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
kraven_app.notifications = (Vue, axios, $, Pace, Cookies, toastr) => {

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
kraven_app.manage_settings_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

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
kraven_app.login_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

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
kraven_app.register_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

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
kraven_app.forgot_password_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

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
kraven_app.reset_password_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

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
kraven_app.profile_screen = (Vue, axios, $, Pace, Cookies, toastr) => {

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
            kraven_app.notifications(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("manage_settings")) {
            kraven_app.manage_settings_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_login")) {
            kraven_app.login_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_register")) {
            kraven_app.register_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_forgot_password")) {
            kraven_app.forgot_password_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_reset_password")) {
            kraven_app.reset_password_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_install")) {
            kraven_app.install_screen(
                Vue,
                axios,
                $,
                Pace,
                Cookies,
                toastr
            );
        }
        if (document.getElementById("app_profile")) {
            kraven_app.profile_screen(
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