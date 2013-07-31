// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    var Bang = Backbone.Model.extend({
        defaults: function() {
            return {
                name: "default_name",
            };
        },
    });


    var BangList = Backbone.Collection.extend({
        model: BangTitle,
        url: 'http://127.0.0.1:5000/api/bang',
        parse: function(response) {
            return response.objects;
        }
    });
    var bangs = new BangList;


    //var filters = [{"name": "id", "op": "lte", "val": 2}];
    //bangs.fetch({
    //    data: {"q": JSON.stringify({"filters": filters })},
    //    dataType: "json",
    //    contentType: "application/json",
    //});


    var BangTitleView = Backbone.View.extend({
        tagName: "li",
        className: "hand",
        template: _.template($('#bang-title-template').html()),

        events: {
            "click": "show",
        },

        initialize: function() {
            this.render();
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        show: function() {
            var detail_view = new BangDetailView({model:this.model})
        },
    });

    var BangDetailView = Backbone.View.extend({
        el: "#bang-detail",

        template: _.template($('#bang-detail-template').html()),
        events: {
        },
        
        initialize: function() {
            this.render();
        },

        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
    });


    var BangListView = Backbone.View.extend({
        el: $("#bang-list"),

        events: {
            //"click .refresh": "refresh",
        },

        initialize: function() {
            this.listenTo(bangs, 'sync', this.render);
            var filters = [{"name": "members__id", "op": "any", "val":"1"}];
            bangs.fetch({
                data: {"q": JSON.stringify({"filters": filters })},
                dataType: "json",
                contentType: "application/json",
            });
        },

        render: function() {
            this.$el.empty();
            bangs.each(this.addOne, this);
        },

        addOne: function(bang) {
            var view = new BangTitleView({model:bang});
            this.$el.append(view.render().el);
        },


    });

    var banglist_view = new BangListView;

});


/*
   $(function() {

//$('#signin-form-cont input#email').first().focus();

$('#view-terms').avgrund({
width: 640, // max is 640px
height: 480, // max is 350px
showClose: true, // switch to 'true' for enabling close button
showCloseText: 'Close', // type your text for close button
closeByEscape: true, // enables closing popup by 'Esc'..
closeByDocument: true, // ..and by clicking document itself
holderClass: '', // lets you name custom class for popin holder..
overlayClass: '', // ..and overlay block
enableStackAnimation: false, // another animation type
onBlurContainer: '', // enables blur filter for specified block
template: $('#terms').html()
});
});
*/
