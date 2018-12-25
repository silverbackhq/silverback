require.config({
    paths: {
        'pace': 'assets/plugins/pace/pace.min'
    }
});

require(['pace'], function (pace) {
  pace.start({document: false});
});