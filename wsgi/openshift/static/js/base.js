$(function () {
    $('.lightbox-type').lightbox ()

    $(document).on("submit", '.jquery-lightbox-html form', null, function(ev) {
        var $form = $(ev.currentTarget)
        $.post($form.attr("action"), $form.serialize(), function(data){
            $form.parent().html(data)
        })
        return false
    })
});

