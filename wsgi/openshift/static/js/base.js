$(function () {
    $('.lightbox-type').lightbox ()

    $(document).on("submit", '.jquery-lightbox-html form', null, function(ev) {
        var $form = $(ev.currentTarget)
        $.post($form.attr("action"), $form.serialize(), function(data){
            $form.parent().html(data)
        })
        return false
    })

    $(document).ready(function() {
        $(".wide").parent(".container").removeClass('container').addClass('dashboard-container')
    })


    var selectCurrentWeek = function(that) {
        window.setTimeout(function () {
            $(that).find('.ui-datepicker-current-day a').addClass('ui-state-active')
        }, 1);
    }

    var collapseToCurrentWeek = function(that) {
        window.setTimeout(function () {
            $(that).find("tbody tr:not(:has(.ui-datepicker-current-day))").hide()
            var is_caret = $(that).find(".ui-datepicker-title .caret").show()
            if (is_caret.length == 0)
                $(that).find(".ui-datepicker-year").after("<b class='caret'></b>")
        }, 1);
    }

    var startDate;
    var endDate;

    $('.weekdate-picker').datepicker( {
        showOtherMonths: true,
        selectOtherMonths: true,
        showWeek: true,
        firstDay: 1,
        onSelect: function(dateText, inst) {
            var date = $(this).datepicker('getDate');
            var dateFormat = inst.settings.dateFormat || $.datepicker._defaults.dateFormat;
            if (! $(this).datepicker("option", "selectDate"))
            {
                var firstDay = $(this).datepicker("option", "firstDay")
                startDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + firstDay);
                endDate = new Date(date.getFullYear(), date.getMonth(), date.getDate() - date.getDay() + 6 + firstDay);

                selectCurrentWeek(this);
                collapseToCurrentWeek(this);
                var formatStart = $.datepicker.formatDate("yy-mm-dd", startDate);
                var formatEnd = $.datepicker.formatDate("yy-mm-dd", endDate);
                var fragment = "from"+formatStart+"to"+formatEnd
                if (typeof dashboard_router != 'undefined')
                    dashboard_router.navigate(fragment, {trigger:true});
                else
                    window.location=dashboardUrl+"#"+fragment
            } else {
                var formatted = $.datepicker.formatDate("yy-mm-dd", date);
                if (typeof dashboard_router != 'undefined')
                    dashboard_router.navigate(formatted, {trigger:true});
                else
                    window.location=dashboardUrl+"#"+formatted
                collapseToCurrentWeek(this);
            }
            //$('#endDate').text($.datepicker.formatDate( dateFormat, endDate, inst.settings ));
        },
        beforeShowDay: function(date) {
            var cssClass = '';
            if(date >= startDate && date <= endDate)
                cssClass = 'ui-datepicker-current-day';
            return [true, cssClass];
        },
        onChangeMonthYear: function(year, month, inst) {
            selectCurrentWeek(this);
        }
    });



    collapseToCurrentWeek($('#dashboard-picker'))
    //$('#dashboard-picker').datepicker("option", "selectDate", true );

    if (typeof dashboard_router != 'undefined')
    {
        var current_date = new Date(Backbone.history.fragment)
        if (Backbone.history.fragment == "")
        {
            current_date = new Date()
            var formatted = $.datepicker.formatDate("yy-mm-dd", current_date);
            dashboard_router.navigate(formatted, {trigger:false});
        }
        $('#dashboard-picker').datepicker("setDate", current_date );
    }

    $("#dashboard-picker").datepicker($.datepicker.regional[ "fi" ] );
    $(".weekdate-picker .ui-datepicker-title").live("click", function() {
        $(this).parents(".ui-datepicker").find("tbody tr").show()
        $(this).find(".caret").hide()
    })

    $('.weekdate-picker .ui-datepicker-calendar tr').live('mousemove', function() { $(this).find('td a').addClass('ui-state-hover'); });
    $('.weekdate-picker .ui-datepicker-calendar tr').live('mouseleave', function() { $(this).find('td a').removeClass('ui-state-hover'); });

    $('.mainnav li:eq(0)').live('mousemove', function() {
        $(this).parents(".subnavbar-inner").next(".subnavbar-inner").removeClass("collapse");
    });
    $('.subnavbar:has(li:eq(0):not(.active))').on('mouseleave', function() {
        $(this).find(".subnavbar-inner:eq(1)").addClass("collapse");
    });
});

