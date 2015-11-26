$(document).ready(function() {
    $('[data-agnocomplete]').each(function(index, select) {

        function getMaxItems() {
            var multi = $(select).attr('multiple') || false;
            if (multi) {
                // null means no limit to maxItems
                return null;
            }
            return 1;
        }

        $(select).selectize({
            valueField: 'value',
            labelField: 'label',
            searchField: 'label',
            maxItems: getMaxItems(),
            create: Boolean($(select).data('create')),
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
