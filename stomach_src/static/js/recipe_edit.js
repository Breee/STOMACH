/**
 * Created by Bree on 20.05.2017.
 */
$(function () {
 $('.ingredient-formset').formset({
        addText: '<button class="btn btn-info"><span class="glyphicon glyphicon-plus"></span> Add ingredient</button>',
        deleteText: '<span class="btn btn-info btn-xs"><span class="glyphicon glyphicon-trash"></span> Remove</span>',
        prefix: 'ingredients'
    });

  $('.category-formset').formset({
        addText: '<button class="btn btn-info"><span class="glyphicon glyphicon-plus"></span> Add category</button>',
        deleteText: '<span class="btn btn-info btn-xs"><span class="glyphicon glyphicon-trash"></span> Remove</span>',
        prefix: 'categories'
    });
});