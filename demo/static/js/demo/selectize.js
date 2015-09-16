$(document).ready(function() {
    $('[data-agnocomplete]').each(function(index, select) {
        $(select).selectize({
            valueField: 'value',
            labelField: 'label',
            searchField: 'label',
            create: false,
            load: function(query, callback) {
                // Using the query size limit to avoid querying too soon.
                if (query.length < $(select).data('query-size'))
                    return callback();
                // Query's ready
                $.ajax({
                    url: $(select).data('url') + '?q=' + encodeURIComponent(query),
                    type: 'GET',
                    error: function() {
                        callback();
                    },
                    success: function(res) {
                        callback(res.data);
                    }
                });
            }
        });
    });
});
