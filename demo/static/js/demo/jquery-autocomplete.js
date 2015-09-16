$(document).ready(function() {
    $('[data-agnocomplete]').each(function(index, input) {
        $(input).autocomplete({
            source: function(request, response) {
                var element = $(this.element);
                var url = $(element).data('url');
                $.getJSON(
                    url,
                    {q: request.term},
                    function(data) {
                        response(data.data);
                    }
                );
            },
            minLength: $(this).data("query-size"),
            select: function(event, ui) {
                event.preventDefault();
                $(input).val(ui.item.label);
            },
            focus: function(event, ui) {
                event.preventDefault();
                $(input).val(ui.item.label);
            }
        });
    });
});
