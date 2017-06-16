/**
 * Created by Bree on 20.05.2017.
 */

// Whole-script strict mode syntax
'use strict';
var lastQuery = "";

$(document).ready(function () {
    // prevents that arrays in get requests get encoded with brackets.
    jQuery.ajaxSettings.traditional = true;

    $('.ingredient-formset').formset({
        addText: '<button class="btn btn-info"><span class="glyphicon glyphicon-plus"></span> Add ingredient</button>',
        deleteText: '<span class="btn btn-info btn-xs"><span class="glyphicon glyphicon-trash"></span> Remove</span>',
        prefix: 'ingredient'
    });

    $('.category-formset').formset({
        addText: '<button class="btn btn-info"><span class="glyphicon glyphicon-plus"></span> Add category</button>',
        deleteText: '<span class="btn btn-info btn-xs"><span class="glyphicon glyphicon-trash"></span> Remove</span>',
        prefix: 'category'
    });

    $('#searchbar').keyup(function (evt) {
        delay(function () {
            getRecipesAndFilters();
        }, 200);
    });

    $(document).on('click', '.recipefilter', function (evt) {
        if ($(this).hasClass("selected-filter")) {
            $(this).removeClass("selected-filter");
        } else {
            $(this).addClass("selected-filter");
        }
        getRecipesAndFilters();
    });

});

var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

function getRecipesAndFilters() {
    var query = $('#searchbar').val();
    if(lastQuery.trim() != query.trim()){
        lastQuery = query;
    $.get('/recipes/', {'q': $('#searchbar').val(), 'initialized': 1, 'filter': getSelectedFilters()}, function (data) {
        var query = $('#searchbar').val();
        prepareRecipeList(data.latest_recipes_list);
        prepareFilters(data.filters, data.selected_filters);
    });
    }
}

function getSelectedFilters() {
    var filterIDs = $.map($(".selected-filter"), function (n, i) {
        return n.id;
    });
    return filterIDs;
}

function prepareRecipeList(recipe_list) {
    var recipe_html = "";
    $.each(JSON.parse(recipe_list), function (i, el) {
        var elem = '<li><a href="/recipes/' + el.rec_id + '">' + el.name + '(Published: ' + el.published_date + ')</a></li>';
        recipe_html += elem;
    });
    if (recipe_html) {
        $("#recipe-list").html(recipe_html);
    } else {
        $("#recipe-list").html("<p> No results available </p>");
    }
}

function prepareFilters(filters, selected_filters) {

    var filters_html = "";

    $.each(JSON.parse(selected_filters), function (i, el) {
        // e.g. <a class="list-group-item recipefilter selected-filter" id="54">Vegetarian<span class="badge">5</span></a>
        var elem = ("<a class=\"list-group-item recipefilter selected-filter\" id=\"")
            .concat(el.id)
            .concat("\">")
            .concat(el.name)
            .concat("</a>");
        filters_html += elem;
    });

    $.each(JSON.parse(filters), function (i, el) {
        // e.g. <a class="list-group-item recipefilter" id="54">Vegetarian<span class="badge">5</span></a>
        var elem = ("<a class=\"list-group-item recipefilter\" id=\"")
            .concat(el.category_ID)
            .concat("\">")
            .concat(el.category_ID__name)
            .concat("<span class=\"badge\">")
            .concat(el.count)
            .concat("</span>")
            .concat("</a>");
        filters_html += elem;
    });

    $(".filters-content").empty().append(filters_html);
}
function validateIngredientForm() {
    var noErrors = true;
    var inputs = $('.ingredient-formset :input');
    inputs.each(function (e) {
        var elem = $("#" + this.id);
        if (!elem.val()) {
            elem.attr('required', '');
            noErrors = false;
        }
    });
    return noErrors;
}


