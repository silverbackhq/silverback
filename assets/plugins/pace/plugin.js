require.config({
    paths: {
        'pace': 'static/plugins/pace/pace.min'
    }
});

require(['pace'], function (pace) {
  pace.start({document: false});
});