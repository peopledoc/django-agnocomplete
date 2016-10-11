$(document).ready(function() {

    function errorCallback(resp) {
        $('.error').remove();
        errors = resp.responseJSON.errors;
        status = resp.status;
        console.debug(status);
        console.debug(errors);
        content = '<div class="error">Error status code: ' + status;
        content += '<ul>';
        for (var i = 0; i < errors.length; i++) {
            content += '<li>' + errors[i].title + ': ' + errors[i].detail + '</li>';
        }
        content += '<ul></div>';
        $('#search-form').after(content);
    }

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
                    error: function(resp) {
                        errorCallback(resp);
                    },
                    success: function(res) {
                        callback(res.data);
                    }
                });
            }
        });
    });
});
