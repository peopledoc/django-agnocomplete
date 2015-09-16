$(function() {
    $('[data-agnocomplete]').each(function(index, input) {
        $(input).typeahead({
            minLength: $(this).data("query-size")
        }, {
            name: 'typeahead__' + $(input).attr('id'),
            display: 'label',
            source: new Bloodhound({
                datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
                queryTokenizer: Bloodhound.tokenizers.whitespace,
                remote: {
                    url: $(input).data('url') + '?q=' + '%QUERY',
                    wildcard: '%QUERY',
                    transform: function(data) {
                        return data.data;
                    }
                }
            })
        });
    });
});
