// Load the application once the DOM is ready, using `jQuery.ready`:
$(function(){

    //bang
    var Bang = Backbone.Model.extend({
        defaults: function() {
            return {
                name: 'No name',
                id: '0'
            };
        }
    });

    //collection of bang
    var BangList = Backbone.Collection.extend({
        model: Bang,
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


    // one item in bang list, on the left of page
    var BangTitleView = Backbone.View.extend({
        tagName: "li",
        className: "hand",
        template: _.template($('#bang-title-template').html()),

        events: {
            "click": "detail"
        },

        initialize: function() {
            this.render();
        },
        render: function() {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
        detail: function() {
            var detail_view = new BangDetailView({model:this.model})
        }
    });

    // bang's description, on the right of page
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
        }
    });

    //bang list, shows with bang's title
    var BangListView = Backbone.View.extend({
        el: "#bang-list",

        events: {
            //"click .refresh": "refresh",
        },

        initialize: function() {
            this.listenTo(bangs, 'sync', this.render);
            //var filters = [{"name": "members__id", "op": "any", "val":"1"}];
            bangs.fetch({
                //data: {"q": JSON.stringify({"filters": filters })},
                dataType: "json",
                contentType: "application/json"
            });
        },

        render: function() {
            this.$el.empty();
            bangs.each(this.addOne, this);
        },

        addOne: function(bang) {
            var view = new BangTitleView({model:bang});
            this.$el.append(view.render().el);
        }


    });

    var banglist_view = new BangListView;

    var BangView = Backbone.View.extend({
        initialize: function() {
            this.bang_list = $("#bang-list");
            this.bang_detail = $("#bang-detail");
            this.activity_list = $("#activity-list");
            this.activity_detail = $("#acitivity-detail");
            this.member_list = $("#member-list");
        },
        render: function() {
            alert('haha');
            this.bang_detail.html('haha');
        }
    });

    var bang = new BangView();

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
