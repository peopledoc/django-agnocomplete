$(function() {
    $('[data-agnocomplete]').each(function(index, select) {
        $(select).select2({
            width: '100%',
            ajax: {
                url: $(select).data('url'),
                dataType: 'json',
                data: function (params) {
                    return {
                        q: params.term
                    };
                },
                processResults: function (data) {
                    var results = [];
                    $.each(data.data, function(index, item) {
                        results.push({id: item.value, label: item.label});
                    });
                    return { results: results };
                }
            },
            minimumInputLength: $(select).data('query-size'),
            templateResult: function(item) { return item.label; },
            templateSelection: function(item) { return item.label; }
        });
    });
});
