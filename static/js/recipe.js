/**
 * Created by Bree on 20.05.2017.
 */

var lastQuery = "";

$(document).ready(function () {
    // prevents that arrays in get requests get encoded with brackets.
    jQuery.ajaxSettings.traditional = true;

    // initialize dynamic formsets
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

    // On the fly search with a delay of 200 ms.
    $('#searchbar').keyup(function (evt) {
        delay(function () {
            getRecipesAndFilters(false);
        }, 200);
    });


    // If a filter is clicked, get the recipes and update filters.
    $(document).on('click', '.recipefilter', function (evt) {
        if ($(this).hasClass("selected-filter")) {
            $(this).removeClass("selected-filter");
        } else {
            $(this).addClass("selected-filter");
        }
        getRecipesAndFilters(true);
    });

});


// simple delay function.
var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();

// function that sends a get request to the server, in order to retrieve recipes.
function getRecipesAndFilters(filterClicked) {
    var query = $('#searchbar').val().trim();
    // compare trimmed queries because such that "flour" and "  flour    " is equal
    // if you click a filter we don't have to care about the query.
    if (lastQuery != query || filterClicked) {
        lastQuery = query;
        // q is the search query,
        // initialized is used to tell the view that it does not have to render the page again.
        // filter is an array of selected filters.
        $.get('/recipes/', {
            'q': query,
            'initialized': 1,
            'filter': getSelectedFilters()
        }, function (data) {
            // if the get was successful, update the filtets and recipes.
            prepareRecipeList(data.latest_recipes_list);
            prepareFilters(data.filters, data.selected_filters);
        });
    }
}

// function that fetches all filters with the 'selected-filter' class.
function getSelectedFilters() {
    var filterIDs = $.map($(".selected-filter"), function (n, i) {
        return n.id;
    });
    return filterIDs;
}

// function to build the recipes list from the results of our get request.
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


// function to build the filters from the results of our get request.
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


// function that checks if all inputfields in an ingredient-formset are filled.
// can be done with django somehow (see issues).
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
